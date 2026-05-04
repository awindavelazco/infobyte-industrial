import json
import os
import random
import urllib.request
import urllib.parse
import re
import sys
from datetime import datetime

# Configurar consola para evitar errores de codificación en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# =============================================================================
# CONFIGURACIÓN DEL CONSEJO EDITORIAL
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class InfobyteEngine:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"
        self.historico_file = 'historico_noticias.txt'
        self.categories = [
            "Economía y Finanzas Personales", "Moda y Tendencias Actuales",
            "Salud Natural y Bienestar", "Alimentación Sana y Nutrición",
            "Remedios Naturales Comprobados", "Noticias Sociales y Virales",
            "Dinero y Cómo Multiplicarlo", "Teoría del Color y Psicología Visual",
            "Tendencias en Decoración del Hogar", "Materiales e Innovación en la Moda",
            "Tecnología Aplicada al Consumidor", "Política General y Tendencias Globales",
            "Neurociencia", "Biología Marina", "Astrofísica", "Robótica e IA",
            "Genética", "Paleontología", "Ingeniería de Materiales", "Meteorología",
            "Física Cuántica", "Entomología", "Geología", "Biotecnología"
        ]

    def extract_json(self, text):
        """Extractor robusto: encuentra el primer bloque JSON válido en cualquier texto."""
        if not text:
            return None
        import re
        # Intentar parsear directamente
        try:
            return json.loads(text)
        except:
            pass
        # Buscar el bloque JSON más grande dentro del texto
        matches = re.findall(r'\{.*?\}', text, re.DOTALL)
        for match in sorted(matches, key=len, reverse=True):
            try:
                return json.loads(match)
            except:
                continue
        print(f"[ERROR] No se pudo extraer JSON del texto: {text[:100]}...")
        return None

    def call_ollama(self, prompt, format_json=True):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        if format_json:
            data["format"] = "json"
            
        req = urllib.request.Request(self.url, data=json.dumps(data).encode('utf-8'))
        req.add_header("Content-Type", "application/json")
        try:
            response = urllib.request.urlopen(req, timeout=300)
            result = json.loads(response.read().decode('utf-8'))
            raw_response = result['response']
            return raw_response
        except Exception as e:
            print(f"Error en Ollama: {e}")
            return None

    # AGENTE 1: SCOUT
    def agent_scout(self, category, historico_txt):
        print(f"[SCOUT] Buscando tema único en: {category}...")
        prompt = f"""
        Actúa como un Scout de Noticias Virales. Tu objetivo es encontrar un tema fascinante y poco común en: {category}.
        
        TEMAS YA PUBLICADOS (PROHIBIDO REPETIR):
        {historico_txt}
        
        Instrucciones:
        1. El tema debe ser real y científico/tecnológico.
        2. NO repitas temas de la lista. Busca algo FRESCO.
        3. Devuelve un JSON: {{ "title": "título corto en inglés", "topic": "breve descripción" }}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result if result else {"title": f"New Discovery in {category}", "topic": category}

    # AGENTE 2: COPYWRITER
    def agent_copywriter(self, scout_data, category):
        print(f"[COPYWRITER] Redactando: {scout_data['title']}")
        prompt = f"""
        You are the Chief Editor of INFOBYTE, an expert in viral copywriting for Facebook. Write a post about: {scout_data['title']} (Category: {category}).
        
        LANGUAGE RULES (CRITICAL - DO NOT BREAK):
        - image_text_hook: ENGLISH ONLY
        - post_title: ENGLISH ONLY
        - post_body: ENGLISH ONLY
        - post_question: ENGLISH ONLY
        - post_authority: ENGLISH ONLY
        - hashtags: ENGLISH ONLY
        - postEN: ENGLISH ONLY (full post for publishing)
        - postES: SPANISH ONLY (summary for the editor to read and understand)
        
        STRUCTURE:
        
        1. IMAGE TEXT HOOK (English, max 15 words):
           Structure: [SHORT PROBLEM] — [MYSTERIOUS HINT OF SOLUTION]
           Example: 'YOUR BRAIN IS LYING TO YOU WHILE YOU SLEEP — THE SIGNAL NO ONE SEES'
           MUST be punchy, mysterious, and create curiosity. NO long sentences.
        
        2. POST COPY (6 blocks, all in English):
           - Catchy title (ALL CAPS + emojis)
           - Paragraph 1: Reframe the discovery (astonishing tone)
           - Paragraph 2: Scientific explanation (translate technical terms to emotional language)
           - Paragraph 3: What this means for the future/humanity
           - Final question for comments
        
        3. AUTHORITY CLOSE:
           - Real scientific backing (Journal, University or Institution)
        
        Return EXACTLY this JSON structure:
        {{
            "image_text_hook": "MAX 15 WORDS IN ENGLISH. [SHORT PROBLEM] — [MYSTERIOUS HINT]",
            "post_title": "TITLE IN ENGLISH HERE",
            "post_body": "The 3 paragraphs in English here...",
            "post_question": "Final question in English?",
            "post_authority": "🔍 Scientific Backing: Institution/Study",
            "hashtags": "#Tag1 #Tag2 #Tag3",
            "postEN": "Complete English post: Title + Body + Question + Authority + Hashtags",
            "postES": "Resumen en ESPAÑOL para que el editor entienda de qué trata este post."
        }}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result if result else {
            "image_text_hook": f"HIDDEN DISCOVERY — THE SECRET SCIENCE JUST REVEALED",
            "post_title": scout_data.get('title', '').upper(),
            "post_body": f"Nuevo descubrimiento en {category}.",
            "post_question": "¿Qué opinas?",
            "post_authority": "🔍 Respaldo: Fuente Científica Internacional",
            "hashtags": "#Ciencia #Infobyte",
            "postEN": f"New discovery: {scout_data.get('title','')}"
        }

    # AGENTE 3: COMPLIANCE
    def agent_compliance(self, post_content):
        print("[COMPLIANCE] Auditando seguridad...")
        prompt = f"""
        Eres el Auditor de Facebook. Revisa este post: {post_content['postEN']}
        Devuelve un JSON: {{"safe": true/false, "reason": "explicación", "fixed_post": "versión corregida"}}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result if result else {"safe": True, "fixed_post": post_content.get('postEN', '')}

    # AGENTE 4: VISUAL ARTIST — Powered by Gemini 2.0 Flash
    def agent_visual(self, post_content):
        print("[VISUAL] Generando prompt PREMIUM con Gemini...")

        title = post_content.get('post_title', post_content.get('title', 'scientific discovery'))
        category = post_content.get('category', 'science')

        # --- INTENTO PRINCIPAL: Gemini 2.0 Flash ---
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key="AIzaSyAq982rk4PvL9q243K2YW_ZhP_xPMtCItA")
            
            # Extraemos la noticia completa para darle contexto total
            full_news = post_content.get('postEN', '')
            
            prompt_instruction = f"""You are the Senior Visual Director for INFOBYTE, a luxury science magazine.
Your mission is to create a premium image prompt based on the following news content:

--- NEWS CONTENT ---
{full_news}
---

INSTRUCTIONS:
1. "Eres el Director Visual de una revista de lujo".
2. "Usa iluminación cinematográfica, texturas de alta gama (oro, titanium, cristal) y estilo de portada de National Geographic".
3. Write ONE detailed, photorealistic image prompt in English (70-90 words).
4. The scene must be directly inspired by the specific scientific/technical details of the news provided above.
5. NO generic cityscapes or astronauts unless they are the central theme of the news.
6. DO NOT include any text, titles, letters or words visible inside the image.
7. End EXACTLY with: "no text, no letters, no watermark, no overlay, clean image only."

Also write a short cinematic animation description (1 sentence, camera movement only).

Respond ONLY with this exact JSON:
{{"image_prompt": "your premium prompt here ending with clean image only.", "video_prompt": "one sentence camera movement"}}"""

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
                contents=prompt_instruction
            )
            
            result = json.loads(response.text)
            if result and result.get('image_prompt') and len(result['image_prompt']) > 30:
                print("[VISUAL] ✅ Prompt Gemini generado correctamente.")
                return result

        except Exception as e:
            print(f"[VISUAL] ⚠️ Gemini no disponible o error: {e}. Activando fallback...")

        # --- FALLBACK: Sistema Híbrido (Llama3 escena + Python assembly) ---
        print("[VISUAL] Usando sistema híbrido de respaldo...")
        scene_prompt = f"""
        You are a visual director for a luxury science magazine.
        Topic: "{title}" (category: {category}).
        Write ONE sentence in English (max 30 words) describing a powerful photorealistic visual scene.
        No camera movements. No title text. Just the scene.
        Return JSON: {{"scene": "scene description here"}}
        """
        response = self.call_ollama(scene_prompt)
        result = self.extract_json(response)
        scene = result.get('scene', f'A dramatic visualization of {title}') if result else f'A dramatic visualization of {title}'
        scene = scene.strip().strip('"').strip("'")

        import random as _random
        lighting = _random.choice([
            "cinematic volumetric lighting with dramatic god rays piercing through atmospheric haze",
            "soft golden hour light casting long shadows with deep contrast and warm tones",
            "cool blue bioluminescent lighting with glowing particles suspended in air",
            "high-contrast studio lighting with sharp shadows and metallic reflections",
            "dramatic chiaroscuro lighting reminiscent of a Renaissance painting, deep shadows"
        ])
        textures = _random.choice([
            "ultra-detailed textures of polished obsidian, brushed titanium, and liquid mercury surfaces",
            "rich textures of aged marble, crystalline structures, and iridescent glass panels",
            "hyper-detailed organic textures with microscopic precision, glowing cell membranes, and fluid dynamics",
            "luxurious materials: hammered gold, liquid chrome, and deep matte carbon fiber surfaces",
            "intricate nano-scale textures, translucent silica structures, and reflective crystalline lattices"
        ])
        style = _random.choice([
            "8k resolution, shot on Phase One IQ4 150MP, Architectural Digest quality, award-winning photography",
            "8k resolution, Unreal Engine 5 render quality, masterpiece, hyperrealism, National Geographic cover style",
            "8k ultra resolution, cinematic color grading, Science magazine cover, Hasselblad medium format quality",
            "8k, photorealistic CGI render, Nature journal cover quality, sharp focus with creamy bokeh background",
            "8k resolution, editorial photography style, Time magazine scientific edition, professional color correction"
        ])
        animation = _random.choice([
            "Slow dolly push-in towards the subject, shallow depth of field, particles floating in foreground",
            "Gentle orbital camera movement around the central subject, ethereal light shifts",
            "Slow reveal from black, cinematic zoom out exposing the full epic scene",
            "Subtle camera drift with atmospheric particles catching the light",
            "Graceful crane shot descending from above, dramatic scale reveal"
        ])

        return {
            "image_prompt": (
                f"{scene}, {lighting}, {textures}, "
                f"set against a richly detailed background that evokes the scale and wonder of the subject, "
                f"extreme depth of field with soft bokeh in the background, "
                f"atmospheric micro-particles suspended in the air catching the light, "
                f"{style}. "
                f"no text, no letters, no watermark, no overlay, clean image only."
            ),
            "video_prompt": animation
        }

    def download_image(self, prompt, filename):
        """Genera y descarga una imagen desde Pollinations.ai usando el prompt técnico."""
        print(f"[IMAGE] Generando imagen en Pollinations.ai...")
        try:
            # Crear carpeta si no existe
            img_folder = os.path.join(BASE_DIR, "fb_images")
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            
            filepath = os.path.join(img_folder, filename)
            seed = random.randint(1, 999999)
            encoded_prompt = urllib.parse.quote(prompt)
            # Usar el subdominio image.pollinations.ai que es más directo para descargar
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&seed={seed}&model=flux&nologo=true"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as response:
                content_type = response.info().get_content_type()
                if "text/html" in content_type:
                    print("[ERROR] Pollinations devolvió HTML en lugar de imagen.")
                    return None
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            
            print(f"[OK] Imagen guardada: {filepath}")
            return os.path.join("fb_images", filename) # Guardar ruta relativa para el JSON
        except Exception as e:
            print(f"[ERROR] No se pudo generar la imagen: {e}")
            return None

def main():
    engine = InfobyteEngine()
    final_posts = []
    
    # Cargar histórico
    historico_file = os.path.join(BASE_DIR, engine.historico_file)
    historico = []
    if os.path.exists(historico_file):
        with open(historico_file, 'r', encoding='utf-8') as f:
            historico = [line.strip() for line in f.readlines() if line.strip()]
            
    count = 10
    CATEGORIES = engine.categories
    
    for i in range(count):
        print(f"\n--- Procesando Noticia {i+1}/{count} ---")
        
        try:
            # 1. SCOUT
            is_unique = False
            attempts = 0
            scout_data = {}
            current_cat = ""
            
            while not is_unique and attempts < 5:
                current_cat = random.choice(CATEGORIES)
                scout_data = engine.agent_scout(current_cat, "\n".join(historico))
                title = scout_data.get('title', 'Untitled')
                
                if title.lower().strip() not in [t.lower().strip() for t in historico]:
                    is_unique = True
                    historico.append(title)
                else:
                    print(f"[SCOUT] Repetición evitada: {title}. Reintentando...")
                    attempts += 1

            # 2. Redacción
            copy = engine.agent_copywriter(scout_data, current_cat)
            
            # Asegurar que postEN sea un string para evitar fallos si Ollama devuelve un diccionario
            hashtags = copy.get('hashtags', '')
            if isinstance(hashtags, list):
                hashtags = " ".join(hashtags)
            post_completo_en = f"{copy.get('post_title', '')}\n\n{copy.get('post_body', '')}\n\n{copy.get('post_question', '')}\n\n{copy.get('post_authority', '')}\n\n{hashtags}"
            
            if isinstance(copy.get('postEN'), dict) or not copy.get('postEN') or len(str(copy.get('postEN'))) < 15:
                copy['postEN'] = post_completo_en
            
            # 3. Seguridad
            audit = engine.agent_compliance(copy)
            if not audit.get('safe', True):
                copy['postEN'] = audit.get('fixed_post', copy['postEN'])
            
            # 4. Visual
            visual = engine.agent_visual(copy)
            
            # 5. Generación de Imagen Real
            img_filename = f"post_{i+1}_{datetime.now().strftime('%H%M%S')}.jpg"
            image_path = engine.download_image(visual.get('image_prompt', ''), img_filename)
            
            post_es_final = copy.get('postES', 'Resumen no disponible.')
            if hashtags and str(hashtags) not in post_es_final:
                post_es_final += f"\n\n{hashtags}"
            
            final_posts.append({
                "id": i + 1,
                "category": current_cat,
                "title": scout_data.get('title', 'Sin Título'),
                "image_text_hook": copy.get('image_text_hook', ''),
                "postES": post_es_final,
                "postEN": copy.get('postEN', ''),
                "prompt": visual.get('image_prompt', 'Luxury photo, 8k'),
                "animationPrompt": visual.get('video_prompt', 'Slow cinematic zoom'),
                "image_path": image_path if image_path else ""
            })
            print(f"[OK] Noticia {i+1} completada: {scout_data.get('title','')}")

        except Exception as e:
            print(f"[SKIP] Error en Noticia {i+1}: {e}. Continuando...")
            continue

    # Guardar
    data_to_save = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "posts": final_posts
    }
    json_path = os.path.join(BASE_DIR, 'posts_content.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    # Actualizar histórico txt
    with open(historico_file, 'a', encoding='utf-8') as f:
        for p in final_posts:
            f.write(f"{p['title']}\n")

    print(f"\n[ÉXITO] {len(final_posts)} Noticias FRESCAS generadas. {len(historico)} títulos en histórico.")

if __name__ == "__main__":
    main()
