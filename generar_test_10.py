
import os
import json
import time
from datetime import datetime
from google import genai
from google.genai import types
from engine_agentes import InfobyteEngine

def read_history(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()
        return ""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def append_history(filename, text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + "\n")

def safe_generate(engine, prompt, retries=5):
    for attempt in range(retries):
        try:
            client = genai.Client(api_key=engine.get_active_key())
            res = client.models.generate_content(
                model='gemini-2.0-flash',
                config=types.GenerateContentConfig(response_mime_type="application/json"),
                contents=prompt
            )
            return json.loads(res.text)
        except Exception as e:
            print(f"⚠️ Error (Intento {attempt+1}): {e}. Rotando llave...")
            engine.rotate_key()
            time.sleep(5)
    return None

def run_test_10():
    print("==================================================")
    print("🧪 PRUEBA BLINDADA INFOBYTE (10-10-7) 🧪")
    print("==================================================")
    
    engine = InfobyteEngine()
    
    # 1. SPIRIT
    print("\n>>> FASE 1: Spirit (7)...")
    prompt_spirit = "Generate 7 deep Zen reflections. Return ONLY valid JSON with this exact structure: {\"phrases\": [{\"id\":1, \"post_title\":\"...\", \"hook_text\":\"...\", \"postEN\":\"...\", \"postES\":\"...\", \"visual_prompt\":\"...\"}]}"
    data = safe_generate(engine, prompt_spirit)
    if data and isinstance(data.get('phrases'), list) and len(data['phrases']) > 0:
        data['generated_at'] = datetime.now().strftime('%d %b %Y %H:%M')
        with open('frases_content.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    OK - {len(data['phrases'])} frases escritas.")
    else:
        print("    ERROR SCHEMA - frases_content.json NO sobreescrito. Datos anteriores conservados.")
    
    # 2. QUIZZES
    print("\n>>> FASE 2: Quizzes (10)...")
    prompt_quizzes = "Generate 10 viral science quizzes for Facebook. Return ONLY valid JSON with this exact structure: {\"quizzes\": [{\"id\":1, \"topic\":\"...\", \"headline\":\"...\", \"hook_question\":\"...\", \"postEN\":\"...\", \"postES\":\"...\", \"visual_prompt\":\"...\"}]}"
    data = safe_generate(engine, prompt_quizzes)
    if data and isinstance(data.get('quizzes'), list) and len(data['quizzes']) > 0:
        for i, q in enumerate(data['quizzes']): q['id'] = i + 1
        data['generated_at'] = datetime.now().strftime('%d %b %Y %H:%M')
        with open('quizzes_content.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"    OK - {len(data['quizzes'])} quizzes escritos.")
    else:
        print("    ERROR SCHEMA - quizzes_content.json NO sobreescrito. Datos anteriores conservados.")
            
    # 3. NOTICIAS
    print("\n>>> FASE 3: Noticias (10)...")
    noticias = []
    categorias = ["Espacio", "Mente", "Naturaleza", "Futuro", "Salud"]
    hist_news = read_history("historico_noticias.txt")
    
    for i in range(10):
        cat = categorias[i % len(categorias)]
        print(f"    Noticia {i+1}/10 - {cat}")
        try:
            scout = engine.agent_scout(cat, hist_news)
            copy = engine.agent_copywriter(scout, cat)
            vp = engine.agent_visual(scout)
            
            post = {
                "id": i + 1,
                "category": cat,
                "title": scout['title'],
                "headline": copy.get('image_text_hook', scout['title']),
                "postES": copy.get('postES', ''),
                "postEN": copy.get('postEN', ''),
                "visual_prompt": vp
            }
            noticias.append(post)
            append_history("historico_noticias.txt", scout['title'])
            with open('posts_content.json', 'w', encoding='utf-8') as f:
                json.dump({
                    "generated_at": datetime.now().strftime('%d %b %Y %H:%M'),
                    "posts": noticias
                }, f, indent=2, ensure_ascii=False)
            time.sleep(2) # Pausa anti-429
        except Exception as e:
            print(f"❌ Error en noticia {i+1}: {e}")

    print("\n✅ PRUEBA FINALIZADA. Auditando...")
    os.system("python auditor_calidad.py")

if __name__ == "__main__":
    run_test_10()
