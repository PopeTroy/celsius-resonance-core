import os
import json
import re
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def extract_json_payload(text):
    """Extracts, cleans, and validates JSON payloads from model completions."""
    if not text:
        return None
    
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        else:
            return None

    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution"]
    if not all(k in data for k in required_keys):
        return None

    return data

def call_inference_endpoint(model_name, prompt):
    """Dispatches a single inference request with a strict 20-second socket timeout."""
    base_url = os.environ.get("INFERENCE_BASE_URL", "https://integrate.api.nvidia.com/v1")
    api_key = os.environ.get("NVIDIA_API_KEY")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=20.0
    )
    
    print(f"[DISPATCH] Racing model endpoint: {model_name}")
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by high-speed inference microservices. "
                    "Perform live systemic audits using dynamic calculations based on the input node. "
                    "You MUST respond ONLY with a raw, valid JSON object matching the exact schema."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )
    
    content = completion.choices[0].message.content
    parsed = extract_json_payload(content)
    if not parsed:
        raise ValueError(f"Endpoint {model_name} returned invalid or incomplete schema.")
    
    return model_name, parsed

def get_verified_active_models(client):
    """Retrieves live active non-Llama model strings directly from NVIDIA NIM API."""
    try:
        models_page = client.models.list()
        active_ids = [m.id for m in models_page if "llama" not in m.id.lower()]
        print(f"[DISCOVERY] Found {len(active_ids)} active non-Llama endpoints on NVIDIA NIM.")
        return active_ids
    except Exception as e:
        print(f"[WARN] Could not auto-fetch active models: {e}")
        # Fallback to verified exact NVIDIA catalog strings
        return [
            "nvidia/nemotron-4-340b-instruct",
            "mistralai/mistral-large-2-instruct",
            "qwen/qwen2.5-72b-instruct",
            "google/gemma-2-27b-it"
        ]

def execute_scan():
    node = os.getenv("TARGET_NODE", "South Africa")
    session_id = os.getenv("SESSION_ID", "UISP_1787151836328")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    SESSION: {session_id}
    TIMELINE MATRIX: 586 AD - 3000 CE

    CORE SYSTEM INSTRUCTIONS:
    1. Compute Technical Integrity (TTI) and Systemic Health (SHI) as dynamic floats (0.00 to 100.00).
    2. Compute absolute Delta between TTI and SHI.
    3. Identify historical parallel (586 AD - 3000 CE).
    4. Apply Divine Ocular Inspection and Tailed Beast Chakra-Matrix Density metrics.
    5. Contrast Era Resolution vs Modern UESP Resolution.
    6. Select a Biblical Scripture anchor.
    7. Formulate protocol summary.

    OUTPUT RAW JSON ONLY matching this schema:
    {{
      "node": "{node}",
      "tti": 85.50,
      "shi": 72.10,
      "delta": 13.40,
      "historical_parallel": "str",
      "era_resolution": "str",
      "modern_resolution": "str",
      "ocular_diagnostic": "str",
      "chakra_matrix_stability": "str",
      "biblical_tie": {{"verse": "str", "context": "str"}},
      "protocol": "str",
      "session_id": "{session_id}"
    }}
    """
    
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY")
    )
    
    # Query NVIDIA NIM directly for endpoints currently online
    verified_models = get_verified_active_models(client)[:5]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Dispatching request across {len(verified_models)} active endpoints...")
    with ThreadPoolExecutor(max_workers=len(verified_models)) as executor:
        futures = {executor.submit(call_inference_endpoint, model, prompt): model for model in verified_models}
        
        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] Fastest valid schema received from: {winning_model}")
                break
            except Exception as err:
                print(f"[RETRY-SKIP] Endpoint {model_name} failed/timed out: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All model endpoints in the execution pool failed.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
