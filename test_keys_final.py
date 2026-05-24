import json
import os
from google import genai

def test_key(key):
    try:
        client = genai.Client(api_key=key)
        # Intentamos una llamada mínima con el modelo más estable
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Hi"
        )
        return True, "ACTIVA"
    except Exception as e:
        return False, str(e)

with open("api_keys.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    video_keys = data.get("video_keys", [])
    news_keys = data.get("news_keys", [])

print("--- VERIFICANDO LLAVES DE VIDEO ---")
for i, key in enumerate(video_keys):
    success, msg = test_key(key)
    print(f"Video Key #{i+1}: {msg}")

print("\n--- VERIFICANDO LLAVES DE NOTICIAS ---")
for i, key in enumerate(news_keys):
    success, msg = test_key(key)
    print(f"News Key #{i+1}: {msg}")
