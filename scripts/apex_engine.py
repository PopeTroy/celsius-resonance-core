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

    # Guarantee frontend required keys to prevent rendering undefined
    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution"]
    if not all(k in data for k in required_keys):
        return None

    return data

def call_inference_endpoint(model_name, prompt):
    """Dispatches a single inference request with a strict 20-second timeout."""
    base_url = "https://integrate.api.nvidia.com/v1"
    api_key = os.environ.get("NVIDIA_API_KEY")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=20.0
    )
    
    print(f"[DISPATCH] Racing verified model: {model_name}")
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
    
    # Active, verified NVIDIA NIM model roster
    verified_target_models = [
        "nvidia/nemotron-3.5-lightning-30b-a3b",
        "meta/llama-3.3-70b-instruct",
        "zhipuai/glm-5.2",
        "qwen/qwen2.5-coder-32b-instruct",
        "meta/llama-3.1-70b-instruct"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Racing {len(verified_target_models)} verified endpoints...")
    with ThreadPoolExecutor(max_workers=len(verified_target_models)) as executor:
        futures = {executor.submit(call_inference_endpoint, model, prompt): model for model in verified_target_models}
        
        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] Response validated from: {winning_model}")
                break
            except Exception as err:
                print(f"[RETRY-SKIP] Endpoint {model_name} failed: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All verified NVIDIA NIM model executions failed.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
