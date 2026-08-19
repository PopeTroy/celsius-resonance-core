import os
import json
import re
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def extract_json_payload(text):
    """Extracts and parses JSON from raw completion text, handling markdown wrapping."""
    if not text:
        return None
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise

def call_nim_endpoint(model_name, prompt):
    """Executes single NIM endpoint completion with hard thread timeout."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY"),
        timeout=35.0  # Prevents hanging threads
    )
    
    print(f"[DISPATCH] Racing heavy endpoint: {model_name}")
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by NVIDIA NIM Microservices. "
                    "You perform live systemic audits integrating high-concurrency neural logic, "
                    "divine ocular analytics, and Shinobi tactical matrices. Never use static figures; "
                    "calculate everything dynamically based on the input node. "
                    "You MUST respond ONLY with a raw, valid JSON object matching the requested schema."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )
    
    content = completion.choices[0].message.content
    parsed = extract_json_payload(content)
    if not parsed:
        raise ValueError("Invalid JSON payload returned.")
    return model_name, parsed

def get_active_non_llama_models(client):
    """Dynamically retrieves live non-Llama model identifiers from NVIDIA NIM."""
    try:
        models_page = client.models.list()
        active_ids = [m.id for m in models_page.data if "llama" not in m.id.lower()]
        return active_ids
    except Exception as e:
        print(f"[WARN] Could not auto-fetch active models: {e}")
        return []

def execute_scan():
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    # Dynamic Timeline Matrix (586 AD - 3000 CE)
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    SESSION: {session_id}
    TIMELINE MATRIX: 586 AD - 3000 CE (Expanded Epoch Horizon)

    CORE SYSTEM INSTRUCTIONS:
    1. CALCULATE TTI & SHI: Compute Technical Integrity (TTI) and Systemic Health (SHI) as dynamic floats (0.00 to 100.00) based on {node}'s live trajectory.
    2. DIFFERENTIAL DELTA: Compute the absolute non-linear Delta between TTI and SHI.
    3. HISTORICAL & FUTURE PARALLEL: Identify a precise historical event or strategic timeline node (586 AD - 3000 CE) mirroring {node}'s friction.
    4. SHINOBI TACTICS & OCULAR DIAGNOSTICS: Apply Divine Ocular Inspection (Jougan/Sharingan perceptive clarity) to detect systemic Genjutsu/anomalies, and integrate Tailed Beast Chakra-Matrix Density to stabilize infrastructure throughput.
    5. RESOLUTION CONTRAST: Contrast the legacy 'Era Resolution' with the advanced 'Modern UESP Resolution'.
    6. BIBLICAL ANCHOR: Select a Biblical Scripture that resonates with this specific systemic state to secure structural integrity.
    7. UESP PROTOCOL: Formulate a final sovereign protocol summary.

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
    
    # Premier non-Llama candidates supporting up to 1M context
    primary_nim_models = [
        "nvidia/nemotron-3-ultra-550b-a55b",     # Flagship 550B MoE (1M context)
        "zhipuai/glm-5.2",                         # Frontier agentic reasoning (1M context)
        "nvidia/nemotron-3.5-lightning-30b-a3b", # High-throughput sparse MoE (1M context)
        "google/gemma-2-27b-it",
        "qwen/qwen2.5-72b-instruct"
    ]
    
    # Fetch live active endpoints to supplement pool
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY")
    )
    live_models = get_active_non_llama_models(client)
    for model_id in live_models:
        if model_id not in primary_nim_models:
            primary_nim_models.append(model_id)

    # Limit maximum concurrency to top active models to avoid socket saturation
    candidate_pool = primary_nim_models[:6]

    winning_model = None
    data = None

    # Kage Bunshin Protocol: Fire concurrent threads to eliminate queue latency
    print(f"[PARALLEL START] Racing {len(candidate_pool)} non-Llama heavy endpoints...")
    with ThreadPoolExecutor(max_workers=len(candidate_pool)) as executor:
        futures = {executor.submit(call_nim_endpoint, model, prompt): model for model in candidate_pool}
        
        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, data = future.result()
                print(f"[VICTORY] Fastest valid response received from: {winning_model}")
                break  # First successful completion locks the result
            except Exception as err:
                print(f"[RETRY-SKIP] Endpoint {model_name} failed or dropped: {err}")

    if not data:
        raise RuntimeError("[CRITICAL] All parallel NVIDIA NIM non-Llama model executions failed.")

    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(data, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
