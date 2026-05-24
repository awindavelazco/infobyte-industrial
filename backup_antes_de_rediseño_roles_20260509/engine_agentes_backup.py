import json
import os
import random
import urllib.request
import urllib.parse
import re
import sys
import time
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
        # POOL DE LLAVES (Agrega aquí todas tus llaves de diferentes cuentas de Google)
        self.api_keys = [
            "AIzaSyAq982rk4PvL9q243K2YW_ZhP_xPMtCItA",
            "AIzaSyCc3NuyF1T7x-Nz0b-1m_97dmK6tUWaWcA",
            "AIzaSyBgjWfq7gHd0PA2sciACVxL4TLqLPiDdcc",
            "AIzaSyD26wgoSSdeu-Z2DYBRX9iHPUe7e1O4zB0",
            "AIzaSyBNxZIit7s6tu8MRkvtuANPxGb1O0fk9c8",
            "AIzaSyDJcSqd44cIIiz-oqr3wIMmW6bazwcfhOM"
        ]
        self.current_key_index = 0
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"
        self.historico_file = 'historico_noticias.txt'
        self.category_groups = {
            "Estilo de Vida y Dinero": {
                "weight": 20,
                "items": ["Economía y Finanzas Personales", "Dinero y Cómo Multiplicarlo", "Moda y Tendencias Actuales", "Tendencias en Decoración del Hogar", "Tecnología Aplicada al Consumidor"]
            },
            "Salud y Bienestar": {
                "weight": 30,
                "items": ["Salud Natural y Bienestar", "Alimentación Sana y Nutrición", "Remedios Naturales Comprobados"]
            },
            "Ciencia y Futuro": {
                "weight": 10,
                "items": ["Neurociencia", "Robótica e IA", "Biotecnología", "Genética", "Física Cuántica", "Ingeniería de Materiales"]
            },
            "Naturaleza y Planeta": {
                "weight": 10,
                "items": ["Biología Marina", "Paleontología", "Meteorología", "Geología", "Entomología", "Astrofísica"]
            },
            "Cultura y Sociedad": {
                "weight": 30,
                "items": ["Política General y Tendencias Globales", "Noticias Sociales y Virales", "Teoría del Color y Psicología Visual", "Materiales e Innovación en la Moda"]
            }
        }

    def get_active_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"[SISTEMA] Rotando a la llave API #{self.current_key_index + 1}...")

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

    # AGENTE 2: COPYWRITER (Viral Master — Powered by Gemini)
    def agent_copywriter(self, scout_data, category):
        print(f"[COPYWRITER] Redactando con estilo VIRAL: {scout_data['title']}")
        
        # --- INTENTO PRINCIPAL: Gemini 2.0 Flash con Rotación ---
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                
                client = genai.Client(api_key=self.get_active_key())
                
                prompt_instruction = f"""
                Actúa como el Director de Contenido Viral de INFOBYTE, experto en psicología del consumidor y copywriting para Facebook. 
                Tu misión es transformar una noticia científica en un post irresistible y transformador.
                
                TEMA: {scout_data['title']}
                DESCRIPCIÓN: {scout_data['topic']}
                CATEGORÍA: {category}

                REGLAS DE ORO DE INFOBYTE:
                1. HOOK (Gancho): Empieza con una situación de la vida diaria o una pregunta que toque una fibra sensible.
                2. VALOR REAL: Explica CÓMO esto cambia la vida del lector mañana mismo.
                3. ESTRUCTURA: Usa viñetas potentes.
                4. TONO: Inspirador, autoritario pero humano.
                5. IDIOMA: INGLÉS (para publicar) y ESPAÑOL (para el editor).

                RESPONDE ÚNICAMENTE CON ESTE JSON:
                {{
                    "postEN": "Full viral post in English",
                    "postES": "Post viral COMPLETO en Español",
                    "image_text_hook": "MAX 15 WORDS IN ENGLISH"
                }}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                
                result = json.loads(response.text)
                if result and result.get('postEN'):
                    print(f"[COPYWRITER] OK con llave #{self.current_key_index + 1}")
                    return result

            except Exception as e:
                print(f"[COPYWRITER] Advertencia: Fallo con llave #{self.current_key_index + 1}: {e}")
                self.rotate_key()
                attempts += 1
                time.sleep(1)

        print("[COPYWRITER] ❌ Todas las llaves fallaron. Usando Llama3...")

        # --- FALLBACK: Ollama (Llama3) ---
        prompt_fallback = f"""
        You are the Chief Editor of INFOBYTE. Write a viral Facebook post about: {scout_data['title']} (Category: {category}).
        Ensure you include an English version for publishing and a Spanish version for the editor.
        Return JSON: {{ "postEN": "...", "postES": "...", "image_text_hook": "..." }}
        """
        response = self.call_ollama(prompt_fallback)
        result = self.extract_json(response)
        return result if result else {
            "image_text_hook": f"HIDDEN DISCOVERY — THE SECRET SCIENCE JUST REVEALED",
            "postEN": f"New discovery: {scout_data.get('title','')}",
            "postES": f"Nuevo descubrimiento en {category}."
        }

    # AGENTE 3: COMPLIANCE
    def agent_compliance(self, post_content):
        print("[COMPLIANCE] Auditando seguridad...")
        prompt = f"""
        Actúa como un Auditor Senior de Políticas de Comunidad de Meta (Facebook). 
        Tu objetivo es asegurar que este post NO sea baneado ni marcado como spam/sensacionalismo.
        
        REVISA ESTE POST: {post_content['postEN']}
        
        CRITERIOS DE AUDITORÍA:
        1. CLICKBAIT PROHIBIDO: No uses ganchos que engañen o retengan información vital.
        2. SALUD Y BIENESTAR: Prohibido prometer curas milagrosas o dar consejos médicos sin base científica.
        3. LENGUAJE SEGURO: Sin palabras que activen filtros de violencia, odio o discriminación.
        4. ESTILO EDITORIAL: El tono debe ser educativo y profesional, no puramente sensacionalista.
        
        Devuelve un JSON: {{"safe": true/false, "reason": "explicación", "fixed_post": "versión corregida si es necesario"}}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result if result else {"safe": True, "fixed_post": post_content.get('postEN', '')}

    # AGENTE 4: VISUAL ARTIST — Powered by Gemini 2.0 Flash
    def agent_visual(self, post_content):
        print("[VISUAL] Generando prompt PREMIUM con Gemini...")

        # --- INTENTO PRINCIPAL: Gemini con Rotación ---
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                
                client = genai.Client(api_key=self.get_active_key())
                full_news = post_content.get('postEN', '')
                
                prompt_instruction = f"""Eres el Director Visual de una revista de lujo. 
Tu misión es crear un prompt de imagen premium basado en esta noticia:
{full_news}

REGLAS DE ESTILO 'SAFE & PREMIUM':
1. Usa iluminación técnica (Chiaroscuro, technical Rim Lighting).
2. Estilo visual: "Professional high-end documentary photography" (SIN NOMBRES DE MARCAS).
3. Especificaciones técnicas: "Shot on 35mm lens, sharp focus, cinematic depth of field".
4. NO menciones marcas como NASA, Discovery o National Geographic.
5. NO texto ni marcas de agua.
6. Prompt en inglés (70-90 palabras) terminando en: "no text, no letters, no watermark, no overlay, clean image only."

Responde solo JSON: {{"image_prompt": "...", "video_prompt": "cinematic zoom"}}"""

                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                
                result = json.loads(response.text)
                if result and result.get('image_prompt'):
                    print(f"[VISUAL] OK con llave #{self.current_key_index + 1}")
                    return result

            except Exception as e:
                wait_time = 2 ** attempts # 1s, 2s, 4s, 8s, 16s, 32s
                print(f"[VISUAL] Advertencia: Fallo con llave #{self.current_key_index + 1}: {e}")
                print(f"[SISTEMA] Reintentando en {wait_time}s con espera exponencial...")
                time.sleep(wait_time)
                self.rotate_key()
                attempts += 1

        # Fallback inteligente COMENTADO para la prueba de estrés
        print("[VISUAL] ❌ El pool de 6 llaves ha fallado tras agotar la espera exponencial.")
        return None
        # news_title = post_content.get('post_title', post_content.get('title', 'Modern Innovation'))
        # return {
        #     "image_prompt": f"Cinematic visualization of {news_title}, technical rim lighting, chiaroscuro, professional documentary photography aesthetic, 35mm lens, no text, clean image only.",
        #     "video_prompt": "Slow cinematic zoom."
        # }

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
            
    count = 1
    
    for i in range(count):
        print(f"\n--- Procesando Noticia {i+1}/{count} ---")
        
        try:
            # 1. SCOUT con Pesos Editoriales
            is_unique = False
            attempts = 0
            scout_data = {}
            current_cat = ""
            
            # Obtener grupos y pesos para random.choices
            groups = list(engine.category_groups.keys())
            weights = [engine.category_groups[g]["weight"] for g in groups]
            
            while not is_unique and attempts < 5:
                # Elegir primero el grupo basado en el peso editorial
                selected_group = random.choices(groups, weights=weights, k=1)[0]
                # Elegir una categoría dentro de ese grupo
                current_cat = random.choice(engine.category_groups[selected_group]["items"])
                
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
            
            # Pausa corta para no saturar RPM de Gemini
            time.sleep(2)
            
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
            
            # Pausa corta antes de la siguiente noticia
            time.sleep(1)
            
            # 5. Generación de Imagen Real
            # Comentado por solicitud: Ya que el sistema ya genera el prompt maestro
            # img_filename = f"post_{i+1}_{datetime.now().strftime('%H%M%S')}.jpg"
            # image_path = engine.download_image(visual.get('image_prompt', ''), img_filename)
            image_path = "" 
            
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
            
            # --- PAUSA DE SEGURIDAD ---
            if i < count - 1:
                print(f"[SISTEMA] Pausa de 6 segundos para proteger cuota de Gemini...")
                time.sleep(6)

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
