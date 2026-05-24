import json
import os
from google import genai

def test_key(key):
    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Hi"
        )
        return True, "OK"
    except Exception as e:
        return False, str(e)

with open("api_keys.json", "r", encoding="utf-8") as f:
    keys = json.load(f).get("video_keys", [])

print(f"Testing {len(keys)} video keys...")
for i, key in enumerate(keys):
    success, msg = test_key(key)
    status = "ACTIVA" if success else f"FALLO: {msg}"
    print(f"Key #{i+1}: {status}")
    if success:
        print("\nFound at least one active key!")
        break
