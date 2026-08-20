import os
import json
import re
import math
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_tti_shi_brus(r_nm=2.4, epsilon_r=6.5, stoichiometric_ratio=1.08):
    """
    Calculates dynamic TTI and SHI floats using the quantum confinement Brus equation
    combined with stoichiometric reaction balance.
    """
    h_bar = 1.054571817e-34    # Reduced Planck's constant (J s)
    e = 1.602176634e-19        # Elementary charge (C)
    eps_0 = 8.8541878128e-12   # Vacuum permittivity (F/m)
    m_0 = 9.1093837015e-31     # Electron rest mass (kg)
    
    m_e = 0.13 * m_0
    m_h = 0.45 * m_0
    r = r_nm * 1e-9

    kinetic_term = ((h_bar**2) * (math.pi**2)) / (2 * (r**2) * ((1 / m_e) + (1 / m_h)))
    coulomb_term = (1.8 * (e**2)) / (4 * math.pi * eps_0 * epsilon_r * r)
    delta_E_joules = kinetic_term - coulomb_term
    
    delta_E_ev = delta_E_joules / e

    tti_raw = 100.0 - (abs(delta_E_ev) * 12.5 * stoichiometric_ratio)
    tti = max(10.0, min(99.9, round(tti_raw, 2)))

    shi_raw = tti * (1.0 / stoichiometric_ratio) * 0.92
    shi = max(5.0, min(99.9, round(shi_raw, 2)))

    delta = round(abs(tti - shi), 2)

    return tti, shi, delta

def extract_and_validate_json(raw_response, calculated_tti, calculated_shi, calculated_delta):
    """Robustly extracts, cleans, and validates JSON output from any LLM response format."""
    if not raw_response:
        return None

    # Strip thinking tags and extra whitespace
    cleaned = re.sub(r"<think>.*?</think>", "", raw_response.strip(), flags=re.DOTALL)
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)

    # Locate first outer bracket pair
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        return None

    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None

    # Overwrite/Bind local math floats directly into JSON
    data["tti"] = calculated_tti
    data["shi"] = calculated_shi
    data["delta"] = calculated_delta

    required_keys = ["tti", "shi", "delta", "historical_parallel", "era_resolution", "modern_resolution", "biblical_tie", "protocol"]
    if not all(k in data for k in required_keys):
        return None

    # Validate string content quality
    banned_tokens = ["float", "str", "string", "none", "null", "<str>"]
    for key in ["historical_parallel", "era_resolution", "modern_resolution", "protocol"]:
        val = str(data.get(key, "")).strip().lower()
        if val in banned_tokens or len(val) < 8:
            return None

    return data

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_tti, calculated_shi, calculated_delta):
    """Dispatches payload to an NVIDIA NIM model via OpenAI SDK with fallback handling."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=60.0  # Increased timeout window for heavy workloads
    )

    print(f"[DISPATCH] Running NVIDIA NIM audit via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine. "
                    "Perform live systemic audits using physical and stoichiometric parameters. "
                    "Output strictly a raw JSON object matching the target structure cleanly. "
                    "Do NOT include markdown block syntax, preambles, or post-commentary."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )

    content = completion.choices[0].message.content
    parsed = extract_and_validate_json(content, calculated_tti, calculated_shi, calculated_delta)
    
    if not parsed:
        raise ValueError(f"Model {model_name} returned unparseable or incomplete JSON schema.")

    return model_name, parsed

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")

    # Perform dynamic local calculation
    tti, shi, delta = calculate_tti_shi_brus(r_nm=2.4, epsilon_r=6.5, stoichiometric_ratio=1.08)
    print(f"[MATH ENGINE] Dynamic Equation Calculated -> TTI: {tti} | SHI: {shi} | DELTA: {delta}")

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
    1. Analyze systemic implications of TTI={tti} and SHI={shi} (Delta={delta}) for {node}.
    2. Identify a historical event/era (586 AD - 1990 AD) mirroring this friction state.
    3. Contrast the 'Era Resolution' with a 'Modern UESP Resolution'.
    4. Select a Biblical Scripture that resonates with this specific state.
    5. Formulate a final UESP Protocol summary.

    OUTPUT JSON ONLY MATCHING THIS EXACT SCHEMA:
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

    # Model roster with Step Flash, Gemma, Llama-3-70b (Laguna-tier), GLM, Nemotron Super, and MiniMax
    nvidia_models = [
        "stepfun-ai/step-3.7-flash",
        "google/gemma-4-31b-it",
        "meta/llama-3.3-70b-instruct",
        "thudm/glm-4-9b-chat",
        "nvidia/nemotron-3-super-120b-a12b",
        "minimax/minimax-text-01"
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
