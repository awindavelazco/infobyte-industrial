import json
import urllib.request
import urllib.parse
import time
import os
import sys
from datetime import datetime

# Fix Windows UTF-8 console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class VideoEngine:
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
        print("[DIRECTOR] Escribiendo guion y prompts de continuidad para Flow AI...")
        prompt_instruction = """
        Expert AI Prompt Engineer for viral Facebook Reels (32s). Create a science/health/psychology concept for US audience.

        TECHNIQUE: CONTINUITY PROMPTING for Flow AI. Each 8s clip MUST start where the previous ended.

        RULES:
        1. 4 prompts in ENGLISH: Cinematic, photorealistic, 4K.
        2. CONTINUITY: Clips 2, 3, 4 MUST start with 'Continuing from previous clip —' and maintain same character, setting, and lighting.
        3. CAMERA: Specify movement (e.g., 'slow zoom in', 'drone shot') for each clip.
        4. HOOK: Clip 1 must be visually shocking.
        5. VO: English, max 55 words total.
        6. CAPTION: First 2 lines = curiosity gap. 5 hashtags.

        JSON STRUCTURE:
        {
           "topic_es": "Tema",
           "video_plan_es": "Breve plan narrativo",
           "character_description_en": "Detailed consistent look",
           "clip_1_hook_en": "THE HOOK (0-8s): [Camera]. [Scene]",
           "clip_2_tension_en": "TENSION (8-16s): Continuing from previous clip — [Camera]. [Scene]",
           "clip_3_revelation_en": "REVELATION (16-24s): Continuing from previous clip — [Camera]. [Scene]",
           "clip_4_impact_en": "IMPACT (24-32s): Continuing from previous clip — [Camera]. [Scene]",
           "voiceover_en": "Max 55 words script",
           "post_text_en": "Curiosity gap + content + hashtags"
        }
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
                if result and result.get('clip_1_hook_en'):
                    print(f"[DIRECTOR] OK con llave #{self.current_key_index + 1}")
                    result["generated_by"] = "Gemini (Cloud)"
                    return result
            except Exception as e:
                print(f"[DIRECTOR] Fallo con llave #{self.current_key_index + 1}: {e}")
                self.rotate_key()
                attempts += 1

        print("[DIRECTOR] Activando Pensamiento Local (Ollama)...")
        res = self.call_ollama(prompt_instruction)
        result = self.extract_json(res)
        if result: result["generated_by"] = "Ollama (Local)"
        return result

    def print_video_summary(self, v, index):
        print(f"\n{'='*60}")
        print(f"  VIDEO #{index} — {v.get('topic_es', 'Sin título')}")
        print(f"{'='*60}")
        print(f"\n📋 PLAN: {v.get('video_plan_es', '')}")
        print(f"\n🎭 PERSONAJE BASE: {v.get('character_description_en', '')}")
        print(f"\n🎬 CLIP 1 — HOOK (0-8s):")
        print(f"   {v.get('clip_1_hook_en', '')}")
        print(f"\n🎬 CLIP 2 — TENSION (8-16s):")
        print(f"   {v.get('clip_2_tension_en', '')}")
        print(f"\n🎬 CLIP 3 — REVELATION (16-24s):")
        print(f"   {v.get('clip_3_revelation_en', '')}")
        print(f"\n🎬 CLIP 4 — IMPACT (24-32s):")
        print(f"   {v.get('clip_4_impact_en', '')}")
        print(f"\n🎙️  VOICEOVER:")
        print(f"   {v.get('voiceover_en', '')}")
        print(f"\n📱 POST CAPTION:")
        print(f"   {v.get('post_text_en', '')}")
        print(f"\n⚙️  Generado por: {v.get('generated_by', 'Unknown')}")

def main():
    engine = VideoEngine()
    final_data = []
    count = 5

    for i in range(count):
        print(f"\n[🎬] Generando Video {i+1} de {count} — Técnica: Continuidad 4×8s para Flow AI...")
        v = engine.generate_video_script()
        if not v:
            print("[ERROR] No se pudo generar el video. Saltando...")
            continue

        v['id'] = i + 1
        final_data.append(v)
        engine.print_video_summary(v, i + 1)
        time.sleep(3)

    output_path = os.path.join(BASE_DIR, "videos_content.json")
    if len(final_data) > 0:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "format": "4x8s_continuity_flow",
                "total_duration_seconds": 32,
                "clips_per_video": 4,
                "videos": final_data
            }, f, indent=2, ensure_ascii=False)
        print(f"\n[✅ ÉXITO] Archivo '{output_path}' creado con {len(final_data)} guiones de video.")
    else:
        print("\n[❌ FALLO] No se generó data válida. El archivo no se ha sobrescrito.")

if __name__ == "__main__":
    main()
