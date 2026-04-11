import os
import json
import datetime
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    # Variables from GitHub Action (passed from WP)
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    SESSION: {session_id}
    TIMELINE: 586 AD - 2026

    TASK:
    1. Identify a specific historical era/event that reflects the current state of {node}.
    2. Analyze the 'Era Resolution' (how they handled it then) vs 'Modern Resolution' (UESP approach).
    3. Calculate TTI (Technical Integrity), SHI (Systemic Health), and Delta.
    4. Provide a relevant Biblical Scripture that ties into this resonance.
    5. Formulate a final UESP Protocol narrative.

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
            {"role": "system", "content": "You are the UESP Apex Engine. You analyze history and prophecy through a technical lens. Output valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    audit_data = json.loads(completion.choices[0].message.content)
    audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save files
    os.makedirs('data', exist_ok=True)
    # Save for JS polling
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(audit_data, f)
    # Save for Action Return
    with open("data/resonance_output.json", "w") as f:
        json.dump(audit_data, f)

if __name__ == "__main__":
    execute_scan()
