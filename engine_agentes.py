import json
import urllib.request
import urllib.parse
import re
import random
import time
import os
from datetime import datetime
from google import genai
from google.genai import types

# Configurar consola para evitar errores de codificación en Windows
try:
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# =============================================================================
# CONFIGURACIÓN DEL CONSEJO EDITORIAL
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class InfobyteEngine:
    def __init__(self):
        # POOL DE LLAVES (Leídas de api_keys.json de forma segura)
        self.api_keys = []
        keys_path = os.path.join(BASE_DIR, "api_keys.json")
        if os.path.exists(keys_path):
            with open(keys_path, "r", encoding="utf-8") as f:
                self.api_keys = json.load(f).get("news_keys", [])

        if not self.api_keys:
            self.api_keys = ["LLAVE_DE_RESPALDO_AQUI"]
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
        try:
            return json.loads(text)
        except:
            pass
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
        prompt_instruction = f"""
        Actúa como un Scout de Noticias Virales. Tu objetivo es encontrar un tema fascinante y poco común en: {category}.

        TEMAS YA PUBLICADOS (PROHIBIDO REPETIR):
        {historico_txt}

        Instrucciones:
        1. El tema debe ser real y científico/tecnológico.
        2. NO repitas temas de la lista. Busca algo FRESCO.
        3. Devuelve un JSON: {{ "title": "título corto en inglés", "topic": "breve descripción" }}
        """

        attempts = 0
        while attempts < len(self.api_keys):
            try:
                client = genai.Client(api_key=self.get_active_key())
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                result = json.loads(response.text)
                if result and result.get('title'):
                    print(f"[SCOUT] OK con gemini-2.5-flash (Llave #{self.current_key_index + 1})")
                    return result
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"[SCOUT] Llave #{self.current_key_index + 1} agotada. Rotando INMEDIATAMENTE...")
                    self.rotate_key()
                    attempts += 1
                else:
                    print(f"[SCOUT] Error con llave #{self.current_key_index + 1}: {e}")
                    self.rotate_key()
                    attempts += 1

        print("[SCOUT] Activando Scout Local (Ollama) por saturación de cuota...")
        response = self.call_ollama(prompt_instruction)
        result = self.extract_json(response)
        return result if result else {"title": f"New Discovery in {category}", "topic": category}

    # AGENTE 2: COPYWRITER
    def agent_copywriter(self, scout_data, category):
        print(f"[COPYWRITER] Redactando con estilo VIRAL: {scout_data['title']}")

        prompt_instruction = f"""
        You are the Chief Editor of INFOBYTE — a viral science magazine for the US market.
        Write a COMPLETE bilingual Facebook post about:
        Title: {scout_data['title']}
        Topic: {scout_data.get('topic', category)}
        Category: {category}

        MANDATORY RULES (ZERO TOLERANCE):
        1. postEN: Full English viral post. MINIMUM 150 words.
           - Hook with emojis to grab attention
           - Science Explained section (biological/tech/psychological mechanism)
           - Action Plan (3 steps, NEVER use "Recipe", "Dose", "Ingredients" unless it's food)
           - Fact Check line: "🔍 Fact Check: Search '[Key Term] + [Real University or Institution]'"
           - Disclaimer: "Note: Always consult a professional..."
           - Signature: "📡 INFOBYTE — Science. Verified."
           - MINIMUM 3 relevant US-market hashtags (e.g. #Neuroscience #BrainHealth)

        2. postES: COMPLETE Spanish translation — SAME LENGTH AND DEPTH as postEN.
           NOT a summary. FULL translation with ALL sections.
           - MINIMUM 3 relevant hashtags in Spanish

        3. image_text_hook: A SHORT, punchy hook (MAX 10 words) that is SEMANTICALLY RELATED
           to the title '{scout_data['title']}'. DO NOT use generic phrases like
           'Mind-Blowing News', 'Discover More', or placeholder text like 'MAX 12 WORDS'.
           Example for 'Neuroplasticity': "Your Brain Can Rewire Itself. Here's How."

        4. HOOK DIVERSITY (STRICT): PROHIBITED to start multiple posts with the same phrase
           (e.g., "Ever wondered", "Did you know", "Imagine a world").
           Each of the 28 posts MUST have a unique opening style:
           - Style A: Interrogative (Question)
           - Style B: Breaking News (Urgent update)
           - Style C: Fact-based (Astonishing data)
           - Style D: Narrative (Short story/scenario)

        5. SPANISH VARIETY: PROHIBIDO empezar con "¿Alguna vez te has preguntado...?" en más de 2
           noticias de todo el batch. Si repites ganchos, el Auditor de Calidad rechazará el trabajo.


        Return EXACTLY this JSON (no extra text):
        {{
          "post_title": "{scout_data['title']}",
          "image_text_hook": "Short hook related to the title (max 10 words)",
          "postEN": "Full English post 150+ words with hook, science, action plan, fact check, disclaimer, signature, hashtags...",
          "postES": "Traduccion COMPLETA en español con TODAS las secciones igual de larga que el ingles, hashtags incluidos..."
        }}
        """

        attempts = 0
        while attempts < len(self.api_keys):
            try:
                client = genai.Client(api_key=self.get_active_key())
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                result = json.loads(response.text)
                if result and result.get('postEN'):
                    print(f"[COPYWRITER] OK con gemini-2.5-flash (Llave #{self.current_key_index + 1})")
                    result["generated_by"] = "Gemini (Cloud)"
                    result["requires_review"] = False
                    return result
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"[COPYWRITER] Llave #{self.current_key_index + 1} agotada. Rotando INMEDIATAMENTE...")
                    self.rotate_key()
                    attempts += 1
                else:
                    print(f"[COPYWRITER] Error con llave #{self.current_key_index + 1}: {e}")
                    self.rotate_key()
                    attempts += 1

        print("[COPYWRITER] Activando Redactor Local (Ollama) por saturación de cuota...")
        prompt_fallback = f"""
        You are the Chief Editor of INFOBYTE. Write a viral Facebook post about: {scout_data['title']} (Category: {category}).
        MANDATORY SECTIONS:
        1. Hook with emojis
        2. Science Explained
        3. Action Plan (NEVER use 'Recipe', 'Dose', 'Ingredients' unless it's food)
        4. Fact Check: "Search '[Term] + [Institution]'"
        5. Disclaimer: "Note: Always consult a professional..."
        6. At least 3 hashtags for the US market
        Return EXACTLY this JSON:
        {{
          "post_title": "{scout_data['title']}",
          "postEN": "Full viral post in English, 150+ words, with all sections and hashtags...",
          "postES": "Traduccion COMPLETA al español de igual extensión, con todos los apartados y hashtags...",
          "image_text_hook": "Short punchy hook related to {scout_data['title']} (max 10 words)"
        }}
        """
        response = self.call_ollama(prompt_fallback)
        result = self.extract_json(response)
        if result:
            result["generated_by"] = "Ollama (Local)"
            result["requires_review"] = True
            if not result.get('post_title'): result['post_title'] = scout_data['title']
            return result

        return {
            "generated_by": "System Fallback",
            "image_text_hook": f"New Discovery: {scout_data.get('title', 'Scientific Update')[:50]}",
            "postEN": f"New discovery: {scout_data.get('title', '')}",
            "postES": f"Nuevo descubrimiento en {category}."
        }

    # AGENTE 3: COMPLIANCE
    def agent_compliance(self, post_content):
        print("[COMPLIANCE] Auditando seguridad...")
        prompt_instruction = f"""
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

        attempts = 0
        while attempts < len(self.api_keys):
            try:
                client = genai.Client(api_key=self.get_active_key())
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                result = json.loads(response.text)
                if result:
                    print(f"[COMPLIANCE] OK con gemini-2.5-flash (Llave #{self.current_key_index + 1})")
                    return result
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    self.rotate_key()
                    attempts += 1
                else:
                    print(f"[COMPLIANCE] Error con llave #{self.current_key_index + 1}: {e}")
                    self.rotate_key()
                    attempts += 1

        print("[COMPLIANCE] Activando Compliance Local (Ollama)...")
        response = self.call_ollama(prompt_instruction)
        result = self.extract_json(response)
        return result if result else {"safe": True, "fixed_post": post_content.get('postEN', '')}

    # AGENTE 4: VISUAL ARTIST
    def agent_visual(self, post_content):
        print("[VISUAL] Generando prompt ARTÍSTICO y PSICOLÓGICO con Gemini Pro...")

        prompt_instruction = f"""
        You are an elite AI Visual Psychologist and Cinematic Director. Your goal is to translate a scientific concept into a powerful visual metaphor that evokes deep emotion.

        Title: {post_content.get('title', '')}
        Topic: {post_content.get('topic', '')}

        CRITICAL ARTISTIC RULES:
        1. VISUAL METAPHORS: Do not be literal. If the topic is 'stress', don't just show a stressed person; show the feeling of stress (e.g., a storm of glass fragments, a tightening spiral of shadows).
        2. EMOTIONAL ATMOSPHERE: Define the psychological state (Tension, Wonder, Melancholy, Euphoria). Use lighting and color to communicate this (e.g., Chiaroscuro for mystery, volumetric neon for futurism).
        3. CINEMATIC SPECIFICATIONS: Use professional terms: 'Anamorphic lens', 'extremely shallow depth of field', 'volumetric fog', 'subsurface scattering', 'macro cinematic shot'.
        4. ABSOLUTELY NO TEXT: No letters, no words, no typography in the image.
        5. STYLE: Hyper-realistic, 8k, Unreal Engine 5.4 render, breathtaking composition.

        Return ONLY the final prompt string in English. No explanations.
        """

        attempts = 0
        models_to_try = ['gemini-1.5-pro', 'gemini-2.5-flash'] # Prioritize Pro for creativity

        while attempts < len(self.api_keys):
            for model_name in models_to_try:
                try:
                    client = genai.Client(api_key=self.get_active_key())
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt_instruction
                    )
                    result = response.text.strip()
                    if result:
                        clean_result = re.sub(r'^(Here is|This is|The following).*?prompt[:\\s]*', '', result, flags=re.IGNORECASE | re.DOTALL).strip()
                        clean_result = clean_result.replace('"', '').strip()
                        if clean_result.startswith(':'): clean_result = clean_result[1:].strip()
                        print(f"[VISUAL] OK con {model_name} (Llave #{self.current_key_index + 1})")
                        return clean_result
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        continue # Try next model
                    print(f"[VISUAL] Error con {model_name}: {e}")

            self.rotate_key()
            attempts += 1

        print("[VISUAL] Activando Visual Local (Ollama)...")
        response = self.call_ollama(prompt_instruction, format_json=False)
        return response if response else f"A high-end documentary photograph about {post_content.get('title', 'science discovery')}."
