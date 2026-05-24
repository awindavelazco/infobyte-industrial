import json
import urllib.request
import urllib.parse
import time
import os
import random
import sys
from datetime import datetime

# Fix Windows UTF-8 console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SeedboyVideoEngine:
    def __init__(self):
        # POOL DE LLAVES (Leídas de api_keys.json)
        self.api_keys = []
        keys_path = os.path.join(BASE_DIR, "api_keys.json")
        if os.path.exists(keys_path):
            with open(keys_path, "r", encoding="utf-8") as f:
                self.api_keys = json.load(f).get("video_keys", [])

        if not self.api_keys:
            self.api_keys = ["LLAVE_DE_RESPALDO_AQUI"]
        self.current_key_index = 0
        self.url = "http://localhost:11434/api/generate"
        self.local_model = "llama3"

    def get_active_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"[SISTEMA] Rotando a la llave API #{self.current_key_index + 1}...")

    def call_ollama(self, prompt, format_json=True):
        data = {
            "model": self.local_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        if format_json: data["format"] = "json"

        try:
            req = urllib.request.Request(self.url, data=json.dumps(data).encode('utf-8'))
            req.add_header("Content-Type", "application/json")
            response = urllib.request.urlopen(req, timeout=300)
            result = json.loads(response.read().decode('utf-8'))
            return result['response']
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

    def generate_video_script(self, visual_style_choice):
        print(f"\n[DIRECTOR] Escribiendo guion optimizado para Flow AI...")

        styles_map = {
            "1": ("Animación 3D Pixar/Dreamworks", "3D Animation, cinematic, Pixar/Dreamworks style, vibrant colors, highly detailed characters, expressive faces"),
            "2": ("Cinemático Realista", "Photorealistic, 8k, cinematic lighting, highly detailed, realistic textures, shot on 35mm lens"),
            "3": ("Anime / Studio Ghibli", "Studio Ghibli style, hand-drawn anime, lush landscapes, soft lighting, nostalgic atmosphere"),
            "4": ("Sintético / Sci-Fi Neon", "Cyberpunk style, neon lighting, synthwave aesthetic, futuristic high-tech environment, sharp contrasts")
        }
        style_name, style_prompt = styles_map.get(visual_style_choice, styles_map["1"])
        print(f"[ESTILO] Aplicando: {style_name}")

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
        You are an expert Animation Director and AI Prompt Engineer for the 'Cartoon Hero x Seedboy AI Animation Contest'.
        Create a 32-second animation script optimized for Flow AI based on this problem: "{problema_elegido}".

        STRUCTURE (Flow AI):
        - Total duration: 32 seconds.
        - Format: 4 clips of 8 seconds each.
        - TECHNIQUE: CONTINUITY PROMPTING. Each clip must start exactly where the previous one ended.

        STORYLINE:
        1. Hook (0-8s): Neighbor complains, Seedboy arrives.
        2. Investigation (8-16s): Seedboy diagnoses, Seeds talk humorously.
        3. Solution (16-24s): Seedboy explains the real science solution.
        4. Finale (24-32s): Garden recovers and plants thrive.

        VISUAL RULES:
        - STYLE: {style_prompt}.
        - Language: Prompts and Voiceover MUST be in ENGLISH.
        - CONTINUITY: Clips 2, 3, and 4 MUST start with "Continuing from previous clip —" and maintain characters/lighting.
        - CAMERA: Include movements like 'slow cinematic zoom', 'macro pan', etc.
        - Plan explanation MUST be in SPANISH.

        JSON STRUCTURE:
        {{
           "topic_es": "Tema del video",
           "video_plan_es": "Explicación breve de la historia",
           "scene_1_prompt_en": "Starting scene... {style_prompt}. (Hook)",
           "scene_2_prompt_en": "Continuing from previous clip — {style_prompt}. (POV Seeds)",
           "scene_3_prompt_en": "Continuing from previous clip — {style_prompt}. (Solution)",
           "scene_4_prompt_en": "Continuing from previous clip — {style_prompt}. (Ending)",
           "voiceover_en": "Full script in English (max 80 words).",
           "post_text_en": "Engaging social media caption with emojis."
        }}
        """

        # JERARQUÍA DE MODELOS (Highest to Lowest)
        models_to_try = [
            'gemini-3.1-pro-preview',
            'gemini-3.0-pro-preview',
            'gemini-3.0-flash-preview',
            'gemini-2.0-flash'
        ]

        attempts = 0
        while attempts < len(self.api_keys):
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=self.get_active_key())

                for model_name in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            config=types.GenerateContentConfig(response_mime_type="application/json"),
                            contents=prompt_instruction
                        )
                        result = json.loads(response.text)
                        if result and result.get('scene_1_prompt_en'):
                            print(f"[DIRECTOR] OK con {model_name} (Llave #{self.current_key_index + 1})")
                            result["generated_by"] = f"Gemini ({model_name})"
                            return result
                    except Exception as inner_e:
                        if "429" in str(inner_e) or "RESOURCE_EXHAUSTED" in str(inner_e):
                            print(f"[SISTEMA] Modelo {model_name} agotado en esta llave...")
                            continue # Try next model in the list
                        print(f"[SISTEMA] Error con {model_name}: {inner_e}")

                print(f"[SISTEMA] Todas las modelos agotadas en Llave #{self.current_key_index + 1}. Rotando...")
                self.rotate_key()
                attempts += 1
            except Exception as e:
                print(f"[SISTEMA] Fallo general con llave #{self.current_key_index + 1}: {e}")
                self.rotate_key()
                attempts += 1

        print("[SISTEMA] Activando Pensamiento Local (Ollama) por saturación total de cuotas...")
        res = self.call_ollama(prompt_instruction)
        result = self.extract_json(res)
        if result: result["generated_by"] = "Ollama (Local)"
        return result

def main():
    print("\n==================================================")
    print("   🎬 SEEDBOY VIDEO ENGINE - FLOW AI EDITION 🎬")
    print("==================================================")

    print("\nSelecciona el ESTILO VISUAL para los videos:")
    print("1. Animación 3D Pixar/Dreamworks")
    print("2. Cinemático Realista (Photorealistic)")
    print("3. Anime / Studio Ghibli")
    print("4. Sintético / Sci-Fi Neon")

    choice = input("\nElige una opción (1-4): ").strip()
    if choice not in ["1", "2", "3", "4"]:
        print("[SISTEMA] Opción inválida. Usando estilo 3D por defecto.")
        choice = "1"

    engine = SeedboyVideoEngine()
    final_data = []

    count = 2 # Generamos 2 opciones
    for i in range(count):
        print(f"\nGenerando Video {i+1} de {count}...")
        v = engine.generate_video_script(choice)
        if not v:
            print("[ERROR] No se pudo generar el guion.")
            continue

        v['id'] = i + 1
        final_data.append(v)
        time.sleep(2)

    # SALIDA SINCRONIZADA CON DASHBOARD
    output_path = os.path.join(BASE_DIR, "videos_content.json")

    if len(final_data) > 0:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "format": "flow_ai_4x8s",
                "videos": final_data
            }, f, indent=2, ensure_ascii=False)
        print(f"\n[ÉXITO] Archivo {output_path} creado con {len(final_data)} guiones.")
        print(f"[TIPS] Copia los prompts en Flow AI respetando la continuidad.")
    else:
        print("\n[FALLO] No se generó data válida.")

if __name__ == "__main__":
    main()
