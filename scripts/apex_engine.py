import os
import json
import re
import math
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_tti_shi_brus(bottlenecks_count, protocols_count, r_nm=2.4, epsilon_r=6.5):
    """
    Calculates dynamic TTI, SHI, and Delta based on the empirical ratio 
    of detected Bottlenecks vs active Protocols.
    """
    b_count = max(1, bottlenecks_count)
    p_count = max(1, protocols_count)
    stoichiometric_ratio = round(b_count / p_count, 4)

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

    # Legacy Old Systemic Values
    legacy_tti = round(max(5.0, modern_tti * 0.65), 2)
    legacy_shi = round(max(5.0, modern_shi * 0.45), 2)
    legacy_delta = round(abs(legacy_tti - legacy_shi), 2)

    return {
        "bottlenecks_found": b_count,
        "protocols_applied": p_count,
        "stoichiometric_ratio": stoichiometric_ratio,
        "modern_uesp": {"tti": modern_tti, "shi": modern_shi, "delta": modern_delta},
        "legacy_old": {"tti": legacy_tti, "shi": legacy_shi, "delta": legacy_delta}
    }

def synthesize_hybrid_payload(raw_data, calculated_metrics):
    """
    Synthesizes both Legacy Keys (top-level tti, shi, delta, historical_parallel, etc.)
    and Modern Nested Keys into a single unified JSON response.
    """
    modern = calculated_metrics["modern_uesp"]
    legacy = calculated_metrics["legacy_old"]

    # Extract lists or convert strings if necessary
    bottlenecks = raw_data.get("sweep_summary", {}).get("bottlenecks_list", [])
    protocols = raw_data.get("sweep_summary", {}).get("protocols_list", [])

    old_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("old_way_description", "")
    modern_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("uesp_prce_modern_way", "")

    hybrid_payload = {
        # --- LEGACY SCHEMA KEYS (Expected by older WordPress frontend scripts) ---
        "node": raw_data.get("node", ""),
        "tti": modern["tti"],
        "shi": modern["shi"],
        "delta": modern["delta"],
        "historical_parallel": f"Structural Friction Analysis (Bottlenecks: {calculated_metrics['bottlenecks_found']}, Protocols: {calculated_metrics['protocols_applied']})",
        "era_resolution": old_desc if old_desc else "Legacy state operating under unresolved structural friction.",
        "modern_resolution": modern_desc if modern_desc else "Modern UESP PRCE state executing full dimensional overwrite.",
        "biblical_tie": {
            "verse": raw_data.get("biblical_tie", {}).get("verse", "Isaiah 40:31"),
            "context": raw_data.get("biblical_tie", {}).get("context", "Systemic renewal via unified structural alignment.")
        },
        "protocol": f"Execute UESP active protocols: {', '.join(protocols[:3]) if protocols else 'System stabilization'}",

        # --- MODERN SCHEMA KEYS (For updated UI modules) ---
        "sweep_summary": {
            "bottlenecks_list": bottlenecks,
            "protocols_list": protocols
        },
        "legacy_vs_modern_analysis": {
            "old_way_description": old_desc,
            "uesp_prce_modern_way": modern_desc
        },
        "metrics": calculated_metrics,
        "calculated_metrics": calculated_metrics,
        "session_id": raw_data.get("session_id", "")
    }

    return hybrid_payload

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_metrics):
    """Dispatches request and reformats into hybrid structure."""
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=120.0
    )

    print(f"[DISPATCH] Running dual-schema generation via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP PRCE Engine. Output strictly valid raw JSON without markdown or code blocks. "
                    "Analyze node bottlenecks vs protocols and legacy vs modern resolutions."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    content = completion.choices[0].message.content
    cleaned = re.sub(r"<think>.*?</think>", "", content.strip(), flags=re.DOTALL)
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError(f"Model {model_name} failed to return a valid JSON string.")

    raw_data = json.loads(match.group(0))
    final_payload = synthesize_hybrid_payload(raw_data, calculated_metrics)

    return model_name, final_payload

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "South Africa")
    session_id = os.getenv("SESSION_ID", "manual_test")

    bottlenecks_count = int(os.getenv("BOTTLENECK_COUNT", "7"))
    protocols_count = int(os.getenv("PROTOCOL_COUNT", "12"))

    calculated_metrics = calculate_tti_shi_brus(bottlenecks_count, protocols_count)
    
    prompt = f"""
    [ACTIVATE UESP PRCE DIAGNOSTIC SWEEP]
    TARGET NODE: {node}
    SESSION ID: {session_id}

    METRICS:
    - Bottlenecks Found: {bottlenecks_count}
    - Protocols Applied: {protocols_count}
    - Stoichiometric Ratio: {calculated_metrics['stoichiometric_ratio']}

    INSTRUCTIONS:
    Output ONLY a JSON object matching this structure:

    {{
      "node": "{node}",
      "sweep_summary": {{
        "bottlenecks_list": ["Detailed bottleneck 1", "Detailed bottleneck 2"],
        "protocols_list": ["Detailed protocol 1", "Detailed protocol 2"]
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "Comprehensive explanation of legacy structural friction.",
        "uesp_prce_modern_way": "Comprehensive explanation of UESP PRCE modern resolution."
      }},
      "biblical_tie": {{
        "verse": "Leviticus 19:34",
        "context": "Context snippet"
      }},
      "session_id": "{session_id}"
    }}
    """

    nvidia_models = [
        "nvidia/nemotron-3-ultra-550b-a55b",
        "nvidia/nemotron-3.5-lightning-30b-a3b",
        "z-ai/glm-5.2"
    ]

    raw_output = None
    winning_model = None

    print(f"[PARALLEL START] Executing dual-schema scan across active endpoints...")
    with ThreadPoolExecutor(max_workers=len(nvidia_models)) as executor:
        futures = {
            executor.submit(
                call_nvidia_endpoint, model, prompt, api_key, calculated_metrics
            ): model for model in nvidia_models
        }

        for future in as_completed(futures):
            model_name = futures[future]
            try:
                winning_model, raw_output = future.result()
                print(f"[VICTORY] Generated hybrid payload via: {winning_model}")
                break
            except Exception as err:
                print(f"[WARN] Endpoint ({model_name}) skipped: {err}")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All endpoint executions failed.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Hybrid JSON output ready for WordPress frontend.")

if __name__ == "__main__":
    execute_scan()
