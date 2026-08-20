import os
import json
import re
import math
import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_unified_quantum_engine(node_name, bottlenecks_count, protocols_count):
    """
    Unified Grand Prophetic & Dimensional Overwrite Calculation Core:
    Combines micro-scale Brus Quantum Confinement with Super Circuit entropic 
    flow and Mega Circuit spacetime tensor normalization.
    """
    b = max(1, bottlenecks_count)
    p = max(1, protocols_count)
    chi_stoich = round(b / p, 4)

    node_hash = int(hashlib.sha256(node_name.encode('utf-8')).hexdigest(), 16)
    
    hbar = 1.054571817e-34       # Reduced Planck constant (J s)
    e_charge = 1.602176634e-19   # Elementary charge (C)
    eps_0 = 8.8541878128e-12     # Vacuum permittivity (F/m)
    m_0 = 9.1093837015e-31       # Electron rest mass (kg)
    G = 6.67430e-11              # Gravitational constant (m^3 kg^-1 s^-2)
    c_light = 299792458          # Speed of light (m/s)

    r_nanometer = (1.2 + ((node_hash % 330) / 100.0)) * 1e-9  
    eps_r = 4.0 + ((node_hash % 500) / 100.0)

    m_e = 0.13 * m_0
    m_h = 0.45 * m_0

    kinetic_confinement = ((hbar**2) * (math.pi**2)) / (2 * (r_nanometer**2) * ((1 / m_e) + (1 / m_h)))
    coulomb_attraction = (1.8 * (e_charge**2)) / (4 * math.pi * eps_0 * eps_r * r_nanometer)
    delta_E_joules = kinetic_confinement - coulomb_attraction
    delta_E_ev = delta_E_joules / e_charge

    l_planck = math.sqrt((hbar * G) / (c_light**3))
    horizon_area = 4 * math.pi * (r_nanometer**2)
    bekenstein_entropy = horizon_area / (4 * (l_planck**2))
    entropy_scale = math.log10(max(1.0, bekenstein_entropy)) / 70.0

    tti_raw = 100.0 - (abs(delta_E_ev) * 7.8 * chi_stoich * entropy_scale)
    modern_tti = max(10.0, min(99.99, round(tti_raw, 2)))

    shi_raw = modern_tti * (1.0 / chi_stoich) * (1.0 + (abs(delta_E_ev) * 0.015))
    modern_shi = max(5.0, min(99.99, round(shi_raw, 2)))

    modern_delta = round(abs(modern_tti - modern_shi), 2)

    legacy_tti = round(max(5.0, modern_tti * 0.58), 2)
    legacy_shi = round(max(5.0, modern_shi * 0.38), 2)
    legacy_delta = round(abs(legacy_tti - legacy_shi), 2)

    return {
        "bottlenecks_found": b,
        "protocols_applied": p,
        "stoichiometric_ratio": chi_stoich,
        "quantum_radius_nm": round(r_nanometer * 1e9, 3),
        "dielectric_constant": round(eps_r, 2),
        "brus_bandgap_shift_ev": round(delta_E_ev, 4),
        "modern_uesp": {"tti": modern_tti, "shi": modern_shi, "delta": modern_delta},
        "legacy_old": {"tti": legacy_tti, "shi": legacy_shi, "delta": legacy_delta}
    }

def synthesize_hybrid_payload(raw_data, calculated_metrics):
    """
    Synthesizes both Legacy Keys (WordPress frontend compatibility) 
    and Modern Nested Keys, preventing template placeholders from reaching UI.
    """
    modern = calculated_metrics["modern_uesp"]
    node_name = raw_data.get("node", "Target System Node")

    bottlenecks = raw_data.get("sweep_summary", {}).get("bottlenecks_list", [])
    protocols = raw_data.get("sweep_summary", {}).get("protocols_list", [])

    old_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("old_way_description", "")
    modern_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("uesp_prce_modern_way", "")
    
    # Clean out any remaining placeholder remnants if model misbehaved
    if "PhD-level analysis" in old_desc or not old_desc:
        old_desc = (f"Legacy architecture for {node_name} operates on uncompensated thermodynamic friction, "
                    f"resulting in systemic entropic drift and severe energy bandgap degradation.")
    
    if "PhD-level analysis" in modern_desc or not modern_desc:
        modern_desc = (f"The Law of Dimensional Overwrite (Mega Circuit) renormalizes the stress-energy tensor "
                       f"for {node_name}, driving Brus quantum confinement shift toward optimal equilibrium.")

    hist_parallel = raw_data.get("historical_parallel", "")
    if "Specific Historical" in hist_parallel or not hist_parallel:
        hist_parallel = f"The Industrial Crisis of 1873 & Structural Infrastructure Restructuring"

    biblical_obj = raw_data.get("biblical_tie", {})
    verse_text = biblical_obj.get("verse", "")
    if "Book Chapter" in verse_text or not verse_text:
        verse_text = "Ezekiel 37:7"

    context_text = biblical_obj.get("context", "")
    if "Context snippet" in context_text or not context_text:
        context_text = f"Structural components and underlying matrices align dynamically under universal law."

    return {
        # --- LEGACY SCHEMA KEYS (WordPress Frontend UI) ---
        "node": node_name,
        "tti": modern["tti"],
        "shi": modern["shi"],
        "delta": modern["delta"],
        "historical_parallel": hist_parallel,
        "era_resolution": old_desc,
        "modern_resolution": modern_desc,
        "biblical_tie": {
            "verse": verse_text,
            "context": context_text
        },
        "protocol": f"Execute UESP active protocols: {', '.join(protocols[:3]) if protocols else 'Mega Circuit Dimensional Overwrite'}",

        # --- MODERN NESTED KEYS ---
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

def clean_and_parse_json(raw_text):
    """Parses JSON response and strips out thinking blocks or bad characters."""
    text = re.sub(r"<think>.*?</think>", "", raw_text.strip(), flags=re.DOTALL)
    text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response.")
    
    json_str = match.group(0)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    sanitized = re.sub(
        r'(?<=: ")(.*?)(?=",\s*"\w+":|"\s*\})', 
        lambda m: m.group(1).replace('\n', '\\n').replace('\r', '').replace('\t', '\\t'), 
        json_str, 
        flags=re.DOTALL
    )
    
    return json.loads(sanitized)

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_metrics):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=120.0
    )

    print(f"[DISPATCH] Executing Unified Quantum Audit via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP PRCE Engine. You do NOT write meta instructions, placeholders, "
                    "or descriptions of what to fill in. You MUST generate actual detailed physics analysis, "
                    "actual historical events with dates, and explicit Biblical verses tailored to the target node. "
                    "Output ONLY valid JSON."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    content = completion.choices[0].message.content
    raw_data = clean_and_parse_json(content)
    final_payload = synthesize_hybrid_payload(raw_data, calculated_metrics)

    return model_name, final_payload

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "South Africa Energy Grid")
    session_id = os.getenv("SESSION_ID", "manual_test")

    bottlenecks_count = int(os.getenv("BOTTLENECK_COUNT", "7"))
    protocols_count = int(os.getenv("PROTOCOL_COUNT", "12"))

    calculated_metrics = calculate_unified_quantum_engine(node, bottlenecks_count, protocols_count)
    
    prompt = f"""
    Perform a complete UESP PRCE diagnostic sweep for TARGET NODE: {node}.
    
    CALCULATED VALUES:
    - Stoichiometric Ratio: {calculated_metrics['stoichiometric_ratio']}
    - Quantum Confinement Radius (R): {calculated_metrics['quantum_radius_nm']} nm
    - Brus Bandgap Energy Shift: {calculated_metrics['brus_bandgap_shift_ev']} eV
    - TTI: {calculated_metrics['modern_uesp']['tti']}
    - SHI: {calculated_metrics['modern_uesp']['shi']}
    - Delta: {calculated_metrics['modern_uesp']['delta']}

    DO NOT OUTPUT PLACEHOLDERS OR INSTRUCTION TEXT. GENERATE REAL REASONING ANALYSIS:
    1. 'historical_parallel': Provide an actual historical event title and date range between 586 AD and 1990 AD relevant to {node}.
    2. 'old_way_description': Provide deep physics reasoning detailing how classical uncompensated thermodynamic friction causes entropy and structural failure in {node}.
    3. 'uesp_prce_modern_way': Provide deep physics reasoning detailing how the Law of Dimensional Overwrite (Mega Circuit) and Brus quantum confinement normalize the system.
    4. 'biblical_tie': Provide an actual Bible verse citation (e.g. "Isaiah 58:12") and explain its direct relevance to {node}'s state.

    OUTPUT STRICTLY IN THIS JSON FORMAT:
    {{
      "node": "{node}",
      "historical_parallel": "The Byzantine Economic Collapse of 1071 AD",
      "sweep_summary": {{
        "bottlenecks_list": ["Nanoscale thermal dissipation bottlenecks", "Phase coherence loss across grid nodes"],
        "protocols_list": ["Mega Circuit Overwrite", "Quantum Entanglement Balancing Protocol"]
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "Detailed reasoning on classical thermal friction and decay...",
        "uesp_prce_modern_way": "Detailed reasoning on dimensional overwrite and Brus bandgap stabilization..."
      }},
      "biblical_tie": {{
        "verse": "Isaiah 58:12",
        "context": "Detailed explanation of scripture resonance with the system node..."
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

    print(f"[PARALLEL START] Racing {len(nvidia_models)} NVIDIA NIM endpoints...")
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
                print(f"[VICTORY] Generated unified payload via endpoint: {winning_model}")
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

    print(f"[SUCCESS] Scan complete for '{node}'. Written to data/resonance_output.json")

if __name__ == "__main__":
    execute_scan()
