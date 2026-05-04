import json
import urllib.request
import re
import os

def extract(marker, text):
    pattern = rf"\[\[{marker}\]\][\s\*:]*(.*?)(?=\[\[|\Z)"
    match = re.search(pattern, text, re.S | re.I)
    return match.group(1).strip() if match else ""

def generate_missing():
    categorias_faltantes = [
        {"rubro": "Datos Insólitos", "tema": "Curiosidades fascinantes, eventos extraños o hechos sorprendentes e inusuales."},
        {"rubro": "Bienestar y Psicología", "tema": "Salud mental en la era digital, psicología de la belleza o terapias del futuro."}
    ]
    
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
        
    for cat in categorias_faltantes:
        print(f"Generando categoría faltante: {cat['rubro']}...")
        prompt_individual = f"""
Genera EXACTAMENTE 1 noticia de alto impacto.

REGLAS DE ORO DE REDACCIÓN (NIVEL ARTICULISTA):
1. MISIÓN: Escribir un REPORTAJE PROFUNDO y EXTENSO. Mínimo 500 palabras. No resumas.
2. ESTRUCTURA OBLIGATORIA (Usa exactamente estos marcadores):
   [[CATEGORY]]: {cat['rubro']}
   [[TITLE]]: Título explosivo y llamativo.
   [[POST_ES]]: El artículo en español. Debe ser muy largo, con Gancho, Contexto Técnico Profundo (mínimo 3 párrafos), Impacto Real y una Pregunta de Debate filosófico. Usa emojis y hashtags.
   [[POST_EN]]: Lo mismo en inglés, con la misma profundidad y extensión.
   [[PROMPT_IMG]]: Descripción fotorealista en inglés (1:1). NO incluyas texto, letras, ni títulos en la imagen, solo el escenario o personaje.
   [[END_STORY]]

3. TEMA OBLIGATORIO PARA ESTA NOTICIA: Debes escribir estrictamente sobre el rubro "{cat['rubro']}". Enfócate en este tema: {cat['tema']}. ¡Asegúrate de que sea fascinante!
4. EVERGREEN: Sin fechas, atemporal.
"""
        payload = {
            "model": "llama3",
            "prompt": prompt_individual,
            "stream": False,
            "options": {"temperature": 0.8, "num_predict": 3000}
        }
        
        try:
            req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(payload).encode('utf-8'))
            req.add_header("Content-Type", "application/json")
            response = urllib.request.urlopen(req, timeout=300)
            result = json.loads(response.read().decode('utf-8'))
            raw_text = result['response']
            
            postES = extract("POST_ES", raw_text).strip("* \n\t")
            if postES:
                noticia = {
                    "category": extract("CATEGORY", raw_text).strip("* \n\t") or cat['rubro'],
                    "title": extract("TITLE", raw_text).strip("* \n\t") or "Noticia",
                    "postES": postES,
                    "postEN": extract("POST_EN", raw_text).strip("* \n\t"),
                    "prompt": extract("PROMPT_IMG", raw_text).strip("* \n\t")
                }
                next_id = max([p['id'] for p in posts]) + 1 if posts else 1
                noticia['id'] = next_id
                posts.append(noticia)
                print(f"✅ Noticia {cat['rubro']} generada y guardada con éxito.")
            else:
                print(f"⚠️ Error generando {cat['rubro']}.")
        except Exception as e:
            print(f"❌ Error: {e}")

    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    generate_missing()
