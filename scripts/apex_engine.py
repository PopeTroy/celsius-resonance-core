import os
import json
import re
import datetime
from openai import OpenAI

def extract_json_payload(text):
    """Extracts and parses JSON from text, handling potential markdown code blocks."""
    if not text:
        return None
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise

def get_fast_completion(prompt, model_name):
    """Executes inference via ultra-fast endpoints (sub-5 second response target)."""
    # Adjust base_url and API key based on your target provider (Hyperbolic, Groq, NVIDIA)
    client = OpenAI(
        base_url=os.environ.get("INFERENCE_BASE_URL", "https://api.hyperbolic.xyz/v1"),
        api_key=os.environ.get("HYPERBOLIC_API_KEY", os.environ.get("NVIDIA_API_KEY")),
        timeout=10.0  # Strict timeout to avoid hanging
    )
    
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the UESP Apex Engine powered by high-speed inference. "
                    "Perform live systemic audits using dynamic calculations. "
                    "Respond ONLY with a raw, valid JSON object matching the schema."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )
    return completion.choices[0].message.content

def execute_scan():
    node = os.getenv("TARGET_NODE", "Israel")
    session_id = os.getenv("SESSION_ID", "UISP_17871497905")
    
    prompt = f"""
    [ACTIVATE UESP PRCE: DIMENSIONAL OVERWRITE]
    SUBJECT: {node}
    SESSION: {session_id}
    TIMELINE MATRIX: 586 AD - 3000 CE

    CORE SYSTEM INSTRUCTIONS:
    1. Compute Technical Integrity (TTI) and Systemic Health (SHI) as dynamic floats (0.00 to 100.00).
    2. Compute absolute Delta between TTI and SHI.
    3. Identify historical parallel (586 AD - 3000 CE).
    4. Apply Divine Ocular Inspection and Tailed Beast Chakra-Matrix Density metrics.
    5. Contrast Era Resolution vs Modern UESP Resolution.
    6. Select a Biblical Scripture anchor.
    7. Formulate protocol summary.

    OUTPUT RAW JSON ONLY matching this schema:
    {{
      "node": "{node}",
      "tti": 85.50,
      "shi": 72.10,
      "delta": 13.40,
      "historical_parallel": "str",
      "era_resolution": "str",
      "modern_resolution": "str",
      "ocular_diagnostic": "str",
      "chakra_matrix_stability": "str",
      "biblical_tie": {{"verse": "str", "context": "str"}},
      "protocol": "str",
      "session_id": "{session_id}"
    }}
    """
    
    # Lightweight, ultra-fast model priority list
    fast_models = [
        "meta-llama/Llama-3.2-3B-Instruct",
        "Qwen/Qwen2.5-Coder-32B-Instruct",
        "deepseek-ai/DeepSeek-V3",
        "google/gemma-2-9b-it"
    ]

    raw_output = None
    for model in fast_models:
        try:
            print(f"[INFO] Executing high-speed audit via model: {model}")
            response_text = get_fast_completion(prompt, model)
            parsed_json = extract_json_payload(response_text)
            if parsed_json:
                raw_output = parsed_json
                print(f"[SUCCESS] Audit resolved in sub-seconds via: {model}")
                break
        except Exception as err:
            print(f"[WARN] Endpoint ({model}) failed or timed out: {err}. Cascading...")

    if not raw_output:
        raise RuntimeError("[CRITICAL] All fast model endpoints failed.")

    raw_output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs('data', exist_ok=True)
    with open(f"data/session_{session_id}.json", "w") as f:
        json.dump(raw_output, f, indent=2)
    with open("data/resonance_output.json", "w") as f:
        json.dump(raw_output, f, indent=2)

    print(f"[SUCCESS] Audit completed for session: {session_id}")

if __name__ == "__main__":
    execute_scan()
