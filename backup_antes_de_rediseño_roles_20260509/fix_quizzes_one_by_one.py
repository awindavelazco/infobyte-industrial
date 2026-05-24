import json
import time
import os
from engine_agentes import InfobyteEngine
from google import genai
from google.genai import types

def generate_quizzes_individual():
    engine = InfobyteEngine()
    all_quizzes = []
    
    print("🚀 INICIANDO GENERACIÓN INDIVIDUAL DE 28 QUIZZES (CALIDAD INDUSTRIAL) 🚀")
    
    # Categorías para variedad
    categorias = ["Neurociencia", "Psicología Social", "Biología Evolutiva", "Física Cuántica", "Arqueología", "Astrofísica"]

    for i in range(28):
        cat = categorias[i % len(categorias)]
        print(f"\n[SISTEMA] Generando Quiz {i+1}/28 (Categoría: {cat})...")
        
        # Cargar historial actualizado en cada vuelta
        try:
            with open('historico_quizzes.txt', 'r', encoding='utf-8') as f:
                hist = f.read()[-2000:]
        except:
            hist = ""

        prompt = f"""
        Eres un experto en {cat}. Genera UN Quiz visual viral único y fascinante.
        TEMAS PROHIBIDOS (YA USADOS): {hist}
        
        MANDATORY RULES:
        1. postEN: 150+ words, interactive, educational.
        2. postES: Full translation, same length as English.
        3. image_text_hook (headline): Max 10 words, NO EMOJIS.
        
        Return JSON:
        {{
          "headline": "Short punchy title",
          "options": ["A", "B", "C", "D"],
          "postEN": "Full English post...",
          "postES": "Traduccion completa...",
          "visual_prompt": "Cinematic visual prompt. NO TEXT."
        }}
        """
        
        success = False
        attempts = 0
        while not success and attempts < 3:
            try:
                client = genai.Client(api_key=engine.get_active_key())
                res = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt
                )
                quiz = json.loads(res.text)
                quiz['id'] = i + 1
                all_quizzes.append(quiz)
                
                # Guardado incremental inmediato
                with open('quizzes_content.json', 'w', encoding='utf-8') as f:
                    json.dump({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "quizzes": all_quizzes}, f, indent=2, ensure_ascii=False)
                
                # Guardar en historial
                with open('historico_quizzes.txt', 'a', encoding='utf-8') as f:
                    f.write(quiz.get('headline','') + "\n")
                
                print(f"✅ Quiz {i+1} guardado con éxito.")
                success = True
            except Exception as e:
                attempts += 1
                print(f"⚠️ Error en Quiz {i+1} (Intento {attempts}): {e}")
                engine.rotate_key()
                time.sleep(1)

    print("\n==================================================")
    print(f"🎯 PROCESO FINALIZADO: {len(all_quizzes)} QUIZZES GENERADOS 🎯")
    print("==================================================")

if __name__ == "__main__":
    generate_quizzes_individual()
