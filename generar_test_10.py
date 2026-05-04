
import os
import json
import time
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

def run_test_10():
    print("==================================================")
    print("🧪 EJECUTANDO PRUEBA DE CALIDAD (10-10-7) 🧪")
    print("==================================================")
    
    engine = InfobyteEngine()
    client = genai.Client(api_key=engine.get_active_key())
    
    # --- 1. SPIRIT (7) ---
    print("\n>>> FASE 1: Spirit (7)...")
    hist_spirit = read_history("historico_spirit.txt")
    prompt_spirit = f"Generate 7 deep Zen reflections for 'Apuntes del Alma'. Unique topics. Avoid repeats from: {hist_spirit}. JSON: {{'phrases': [{{'post_title':'', 'hook_text':'', 'postEN':'', 'postES':'', 'visual_prompt':''}}]}}"
    res = client.models.generate_content(model='gemini-2.0-flash', config=types.GenerateContentConfig(response_mime_type="application/json"), contents=prompt_spirit)
    with open('frases_content.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(res.text), f, indent=2, ensure_ascii=False)
    
    # --- 2. QUIZZES (10) ---
    print("\n>>> FASE 2: Quizzes (10)...")
    prompt_quizzes = "Generate 10 viral scientific quizzes. Unique topics. JSON: {{'quizzes': [{{'headline':'', 'options':[], 'postEN':'', 'postES':'', 'visual_prompt':''}}]}}"
    res = client.models.generate_content(model='gemini-2.0-flash', config=types.GenerateContentConfig(response_mime_type="application/json"), contents=prompt_quizzes)
    quizzes_data = json.loads(res.text)
    for i, q in enumerate(quizzes_data['quizzes']): q['id'] = i + 1
    with open('quizzes_content.json', 'w', encoding='utf-8') as f:
        json.dump(quizzes_data, f, indent=2, ensure_ascii=False)
    
    # --- 3. NOTICIAS (10) ---
    print("\n>>> FASE 3: Noticias Dinámicas (10)...")
    hist_news = read_history("historico_noticias.txt")
    noticias = []
    categorias = ["Neurociencia", "Biología", "Astronomía", "IA", "Salud"]
    
    for i in range(10):
        cat = categorias[i % len(categorias)]
        print(f"    Noticia {i+1}/10 - {cat}")
        scout = engine.agent_scout(cat, hist_news)
        copy = engine.agent_copywriter(scout, cat)
        vp = engine.agent_visual(scout)
        
        noticias.append({
            "id": i + 1,
            "category": cat,
            "title": scout['title'],
            "headline": copy.get('image_text_hook', scout['title']),
            "postES": copy.get('postES', ''),
            "postEN": copy.get('postEN', ''),
            "visual_prompt": vp
        })
        append_history("historico_noticias.txt", scout['title'])
        # Guardado incremental
        with open('posts_content.json', 'w', encoding='utf-8') as f:
            json.dump({"posts": noticias}, f, indent=2, ensure_ascii=False)

    print("\n✅ PRUEBA COMPLETADA. Ejecutando Auditoría Final...")
    os.system("python auditor_calidad.py")

if __name__ == "__main__":
    run_test_10()
