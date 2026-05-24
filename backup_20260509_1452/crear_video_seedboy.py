import json
import urllib.request
import urllib.parse
import time
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SeedboyVideoEngine:
    def __init__(self):
        # POOL DE LLAVES (Leídas de api_keys.json de forma segura)
        self.api_keys = []
        keys_path = os.path.join(BASE_DIR, "api_keys.json")
        if os.path.exists(keys_path):
            with open(keys_path, "r", encoding="utf-8") as f:
                self.api_keys = json.load(f).get("video_keys", [])
        
        if not self.api_keys:
            self.api_keys = ["LLAVE_DE_RESPALDO_AQUI"]
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

    def generate_video_script(self):
        print("[DIRECTOR] Escribiendo guion y prompts para el concurso de Seedboy...")
        
        # Seleccionamos un problema aleatorio para darle variedad a los guiones
        problemas = [
            "Demasiada agua (las semillas se ahogan, aparece moho).",
            "Tierra demasiado seca (las semillas tienen sed, se duermen).",
            "Plantadas demasiado profundas (no ven el sol, se rinden).",
            "Plantadas demasiado superficiales (expuestas al sol/pájaros).",
            "Tierra demasiado fría (se sienten en un congelador).",
            "Tierra demasiado caliente (se sienten en un horno).",
            "Demasiadas semillas amontonadas (pelean por espacio/comida)."
        ]
        problema_elegido = random.choice(problemas)
        
        prompt_instruction = f"""
        You are an expert Animation Director and AI Prompt Engineer participating in the 'Cartoon Hero x Seedboy AI Animation Contest'.
        Create a 30-second animation script and prompt sequence based on this specific problem: "{problema_elegido}".
        
        IMPORTANT CONTEST RULES & STRUCTURE:
        The video must be 30 seconds long (exactly 6 scenes of 5 seconds each for AI video generators like Luma/Kling).
        The story must follow these 5 steps:
        1. Enganche: A neighbor has a garden problem and complains. Seedboy arrives.
        2. Investigación: Seedboy uses real science to diagnose it.
        3. Punto de vista de las semillas: Seeds talk to each other playfully/humorously, revealing the issue.
        4. Diagnóstico y solución: Seedboy explains the real science solution simply.
        5. Desenlace: The garden recovers.
        
        TONE: Educational but simple. Seeds are playful teammates. Seedboy is a curious, kind teacher. Light humor.
        
        STRICT RULES:
        1. Prompts for AI video (Scenes 1 to 6) MUST be in ENGLISH, highly descriptive, cinematic, 3D animation style (like Pixar/Dreamworks). Mention camera movements.
        2. Voiceover MUST be in ENGLISH (Seedboy, neighbor, and seeds speaking) and fit within 30 seconds total.
        3. Explain the plan in SPANISH so the human creator understands the concept.
        
        STRUCTURE EXACTLY LIKE THIS JSON:
        {{ 
           "topic_es": "Tema del video (Ej: Semillas con demasiada agua)",
           "video_plan_es": "Explicación breve de la historia y el problema científico a resolver.",
           "scene_1_prompt_en": "3D Animation, cinematic... (Hook: Neighbor complains, Seedboy arrives)",
           "scene_2_prompt_en": "3D Animation, macro shot... (Investigation: Seedboy checks the soil)",
           "scene_3_prompt_en": "3D Animation, close up... (Seed POV: Seeds complaining about the problem humorously)",
           "scene_4_prompt_en": "3D Animation... (Diagnosis: Seedboy explains the issue)",
           "scene_5_prompt_en": "3D Animation... (Solution: Applying the fix)",
           "scene_6_prompt_en": "3D Animation, epic finale... (Ending: Plants growing and thriving)",
           "voiceover_en": "The exact script to be spoken (Neighbor, Seedboy, Seeds). Max 70 words total.",
           "post_text_en": "Engaging Facebook/Instagram post caption with emojis and hashtags."
        }}
        """
        
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=self.get_active_key())
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                    contents=prompt_instruction
                )
                
                result = json.loads(response.text)
                if result and result.get('scene_1_prompt_en'):
                    print(f"[DIRECTOR] OK con llave #{self.current_key_index + 1}")
                    result["generated_by"] = "Gemini (Cloud)"
                    return result
            except Exception as e:
                wait_time = 2 ** attempts
                print(f"[DIRECTOR] Advertencia: Fallo con llave #{self.current_key_index + 1}: {e}")
                print(f"[SISTEMA] Reintentando en {wait_time}s...")
                time.sleep(wait_time)
                self.rotate_key()
                attempts += 1

        print("[DIRECTOR] Activando Pensamiento Local (Ollama)...")
        res = self.call_ollama(prompt_instruction)
        result = self.extract_json(res)
        if result: result["generated_by"] = "Ollama (Local)"
        return result

def main():
    engine = SeedboyVideoEngine()
    final_data = []
    
    # Generaremos 2 videos para tener diferentes opciones para el concurso
    count = 2
    
    for i in range(count):
        print(f"\nGenerando Guion Seedboy {i+1} de {count}...")
        v = engine.generate_video_script()
        if not v: 
            print("[ERROR] No se pudo generar el guion.")
            continue
        
        v['id'] = i + 1
        final_data.append(v)
        time.sleep(2) # Pausa por Rate Limits
        
    output_path = os.path.join(BASE_DIR, "seedboy_content.json")
    
    if len(final_data) > 0:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "videos": final_data}, f, indent=2, ensure_ascii=False)
        print(f"\n[ÉXITO] Archivo {output_path} creado con {len(final_data)} guiones.")
    else:
        print("\n[FALLO] No se generó data válida. El archivo no se ha sobrescrito.")

if __name__ == "__main__":
    main()
