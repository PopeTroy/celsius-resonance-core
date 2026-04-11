import os
import json
import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    # FORCING LIVE CALCULATION: No static defaults allowed.
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    SESSION: {session_id}
    TIMELINE: 586 AD - 2026

    CORE INSTRUCTIONS:
    1. Calculate Technical Integrity (TTI) and Systemic Health (SHI) as dynamic floats based on {node}'s current global status.
    2. Compute the Differential Delta between TTI and SHI.
    3. Identify a precise historical event/era (586 AD - 1990 AD) that mirrors the systemic friction of {node}.
    4. Contrast the 'Era Resolution' (how it was handled then) with a 'Modern UESP Resolution' (the advanced technical/prophetic solution).
    5. Select a Biblical Scripture that resonates specifically with this specific systemic state.
    6. Formulate a final UESP Protocol summary.

    OUTPUT JSON ONLY (Strict Schema):
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
            {"role": "system", "content": "You are the UESP Apex Engine. You perform live systemic audits. Never use static figures; calculate everything dynamically based on the input node."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    data = json.loads(completion.choices[0].message.content)
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(data, f)
    with open("data/resonance_output.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    execute_scan()
