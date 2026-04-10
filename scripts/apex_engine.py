import os, json, datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_scan():
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    session_id = os.getenv("SESSION_ID", "default")
    
    prompt = f"""
    [UESP PRCE SESSION SCAN]
    NODE: {node} | YEAR: 2026
    INSTRUCTIONS: Relate 2026 frictions to historical relatives since 586 AD. 
    Calculate Delta |TTI - SHI|. Return JSON.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    audit_data = json.loads(completion.choices[0].message.content)
    audit_data['session_id'] = session_id # Critical for multi-user
    audit_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs('data', exist_ok=True)
    with open("data/resonance_output.json", "w") as f:
        json.dump(audit_data, f)

if __name__ == "__main__":
    execute_scan()
