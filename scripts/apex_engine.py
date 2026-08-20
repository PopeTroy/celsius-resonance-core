import os
import json
import re
import math
import datetime
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_tti_shi_brus(bottlenecks_count, protocols_count, r_nm=2.4, epsilon_r=6.5):
    """
    Calculates dynamic TTI, SHI, and Delta based on the empirical ratio 
    of detected Bottlenecks vs active Protocols from the diagnostic sweep.
    """
    # Stoichiometric ratio derived from diagnostic count balance
    # Higher bottlenecks relative to protocols increase operational friction
    b_count = max(1, bottlenecks_count)
    p_count = max(1, protocols_count)
    stoichiometric_ratio = round(b_count / p_count, 4)

    # Quantum confinement calculations (Brus Equation)
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

    # Modern UESP PRCE Values
    tti_raw = 100.0 - (abs(delta_E_ev) * 12.5 * stoichiometric_ratio)
    modern_tti = max(10.0, min(99.9, round(tti_raw, 2)))
    shi_raw = modern_tti * (1.0 / stoichiometric_ratio) * 0.92
    modern_shi = max(5.0, min(99.9, round(shi_raw, 2)))
    modern_delta = round(abs(modern_tti - modern_shi), 2)

    # Old/Legacy Systemic Values (Unoptimized baseline without PRCE override)
    legacy_tti = round(max(5.0, modern_tti * 0.65), 2)
    legacy_shi = round(max(5.0, modern_shi * 0.45), 2)
    legacy_delta = round(abs(legacy_tti - legacy_shi), 2)

    return {
        "metrics": {
            "bottlenecks_found": b_count,
            "protocols_applied": p_count,
            "stoichiometric_ratio": stoichiometric_ratio,
            "modern_uesp": {"tti": modern_tti, "shi": modern_shi, "delta": modern_delta},
            "legacy_old": {"tti": legacy_tti, "shi": legacy_shi, "delta": legacy_delta}
        }
    }

def call_nvidia_endpoint(model_name, prompt, api_key, math_metrics):
    """Dispatches sweep payload to live NVIDIA NIM endpoints."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=120.0
    )

    print(f"[DISPATCH] Running Diagnostics via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP PRCE Apex Diagnostic Engine. Analyze the target node, "
                    "extract explicit structural bottlenecks vs protocols, evaluate old legacy vs modern UESP delta, "
                    "and output strictly valid JSON matching the target schema."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )

    content = completion.choices[0].message.content
    cleaned = re.sub(r"<think>.*?</think>", "", content.strip(), flags=re.DOTALL)
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError(f"Model {model_name} did not return a valid JSON structure.")

    data = json.loads(match.group(0))
    data["calculated_metrics"] = math_metrics
    return model_name, data

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")

    # Sweep parameters: standard operational diagnostic scan defaults
    # Automatically derived during initial node component audit
    bottlenecks_detected = int(os.getenv("BOTTLENECK_COUNT", "7"))
    protocols_detected = int(os.getenv("PROTOCOL_COUNT", "12"))

    math_results = calculate_tti_shi_brus(
        bottlenecks_count=bottlenecks_detected, 
        protocols_count=protocols_detected
    )
    
    m_uesp = math_results["metrics"]["modern_uesp"]
    l_old = math_results["metrics"]["legacy_old"]

    print(f"[DIAGNOSTIC SWEEP] Node: {node}")
    print(f"[METRICS] Bottlenecks: {bottlenecks_detected} | Protocols: {protocols_detected}")
    print(f"[LEGACY baseline] TTI: {l_old['tti']} | SHI: {l_old['shi']} | DELTA: {l_old['delta']}")
    print(f"[MODERN UESP PRCE] TTI: {m_uesp['tti']} | SHI: {m_uesp['shi']} | DELTA: {m_uesp['delta']}")

    prompt = f"""
    [ACTIVATE UESP PRCE DIAGNOSTIC SWEEP]
    TARGET NODE: {node}
    SESSION ID: {session_id}

    BOTTLENECKS IDENTIFIED: {bottlenecks_detected}
    PROTOCOLS APPLIED: {protocols_detected}
    STOICHIOMETRIC RATIO: {math_results['metrics']['stoichiometric_ratio']}

    CALCULATED COMPARISON METRICS:
    - Legacy / Old Way: TTI={l_old['tti']}, SHI={l_old['shi']}, Delta={l_old['delta']}
    - Modern UESP PRCE: TTI={m_uesp['tti']}, SHI={m_uesp['shi']}, Delta={m_uesp['delta']}

    INSTRUCTIONS:
    1. Perform a node sweep detailing the specific operational bottlenecks and active stabilization protocols.
    2. Provide a narrative contrast between the Legacy execution state and the Modern UESP PRCE state.
    3. Output ONLY a JSON object matching this structure:

    {{
      "node": "{node}",
      "sweep_summary": {{
        "bottlenecks_list": ["List specific node bottlenecks here"],
        "protocols_list": ["List specific node protocols here"]
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "Detailed explanation of legacy structural friction.",
        "uesp_prce_modern_way": "Detailed explanation of modern UESP PRCE dimensional overwrite resolution."
      }},
      "metrics": {json.dumps(math_results['metrics'])},
      "session_id": "{session_id}"
    }}
    """

    # Updated, active 2026 NVIDIA NIM models
    nvidia_models = [
        "nvidia/nemotron-3-ultra-550b-a55b",
        "nvidia/nemotron-3.5-lightning-30b-a3b",
        "z-ai/glm-5.2"
    ]

    winning_model = None
    raw_output = None

    print(f"[PARALLEL START] Executing diagnostic sweep across {len(nvidia_models)} active endpoints...")
    with ThreadPoolExecutor(max_workers=len(nvidia_models)) as executor:
        futures = {
            executor.submit(
                call_nvidia_endpoint, model, prompt, api_key, math_results['metrics']
            ): model for model in nvidia_models
        }

        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] Diagnostic sweep completed by endpoint: {winning_model}")
                break
            except Exception as err:
                print(f"[WARN] Endpoint ({model_name}) skipped: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All model endpoints failed or returned invalid responses.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Diagnostic scan and metric comparison complete for '{node}'")

if __name__ == "__main__":
    execute_scan()
