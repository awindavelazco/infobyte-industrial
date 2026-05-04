import json
import time
import os
from engine_agentes import InfobyteEngine
from google import genai
from google.genai import types

def generate_quizzes_emergency():
    engine = InfobyteEngine()
    client = genai.Client(api_key=engine.get_active_key())
    all_quizzes = []
    
    print("🚀 INICIANDO GENERACIÓN DE EMERGENCIA DE 28 QUIZZES 🚀")
    
    # Intentar cargar existentes por si acaso (para no repetir)
    try:
        with open('historico_quizzes.txt', 'r', encoding='utf-8') as f:
            hist_quizzes = f.read()
    except:
        hist_quizzes = ""

    # Generar en 7 lotes de 4 (más estable que 4 lotes de 7)
    for lote in range(7):
        print(f"\n>>> Procesando Lote {lote+1}/7...")
        prompt = f"""
        Eres un experto en Psicología y Neurociencia. Genera 4 Quizzes visuales virales únicos.
        Temas ya tocados (PROHIBIDO REPETIR):
        {hist_quizzes[-2000:]} 
        
        Devuelve un JSON estricto:
        {{
          "quizzes": [
            {{
              "headline": "Título enganchador SIN EMOJIS (Max 10 palabras)",
              "options": ["OPCION1", "OPCION2", "OPCION3", "OPCION4"],
              "postEN": "Post en inglés interactivo con hashtags...",
              "postES": "Traducción COMPLETA al español con hashtags...",
              "visual_prompt": "Prompt visual macro, surrealista científico. NO TEXT, NO LETTERS."
            }}
          ]
        }}
        """
        
        success = False
        retry_count = 0
        while not success and retry_count < 3:
            try:
                res = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt
                )
                lote_data = json.loads(res.text)
                items = lote_data.get('quizzes', [])
                for q in items:
                    q['id'] = len(all_quizzes) + 1
                    all_quizzes.append(q)
                    hist_quizzes += f"\n{q.get('headline','')}"
                    with open('historico_quizzes.txt', 'a', encoding='utf-8') as f:
                        f.write(q.get('headline','') + "\n")
                
                # Guardado incremental
                with open('quizzes_content.json', 'w', encoding='utf-8') as f:
                    json.dump({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "quizzes": all_quizzes}, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Lote {lote+1} completado. Total acumulado: {len(all_quizzes)}")
                success = True
            except Exception as e:
                retry_count += 1
                print(f"⚠️ Error en lote {lote+1} (Intento {retry_count}): {e}")
                engine.rotate_key()
                client = genai.Client(api_key=engine.get_active_key())
                time.sleep(2)
    
    print("\n==================================================")
    print(f"🎯 EMERGENCIA COMPLETADA: {len(all_quizzes)} QUIZZES LISTOS 🎯")
    print("==================================================")

if __name__ == "__main__":
    generate_quizzes_emergency()
