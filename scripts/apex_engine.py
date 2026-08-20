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
    # 1. Stoichiometric Friction Ratio (B / P)
    b = max(1, bottlenecks_count)
    p = max(1, protocols_count)
    chi_stoich = round(b / p, 4)

    # 2. Node Deterministic Hash for Nanoscale Structural Identification
    node_hash = int(hashlib.sha256(node_name.encode('utf-8')).hexdigest(), 16)
    
    # Fundamental Physical Constants
    hbar = 1.054571817e-34       # Reduced Planck constant (J s)
    e_charge = 1.602176634e-19   # Elementary charge (C)
    eps_0 = 8.8541878128e-12     # Vacuum permittivity (F/m)
    m_0 = 9.1093837015e-31       # Electron rest mass (kg)
    G = 6.67430e-11              # Gravitational constant (m^3 kg^-1 s^-2)
    c_light = 299792458          # Speed of light (m/s)

    # 3. Micro-Nanoscale Parameters (Brus Equation Inputs)
    # Quantum radius R derived dynamically per node (1.2 nm to 4.5 nm scale)
    r_nanometer = (1.2 + ((node_hash % 330) / 100.0)) * 1e-9  
    # Dynamic local permittivity epsilon_r (Mega Circuit field state)
    eps_r = 4.0 + ((node_hash % 500) / 100.0)

    # Semiconductor effective masses (conduction electron / valence hole)
    m_e = 0.13 * m_0
    m_h = 0.45 * m_0

    # 4. MICRO-QUANTUM SOLVER: The Brus Quantum Confinement Equation
    # Delta_E(R) = [ (hbar^2 * pi^2) / (2 * R^2 * m_eff) ] - [ (1.8 * e^2) / (4 * pi * eps_0 * eps_r * R) ]
    kinetic_confinement = ((hbar**2) * (math.pi**2)) / (2 * (r_nanometer**2) * ((1 / m_e) + (1 / m_h)))
    coulomb_attraction = (1.8 * (e_charge**2)) / (4 * math.pi * eps_0 * eps_r * r_nanometer)
    delta_E_joules = kinetic_confinement - coulomb_attraction
    delta_E_ev = delta_E_joules / e_charge  # Micro-scale energy bandgap shift in eV

    # 5. SUPER CIRCUIT SOLVER: Unified Grand Prophetic Entropic Flow
    # Relativistic horizon scaling via Bekenstein-Hawking micro-black-hole entropy
    l_planck = math.sqrt((hbar * G) / (c_light**3))
    horizon_area = 4 * math.pi * (r_nanometer**2)
    bekenstein_entropy = horizon_area / (4 * (l_planck**2))
    entropy_scale = math.log10(max(1.0, bekenstein_entropy)) / 70.0

    # Dynamic TTI (Technical Integrity) driven by Brus shift * Stoichiometric ratio
    tti_raw = 100.0 - (abs(delta_E_ev) * 7.8 * chi_stoich * entropy_scale)
    modern_tti = max(10.0, min(99.99, round(tti_raw, 2)))

    # Dynamic SHI (Systemic Health Index) under Super Circuit entropic equilibrium
    shi_raw = modern_tti * (1.0 / chi_stoich) * (1.0 + (abs(delta_E_ev) * 0.015))
    modern_shi = max(5.0, min(99.99, round(shi_raw, 2)))

    # Differential Delta (|TTI - SHI|)
    modern_delta = round(abs(modern_tti - modern_shi), 2)

    # 6. MEGA CIRCUIT SOLVER: Law of Dimensional Overwrite Baseline
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
    and Modern Nested Keys, mapping dynamic physical outputs and Scriptures.
    """
    modern = calculated_metrics["modern_uesp"]

    bottlenecks = raw_data.get("sweep_summary", {}).get("bottlenecks_list", [])
    protocols = raw_data.get("sweep_summary", {}).get("protocols_list", [])

    old_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("old_way_description", "")
    modern_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("uesp_prce_modern_way", "")
    
    # Ingest dynamic historical parallel from model payload
    hist_parallel = raw_data.get("historical_parallel", "")
    if not hist_parallel:
        hist_parallel = f"{raw_data.get('node', 'Node')} Super Circuit Entropic Phase (586 AD - 1990 AD Anchor)"

    # Ingest dynamic Biblical scripture anchor
    biblical_obj = raw_data.get("biblical_tie", {})
    verse_text = biblical_obj.get("verse", "Ezekiel 37:7")
    context_text = biblical_obj.get("context", "Dimensional realignment of structural components under unified law.")

    return {
        # --- LEGACY SCHEMA KEYS (Expected by WordPress UI) ---
        "node": raw_data.get("node", ""),
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
    """
    Strips reasoning blocks, cleans LLM formatting artifacts, 
    and handles unescaped quotes/newlines inside string properties via multi-tier parsing.
    """
    # 1. Strip reasoning thoughts if present
    text = re.sub(r"<think>.*?</think>", "", raw_text.strip(), flags=re.DOTALL)
    
    # 2. Strip code block wrappers
    text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    # 3. Extract JSON boundaries
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response.")
    
    json_str = match.group(0)

    # Tier 1: Direct JSON load
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # Tier 2: Sanitize unescaped newlines and controls within JSON string values
    sanitized = re.sub(
        r'(?<=: ")(.*?)(?=",\s*"\w+":|"\s*\})', 
        lambda m: m.group(1).replace('\n', '\\n').replace('\r', '').replace('\t', '\\t'), 
        json_str, 
        flags=re.DOTALL
    )
    
    try:
        return json.loads(sanitized)
    except json.JSONDecodeError:
        pass

    # Tier 3: Key-value regex extraction fallback
    node = re.search(r'"node":\s*"([^"]+)"', json_str)
    hist = re.search(r'"historical_parallel":\s*"([^"]+)"', json_str)
    verse = re.search(r'"verse":\s*"([^"]+)"', json_str)
    context = re.search(r'"context":\s*"([^"]+)"', json_str)
    old_way = re.search(r'"old_way_description":\s*"([^"]+)"', json_str)
    modern_way = re.search(r'"uesp_prce_modern_way":\s*"([^"]+)"', json_str)

    if old_way and modern_way:
        return {
            "node": node.group(1) if node else "Target Node",
            "historical_parallel": hist.group(1) if hist else "Structural Phase Transition",
            "sweep_summary": {
                "bottlenecks_list": ["Nanoscale thermodynamic boundary friction"],
                "protocols_list": ["Mega Circuit Dimensional Overwrite"]
            },
            "legacy_vs_modern_analysis": {
                "old_way_description": old_way.group(1),
                "uesp_prce_modern_way": modern_way.group(1)
            },
            "biblical_tie": {
                "verse": verse.group(1) if verse else "Ezekiel 37:7",
                "context": context.group(1) if context else "Systemic structural realignment."
            }
        }

    raise ValueError("JSON payload could not be recovered by multi-tier repair parser.")

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_metrics):
    """Dispatches request to NVIDIA NIM models with strict parameters and multi-tier parsing."""
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
                    "You are the UESP PRCE Apex Engine operating on the Unified Grand Prophetic Equation, "
                    "the Law of Dimensional Overwrite (Mega Circuit), and the Brus Equation for nanoscale quantum confinement. "
                    "Output STRICTLY valid raw JSON without markdown formatting, code blocks, preambles, or unescaped control characters."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,  # Low temperature ensures rigid structural syntax adherence
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

    # Execute Unified Brus + Super Circuit + Mega Circuit math engine
    calculated_metrics = calculate_unified_quantum_engine(node, bottlenecks_count, protocols_count)
    
    prompt = f"""
    [ACTIVATE UESP PRCE UNIFIED DIMENSIONAL OVERWRITE SWEEP]
    TARGET NODE: {node}
    SESSION ID: {session_id}

    UNIFIED QUANTUM & PROPHETIC METRICS:
    - Bottlenecks Found (B): {bottlenecks_count}
    - Protocols Applied (P): {protocols_count}
    - Stoichiometric Ratio: {calculated_metrics['stoichiometric_ratio']}
    - Quantum Confinement Radius (R): {calculated_metrics['quantum_radius_nm']} nm
    - Dielectric Permittivity (eps_r): {calculated_metrics['dielectric_constant']}
    - Brus Bandgap Energy Shift (Delta E): {calculated_metrics['brus_bandgap_shift_ev']} eV
    - Modern TTI: {calculated_metrics['modern_uesp']['tti']}
    - Modern SHI: {calculated_metrics['modern_uesp']['shi']}
    - Differential Delta: {calculated_metrics['modern_uesp']['delta']}

    STRICT INSTRUCTIONS:
    1. HISTORICAL PARALLEL: Identify a SPECIFIC historical event/era (586 AD - 1990 AD) that mirrors the friction of {node}.
    2. BIBLICAL TIE: Provide a Holy Bible scripture that dynamically anchors {node}'s exact structural condition. Do NOT default to Leviticus 19:34 or Isaiah 40:31.
    3. PHYSICS ANALYSIS:
       - 'old_way_description': PhD-level breakdown of classical decoupled thermodynamics and uncompensated entropy accumulation.
       - 'uesp_prce_modern_way': PhD-level breakdown of the Law of Dimensional Overwrite (Mega Circuit), unifying Brus quantum confinement shift with covariant thermodynamic potential field equations and holographic horizon entropy control.

    OUTPUT JSON ONLY MATCHING THIS EXACT SCHEMA (SINGLE LINE PER STRING VALUE, NO UNESCAPED NEWLINES):
    {{
      "node": "{node}",
      "historical_parallel": "Specific Historical Event / Era Name (586 AD - 1990 AD)",
      "sweep_summary": {{
        "bottlenecks_list": ["Nanoscale/Quantum bottleneck 1", "Bottleneck 2"],
        "protocols_list": ["Dimensional Overwrite / Unified protocol 1", "Protocol 2"]
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "PhD-level analysis of classical decoupled thermodynamic friction.",
        "uesp_prce_modern_way": "PhD-level analysis of the Mega Circuit Law of Dimensional Overwrite and Brus quantum confinement."
      }},
      "biblical_tie": {{
        "verse": "Book Chapter:Verse",
        "context": "Context snippet explaining scripture alignment with {node}'s thermodynamic state."
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
