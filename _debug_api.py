import json
from engine_agentes import InfobyteEngine
from google import genai
from google.genai import types

def diagnostic():
    engine = InfobyteEngine()
    key = engine.get_active_key()
    print(f"Probando llave: {key[:10]}...")
    
    client = genai.Client(api_key=key)
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            config=types.GenerateContentConfig(response_mime_type="application/json"),
            contents="Generate a valid JSON with a 'test' key and 'ok' value."
        )
        print("Respuesta recibida:")
        print(response.text)
    except Exception as e:
        print(f"ERROR DETECTADO: {e}")

if __name__ == "__main__":
    diagnostic()
