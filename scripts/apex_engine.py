import os
import json
import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def deep_history_audit():
    target_node = os.getenv("TARGET_NODE", "Global Infrastructure Resonance")
    
    # SYSTEM PROMPT: Locking the scan start to 586 AD
    prompt = f"""
    [ACTIVATE UESP PRCE DEEP SCAN]
    TARGET: {target_node}
    TEMPORAL SCOPE: 586 AD to April 2026
    
    CORE TASKS:
    1. Identify systemic friction in 586 AD (Byzantine transition) relevant to {target_node}.
    2. Identify industrial bottlenecks in the 1880s (Victorian Era).
    3. Calculate April 2026 SHI (Health) and TTI (Integrity) FRESHLY.
    4. Calculate the 18.52% Differential (|TTI - SHI|).
    5. Formulate a Deterministic Protocol for industrial overwrite.

    OUTPUT JSON ONLY:
    {{
      "node": "{target_node}",
      "shi": float,
      "tti": float,
      "delta": float,
      "history_alignment": "Analysis from 586 AD to Victorian Era",
      "industrial_protocol": "Macro-scale overwrite protocol",
      "status_label": "TWILIGHT ZONE"
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    audit_data = json.loads(completion.choices[0].message.content)
    audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save the JSON for the GitHub Action to push
    os.makedirs('data', exist_ok=True)
    with open("data/resonance_output.json", "w") as f:
        json.dump(audit_data, f)

if __name__ == "__main__":
    deep_history_audit()
