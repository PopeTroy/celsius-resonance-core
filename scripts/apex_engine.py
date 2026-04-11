import os
import json
import datetime
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    # Retrieve parameters from GitHub Environment (passed from WordPress)
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "manual_test")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    TIMELINE: 586 AD - 2026
    
    EQUATION:
    1. Apply Unified Grand Prophetic Equation to {node}.
    2. Assess Technical Integrity (TTI) vs Systemic Health (SHI).
    3. Calculate Differential Delta.
    4. Match against Book of Revelations and historical frictions (586 AD).

    OUTPUT JSON ONLY:
    {{
      "node": "{node}",
      "tti": float,
      "shi": float,
      "delta": float,
      "session_id": "{session_id}",
      "prophetic_match": "str",
      "historical_sync": [
        {{"year": "str", "event": "str", "resonance": "str"}}
      ],
      "protocol": "str"
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are the UESP Apex Engine. Output only valid JSON."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Parse Groq's Response
        audit_data = json.loads(completion.choices[0].message.content)
        audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        audit_data['session_id'] = session_id  # Ensure session ID is reflected
        
        # Save to a unique session file to prevent multi-user interference
        os.makedirs('data', exist_ok=True)
        filename = f"data/session_{session_id}.json"
        
        with open(filename, "w") as f:
            json.dump(audit_data, f)
            
        print(f"SUCCESS: Audit complete for session {session_id}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    execute_scan()
