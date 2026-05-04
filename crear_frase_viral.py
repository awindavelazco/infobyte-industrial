import json
import urllib.request
import urllib.parse
import re
import random
import time
import os
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN GENERADOR DE FRASES "BITÁCORA DEL GENIO"
# =============================================================================

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

    def get_active_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"[SISTEMA] Rotando a la llave API #{self.current_key_index + 1}...")

    def call_ollama(self, prompt, format_json=True):
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        if format_json: data["format"] = "json"
        
        try:
            req = urllib.request.Request("http://localhost:11434/api/generate")
            req.add_header('Content-Type', 'application/json')
            response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))
            return json.loads(response.read().decode('utf-8'))['response']
        except Exception as e:
            print(f"[OLLAMA ERROR] {e}")
            return None

    def extract_json(self, text):
        if not text: return None
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
        return None

    def generate_phrase(self):
        print("[CEREBRO] Redactando frase viral con Gemini...")
        prompt_instruction = f"""
        You are an expert psychologist and persuasive copywriter. Write a deep, reflective post for 'Apuntes del Alma' (Soul Notes).
        
        STRICT RULES:
        1. VOICE: Empathetic, luxury, and deeply insightful (US English).
        2. VIRAL ELEMENTS: Use emotive emojis (✨, 🧘‍♂️, 💖) and at least 5 inspirational hashtags (e.g., #SoulWisdom, #Mindfulness, #InnerPeace).
        3. INTERACTION: Every post MUST end with a deep question that invites the reader to reflect and comment.
        
        STRUCTURE:
        {{ 
           "hook_quote": "English quote max 12 words", 
           "hook_instructions": ["Step 1", "Step 2", "Step 3"], 
           "hook_action": "ACT NOW",
           "post_title": "TITLE IN ENGLISH", 
           "post_reframe": "...", 
           "post_science": "Neuroscience behind this feeling...",
           "post_psychology": "Psychological depth...", 
           "post_action_plan": "1...\\n2...",
           "postEN": "Full viral post including Emojis, Hashtags, and the Interaction Question.",
           "postES": "Traducción COMPLETA Y EXACTA del postEN al español (todo el post, no un resumen)."
        }}
        """
        
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=self.get_active_key())
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                
                result = json.loads(response.text)
                if result and result.get('hook_quote'):
                    print(f"[CEREBRO] OK con llave #{self.current_key_index + 1}")
                    result["generated_by"] = "Gemini (Cloud)"
                    return result
            except Exception as e:
                wait_time = 2 ** attempts
                print(f"[CEREBRO] Advertencia: Fallo con llave #{self.current_key_index + 1}: {e}")
                print(f"[SISTEMA] Reintentando en {wait_time}s...")
                time.sleep(wait_time)
                self.rotate_key()
                attempts += 1

        print("[CEREBRO] Activando Pensamiento Local (Ollama)...")
        res = self.call_ollama(prompt_instruction)
        result = self.extract_json(res)
        if result: result["generated_by"] = "Ollama (Local)"
        return result

    def create_visual_prompt(self, phrase_data):
        print(f"[ARTE] Diseñando visual PREMIUM para el alma...")
        prompt_instruction = f"""Eres el Director de Arte de una revista de psicología de lujo.
Crea un prompt de imagen para: "{phrase_data.get('hook_quote', '')}"
INSTRUCCIONES ZEN:
1. Estilo 'Zen Minimalism', Fotografía macro o paisajes etéreos.
2. Iluminación Chiaroscuro o Golden Hour. Lente 35mm.
3. NO texto, NO marcas de agua.
4. El prompt debe ser en inglés (80 palabras) y terminar con: "no text, no letters, no watermark, clean image only."
Responde solo JSON: {{"image_prompt": "..."}}"""
        
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=self.get_active_key())
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                
                result = json.loads(response.text)
                if result and result.get('image_prompt'):
                    print(f"[ARTE] OK con llave #{self.current_key_index + 1}")
                    return {
                        "prompt": result.get('image_prompt'),
                        "generated_by": "Gemini (Cloud)"
                    }
            except Exception as e:
                wait_time = 2 ** attempts
                print(f"[ARTE] Advertencia: Fallo con llave #{self.current_key_index + 1}: {e}")
                print(f"[SISTEMA] Reintentando en {wait_time}s...")
                time.sleep(wait_time)
                self.rotate_key()
                attempts += 1

        print("[ARTE] Activando Artista Zen Local (Ollama)...")
        # Enviar contexto completo para que la imagen sea 100% coherente
        full_context = f"Title: {phrase_data.get('post_title')}\nReframe: {phrase_data.get('post_reframe')}\nScience: {phrase_data.get('post_science')}"
        
        fallback_prompt = f"""Create a minimalist Zen image prompt based on this context:
        ---
        {full_context}
        ---
        STYLE: Soft light, nature, 35mm, chiaroscuro, high-end photography. 
        No brands, no text. Respond ONLY with the prompt in English."""
        
        local_prompt = self.call_ollama(fallback_prompt, format_json=False)
        return {
            "prompt": local_prompt.strip() if local_prompt else "Minimalist Zen nature photography, soft light, 8k",
            "generated_by": "Ollama (Local)"
        }

    def download_image(self, prompt, filename):
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
    count = 28
    
    for i in range(count):
        p = engine.generate_phrase()
        if not p: continue
        
        visual_data = engine.create_visual_prompt(p)
        art_prompt = visual_data.get('prompt', '')
        
        # Ensamblar post (Priorizar el bloque completo de Gemini)
        post_completo_en = p.get('postEN')
        if not post_completo_en or len(str(post_completo_en)) < 20:
            post_completo_en = f"{p.get('post_title','')}\n\n{p.get('post_reframe','')}\n\n{p.get('post_science','')}\n\n{p.get('post_psychology','')}\n\n{p.get('post_benefits','')}\n\nAction Plan:\n{p.get('post_action_plan','')}"
        
        final_data.append({
            "id": i + 1,
            "generated_by_text": p.get('generated_by', 'Unknown'),
            "generated_by_visual": visual_data.get('generated_by', 'Unknown'),
            "hook_text": f"{p.get('hook_quote','')}\n" + "\n".join(p.get('hook_instructions',[])) + f"\n{p.get('hook_action','')}",
            "postES": p.get('postES', 'Resumen no disponible.'),
            "postEN": post_completo_en,
            "prompt": art_prompt,
            "image_path": ""
        })
        print(f"[OK] Frase {i+1} completada.")

    output_path = os.path.join(BASE_DIR, "frases_content.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "phrases": final_data}, f, indent=2, ensure_ascii=False)
    print(f"\n[ÉXITO] Archivo {output_path} actualizado.")

if __name__ == "__main__":
    main()
