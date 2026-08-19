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
    
    # Strip deepseek reasoning blocks if present (<think>...</think>)
    cleaned = re.sub(r"<think>.*?</think>", "", text.strip(), flags=re.DOTALL)
    
    # Strip markdown block quotes
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

    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution", "protocol"]
    if not all(k in data for k in required_keys):
        return None

    # Reject responses where the model copies structural hints verbatim
    banned_phrases = ["detailed historical", "historical strategy", "advanced uesp", "final sovereign", "description"]
    for key in ["historical_parallel", "era_resolution", "modern_resolution", "protocol"]:
        val = str(data.get(key, "")).lower()
        if any(phrase in val for phrase in banned_phrases) or len(val) < 10:
            return None

    return data

def call_inference_endpoint(model_name, prompt):
    """Dispatches a single inference request with strict timeout and reasoning validation."""
    base_url = "https://integrate.api.nvidia.com/v1"
    api_key = os.environ.get("NVIDIA_API_KEY")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=35.0  # Extended timeout for deep reasoning chains (DeepSeek R1)
    )
    
    print(f"[DISPATCH] Racing deep reasoning model: {model_name}")
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by DeepSeek Reasoning Architecture. "
                    "You execute deep neural-tactical systemic audits. You MUST NOT copy prompt placeholder text. "
                    "Calculate dynamic TTI and SHI values based on real-world factors for the subject node. "
                    "Perform deep, original historical and tactical reasoning for all string parameters. "
                    "Output ONLY valid JSON matching the target schema."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,  # Raised slightly to prompt creative analytical output
        max_tokens=2048
    )
    
    content = completion.choices[0].message.content
    parsed = extract_json_payload(content)
    if not parsed:
        raise ValueError(f"Endpoint {model_name} returned placeholder text or invalid schema.")
    
    return model_name, parsed

def execute_scan():
    node = os.getenv("TARGET_NODE", "South Africa")
    session_id = os.getenv("SESSION_ID", "UISP_1787151836328")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT NODE: {node}
    SESSION ID: {session_id}
    TIMELINE MATRIX: 586 AD - 3000 CE

    REASONING AUDIT MANDATE:
    1. Calculate dynamic Technical Integrity (TTI) and Systemic Health (SHI) floats (0.0 to 100.0) based on current real-world macro conditions of {node}.
    2. Compute absolute Delta (|TTI - SHI|).
    3. Perform deep historical parallel analysis connecting {node}'s present state to a specific historical event/epoch between 586 AD and 3000 CE.
    4. Contrast the resolution used in that historical era with a modern UESP technical resolution.
    5. Formulate divine ocular diagnostics and infrastructure matrix stability metrics.
    6. Select a resonant Biblical Scripture tie and formulate an executive protocol.

    CRITICAL: DO NOT OUTPUT PLACEHOLDER TEXT. WRITE FULL, COMPREHENSIVE REASONING PARAGRAPHS FOR EVERY FIELD.

    JSON SCHEMA TO FULFILL:
    {{
      "node": "{node}",
      "tti": 78.42,
      "shi": 64.15,
      "delta": 14.27,
      "historical_parallel": "<WRITE REAL HISTORICAL ANALYSIS HERE>",
      "era_resolution": "<WRITE REAL HISTORICAL STRATEGY HERE>",
      "modern_resolution": "<WRITE REAL MODERN TECHNICAL RESOLUTION HERE>",
      "ocular_diagnostic": "<WRITE REAL OCULAR ANOMALY DIAGNOSTIC HERE>",
      "chakra_matrix_stability": "<WRITE REAL INFRASTRUCTURE MATRIX ANALYSIS HERE>",
      "biblical_tie": {{
        "verse": "<BOOK CHAPTER:VERSE>",
        "context": "<REAL SCRIPTURAL CONTEXTUAL ANALYSIS>"
      }},
      "protocol": "<WRITE REAL EXECUTIVE SYSTEM PROTOCOL SUMMARY HERE>",
      "session_id": "{session_id}"
    }}
    """
    
    # Priority roster focusing on DeepSeek R1 and premier reasoning engines
    deep_reasoning_models = [
        "deepseek-ai/deepseek-r1",              # Primary DeepSeek Reasoning Engine
        "nvidia/nemotron-3-ultra-550b-a55b",     # 550B Frontier MoE
        "meta/llama-3.3-70b-instruct"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Racing {len(deep_reasoning_models)} deep reasoning endpoints...")
    with ThreadPoolExecutor(max_workers=len(deep_reasoning_models)) as executor:
        futures = {executor.submit(call_inference_endpoint, model, prompt): model for model in deep_reasoning_models}
        
        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] Deep reasoning scan resolved via: {winning_model}")
                break
            except Exception as err:
                print(f"[RETRY-SKIP] Endpoint {model_name} failed validation: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All deep reasoning endpoints failed validation.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
