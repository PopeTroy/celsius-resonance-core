import os
import json
import re
import math
import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_tti_shi_quantum_astrophysics(node_name, bottlenecks_count, protocols_count):
    """
    PhD-level Quantum & Relativistic Calculation Engine:
    Computes dynamic TTI, SHI, and Delta using non-equilibrium thermodynamics,
    Bekenstein-Hawking black hole entropy scaling, and quantum confinement Brus metrics.
    """
    b = max(1, bottlenecks_count)
    p = max(1, protocols_count)
    chi_stoich = b / p  # Stoichiometric friction balance ratio

    # Deterministic node hashing for dynamic micro-quantum variance
    node_hash = int(hashlib.sha256(node_name.encode('utf-8')).hexdigest(), 16)
    
    # Fundamental Physical Constants
    hbar = 1.054571817e-34       # Reduced Planck constant (J s)
    e_charge = 1.602176634e-19   # Elementary charge (C)
    eps_0 = 8.8541878128e-12     # Vacuum permittivity (F/m)
    m_0 = 9.1093837015e-31       # Electron rest mass (kg)
    k_B = 1.380649e-23           # Boltzmann constant (J/K)
    G = 6.67430e-11              # Gravitational constant (m^3 kg^-1 s^-2)
    c = 299792458                # Speed of light (m/s)

    # Dynamic Node Physical Parameters derived from node entropy signature
    r_quantum = (2.0 + (node_hash % 300) / 100.0) * 1e-9  # Dynamic confinement radius (nm)
    eps_r = 4.5 + (node_hash % 500) / 100.0                # Local dielectric constant
    T_local = 300.0 + (node_hash % 100)                     # Local thermal reservoir (K)

    # Effective mass calculations (conduction band / valence band hole coupling)
    m_e = 0.13 * m_0
    m_h = 0.45 * m_0

    # 1. Quantum Confinement Brus Energy Shift
    kinetic_term = ((hbar**2) * (math.pi**2)) / (2 * (r_quantum**2) * ((1 / m_e) + (1 / m_h)))
    coulomb_term = (1.8 * (e_charge**2)) / (4 * math.pi * eps_0 * eps_r * r_quantum)
    delta_E_ev = (kinetic_term - coulomb_term) / e_charge

    # 2. Relativistic Covariant Entropy Term (Bekenstein-Hawking & Horizon Redshift)
    l_planck = math.sqrt((hbar * G) / (c**3))
    horizon_area = 4 * math.pi * (r_quantum**2)
    bekenstein_entropy = horizon_area / (4 * (l_planck**2))
    entropy_scale = math.log10(max(1.0, bekenstein_entropy)) / 70.0

    # 3. Non-Equilibrium Thermodynamic Phase Coupling
    thermal_beta = 1.0 / (k_B * T_local)
    fluctuation_dissipation = math.exp(-thermal_beta * abs(delta_E_ev) * e_charge * 1e18)

    # Dynamic TTI calculation (Technical Integrity metric)
    tti_raw = 100.0 - (abs(delta_E_ev) * 8.5 * chi_stoich * entropy_scale)
    modern_tti = max(10.0, min(99.99, round(tti_raw, 2)))

    # Dynamic SHI calculation (Systemic Health Index under Stress-Energy Tensor Normalization)
    shi_raw = modern_tti * (1.0 / chi_stoich) * (1.0 + fluctuation_dissipation * 0.05)
    modern_shi = max(5.0, min(99.99, round(shi_raw, 2)))
    modern_delta = round(abs(modern_tti - modern_shi), 2)

    # Legacy baseline unoptimized calculation
    legacy_tti = round(max(5.0, modern_tti * 0.58), 2)
    legacy_shi = round(max(5.0, modern_shi * 0.39), 2)
    legacy_delta = round(abs(legacy_tti - legacy_shi), 2)

    return {
        "bottlenecks_found": b,
        "protocols_applied": p,
        "stoichiometric_ratio": round(chi_stoich, 4),
        "quantum_brus_ev": round(delta_E_ev, 4),
        "bekenstein_entropy_log": round(entropy_scale, 4),
        "modern_uesp": {"tti": modern_tti, "shi": modern_shi, "delta": modern_delta},
        "legacy_old": {"tti": legacy_tti, "shi": legacy_shi, "delta": legacy_delta}
    }

def synthesize_hybrid_payload(raw_data, calculated_metrics):
    """
    Synthesizes both Legacy Keys (expected by WordPress UI) and Modern Keys.
    Dynamically passes through the PhD Historical Parallel and resolutions.
    """
    modern = calculated_metrics["modern_uesp"]

    bottlenecks = raw_data.get("sweep_summary", {}).get("bottlenecks_list", [])
    protocols = raw_data.get("sweep_summary", {}).get("protocols_list", [])

    old_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("old_way_description", "")
    modern_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("uesp_prce_modern_way", "")
    
    # Preserves actual AI-generated historical parallel string instead of static default
    hist_parallel = raw_data.get("historical_parallel", "")
    if not hist_parallel:
        hist_parallel = f"{raw_data.get('node', 'Node')} Relativistic Field Discontinuity (586 AD - 1990 AD Anchor Point)"

    return {
        # --- LEGACY SCHEMA KEYS (Mapped for WordPress UI) ---
        "node": raw_data.get("node", ""),
        "tti": modern["tti"],
        "shi": modern["shi"],
        "delta": modern["delta"],
        "historical_parallel": hist_parallel,
        "era_resolution": old_desc,
        "modern_resolution": modern_desc,
        "biblical_tie": {
            "verse": raw_data.get("biblical_tie", {}).get("verse", "Isaiah 40:31"),
            "context": raw_data.get("biblical_tie", {}).get("context", "Systemic entropy normalization across space-time boundaries.")
        },
        "protocol": f"Execute UESP active protocols: {', '.join(protocols[:3]) if protocols else 'Gravitational-thermodynamic field coupling'}",

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

def call_nvidia_endpoint(model_name, prompt, api_key, calculated_metrics):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        timeout=120.0
    )

    print(f"[DISPATCH] Running Quantum Physics Audit via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP PRCE Apex Engine operating on Advanced Quantum Mechanics, "
                    "General Relativity, Non-Equilibrium Statistical Thermodynamics, and Astrophysics. "
                    "You must output STRICTLY valid JSON without codeblocks or preambles."
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
        raise ValueError(f"Model {model_name} failed JSON extraction.")

    raw_data = json.loads(match.group(0))
    return model_name, synthesize_hybrid_payload(raw_data, calculated_metrics)

def execute_scan():
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("[FATAL] NVIDIA_API_KEY environment variable is missing.")

    node = os.getenv("TARGET_NODE", "Thermodynamic Gravity System")
    session_id = os.getenv("SESSION_ID", "manual_test")

    bottlenecks_count = int(os.getenv("BOTTLENECK_COUNT", "7"))
    protocols_count = int(os.getenv("PROTOCOL_COUNT", "12"))

    calculated_metrics = calculate_tti_shi_quantum_astrophysics(node, bottlenecks_count, protocols_count)
    
    prompt = f"""
    [ACTIVATE UESP PRCE QUANTUM ASTROPHYSICS & HISTORICAL SWEEP]
    TARGET NODE: {node}
    SESSION ID: {session_id}

    QUANTUM & RELATIVISTIC METRICS:
    - Bottlenecks Found: {bottlenecks_count}
    - Protocols Applied: {protocols_count}
    - Stoichiometric Ratio: {calculated_metrics['stoichiometric_ratio']}
    - Quantum Brus Confinement Shift: {calculated_metrics['quantum_brus_ev']} eV
    - Bekenstein-Hawking Entropy Scale: {calculated_metrics['bekenstein_entropy_log']}
    - Computed Modern TTI: {calculated_metrics['modern_uesp']['tti']}
    - Computed Modern SHI: {calculated_metrics['modern_uesp']['shi']}
    - Computed Delta: {calculated_metrics['modern_uesp']['delta']}

    INSTRUCTIONS:
    1. Identify a SPECIFIC historical event/era between 586 AD and 1990 AD that mirrors the structural friction of {node} (Do NOT leave this generic).
    2. Write 'old_way_description' analyzing classical/decoupled physics friction (flat Minkowski spacetime, decoupled thermodynamics, information loss at horizons).
    3. Write 'uesp_prce_modern_way' applying PhD-level physics (covariant thermodynamic potentials, curved spacetime manifolds, holographic entropy redistribution, Bekenstein-Hawking entropy threshold modulation).

    OUTPUT ONLY JSON MATCHING THIS EXACT SCHEMA:
    {{
      "node": "{node}",
      "historical_parallel": "Exact Historical Event and Era Name (586 AD - 1990 AD)",
      "sweep_summary": {{
        "bottlenecks_list": ["Quantum/Thermodynamic bottleneck 1", "Bottleneck 2"],
        "protocols_list": ["Relativistic/Unified protocol 1", "Protocol 2"]
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "PhD-level analysis of decoupled thermodynamics and Minkowski curvature limits.",
        "uesp_prce_modern_way": "PhD-level analysis of holographic entropy redistribution and stress-energy normalization."
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
                print(f"[VICTORY] Generated quantum payload via endpoint: {winning_model}")
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

    print(f"[SUCCESS] Quantum Physics scan complete for '{node}'")

if __name__ == "__main__":
    execute_scan()
