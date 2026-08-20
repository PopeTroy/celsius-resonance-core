import os
import json
import re
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def extract_and_validate_json(raw_response):
    """Cleans completion output and ensures string fields contain real text, not type placeholders."""
    if not raw_response:
        return None
        
    # Strip potential reasoning/thinking tags or markdown wrappers
    cleaned = re.sub(r"<think>.*?</think>", "", raw_response.strip(), flags=re.DOTALL)
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

    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution", "biblical_tie", "protocol"]
    if not all(k in data for k in required_keys):
        return None

    # Anti-Placeholder Filter: Reject responses that literally copy type hints
    banned_tokens = ["float", "str", "string", "none", "null", "<str>"]
    for key in ["historical_parallel", "era_resolution", "modern_resolution", "protocol"]:
        val = str(data.get(key, "")).strip().lower()
        if val in banned_tokens or len(val) < 8:
            return None

    # Calculate and enforce numerical float precision
    try:
        data["tti"] = round(float(data["tti"]), 2)
        data["shi"] = round(float(data["shi"]), 2)
        data["delta"] = round(abs(data["tti"] - data["shi"]), 2)
    except (ValueError, TypeError):
        return None

    return data

def call_nvidia_endpoint(model_name, prompt, api_key):
    """Dispatches request via NVIDIA NIM API using OpenAI SDK."""
    base_url = "https://integrate.api.nvidia.com/v1"

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=35.0
    )
    
    print(f"[DISPATCH] Running NVIDIA NIM audit via model: {model_name}")
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by NVIDIA NIM Microservices. "
                    "You perform live systemic audits integrating high-concurrency neural logic. "
                    "Analyze the given node dynamically. Compute TTI and SHI as dynamic floats. "
                    "Do NOT output type placeholders like 'str' or 'float'. "
                    "Output ONLY a raw, valid JSON object matching the requested schema."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=896
    )
    
    content = completion.choices[0].message.content
    parsed = extract_and_validate_json(content)
    if not parsed:
        raise ValueError(f"Endpoint {model_name} failed schema validation or echoed placeholders.")
    
    return model_name, parsed

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    # Prompt provides realistic example data to prevent LLM from copying type strings
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT NODE: {node}
    SESSION ID: {session_id}
    TIMELINE MATRIX: 586 AD - 2026

    CORE INSTRUCTIONS:
    1. Calculate Technical Integrity (TTI) and Systemic Health (SHI) as dynamic floats (0.00 to 100.00) based on {node}'s current macro status.
    2. Compute the Differential Delta (|TTI - SHI|).
    3. Identify a precise historical event/era (586 AD - 1990 AD) that mirrors the systemic friction of {node}.
    4. Contrast the 'Era Resolution' (how it was handled then) with a 'Modern UESP Resolution' (the advanced technical/prophetic solution).
    5. Select a Biblical Scripture that resonates specifically with this systemic state.
    6. Formulate a final UESP Protocol summary.

    CRITICAL: DO NOT OUTPUT TYPE PLACEHOLDERS LIKE "str" OR "float". POPULATE WITH REAL CALCULATED ANALYSIS.

    OUTPUT JSON ONLY (Strict Schema Structure):
    {{
      "node": "{node}",
      "tti": 78.42,
      "shi": 64.15,
      "delta": 14.27,
      "historical_parallel": "During 15th-century maritime trade shifts, structural bottlenecks caused systemic economic friction similar to current infrastructure bottlenecks.",
      "era_resolution": "Localized decentralization of agrarian hubs and manual resource rationing.",
      "modern_resolution": "Deployment of automated microgrid load-balancing and AI-driven predictive routing.",
      "biblical_tie": {{
        "verse": "Isaiah 40:31",
        "context": "Systemic renewal through structural alignment and constant energy monitoring."
      }},
      "protocol": "Initiate sovereign protocols to stabilize resource distribution and eliminate signal latency.",
      "session_id": "{session_id}"
    }}
    """
    
    # Active, verified NVIDIA NIM model roster
    nvidia_models = [
        "meta/llama-3.3-70b-instruct",
        "meta/llama-3.1-70b-instruct",
        "nvidia/nemotron-4-340b-instruct",
        "meta/llama-3.2-3b-instruct"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Racing {len(nvidia_models)} NVIDIA NIM endpoints...")
    with ThreadPoolExecutor(max_workers=len(nvidia_models)) as executor:
        futures = {executor.submit(call_nvidia_endpoint, model, prompt, api_key): model for model in nvidia_models}
        
        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] Dynamic audit generated by NVIDIA model: {winning_model}")
                break
            except Exception as err:
                print(f"[WARN] NVIDIA Endpoint ({model_name}) skipped: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All NVIDIA NIM model executions failed.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Persist outputs locally
    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
