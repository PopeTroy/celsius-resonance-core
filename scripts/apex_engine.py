import os, json, datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def deep_scan_586ad():
    node = os.getenv("TARGET_NODE", "Global Infrastructure")
    
    # The Deterministic Prompt for Groq
    prompt = f"""
    [ACTIVATE UESP PRCE] 
    TEMPORAL SCOPE: 586 AD to 2026.
    NODE: {node}.
    
    1. Scan Byzantine (586 AD) and Victorian (1880s) industrial friction.
    2. Calculate real-time April 2026 SHI and TTI.
    3. Determine the 18.52% Differential gap.
    4. Provide the Overwrite Protocol.
    
    Output JSON ONLY: {{
        "node": "str", 
        "shi": float, 
        "tti": float, 
        "delta": float, 
        "history_sync": "str", 
        "protocol": "str"
    }}
    """
    
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    data = json.loads(chat.choices[0].message.content)
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("resonance_output.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    deep_scan_586ad()
