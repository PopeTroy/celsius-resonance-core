import os
import json
import datetime
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    # Superman Prompt: Historical Analysis + Modern Resolution + Prophecy
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    TIMELINE: 586 AD - 2026
    
    TASK:
    1. Match {node} to a historical era/event with similar systemic friction.
    2. Define the 'Era Resolution' (then) vs the 'Modern UESP Resolution' (now).
    3. Calculate TTI (Technical Integrity), SHI (Systemic Health), and Delta.
    4. Provide a Biblical Scripture (Verse + Context) that anchors this resonance.
    5. Formulate the final UESP Protocol narrative.

    OUTPUT JSON ONLY:
    {{
      "node": "{node}",
      "tti": float,
      "shi": float,
      "delta": float,
      "historical_parallel": "str",
      "era_resolution": "str",
      "modern_resolution": "str",
      "biblical_tie": {{"verse": "str", "context": "str"}},
      "protocol": "str",
      "session_id": "{session_id}"
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are the UESP Apex Engine. Output valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    audit_data = json.loads(completion.choices[0].message.content)
    audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    
    # Save for polling
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(audit_data, f)
        
    # Save static for CURL
    with open("data/resonance_output.json", "w") as f:
        json.dump(audit_data, f)

if __name__ == "__main__":
    execute_scan()
