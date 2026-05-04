import json
import os
import random
import urllib.request
import re
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN DEL CONSEJO EDITORIAL
# =============================================================================

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

    # AGENTE 4: VISUAL ARTIST (Hybrid — LLM scene + Python premium assembly)
    def agent_visual(self, post_content):
        print("[VISUAL] Construyendo prompt de imagen PREMIUM...")
        
        title = post_content.get('post_title', post_content.get('title', 'scientific discovery'))
        category = post_content.get('category', 'science')
        
        # --- PASO 1: El LLM solo describe LA ESCENA CENTRAL (1 oración, sin texto) ---
        scene_prompt = f"""
        You are a visual director for a luxury science magazine.
        The topic of the photo is: "{title}" (category: {category}).
        
        Write ONLY ONE SENTENCE in English describing a powerful, photorealistic visual scene 
        that represents this topic. Rules:
        - Do NOT mention the title text literally.
        - Do NOT describe camera movements.
        - Do NOT add any explanation, just the scene description.
        - Maximum 30 words.
        - Focus on the most visually striking element of the topic.
        
        Return JSON: {{"scene": "one sentence scene description here"}}
        """
        response = self.call_ollama(scene_prompt)
        result = self.extract_json(response)
        scene = result.get('scene', f'A dramatic and detailed visualization of {title}') if result else f'A dramatic and detailed visualization of {title}'
        
        # Limpiar la escena de comillas y texto extra
        scene = scene.strip().strip('"').strip("'")

        # --- PASO 2: Python ensambla el prompt premium completo (estructura fija) ---
        lighting_options = [
            "cinematic volumetric lighting with dramatic god rays piercing through atmospheric haze",
            "soft golden hour light casting long shadows with deep contrast and warm tones",
            "cool blue bioluminescent lighting with glowing particles suspended in air",
            "high-contrast studio lighting with sharp shadows and metallic reflections",
            "dramatic chiaroscuro lighting reminiscent of a Renaissance painting, deep shadows"
        ]
        texture_options = [
            "ultra-detailed textures of polished obsidian, brushed titanium, and liquid mercury surfaces",
            "rich textures of aged marble, crystalline structures, and iridescent glass panels",
            "hyper-detailed organic textures with microscopic precision, glowing cell membranes, and fluid dynamics",
            "luxurious materials: hammered gold, liquid chrome, and deep matte carbon fiber surfaces",
            "intricate nano-scale textures, translucent silica structures, and reflective crystalline lattices"
        ]
        style_options = [
            "8k resolution, shot on Phase One IQ4 150MP, Architectural Digest quality, award-winning photography",
            "8k resolution, Unreal Engine 5 render quality, masterpiece, hyperrealism, National Geographic cover style",
            "8k ultra resolution, cinematic color grading, Science magazine cover, Hasselblad medium format quality",
            "8k, photorealistic CGI render, Nature journal cover quality, sharp focus with creamy bokeh background",
            "8k resolution, editorial photography style, Time magazine scientific edition, professional color correction"
        ]
        animation_options = [
            "Slow dolly push-in towards the subject, shallow depth of field, particles floating in foreground",
            "Gentle orbital camera movement around the central subject, ethereal light shifts",
            "Slow reveal from black, cinematic zoom out exposing the full epic scene",
            "Subtle camera drift with atmospheric particles catching the light",
            "Graceful crane shot descending from above, dramatic scale reveal"
        ]
        
        import random as _random
        lighting = _random.choice(lighting_options)
        textures = _random.choice(texture_options)
        style = _random.choice(style_options)
        animation = _random.choice(animation_options)
        
        full_image_prompt = (
            f"{scene}, {lighting}, {textures}, "
            f"set against a richly detailed background that evokes the scale and wonder of the subject, "
            f"extreme depth of field with soft bokeh in the background, "
            f"atmospheric micro-particles suspended in the air catching the light, "
            f"{style}. "
            f"no text, no letters, no watermark, no overlay, clean image only."
        )
        
        return {
            "image_prompt": full_image_prompt,
            "video_prompt": animation
        }

def main():
    engine = InfobyteEngine()
    final_posts = []
    
    # Cargar histórico
    historico = []
    if os.path.exists(engine.historico_file):
        with open(engine.historico_file, 'r', encoding='utf-8') as f:
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
                "animationPrompt": visual.get('video_prompt', 'Slow cinematic zoom')
            })
            print(f"[OK] Noticia {i+1} completada: {scout_data.get('title','')}")

        except Exception as e:
            print(f"[SKIP] Error en Noticia {i+1}: {e}. Continuando...")
            continue

    # Guardar
    if not os.path.exists('data'): os.mkdir('data')
    data_to_save = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "posts": final_posts
    }
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    # Actualizar histórico txt
    with open('historico_noticias.txt', 'a', encoding='utf-8') as f:
        for p in final_posts:
            f.write(f"{p['title']}\n")

    print(f"\n[ÉXITO] 10 Noticias FRESCAS generadas. {len(historico)} títulos en histórico.")

if __name__ == "__main__":
    main()
