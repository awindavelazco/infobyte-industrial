import json
import urllib.request
import urllib.parse
import time
import os
import sys
import auditor_videos
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

    def generate_video_script(self, forced_topic=None):
        print(f"[DIRECTOR] Escribiendo guion DINÁMICO para Facebook Reels (Estándar Cero Aburrimiento)...")

        topic_context = f" focus on the topic: {forced_topic}" if forced_topic else " Create a science/health/psychology concept for US audience"

        guidelines = ""
        guidelines_path = os.path.join(BASE_DIR, "CINEMATIC_AI_VIDEO_GUIDELINES.md")
        if os.path.exists(guidelines_path):
            with open(guidelines_path, "r", encoding="utf-8") as f:
                guidelines = f"\n\n--- MANDATORY CINEMATIC GUIDELINES (APPLY THESE TO ALL CLIPS) ---\n" + f.read()

        prompt_instruction = f"""
        You are a world-class Cinematic Director and AI Prompt Engineer, certified in the 'Cartoon Hero' high-retention methodology for Facebook Reels (30s).
        Your goal is to create a dynamic visual montage that translates a scientific/psychological concept into a powerful human transformation journey.{topic_context}.

        STRATEGY: DYNAMIC CHARACTER JUMP.
        The character is the constant, but the environment, clothing, and mood MUST evolve in every clip.

        SEQUENCE OF 5 CLIPS (6 seconds each):
        1. CLIP 1 (HOOK: 0-6s) -> MACRO/CLOSE-UP. High-impact detail/emotion. Cold/Cluttered environment. Casual clothes.
        2. CLIP 2 (TENSION: 6-12s) -> MEDIUM SHOT. Struggle with problem. New environment. New outfit.
        3. CLIP 3 (REVELATION: 12-18s) -> INSERT SHOT. 'Aha!' moment. Clearer space. Hopeful light. Third outfit.
        4. CLIP 4 (EXPANSION: 18-24s) -> WIDE SHOT. Applying solution. Open space. Vibrant/Golden light. Confident outfit.
        5. CLIP 5 (IMPACT: 24-30s) -> EPIC SLOW-MOTION CLOSE-UP. Final resolution. Breathtaking serene setting. Golden Hour. Elegant outfit.

        MANDATORY PROMPT FORMAT:
        You MUST follow the 'Anatomía del Prompt' strictly as defined in the CINEMATIC GUIDELINES below.
        - You MUST generate a 'global_context_block_en' containing FORMAT, SUBJECT, WARDROBE, ENVIRONMENT, MOOD, MUSIC, COLOR LOGIC, RULES, and NEGATIVE PROMPT.
        - For each clip, you MUST use the Timeline Prompting syntax: "SHOT [X] — [START]-[END]s — [SHOT SIZE], [LENS mm], [CAMERA MOVEMENT]. [Description]"
        - Example clip: "SHOT 1 — 0:00-0:06 — MCU, 50mm, locked. A determined woman's hand gripping..."

        CRIITICAL CONSTRAINTS:
        - BE CONCISE: Each clip prompt MUST be under 300 characters. Use powerful nouns/verbs.
        - NO CONTINUITY STRINGS: Do NOT use 'Continuing from previous clip'.
        - CHARACTER CONSISTENCY: Repeat the exact core physical traits in every clip, but change clothing and location.
        - NO ABSTRACTS: Use real-world cinematic environments.
        - LIGHTING EVOLUTION: Cold/Dark (C1) -> Natural/Mixed (C2-3) -> Golden/Bright (C4-5).

        VO & CAPTION:
        - VO: Divide the script into 5 segments (one per clip). Each segment must be exactly 6 seconds of speech (approx 12-15 words). Total max 60 words. Poetic, punchy, mysterious.
        - CAPTION: First 2 lines = irresistible 'Curiosity Gap'. 5 strategic hashtags.
        {guidelines}

        JSON STRUCTURE:
        {{
           "topic_es": "Tema",
           "video_plan_es": "Plan de montaje dinámico: Hook(Macro) -> Tension(Medium) -> Revelation(Insert) -> Expansion(Wide) -> Impact(Slow-mo)",
           "global_context_block_en": "FORMAT: 30s / 5 SHOTS / [Topic]\nSUBJECT: [Base physical description]\nWARDROBE: ...\nENVIRONMENT: ...\nMOOD: ...\nMUSIC: ...\nCOLOR LOGIC: ...\nRULES: ...\nNEGATIVE PROMPT: ...",
           "clip_1_hook_en": "SHOT 1 — 0:00-0:06 — [SIZE], [LENS], [MOTION]. [Description]",
           "clip_2_tension_en": "SHOT 2 — 0:06-0:12 — [SIZE], [LENS], [MOTION]. [Description]",
           "clip_3_revelation_en": "SHOT 3 — 0:12-0:18 — [SIZE], [LENS], [MOTION]. [Description]",
           "clip_4_expansion_en": "SHOT 4 — 0:18-0:24 — [SIZE], [LENS], [MOTION]. [Description]",
           "clip_5_impact_en": "SHOT 5 — 0:24-0:30 — [SIZE], [LENS], [MOTION]. [Description]",
           "voiceover_segments": {{
              "clip_1": "VO text for 0-6s",
              "clip_2": "VO text for 6-12s",
              "clip_3": "VO text for 12-18s",
              "clip_4": "VO text for 18-24s",
              "clip_5": "VO text for 24-30s"
           }},
           "post_text_en": "Curiosity gap + content + hashtags"
        }}
        """

        attempts = 0
        models_to_try = ['gemini-1.5-pro', 'gemini-2.5-flash']

        while attempts < len(self.api_keys):
            for model_name in models_to_try:
                try:
                    from google import genai
                    from google.genai import types
                    client = genai.Client(api_key=self.get_active_key())

                    response = client.models.generate_content(
                        model=model_name,
                        config=types.GenerateContentConfig(response_mime_type="application/json"),
                        contents=prompt_instruction
                    )

                    result = json.loads(response.text)
                    if result and result.get('clip_1_hook_en'):
                        print(f"[DIRECTOR] OK con {model_name} (Llave #{self.current_key_index + 1})")
                        result["generated_by"] = f"Gemini ({model_name})"
                        return result
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        continue
                    print(f"[DIRECTOR] Error con {model_name}: {e}")

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
        print(f"\n🎬 CLIP 1 — HOOK (0-6s):")
        print(f"   {v.get('clip_1_hook_en', '')}")
        print(f"\n🎬 CLIP 2 — TENSION (6-12s):")
        print(f"   {v.get('clip_2_tension_en', '')}")
        print(f"\n🎬 CLIP 3 — REVELATION (12-18s):")
        print(f"   {v.get('clip_3_revelation_en', '')}")
        print(f"\n🎬 CLIP 4 — EXPANSION (18-24s):")
        print(f"   {v.get('clip_4_expansion_en', '')}")
        print(f"\n🎬 CLIP 5 — IMPACT (24-30s):")
        print(f"   {v.get('clip_5_impact_en', '')}")

        vo_segments = v.get('voiceover_segments', {})
        print(f"\n🎙️  VOICEOVER SEGMENTED:")
        print(f"   0-6s:   {vo_segments.get('clip_1', '')}")
        print(f"   6-12s:  {vo_segments.get('clip_2', '')}")
        print(f"   12-18s: {vo_segments.get('clip_3', '')}")
        print(f"   18-24s: {vo_segments.get('clip_4', '')}")
        print(f"   24-30s: {vo_segments.get('clip_5', '')}")

        print(f"\n📱 POST CAPTION:")
        print(f"   {v.get('post_text_en', '')}")
        print(f"\n⚙️  Generado por: {v.get('generated_by', 'Unknown')}")



def main():
    engine = VideoEngine()
    final_data = []
    count = 1 # Generamos solo el video solicitado
    topic = "La Regla de los 90 Segundos (una emocion solo dura 90 segundos en tu cuerpo, despues tu decides si la alimentas)"

    for i in range(count):
        print(f"\n[🎬] Generando Video {i+1} de {count} — Tema: {topic} — Técnica: Continuidad 4×8s...")
        v = engine.generate_video_script(forced_topic=topic)
        if not v:
            print("[ERROR] No se pudo generar el video. Saltando...")
            continue

        v['id'] = i + 1
        final_data.append(v)
        engine.print_video_summary(v, i + 1)
        time.sleep(3)

    output_path = os.path.join(BASE_DIR, "videos_content_v2.json")
    if len(final_data) > 0:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "format": "5x6s_dynamic_montage",
                "total_duration_seconds": 30,
                "clips_per_video": 5,
                "videos": final_data
            }, f, indent=2, ensure_ascii=False)
        print(f"\n[✅ ÉXITO] Archivo '{output_path}' creado con {len(final_data)} guiones de video.")
        print("\n[🔍 QA] Iniciando Auditoría Automática de Calidad...")
        auditor_videos.main()
    else:
        print("\n[❌ FALLO] No se generó data válida. El archivo no se ha sobrescrito.")


if __name__ == "__main__":
    main()
