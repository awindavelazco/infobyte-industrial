import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

prompt = """
Genera ESTRICTAMENTE un arreglo JSON con 2 objetos.
Son 2 noticias sobre DISEÑO DE MODA o TECNO-MODA (Innovación, Tejidos del futuro, Wearables).
NO hables sobre "Adobe Primrose" (vestido que cambia de color) ni de "Zapatillas 3D Zellerfeld" o "Ropa 3D impresa", ya que esos temas están repetidos.

Estructura de CADA UNO de los 2 objetos:
{
  "category": "Moda",
  "title": "String corto",
  "postES": "String (Noticia en español, muy detallada usando emojis y hashtags al final)",
  "postEN": "String (Misma noticia en ingles, detallada)",
  "prompt": "String descriptivo fotorealista para generar una imagen cuadrada en inglés. Ejemplo: A cinematic photography of..."
}

Devuelve SOLO EL ARREGLO JSON [ ... ]
"""

data = {
    "model": "llama3",
    "prompt": prompt,
    "stream": False,
    "format": "json",
    "options": {
        "temperature": 0.4
    }
}

req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(data).encode('utf-8'))
req.add_header("Content-Type", "application/json")
print("Solicitando 2 noticias de MODA a tu Ollama local (llama3)...")

try:
    response = urllib.request.urlopen(req, timeout=180)
    result = json.loads(response.read().decode('utf-8'))
    raw_json = result['response']
    
    print("Ollama respondió. Analizando...")
    
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
        new_noticias = []
    
    if len(new_noticias) != 2:
        print(f"Ollama devolvió {len(new_noticias)} noticias. Recortando/usando disponibles.")
        new_noticias = new_noticias[:2]

    with open('posts_content.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
        
    # Asignar IDs nuevos
    latest_id = max([p['id'] for p in posts]) if posts else 0
    
    new_titles = []
    for i, n in enumerate(new_noticias):
        post = {
            "id": latest_id + i + 1,
            "category": n.get("category", "Moda"),
            "title": n.get("title", "Innovación de Moda"),
            "postES": n.get("postES", ""),
            "postEN": n.get("postEN", ""),
            "prompt": n.get("prompt", "")
        }
        posts.append(post)
        new_titles.append(post["title"])
        
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print("posts_content.json actualizado.")
    
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
            obj_str = f'  {{\n    category: "{cat}",\n    title: "{tit}",\n    postES: {pes},\n    postEN: {pen},\n    prompt: "{prm}"\n  }}'
            js_objects.append(obj_str)
        
        new_content = parts[0] + 'const newsData = [\n' + ',\n'.join(js_objects) + '\n];' + tail_parts[1]
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("script.js actualizado.")
        
    with open('historico_noticias.txt', 'a', encoding='utf-8') as f:
        for idx, title in enumerate(new_titles):
            f.write(f"{latest_id + idx + 1}. {title}\n")
    print("historico_noticias.txt actualizado.")
    
except Exception as e:
    print(f"Error procesando Ollama: {e}")
