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
        You are an expert Video Director and AI Prompt Engineer for viral Facebook Reels (32 seconds).
        Create a compelling video concept about a fascinating Science, Health, or Psychology topic aimed at a US English-speaking audience.

        TOOL: Flow AI (generates 8-second video clips).
        TECHNIQUE: CONTINUITY PROMPTING — Each clip must begin exactly where the previous one ended.
        This creates a seamless, fluid 32-second Reel from 4 × 8-second clips.

        STRICT RULES FOR PROMPTS:
        1. ALL 4 clip prompts MUST be in ENGLISH. Highly descriptive, cinematic, 4K, photorealistic.
        2. CONTINUITY: Clips 2, 3, and 4 MUST start with "Continuing from previous clip —" and describe the same character, setting, and lighting to maintain visual consistency.
        3. CAMERA MOVEMENTS: Each clip must specify a camera movement (e.g., 'slow zoom in', 'pull back', 'pan left', 'close-up on face', 'drone rising shot').
        4. HOOK in Clip 1: The first 8 seconds must visually stop the scroll. Use an emotionally powerful or surprising scene.
        5. VOICEOVER: In ENGLISH, max 55 words total (fits 32 seconds). Write natural spoken dialogue, not a description.
        6. CURIOSITY GAP: The post_text_en must open with a shocking fact or question in the first 2 lines (visible before "See More").
        7. Explain the concept in SPANISH for the human creator.

        NARRATIVE STRUCTURE (32 seconds):
        - Clip 1 (0-8s): THE HOOK — Grab attention immediately. Show the problem or a shocking visual.
        - Clip 2 (8-16s): THE TENSION — Deepen the situation. Build curiosity or emotion.
        - Clip 3 (16-24s): THE REVELATION — Introduce the surprising insight or solution.
        - Clip 4 (24-32s): THE IMPACT — Emotional finale. Close-up, slow motion, powerful ending.

        STRUCTURE EXACTLY LIKE THIS JSON:
        {
           "topic_es": "Tema del video (Ej: Por qué tu cerebro sabotea tu sueño)",
           "video_plan_es": "Explicación breve de la historia, el personaje, el arco narrativo y el sentimiento que debe evocar.",
           "character_description_en": "Consistent character/scene description to maintain across all clips (e.g., 'A 35-year-old woman with dark hair, wearing a white shirt, in a warmly lit modern apartment').",
           "clip_1_hook_en": "THE HOOK (0-8s): [Camera movement]. [Describe the powerful opening scene. Same character/setting as character_description_en.]",
           "clip_2_tension_en": "THE TENSION (8-16s): Continuing from previous clip — [Camera movement]. [Describe the evolving scene, same character, building emotion.]",
           "clip_3_revelation_en": "THE REVELATION (16-24s): Continuing from previous clip — [Camera movement]. [Describe the insight or turning point moment.]",
           "clip_4_impact_en": "THE IMPACT (24-32s): Continuing from previous clip — [Camera movement]. [Describe the powerful emotional finale, slow motion preferred.]",
           "voiceover_en": "Full 32-second narration script (max 55 words). Natural, conversational, emotionally engaging.",
           "post_text_en": "First 2 lines: shocking fact or curiosity-gap question (visible before See More). Then full post with emojis, science reference, and ending with an open question inviting comments. Include 5 relevant hashtags."
        }
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
                if result and result.get('clip_1_hook_en'):
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

def print_video_summary(v, index):
    """Imprime un resumen legible de los 4 clips de continuidad en consola."""
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
    
    # Lote semanal: 5 videos (Lun, Mar, Mié, Vie, Sáb a las 8am EST)
    count = 5
    
    for i in range(count):
        print(f"\n[🎬] Generando Video {i+1} de {count} — Técnica: Continuidad 4×8s para Flow AI...")
        v = engine.generate_video_script()
        if not v: 
            print("[ERROR] No se pudo generar el video. Saltando...")
            continue
        
        v['id'] = i + 1
        final_data.append(v)
        print_video_summary(v, i + 1)
        time.sleep(3) # Pausa de seguridad por Rate Limits
        
    output_path = os.path.join(BASE_DIR, "videos_content.json")
    
    # PREVENCIÓN ERROR #001 DE BITÁCORA: Validar antes de escribir
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
        print(f"[📋 INSTRUCCIÓN] Abre 'videos_content.json', copia cada clip_1/2/3/4 y pégalos en Flow AI en orden.")
    else:
        print("\n[❌ FALLO] No se generó data válida. El archivo no se ha sobrescrito.")

if __name__ == "__main__":
    main()
