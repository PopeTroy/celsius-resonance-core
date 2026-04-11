import os
import json
import datetime
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    # Retrieve parameters from GitHub Environment
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    SESSION: {session_id}
    TIMELINE: 586 AD - 2026

    TASK:
    1. Identify a specific historical era/event that reflects the current state of {node}.
    2. Analyze the 'Era Resolution' vs 'Modern Resolution' (UESP approach).
    3. Calculate TTI (Technical Integrity), SHI (Systemic Health), and Delta.
    4. Provide a relevant Biblical Scripture (Verse and Context) that ties into this resonance.
    5. Formulate a final UESP Protocol narrative.

    OUTPUT JSON ONLY:
    {{
      "node": "{node}",
      "tti": 98.4,
      "shi": 92.1,
      "delta": 24.5,
      "historical_parallel": "str",
      "era_resolution": "str",
      "modern_resolution": "str",
      "biblical_tie": {{"verse": "str", "context": "str"}},
      "protocol": "str",
      "session_id": "{session_id}"
    }}
    """
    
    try:
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

        # Create directory and save files
        os.makedirs('data', exist_ok=True)
        
        # Save unique session file for the JS Bridge
        with open(f"data/session_{session_id}.json", "w") as f:
            json.dump(audit_data, f)
            
        # Save static file for the GitHub Action CURL command
        with open("data/resonance_output.json", "w") as f:
            json.dump(audit_data, f)
            
        print(f"SUCCESS: Audit saved for session {session_id}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    execute_scan()
