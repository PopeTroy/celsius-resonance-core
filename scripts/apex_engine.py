import os
import json
import re
import math
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_tti_shi_brus(r_nm=2.5, epsilon_r=8.0, stoichiometric_ratio=1.05):
    """
    Calculates dynamic TTI and SHI floats based on the quantum confinement Brus equation 
    and stoichiometric balance parameters (b, p).
    
    Parameters:
    - r_nm: Particle/Core radius in nanometers
    - epsilon_r: Relative permittivity / dielectric constant
    - stoichiometric_ratio: Reaction balance ratio (b/p)
    """
    # Physical constants
    h_bar = 1.054571817e-34    # Reduced Planck's constant (J s)
    e = 1.602176634e-19        # Elementary charge (C)
    eps_0 = 8.8541878128e-12   # Vacuum permittivity (F/m)
    m_0 = 9.1093837015e-31     # Rest electron mass (kg)
    
    # Effective masses
    m_e = 0.13 * m_0
    m_h = 0.45 * m_0
    r = r_nm * 1e-9            # Convert nm to meters

    # Brus confinement energy shift (Joules)
    kinetic_term = ((h_bar**2) * (math.pi**2)) / (2 * (r**2) * ((1 / m_e) + (1 / m_h)))
    coulomb_term = (1.8 * (e**2)) / (4 * math.pi * eps_0 * epsilon_r * r)
    delta_E_joules = kinetic_term - coulomb_term
    
    # Convert shift to eV for scaling
    delta_E_ev = delta_E_joules / e

    # Derive dynamic floats bounded to [0.00, 100.00]
    # TTI reflects technical integrity derived from energy quantum alignment
    tti_raw = 100.0 - (abs(delta_E_ev) * 12.5 * stoichiometric_ratio)
    tti = max(10.0, min(99.9, round(tti_raw, 2)))

    # SHI reflects systemic health scaled by stoichiometric index
    shi_raw = tti * (1.0 / stoichiometric_ratio) * 0.92
    shi = max(5.0, min(99.9, round(shi_raw, 2)))

    # Absolute differential delta
    delta = round(abs(tti - shi), 2)

    return tti, shi, delta

def extract_and_validate_json(raw_response, calculated_tti, calculated_shi, calculated_delta):
    """Validates structural output and binds the calculated float metrics."""
    if not raw_response:
        return None
        
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

    # Force exact locally-calculated floats into the structure
    data["tti"] = calculated_tti
    data["shi"] = calculated_shi
    data["delta"] = calculated_delta

    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution", "biblical_tie", "protocol"]
    if not all(k in data for k in required_keys):
        return None

    banned_tokens = ["float", "str", "string", "none", "null", "<str>"]
    for key in ["historical_parallel", "era_resolution", "modern_resolution", "protocol"]:
        val = str(data.get(key, "")).strip().lower()
        if val in banned_tokens or len(val) < 8:
            return None

    return data

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_tti, calculated_shi, calculated_delta):
    """Dispatches request via NVIDIA API using OpenAI SDK."""
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
                    "You perform live systemic audits integrating stoichiometry and physical equations. "
                    "Output ONLY a raw, valid JSON object matching the requested schema without type hints or markdown wrappers."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024
    )
    
    content = completion.choices[0].message.content
    parsed = extract_and_validate_json(content, calculated_tti, calculated_shi, calculated_delta)
    if not parsed:
        raise ValueError(f"Endpoint {model_name} failed schema validation.")
    
    return model_name, parsed

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")

    # Step 1: Perform actual mathematical/stoichiometric calculations locally
    tti, shi, delta = calculate_tti_shi_brus(r_nm=2.4, epsilon_r=6.5, stoichiometric_ratio=1.08)
    print(f"[MATH ENGINE] Dynamic Equation Calculated -> TTI: {tti} | SHI: {shi} | DELTA: {delta}")

    # Step 2: Pass calculated float results directly into prompt schema context
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT NODE: {node}
    SESSION ID: {session_id}
    TIMELINE MATRIX: 586 AD - 2026

    SYSTEM METRICS (LIVE CALCULATED VIA BRUS & STOICHIOMETRIC EQUATION):
    - Technical Integrity (TTI): {tti}
    - Systemic Health (SHI): {shi}
    - Differential Delta: {delta}

    CORE INSTRUCTIONS:
    1. Analyze the systemic implications of TTI={tti} and SHI={shi} (Delta={delta}) for {node}.
    2. Identify a precise historical event/era (586 AD - 1990 AD) that mirrors this friction state.
    3. Contrast the 'Era Resolution' (how it was handled then) with a 'Modern UESP Resolution' (the advanced technical/prophetic solution).
    4. Select a Biblical Scripture that resonates specifically with this exact calculated state.
    5. Formulate a final UESP Protocol summary.

    OUTPUT RAW JSON ONLY matching this structure:
    {{
      "node": "{node}",
      "tti": {tti},
      "shi": {shi},
      "delta": {delta},
      "historical_parallel": "During 15th-century maritime trade shifts, structural bottlenecks caused systemic economic friction.",
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
    
    nvidia_models = [
        "nvidia/nemotron-3-super-120b-a12b",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        "google/gemma-4-31b-it",
        "stepfun-ai/step-3.7-flash"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Racing {len(nvidia_models)} NVIDIA NIM endpoints...")
    with ThreadPoolExecutor(max_workers=len(nvidia_models)) as executor:
        futures = {
            executor.submit(
                call_nvidia_endpoint, model, prompt, api_key, tti, shi, delta
            ): model for model in nvidia_models
        }
        
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

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session {session_id} via {winning_model}")

if __name__ == "__main__":
    execute_scan()
