import os
import json
import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    # Use the node passed from WordPress
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    
    prompt = f"""
    [UESP PRCE REAL-TIME CALCULATION]
    NODE: {node}
    YEAR: 2026
    
    INSTRUCTIONS:
    1. Identify the primary 2026 friction for '{node}'.
    2. Scan history back to 586 AD. 
    3. Select ONLY historical frictions similar to the 2026 issue.
    4. Calculate Dynamic Delta: |TTI - SHI|.
    5. Formulate Deterministic Overwrite Protocol.

    OUTPUT JSON ONLY:
    {{
      "node": "{node}",
      "delta": float,
      "historical_relatives": [
        {{"year": "str", "event": "str", "correlation": "str"}}
      ],
      "protocol": "str"
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    audit_data = json.loads(completion.choices[0].message.content)
    audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs('data', exist_ok=True)
    with open("data/resonance_output.json", "w") as f:
        json.dump(audit_data, f)

if __name__ == "__main__":
    execute_scan()
