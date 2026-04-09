import os
import json
import datetime
from groq import Groq

# Initialize Groq with your Repository Secret
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_celsius_audit():
    target_node = os.getenv("TARGET_NODE", "Global Infrastructure")
    
    # Deterministic Prompt focusing on 586 AD to 2026
    prompt = f"""
    [ACTIVATE UESP PRCE DEEP SCAN]
    NODE: {target_node}
    TEMPORAL SCOPE: 586 AD to April 2026
    
    REQUIRED ANALYSIS:
    1. Scan 586 AD Byzantine systemic friction (Integrity vs Health).
    2. Identify 1880s Victorian industrial bottlenecks.
    3. Calculate April 2026 SHI (Health) and TTI (Integrity).
    4. Apply the 18.52% Differential constant (|TTI - SHI|).
    5. Formulate the Overwrite Protocol.

    OUTPUT JSON FORMAT ONLY:
    {{
      "node": "{target_node}",
      "shi": float,
      "tti": float,
      "delta": float,
      "history_sync": "Summary of 586 AD to 2026 findings",
      "protocol": "Deterministic industrial overwrite protocol"
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        audit_data = json.loads(completion.choices[0].message.content)
        audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ensure directory exists for output
        os.makedirs('data', exist_ok=True)
        with open("data/resonance_output.json", "w") as f:
            json.dump(audit_data, f)
            
    except Exception as e:
        print(f"Audit Fracture: {str(e)}")

if __name__ == "__main__":
    run_celsius_audit()
