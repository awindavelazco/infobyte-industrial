import urllib.request
import json
import re
import sys
import os
import random

sys.stdout.reconfigure(encoding='utf-8')

historico_temas = ""
if os.path.exists('historico_noticias.txt'):
    with open('historico_noticias.txt', 'r', encoding='utf-8') as f:
        historico_temas = f.read()

# Pool completo de categorías (editoriales + ciencia) para máxima variedad
ramas_ciencia = [
    # Temas editoriales del canal
    "Economía y Finanzas Personales",
    "Moda y Tendencias Actuales",
    "Salud Natural y Bienestar",
    "Alimentación Sana y Nutrición",
    "Remedios Naturales Comprobados",
    "Noticias Sociales y Virales",
    "Dinero y Cómo Multiplicarlo",
    "Teoría del Color y Psicología Visual",
    "Tendencias en Decoración del Hogar",
    "Materiales e Innovación en la Industria de la Moda",
    "Tecnología Aplicada al Consumidor",
    "Política General y Tendencias Globales",
    # Ciencia y tecnología
    "Neurociencia y el Cerebro Humano",
    "Biología Marina y Océanos",
    "Nanotecnología Médica",
    "Astrofísica y Exploración Espacial",
    "Robótica e Inteligencia Artificial",
    "Genética y ADN",
    "Paleontología y Fósiles",
    "Ingeniería de Materiales",
    "Meteorología y Fenómenos Climáticos",
    "Física Cuántica",
    "Entomología (Insectos asombrosos)",
    "Geología y Volcanes",
    "Biotecnología y Medicina del Futuro",
]

import random
ramas_elegidas = random.sample(ramas_ciencia, 10)
ramas_texto = ", ".join(ramas_elegidas)

prompt = f"""
Genera un arreglo JSON con EXACTAMENTE 10 objetos. Una noticia por cada categoría de esta lista:
{ramas_texto}

HISTORIAL (NO repetir estos temas):
{historico_temas}

REGLAS:
1. Cada noticia debe pertenecer estrictamente a su categoría asignada.
2. Menciona la institución real que hizo el descubrimiento.
3. PROHIBIDO: CRISPR, CO2, cambio climático, evolución humana, fusión nuclear.

Formato de CADA objeto:
{{
  "category": "la categoría asignada",
  "title": "titular atractivo en inglés",
  "postEN": "2-3 párrafos en inglés + '🔍 Fact Check: Search for X' + pregunta de debate + '━━━━━━━━━━━━━━━\\n📡 INFOBYTE — Science. Verified.\\n🔔 Follow us!\\n\\n#Infobyte #tag1 #tag2 #tag3 #tag4 #tag5'",
  "postES": "traducción literal exacta del postEN al español",
  "prompt": "imagen viral: ángulo específico + narrativa de contraste + detalle emocional + estilo fotorrealista sin texto ni ilustraciones, ratio 1:1",
  "animationPrompt": "descripción de movimiento de cámara lento y cinematográfico"
}}

Devuelve SOLO el arreglo JSON [ ... ] sin texto adicional.
"""

data = {
    "model": "llama3",
    "prompt": prompt,
    "stream": False,
    "format": "json",
    "options": {
        "temperature": 0.7
    }
}

req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(data).encode('utf-8'))
req.add_header("Content-Type", "application/json")
print("Solicitando respuestas a tu Ollama local (llama3) con format JSON...")

try:
    response = urllib.request.urlopen(req, timeout=600)
    result = json.loads(response.read().decode('utf-8'))
    raw_json = result['response']
    
    print("Ollama respondió. Intentando parsear...")
    
    try:
        new_noticias = json.loads(raw_json)
        if isinstance(new_noticias, dict):
            for k, v in new_noticias.items():
                if isinstance(v, list):
                    new_noticias = v
                    break
    except:
        match = re.search(r'\[.*\]', raw_json, re.DOTALL)
        if match:
            new_noticias = json.loads(match.group(0))
        else:
            new_noticias = []
    
    if not isinstance(new_noticias, list):
        if isinstance(new_noticias, dict):
            new_noticias = [new_noticias]
        else:
            new_noticias = []
            
    if len(new_noticias) < 5:
        print(f"Alerta: Ollama devolvió solo {len(new_noticias)} noticias. Se necesitan al menos 5.")
    else:
        print(f"Ollama generó {len(new_noticias)} noticias correctamente.")
    new_noticias = new_noticias[:10]

    # ─── VERIFICADOR AUTOMÁTICO DE DUPLICADOS ───────────────────────────────
    print("\n🔍 Verificando duplicados internos...")
    titulos = [n.get('title', '').lower() for n in new_noticias]
    categorias = [n.get('category', '').lower() for n in new_noticias]
    duplicados_encontrados = False

    for i in range(len(titulos)):
        palabras_i = set(titulos[i].split())
        for j in range(i + 1, len(titulos)):
            palabras_j = set(titulos[j].split())
            # Si comparten más del 40% de palabras, son sospechosas
            comunes = palabras_i & palabras_j - {'a', 'the', 'of', 'in', 'and', 'to', 'for', 'with', 'new', 'how'}
            similitud = len(comunes) / max(len(palabras_i), 1)
            if similitud > 0.4:
                print(f"  ⚠️  POSIBLE DUPLICADO: Noticia {i+1} y {j+1} son similares:")
                print(f"      [{i+1}] {new_noticias[i].get('title','')}")
                print(f"      [{j+1}] {new_noticias[j].get('title','')}")
                duplicados_encontrados = True

    # Verificar también categorías repetidas
    categorias_unicas = set()
    for i, cat in enumerate(categorias):
        if cat in categorias_unicas:
            print(f"  ⚠️  CATEGORÍA REPETIDA: Noticia {i+1} repite la categoría '{cat}'")
            duplicados_encontrados = True
        categorias_unicas.add(cat)

    if not duplicados_encontrados:
        print("  ✅ Sin duplicados detectados. ¡Las 10 noticias son únicas!\n")
    else:
        print("\n  💡 Consejo: Corre el script de nuevo para regenerar una tanda sin repetidos.\n")
    # ────────────────────────────────────────────────────────────────────────

    # Reemplazar TODO el archivo con las noticias nuevas (cero mezcla con contenido viejo)
    old_titles = []
    new_titles = []
    new_prompts_info = []
    posts = []

    for idx, new_n in enumerate(new_noticias):
        posts.append({
            "category": new_n.get('category', 'Technology'),
            "title": new_n.get('title', 'New Article'),
            "postES": new_n.get('postES', ''),
            "postEN": new_n.get('postEN', ''),
            "prompt": new_n.get('prompt', ''),
            "animationPrompt": new_n.get('animationPrompt', ''),
            "id": idx + 1
        })
        new_titles.append(new_n.get('title', ''))
        new_prompts_info.append(f"[ID {idx+1}]: {new_n.get('prompt', '')}")
            
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print("posts_content.json actualizado exitosamente.")
    
    with open('script.js', 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('const newsData = [', 1)
    if len(parts) == 2:
        tail_parts = parts[1].split('];', 1)
        js_objects = []
        for item in posts:
            cat = item.get('category', '').replace('"', '\\"')
            tit = item.get('title', '').replace('"', '\\"')
            pes = json.dumps(item.get('postES', ''), ensure_ascii=False)
            pen = json.dumps(item.get('postEN', ''), ensure_ascii=False)
            prm = item.get('prompt', '').replace('"', '\\"')
            anim = item.get('animationPrompt', '').replace('"', '\\"')
            obj_str = f'  {{\n    category: "{cat}",\n    title: "{tit}",\n    postES: {pes},\n    postEN: {pen},\n    prompt: "{prm}",\n    animationPrompt: "{anim}"\n  }}'
            js_objects.append(obj_str)
        
        new_content = parts[0] + 'const newsData = [\n' + ',\n'.join(js_objects) + '\n];' + tail_parts[1]
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("script.js actualizado exitosamente.")
        
    with open('historico_noticias.txt', 'r', encoding='utf-8') as f:
        historico = f.readlines()
        
    for i, old_title in enumerate(old_titles):
        for j, line in enumerate(historico):
            if old_title in line and i < len(new_titles):
                num_prefix = line.split('.')[0]
                historico[j] = f"{num_prefix}. {new_titles[i]}\n"
                break
                
    with open('historico_noticias.txt', 'w', encoding='utf-8') as f:
        f.writelines(historico)
    print("historico_noticias.txt actualizado exitosamente.")
    
    # Save the new prompts so Antigravity can read them
    with open('new_prompts_to_generate.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_prompts_info))

except Exception as e:
    print(f"Error procesando la solicitud con Ollama: {e}")
