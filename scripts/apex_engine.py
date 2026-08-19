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
    
    # Strip deepseek/reasoning blocks if present
    cleaned = re.sub(r"<think>.*?</think>", "", text.strip(), flags=re.DOTALL)
    
    # Strip markdown code blocks
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned.strip(), flags=re.MULTILINE)
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

    # Required keys for the UESP frontend interface
    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution", "protocol"]
    if not all(k in data for k in required_keys):
        return None

    # Ensure field values are non-trivial and generated
    for key in ["historical_parallel", "era_resolution", "modern_resolution", "protocol"]:
        val = str(data.get(key, "")).strip().lower()
        if val in ["str", "string", "none", "null"] or len(val) < 8:
            return None

    return data

def call_inference_endpoint(model_name, prompt):
    """Dispatches a single inference request with a 25-second socket timeout."""
    base_url = "https://integrate.api.nvidia.com/v1"
    api_key = os.environ.get("NVIDIA_API_KEY")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=25.0
    )
    
    print(f"[DISPATCH] Racing model endpoint: {model_name}")
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by NVIDIA NIM Microservices. "
                    "You perform live systemic audits integrating high-concurrency neural logic. "
                    "Analyze the given node dynamically. Compute TTI and SHI as unique floats. "
                    "Write rich, real-world narrative text for all analytical parameters. "
                    "Output ONLY a raw, valid JSON object matching the exact JSON structure requested."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024
    )
    
    content = completion.choices[0].message.content
    parsed = extract_json_payload(content)
    if not parsed:
        raise ValueError(f"Endpoint {model_name} failed JSON schema validation.")
    
    return model_name, parsed

def execute_scan():
    node = os.getenv("TARGET_NODE", "South Africa")
    session_id = os.getenv("SESSION_ID", "UISP_1787151836328")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT NODE: {node}
    SESSION ID: {session_id}
    TIMELINE MATRIX: 586 AD - 3000 CE

    EXECUTE SYSTEM AUDIT:
    1. Compute Technical Integrity (TTI) and Systemic Health (SHI) as dynamic floats (0.00 to 100.00) reflecting {node}'s macro status.
    2. Compute absolute Delta (|TTI - SHI|).
    3. Analyze a historical parallel between 586 AD and 3000 CE that mirrors {node}'s current friction.
    4. Contrast the resolution used in that historical era with a modern technical UESP resolution.
    5. Formulate divine ocular diagnostic and infrastructure matrix stability metrics.
    6. Anchor with a relevant Biblical scripture tie and executive protocol summary.

    OUTPUT RAW JSON ONLY IN THIS EXACT FORMAT (populate with actual dynamic analysis, not template labels):
    {{
      "node": "{node}",
      "tti": 78.4,
      "shi": 64.1,
      "delta": 14.3,
      "historical_parallel": "During the 15th-century maritime trade shifts, structural bottlenecks caused systemic economic friction similar to present energy grid instability.",
      "era_resolution": "Localized decentralization of agrarian hubs and manual resource rationing.",
      "modern_resolution": "Deployment of automated microgrid load-balancing and AI-driven predictive rerouting.",
      "ocular_diagnostic": "Perceptive Jougan alignment indicates non-linear signal latency across core grid nodes.",
      "chakra_matrix_stability": "Tailed Beast density stabilization at 88.4% throughput capacity.",
      "biblical_tie": {{
        "verse": "Isaiah 40:31",
        "context": "Systemic renewal through structural alignment and constant energy monitoring."
      }},
      "protocol": "Initiate sovereign protocols to stabilize energy distribution and eliminate non-linear latency.",
      "session_id": "{session_id}"
    }}
    """
    
    # Active, highly resilient endpoints hosted on NVIDIA NIM
    verified_models = [
        "meta/llama-3.3-70b-instruct",
        "qwen/qwen2.5-72b-instruct",
        "nvidia/nemotron-4-340b-instruct",
        "meta/llama-3.1-70b-instruct"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Racing {len(verified_models)} verified endpoints...")
    with ThreadPoolExecutor(max_workers=len(verified_models)) as executor:
        futures = {executor.submit(call_inference_endpoint, model, prompt): model for model in verified_models}
        
        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] High-fidelity audit generated by: {winning_model}")
                break
            except Exception as err:
                print(f"[RETRY-SKIP] Endpoint {model_name} failed: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All model endpoints failed validation.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
