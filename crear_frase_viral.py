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
        # POOL DE LLAVES (Leídas de api_keys.json de forma segura)
        self.api_keys = []
        keys_path = os.path.join(BASE_DIR, "api_keys.json")
        if os.path.exists(keys_path):
            with open(keys_path, "r", encoding="utf-8") as f:
                self.api_keys = json.load(f).get("news_keys", [])

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

    def generate_phrase(self):
        print("[CEREBRO] Redactando frase viral con Gemini...")
        prompt_instruction = f"""
        You are an expert neuroscientist, psychologist, and viral copywriter creating content for 'Infobyte' on Facebook (US English audience, ages 30-55).

        GOAL: Create a post that STOPS THE SCROLL and drives comments and shares.

        STRICT RULES:
        1. CURIOSITY GAP (CRITICAL): The first 2 lines of 'postEN' (visible before 'See More') MUST be a shocking fact or polarizing question that creates irresistible curiosity. Example: "Your brain is literally deleting memories right now. And you don't even know it's happening."
        2. SCIENCE AUTHORITY: Reference a real scientific institution (Harvard, NIH, Stanford, Mayo Clinic) or a recognized study to build trust.
        3. RELATABLE PAIN POINT: Address a common daily struggle (fatigue, stress, memory, relationships, sleep, diet, loneliness). Make the reader feel 'this is about ME'.
        4. VOICE: Conversational US English. Not academic. Like a brilliant friend explaining science.
        5. INTERACTION: The post MUST end with a binary or personal question that forces a response. Example: 'Do you feel this too? Tell me YES or NO below.' or 'Tag someone who NEEDS to read this.'
        6. VIRAL ELEMENTS: 3-5 relevant emojis and 5 power hashtags (#BrainHealth, #MindsetShift, #ScienceFacts, #MentalHealth, #Psychology).

        TOPICS POOL (choose one per post): Brain science, Sleep & memory, Stress & cortisol, Gut-brain connection, Loneliness & psychology, Hidden symptoms of burnout, Emotional intelligence, The science of habits.

        STRUCTURE EXACTLY LIKE THIS JSON:
        {{
           "hook_quote": "The shocking first sentence / curiosity gap (max 15 words)",
           "post_title": "TITLE IN ENGLISH (for internal reference)",
           "post_science": "The science/study backing this post (1-2 sentences).",
           "post_psychology": "The psychological or human angle that makes this relatable.",
           "post_action_plan": "3 short, actionable takeaways the reader can apply TODAY.",
           "postEN": "FULL viral post: Line 1-2 = Curiosity Gap. Then science. Then relatable story. Then action plan. Then interaction question. Emojis and hashtags at the end.",
           "postES": "Traduccion COMPLETA Y EXACTA del postEN al espanol."
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
                print(f"[CEREBRO] Fallo con llave #{self.current_key_index + 1}: {e}")
                self.rotate_key()
                attempts += 1

        print("[CEREBRO] Activando Pensamiento Local (Ollama)...")
        res = self.call_ollama(prompt_instruction)
        result = self.extract_json(res)
        if result: result["generated_by"] = "Ollama (Local)"
        return result

    def create_visual_prompt(self, phrase_data):
        print(f"[ARTE] Disenando visual PREMIUM para Facebook...")
        topic = phrase_data.get('post_title', '')
        hook = phrase_data.get('hook_quote', '')
        prompt_instruction = f"""You are a top-tier Art Director for a viral US science & psychology Facebook page.

        Create an image prompt for this post topic: "{hook} — {topic}"

        CRITICAL IMAGE RULES (based on what stops the scroll on Facebook USA):
        1. STYLE: Photorealistic, cinematic photography (NOT illustration, NOT abstract art, NOT fractals, NOT nebulas).
        2. SUBJECT: Show a REAL PERSON (or 2 people) in a recognizable, emotionally relatable everyday situation. Examples: a tired person staring at their phone at 3am, a woman smiling alone with coffee, a man holding his head at a desk, a couple sitting apart looking down at their phones.
        3. EMOTION: The image must convey one powerful emotion that connects to the post (fatigue, hope, loneliness, breakthrough, peace, stress).
        4. LIGHTING: Cinematic. Golden hour, dramatic window light, or soft morning light. NO flat lighting.
        5. CAMERA: Specify angle. Close-up on face OR medium shotL OR over-the-shoulder. 35mm or 85mm lens.
        6. NO text, NO logos, NO watermarks, NO abstract elements. Clean, real, emotional photography only.
        7. The prompt MUST be in English, ~70 words, and end with: "photorealistic, cinematic, 4K, no text, no watermark."

        Respond ONLY with this JSON: {{"image_prompt": "..."}}"""

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
                print(f"[ARTE] Fallo con llave #{self.current_key_index + 1}: {e}")
                self.rotate_key()
                attempts += 1

        print("[ARTE] Activando Artista Zen Local (Ollama)...")
        full_context = f"Title: {phrase_data.get('post_title')}\nReframe: {phrase_data.get('post_reframe')}\nScience: {phrase_data.get('post_science')}"
        fallback_prompt = f"""Create a minimalist Zen image prompt based on this la context:
        ---
        {full_context}
        ---
        STYLE: Soft la light, nature, 35mm, chiaroscuro, high-end photography.
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
    count = 7
    for i in range(count):
        p = engine.generate_phrase()
        if not p: continue
         la = [
            "Sugerencia la de la IA",
            "Sugerencia de la IA",
            "Sugerencia la de la IA",
            "Sugerencia de la IA",
            "Suger la la la la",
            "Suger la l la l la l l la la la la",
            "Suger la l la l l la l l l la l la la l la la la la"
        ]
        # Para evitar que el dashboard se llene de basura,
        # solo agregamos el post si Gemini generó algo coherente.
        # (Ollama a veces genera basura en la fase de frases)
        if p.get('generated_by') == "Ollama (Local)" and (not p.get('postEN') or len(p.get('postEN')) < 50):
            print(f"[SKIP] Saltando post {i+1} por calidad insuficiente de Ollama.")
            continue

        visual_data = engine.create_visual_prompt(p)
        art_prompt = visual_data.get('prompt', '')
        post_completo_en = p.get('postEN')
        if not post_completo_en or len(str(post_completo_en)) < 20:
            post_completo_en = f"{p.get('post_title','')}\n\n{p.get('post_reframe','')}\n\n{p.get('post_science','')}\n\n{p.get('post_psychology','')}\n\nSugerencias:\n{p.get('post_action_plan','')}"

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
