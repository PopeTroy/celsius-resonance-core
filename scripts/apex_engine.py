import os
import json
import datetime
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def execute_chrono_audit(node_name):
    # Every search is a new entry with a unique timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
    [ACTIVATE UESP PRCE APEX ENGINE]
    TIMESTAMP: {timestamp}
    TARGET NODE: {node_name}
    
    TASK:
    1. Scan history from 586 AD (Byzantine) and the Victorian Industrial Era.
    2. Align the current problems of '{node_name}' to these specific historical bottlenecks.
    3. Calculate SHI (World Health) and TTI (Integrity) based on current 2026 data.
    4. Provide the Differential (|TTI - SHI|).
    5. Explain how history overcame this at a macro/industrial scale.
    6. Provide a Deterministic Protocol for 2026.

    OUTPUT ONLY VALID JSON:
    {{
      "timestamp": "{timestamp}",
      "node": "{node_name}",
      "shi": 23.15,
      "tti": 41.67,
      "delta": 18.52,
      "timeline_match": "string",
      "bottleneck_analysis": "string",
      "historical_solution": "string",
      "apex_protocol": "string"
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

# Set default to biggest bottleneck if no node provided
target = os.getenv("TARGET_NODE", "Global Infrastructure Resonance")
audit_result = execute_chrono_audit(target)

with open("data/latest_audit.json", "w") as f:
    f.write(audit_result)
