import os
import json
import datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_temporal_scan():
    target_node = os.getenv("TARGET_NODE", "Global Infrastructure")
    
    prompt = f"""
    [ACTIVATE UESP PRCE DYNAMIC SCAN]
    NODE: {target_node}
    YEAR: 2026
    
    INSTRUCTIONS:
    1. Identify April 2026 frictions for '{target_node}'.
    2. Scan the timeline back to 586 AD. 
    3. Relate current issues to similar frictions found in the timeline.
    4. Compute Dynamic Differential: Delta = |TTI - SHI|.
    5. Generate the Overwrite Protocol.

    OUTPUT JSON ONLY:
    {{
      "node": "{target_node}",
      "shi": float,
      "tti": float,
      "delta": float,
      "historical_relatives": [
        {{"year": "str", "event": "str", "correlation": "str"}}
      ],
      "protocol": "str"
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(completion.choices[0].message.content)
        data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        os.makedirs('data', exist_ok=True)
        with open("data/resonance_output.json", "w") as f:
            json.dump(data, f)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_temporal_scan()
