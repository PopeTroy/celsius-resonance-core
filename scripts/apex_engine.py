import os
import json
import datetime
from openai import OpenAI

def get_nvidia_nim_completion(prompt, model_name):
    """Executes inference via specified NVIDIA NIM Microservices model."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY")
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by NVIDIA NIM Microservices. "
                    "You perform live systemic audits integrating high-concurrency neural logic, "
                    "divine ocular analytics, and Shinobi tactical matrices. Never use static figures; "
                    "calculate everything dynamically based on the input node. Always output strict JSON."
                )
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

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

    OUTPUT JSON ONLY (Strict Schema):
    {{
      "node": "{node}",
      "tti": float,
      "shi": float,
      "delta": float,
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
    
    # Primary candidate models (Non-Llama enterprise models)
    nim_models = [
        "mistralai/mistral-nemotron",
        "mistralai/mistral-large-2-instruct",
        "google/gemma-2-27b-it",
        "qwen/qwen2.5-72b-instruct"
    ]
    
    # Fetch live active endpoints to supplement fallback cascade
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY")
    )
    live_models = get_active_non_llama_models(client)
    for model_id in live_models:
        if model_id not in nim_models:
            nim_models.append(model_id)

    raw_output = None
    for model in nim_models:
        try:
            print(f"[INFO] Executing audit via NVIDIA NIM Model: {model}")
            raw_output = get_nvidia_nim_completion(prompt, model)
            if raw_output:
                break
        except Exception as err:
            print(f"[WARN] NVIDIA NIM Model ({model}) failure: {err}. Triaging to next model...")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All NVIDIA NIM multi-model executions failed.")

    data = json.loads(raw_output)
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(data, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"[SUCCESS] Audit completed for session: {session_id}")

if __name__ == "__main__":
    execute_scan()
