import os
import json
import datetime
from groq import Groq

# Pulling directly from your Repository Secrets
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def deep_historical_audit():
    # Targeted node passed from the trigger
    target_node = os.getenv("TARGET_NODE", "Global Infrastructure")
    
    prompt = f"""
    [ACTIVATE UESP PRCE DEEP SCAN]
    NODE: {target_node}
    TEMPORAL SCOPE: 586 AD to April 2026
    
    TASKS:
    1. Identify 586 AD Byzantine systemic friction.
    2. Identify 1880s Victorian industrial bottlenecks.
    3. Calculate April 2026 SHI (Health) and TTI (Integrity).
    4. Provide the 18.52% Differential analysis.
    5. Formulate the Deterministic Overwrite Protocol.

    Output JSON only:
    {{
      "node": "{target_node}",
      "shi": float,
      "tti": float,
      "delta": float,
      "history_sync": "str",
      "protocol": "str"
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    data = json.loads(completion.choices[0].message.content)
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensuring the data folder exists for the workflow to find it
    os.makedirs('data', exist_ok=True)
    with open("data/resonance_output.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    deep_historical_audit()
