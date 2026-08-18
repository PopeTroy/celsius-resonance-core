import os
import json
import datetime
from groq import Groq
from openai import OpenAI

def get_groq_completion(prompt):
    """Executes inference via Groq LPU pipeline using Groq Compound architecture."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    # Utilizing Groq Compound model pipeline
    completion = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by Groq Compound architecture. "
                    "You perform live systemic audits integrating high-concurrency neural logic, "
                    "divine ocular analytics, and Shinobi tactical matrices. Never use static figures; "
                    "calculate everything dynamically based on the input node."
                )
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

def get_chatgpt_oss_completion(prompt):
    """Fallback / High-Precision inference via ChatGPT OSS / OpenAI Endpoint."""
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # Utilizing ChatGPT OSS / OpenAI open model series
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine utilizing ChatGPT OSS architecture. "
                    "You execute deep neural-tactical systemic audits. Always output strict JSON."
                )
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

def get_nvidia_nim_completion(prompt):
    """Secondary Fallback via NVIDIA NIM Microservices."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ.get("NVIDIA_API_KEY")
    )
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by NVIDIA NIM Microservices. "
                    "You execute deep neural-tactical systemic audits. Always output strict JSON."
                )
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

def execute_scan():
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    # FORCING LIVE CALCULATION: Dynamic Timeline (586 AD - 3000 CE)
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
    
    # Multi-Engine Fallback Cascade: Groq Compound -> ChatGPT OSS -> NVIDIA NIM
    raw_output = None
    try:
        raw_output = get_groq_completion(prompt)
    except Exception as groq_err:
        print(f"[WARN] Groq Compound Engine failure ({groq_err}). Rerouting to ChatGPT OSS pipeline...")
        try:
            raw_output = get_chatgpt_oss_completion(prompt)
        except Exception as oss_err:
            print(f"[WARN] ChatGPT OSS failure ({oss_err}). Rerouting to NVIDIA NIM Microservices...")
            raw_output = get_nvidia_nim_completion(prompt)
    
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
