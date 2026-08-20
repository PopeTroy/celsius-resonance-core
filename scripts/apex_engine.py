import os
import json
import re
import math
import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

def calculate_sequential_node_metrics(node_name, bottlenecks_count, protocols_count):
    """
    Calculates TTI, SHI, and Delta purely based on the ratio of Bottlenecks (B) vs 
    Protocols (P) applied across the node's historical timeline entropic scale (586 AD - Present).
    Completely removes physics/thermodynamic variables while guaranteeing non-static calculations per node.
    """
    # 1. Sequential Inputs
    b = max(1, bottlenecks_count)
    p = max(1, protocols_count)
    stoichiometric_ratio = round(b / p, 4)

    # 2. Sequential Node Entropy Seed (derived from node string signature)
    node_hash = int(hashlib.sha256(node_name.encode('utf-8')).hexdigest(), 16)
    
    # Historical Entropy Index (S_node) bound between 1.05 and 2.45 based on the node signature
    s_node = 1.05 + ((node_hash % 1400) / 1000.0)

    # 3. Dynamic Calculation Core
    # TTI: Technical Integrity calculated from structural friction (Bottlenecks / Protocols * Node Entropy)
    friction_coefficient = stoichiometric_ratio * s_node
    tti_raw = 100.0 - (friction_coefficient * 4.25)
    modern_tti = max(15.0, min(99.95, round(tti_raw, 2)))

    # SHI: Systemic Health Index under active protocol balancing
    shi_raw = 100.0 - (stoichiometric_ratio * 0.85)
    modern_shi = max(20.0, min(99.99, round(shi_raw, 2)))

    # Differential Delta (|TTI - SHI|)
    modern_delta = round(abs(modern_tti - modern_shi), 2)

    # Legacy Old System Metrics (Uncompensated structural decay baseline)
    legacy_tti = round(max(5.0, modern_tti * 0.62), 2)
    legacy_shi = round(max(5.0, modern_shi * 0.42), 2)
    legacy_delta = round(abs(legacy_tti - legacy_shi), 2)

    return {
        "bottlenecks_found": b,
        "protocols_applied": p,
        "stoichiometric_ratio": stoichiometric_ratio,
        "node_entropy_index": round(s_node, 3),
        "modern_uesp": {"tti": modern_tti, "shi": modern_shi, "delta": modern_delta},
        "legacy_old": {"tti": legacy_tti, "shi": legacy_shi, "delta": legacy_delta}
    }

def synthesize_hybrid_payload(raw_data, calculated_metrics):
    """
    Synthesizes both Legacy Keys (WordPress frontend compatibility) 
    and Modern Nested Keys, stripping out thermodynamic text in favor of pure resolution reasoning.
    """
    modern = calculated_metrics["modern_uesp"]
    node_name = raw_data.get("node", "Target System Node")

    bottlenecks = raw_data.get("sweep_summary", {}).get("bottlenecks_list", [])
    protocols = raw_data.get("sweep_summary", {}).get("protocols_list", [])

    old_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("old_way_description", "")
    modern_desc = raw_data.get("legacy_vs_modern_analysis", {}).get("uesp_prce_modern_way", "")
    
    # Strip any stray thermodynamic text out if the AI hallucinated physics terms
    old_desc = re.sub(r'\b(thermodynamic|entropy|energy bandgap|eV|Brus|phonon|quantum)\b', 'structural', old_desc, flags=re.IGNORECASE)
    modern_desc = re.sub(r'\b(thermodynamic|entropy|energy bandgap|eV|Brus|phonon|quantum)\b', 'systemic', modern_desc, flags=re.IGNORECASE)

    hist_parallel = raw_data.get("historical_parallel", "")
    biblical_obj = raw_data.get("biblical_tie", {})

    return {
        # --- LEGACY SCHEMA KEYS (WordPress Frontend Compatibility) ---
        "node": node_name,
        "tti": modern["tti"],
        "shi": modern["shi"],
        "delta": modern["delta"],
        "historical_parallel": hist_parallel,
        "era_resolution": old_desc,
        "modern_resolution": modern_desc,
        "biblical_tie": {
            "verse": biblical_obj.get("verse", "Ezekiel 37:7"),
            "context": biblical_obj.get("context", "Sequential alignment of system components under unified law.")
        },
        "protocol": f"Execute UESP active protocols: {', '.join(protocols[:3]) if protocols else 'Dimensional Overwrite & Structural Alignment'}",

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
    """Parses JSON response and strips out code blocks, preambles, or unescaped characters."""
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

    print(f"[DISPATCH] Executing Sequential Node Sweep via model: {model_name}")
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP PRCE Engine. Explain resolutions in pure, direct historical and "
                    "structural terms. DO NOT mention thermodynamics, quantum mechanics, Brus equations, "
                    "or mathematical formulas in your explanations. Output strictly valid JSON."
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

    # Calculate sequential node metrics from Bottlenecks vs Protocols
    calculated_metrics = calculate_sequential_node_metrics(node, bottlenecks_count, protocols_count)
    
    prompt = f"""
    Perform a UESP PRCE diagnostic sweep for TARGET NODE: {node}.
    
    SEQUENTIAL CALCULATED METRICS:
    - Bottlenecks Found: {bottlenecks_count}
    - Protocols Applied: {protocols_count}
    - Stoichiometric Friction Ratio: {calculated_metrics['stoichiometric_ratio']}
    - Node Historical Entropy Index: {calculated_metrics['node_entropy_index']}
    - Calculated TTI: {calculated_metrics['modern_uesp']['tti']}
    - Calculated SHI: {calculated_metrics['modern_uesp']['shi']}
    - Calculated Delta: {calculated_metrics['modern_uesp']['delta']}

    STRICT INSTRUCTIONS:
    1. 'historical_parallel': Provide an actual historical event title and date range between 586 AD and 1990 AD relevant to {node}.
    2. 'old_way_description': Explain clearly how the old, legacy system operated under uncompensated structural friction, bottleneck buildup, and institutional decay without mentioning physics or thermodynamics.
    3. 'uesp_prce_modern_way': Explain clearly how the UESP PRCE Modern Way executes a complete dimensional overwrite to eliminate bottlenecks, restore integrity (TTI: {calculated_metrics['modern_uesp']['tti']}), and stabilize systemic health (SHI: {calculated_metrics['modern_uesp']['shi']}).
    4. 'biblical_tie': Provide an actual Bible verse citation and explain its direct prophetic resonance with {node}'s structural restoration.

    DO NOT USE THERMODYNAMICS, QUANTUM MECHANICS, OR PHYSICS EQUATIONS IN THE TEXT.

    OUTPUT STRICTLY IN THIS JSON FORMAT:
    {{
      "node": "{node}",
      "historical_parallel": "Parallel Era: The Six-Day War and Territorial Reconfiguration of June 5-10, 1967 AD",
      "sweep_summary": {{
        "bottlenecks_list": ["Bottleneck description 1", "Bottleneck description 2"],
        "protocols_list": ["Protocol description 1", "Protocol description 2"]
      }},
      "legacy_vs_modern_analysis": {{
        "old_way_description": "Pure structural explanation of legacy friction and system failures...",
        "uesp_prce_modern_way": "Pure structural explanation of UESP PRCE modern dimensional overwrite resolution..."
      }},
      "biblical_tie": {{
        "verse": "Isaiah 58:12",
        "context": "Direct prophetic explanation of scripture resonance..."
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
