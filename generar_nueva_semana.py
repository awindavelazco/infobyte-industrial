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

def generate_weekly_content():
    print("==================================================")
    print("🚀 INICIANDO GENERACIÓN DE SEMANA INFOBYTE 🚀")
    print("==================================================")
    
    engine = InfobyteEngine()
    client = genai.Client(api_key=engine.get_active_key())
    
    # --- 1. GENERAR 7 APUNTES DEL ALMA (SPIRIT) ---
    print("\n>>> FASE 1: Generando 7 Apuntes del Alma (Spirit)...")
    # Limpiamos interfaz borrando archivos previos
    with open('frases_content.json', 'w', encoding='utf-8') as f: json.dump({"phrases":[]}, f)
    with open('quizzes_content.json', 'w', encoding='utf-8') as f: json.dump({"quizzes":[]}, f)
    with open('posts_content.json', 'w', encoding='utf-8') as f: json.dump({"posts":[]}, f)
    
    hist_spirit = read_history("historico_spirit.txt")
    prompt_spirit = f"""
    Eres un Maestro Zen y Escritor Premium. Genera 7 reflexiones profundas para 'Apuntes del Alma'.
    Temas ya tocados (NO REPETIR):
    {hist_spirit}
    
    Devuelve un JSON estricto con esta estructura:
    {{
      "phrases": [
        {{
          "id": 1,
          "post_title": "Título del tema en inglés",
          "hook_text": "Breve frase reflexiva de impacto (Max 15 palabras) SIN EMOJIS",
          "postEN": "Post completo en inglés con hashtags...",
          "postES": "Traducción exacta al español...",
          "visual_prompt": "Prompt visual cinemático enfocado en naturaleza, luz suave. NO TEXT, NO LETTERS."
        }}
      ]
    }}
    """
    try:
        res = client.models.generate_content(
            model='gemini-2.0-flash',
            config=types.GenerateContentConfig(response_mime_type="application/json"),
            contents=prompt_spirit
        )
        spirit_data = json.loads(res.text)
        with open('frases_content.json', 'w', encoding='utf-8') as f:
            json.dump(spirit_data, f, indent=2, ensure_ascii=False)
        for p in spirit_data.get('phrases', []):
            append_history("historico_spirit.txt", p.get('post_title', ''))
        print("✅ 7 Apuntes del Alma generados con éxito.")
    except Exception as e:
        print(f"❌ Error en Spirit: {e}")

    # --- 2. GENERAR 28 QUIZZES (En 4 lotes de 7 para mayor calidad) ---
    print("\n>>> FASE 2: Generando 28 Quizzes Científicos (4 lotes de 7)...")
    all_quizzes = []
    hist_quizzes = read_history("historico_quizzes.txt")
    
    for lote in range(4):
        print(f"    -> Generando Lote {lote+1}/4...")
        prompt_quizzes = f"""
        Eres un experto en Psicología y Neurociencia. Genera 7 Quizzes visuales virales únicos.
        Temas ya tocados (PROHIBIDO REPETIR):
        {hist_quizzes}
        
        Estructura JSON:
        {{
          "quizzes": [
            {{
              "headline": "Título SIN EMOJIS (Max 10 palabras)",
              "options": ["OPCION1", "OPCION2", "OPCION3", "OPCION4"],
              "postEN": "Post en inglés interactivo explicando la ciencia de cada opción 1-4. Incluye hashtags.",
              "postES": "Traducción COMPLETA al español de igual extensión. Incluye hashtags.",
              "visual_prompt": "Prompt visual macro, surrealista científico. NO TEXT, NO LETTERS."
            }}
          ]
        }}
        """
        try:
            res = client.models.generate_content(
                model='gemini-2.0-flash',
                config=types.GenerateContentConfig(response_mime_type="application/json"),
                contents=prompt_quizzes
            )
            lote_data = json.loads(res.text)
            for q in lote_data.get('quizzes', []):
                q['id'] = len(all_quizzes) + 1
                all_quizzes.append(q)
                hist_quizzes += f"\n{q.get('headline','')}"
                append_history("historico_quizzes.txt", q.get('headline', ''))
            
            # Guardado parcial
            with open('quizzes_content.json', 'w', encoding='utf-8') as f:
                json.dump({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "quizzes": all_quizzes}, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"❌ Error en Lote {lote+1} de Quizzes: {e}")
            time.sleep(5)
    print(f"✅ {len(all_quizzes)} Quizzes generados con éxito.")

    # --- 3. GENERAR 28 NOTICIAS (Usando motor dinámico con Histórico) ---
    print("\n>>> FASE 3: Generando 28 Noticias Dinámicas (Scout & Copywriter)...")
    hist_news = read_history("historico_noticias.txt")
    
    # Categorías clave para Infobyte
    categorias_infobyte = [
        "Neurociencia y Cerebro", "Biología Marina", "Astronomía y Espacio", 
        "Robótica e Inteligencia Artificial", "Remedios y Salud Natural", 
        "Teoría del Color y Psicología", "Avances Médicos"
    ]
    
    todas_las_noticias = []
    
    for i in range(28):
        cat_actual = categorias_infobyte[i % len(categorias_infobyte)]
        print(f"\n[SISTEMA] Procesando Noticia Dinámica {i+1}/28: Categoría {cat_actual}")
        
        # 1. Scout busca una noticia fresca que NO esté en el historial
        scout_data = engine.agent_scout(cat_actual, hist_news)
        if not scout_data or not scout_data.get('title'):
            scout_data = {"title": f"New Scientific Discovery in {cat_actual}", "topic": cat_actual}
        
        # Actualizamos el historial en memoria para que no se repita en este mismo loop
        hist_news += f"\n- {scout_data['title']}"
        append_history("historico_noticias.txt", scout_data['title'])
        
        # 2. Redacción Viral
        copy_data = engine.agent_copywriter(scout_data, cat_actual)
        
        # 3. Prompt Visual
        vp = engine.agent_visual(scout_data)
        
        post_final = {
            "id": i + 1,
            "category": cat_actual,
            "title": scout_data['title'],
            "headline": copy_data.get('image_text_hook', scout_data['title']),
            "postES": copy_data.get('postES', ''),
            "postEN": copy_data.get('postEN', ''),
            "generated_by_text": "Gemini 2.0 Flash",
            "visual_prompt": vp,
            "image_path": ""
        }
        todas_las_noticias.append(post_final)
        
        # Guardado incremental para seguridad
        with open('posts_content.json', 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "posts": todas_las_noticias
            }, f, ensure_ascii=False, indent=2)

    print("\n==================================================")
    print(f"🎯 ¡LOTE SEMANAL COMPLETO! ({len(todas_las_noticias) + len(all_quizzes) + 7} POSTS) 🎯")
    print("==================================================")

if __name__ == "__main__":
    generate_weekly_content()
