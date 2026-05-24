import json
import urllib.request
import re
import random
import time
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN GENERADOR DE FRASES "BITÁCORA DEL GENIO"
# =============================================================================

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GeniusJournalEngine:
    def __init__(self):
        # POOL DE LLAVES
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

    def get_active_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"[SISTEMA] Rotando a la llave API #{self.current_key_index + 1}...")

    def call_ollama(self, prompt, format_json=True):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.8}
        }
        if format_json:
            data["format"] = "json"
            
        req = urllib.request.Request(self.url, data=json.dumps(data).encode('utf-8'))
        req.add_header("Content-Type", "application/json")
        try:
            response = urllib.request.urlopen(req, timeout=300)
            result = json.loads(response.read().decode('utf-8'))
            return result['response']
        except Exception as e:
            print(f"Error en Ollama: {e}")
            return None

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

    def generate_phrase(self):
        prompt = f"""
        You are an expert psychologist and persuasive copywriter for Facebook. Write a deep, reflective post for the category 'Notes from the Soul' (Apuntes del Alma).
        Generate 1 post that connects universally with life, resilience, and emotions.
        
        CRITICAL RULES - STRICT ADHERENCE REQUIRED:
        1. ALL FIELDS MUST BE IN ENGLISH, EXCEPT 'postES' WHICH MUST BE IN SPANISH.
        2. DO NOT USE SPANISH in the quotes, hooks, titles, or body paragraphs.
        
        STRUCTURE FOR THE POST:
        
        1. IMAGE VISUAL HOOK (ENGLISH ONLY):
           - "hook_quote": A powerful golden rule or bold statement. Max 12 words. (IN ENGLISH)
           - "hook_instructions": 3 short micro-instructions starting with "Don't...". (IN ENGLISH)
           - "hook_action": Final call to action (1-2 words MAX, highlighted). (IN ENGLISH)
        
        2. POST COPY (ENGLISH ONLY):
           - "post_title": ALL CAPS, central theme + emotional benefit + 2 emojis. (IN ENGLISH)
           - "post_reframe": Reframe (destroy a popular belief, explain why it is vital). (IN ENGLISH)
           - "post_science": Biology/Neuroscience (cortisol, nervous system, etc.). (IN ENGLISH)
           - "post_psychology": Psychology (clinical term for this behavior). (IN ENGLISH)
           - "post_benefits": Benefits of changing this pattern. (IN ENGLISH)
           - "post_action_plan": Action plan with 2-3 numbered practical steps. (IN ENGLISH)
           - "postES": Resumen en ESPAÑOL de qué trata este post (para que el editor lo entienda). (IN SPANISH)
        
        Return EXACTLY a JSON with this format:
        {{ 
           "hook_quote": "English quote max 12 words", 
           "hook_instructions": ["Don't overthink", "Don't settle", "Don't rush"], 
           "hook_action": "ACT NOW",
           "post_title": "TITLE IN ENGLISH", 
           "post_reframe": "paragraph 1 in English...", 
           "post_science": "paragraph 2 in English...",
           "post_psychology": "paragraph 3 in English...", 
           "post_benefits": "paragraph 4 in English...", 
           "post_action_plan": "1. ...\\n2. ...",
           "postES": "Resumen en español para el editor..."
        }}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result if result else None

    def create_visual_prompt(self, phrase_data):
        print(f"[ARTE] Diseñando visual PREMIUM para el alma...")
        
        # Usamos Gemini con Rotación
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                
                client = genai.Client(api_key=self.get_active_key())
                
                prompt_instruction = f"""Eres el Director de Arte de una revista de psicología de lujo.
Crea un prompt de imagen para: "{phrase_data.get('hook_quote', '')}"

REGLAS 'ALMA':
1. Estilo 'Zen Minimalism': Fotografía macro, paisajes etéreos.
2. Iluminación Chiaroscuro o Golden Hour.
3. Transmitir paz y profundidad.
4. NO texto ni marcas de agua.
5. Prompt en inglés (60-80 palabras) terminando en: "no text, no letters, no watermark, no overlay, clean image only."

Responde solo JSON: {{"image_prompt": "..."}}"""

                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                
                result = json.loads(response.text)
                if result and result.get('image_prompt'):
                    print(f"[ARTE] OK con llave #{self.current_key_index + 1}")
                    return result.get('image_prompt')

            except Exception as e:
                print(f"[ARTE] Advertencia: Fallo con llave #{self.current_key_index + 1}: {e}")
                self.rotate_key()
                attempts += 1
                time.sleep(1)

        return 'Minimalist Zen nature photography, soft light, 8k'

    def download_image(self, prompt, filename):
        print(f"[IMAGE] Descargando arte para el alma...")
        try:
            img_folder = os.path.join(BASE_DIR, "fb_images")
            if not os.path.exists(img_folder): os.makedirs(img_folder)
            filepath = os.path.join(img_folder, filename)
            seed = random.randint(1, 999999)
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&seed={seed}&model=flux&nologo=true"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(filepath, 'wb') as f: f.write(response.read())
            return os.path.join("fb_images", filename)
        except Exception as e:
            print(f"Error al descargar imagen: {e}")
            return None

def main():
    engine = GeniusJournalEngine()
    
    final_data = []
    count = 1
    print(f"\n--- Iniciando Generación de {count} Frases Maestras ---")
    
    for i in range(count):
        print(f"\n[CEREBRO] Generando Frase {i+1}/{count}...")
        p = engine.generate_phrase()
        if not p:
            print(f"[ERROR] No se pudo generar la frase {i+1}. Saltando...")
            continue
            
        # 2. Generar Arte para cada frase
        art_prompt = engine.create_visual_prompt(p)
        # img_name = f"alma_{i+1}_{datetime.now().strftime('%H%M%S')}.jpg"
        # img_path = engine.download_image(art_prompt, img_name)
        img_path = ""
        
        # Ensamblar post completo en inglés
        post_completo_en = f"{p.get('post_title','')}\n\n{p.get('post_reframe','')}\n\n{p.get('post_science','')}\n\n{p.get('post_psychology','')}\n\n{p.get('post_benefits','')}\n\nAction Plan:\n{p.get('post_action_plan','')}"
        
        final_data.append({
            "id": i + 1,
            "hook_text": f"{p.get('hook_quote','')}\n" + "\n".join(p.get('hook_instructions',[])) + f"\n{p.get('hook_action','')}",
            "postES": p.get('postES', 'Resumen no disponible.'),
            "postEN": post_completo_en,
            "prompt": art_prompt,
            "image_path": img_path if img_path else ""
        })
        print(f"[OK] Frase {i+1} completada.")
    
    # 3. Guardar con Timestamp
    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phrases": final_data
    }
    
    json_path = os.path.join(BASE_DIR, 'frases_content.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    print(f"\n[ÉXITO] {len(final_data)} Frases Maestras generadas en frases_content.json")

if __name__ == "__main__":
    main()
