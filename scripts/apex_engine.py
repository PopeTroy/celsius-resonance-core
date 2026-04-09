# apex_engine.py - REAL-TIME LIVE VERSION
import os, json, datetime
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_fresh_audit(node):
    # Precise timestamp for the new entry
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # SYSTEM PROMPT: Zero-latency Groq calculation
    prompt = f"""
    [ACTIVATE LIVE UESP PRCE] 
    TIME: {timestamp} | NODE: {node}
    
    INSTRUCTIONS:
    1. Retrieve April 2026 Economic/Health Data for {node}.
    2. Identify the recurring 586 AD and 1880s Industrial bottlenecks.
    3. CALCULATE SHI (World Health) and TTI (Technical Integrity) FRESHLY.
    4. CALCULATE the Differential Delta (|TTI - SHI|).
    5. Output JSON ONLY: {{
        "node": "{node}",
        "timestamp": "{timestamp}",
        "shi": float,
        "tti": float,
        "delta": float,
        "history_sync": "string",
        "industrial_macro": "string",
        "explanation": "string"
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content
