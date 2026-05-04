import json
import os
import random
import urllib.request
import re
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN DEL CONSEJO EDITORIAL
# =============================================================================

class InfobyteEngine:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"
        self.historico_file = 'historico_noticias.txt'
        self.categories = [
            "Economy and Personal Finance", "Health and Natural Wellness",
            "Nutrition and Healthy Eating", "Proven Natural Remedies",
            "Money and How to Multiply It", "Consumer Technology",
            "Neuroscience", "Marine Biology", "Astrophysics", "Robotics and AI",
            "Genetics", "Paleontology", "Materials Engineering", "Meteorology",
            "Quantum Physics", "Entomology", "Geology", "Biotechnology",
            "Psychology and Human Behavior", "Environmental Science"
        ]

    def repair_json(self, text):
        if not text: return None
        text = text.strip()
        text = text.replace('\n', ' ').replace('\r', ' ')
        return text

    def call_ollama(self, prompt, format_json=True, retries=2):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        if format_json:
            data["format"] = "json"

        for attempt in range(1, retries + 1):
            try:
                req = urllib.request.Request(self.url, data=json.dumps(data).encode('utf-8'))
                req.add_header("Content-Type", "application/json")
                response = urllib.request.urlopen(req, timeout=300)
                result = json.loads(response.read().decode('utf-8'))
                return result['response']
            except Exception as e:
                print(f"[OLLAMA] Intento {attempt}/{retries} fallido: {e}")
        print("[OLLAMA] Todos los intentos fallaron. Devolviendo None.")
        return None

    def safe_parse(self, response, default=None):
        """Parse JSON safely — never crashes even if Ollama timed out."""
        if response is None:
            print("[PARSE] Respuesta vacía de Ollama.")
            return default if default is not None else {}
        try:
            parsed = json.loads(response)
            return parsed
        except Exception as e:
            print(f"[PARSE] Error al parsear JSON: {e}")
            return default if default is not None else {}

    # AGENTE 1: SCOUT (Selección de Tema Único)
    def agent_scout(self, category, historico_txt):
        print(f"[SCOUT] Searching unique topic in: {category}...")
        prompt = f"""
        Act as a Viral News Scout. Find a fascinating and uncommon topic in: {category}.
        
        TOPICS ALREADY PUBLISHED (DO NOT REPEAT):
        {historico_txt}
        
        Instructions:
        1. The topic must be real and scientific/technological.
        2. Do NOT repeat topics from the list. Find something FRESH.
        3. Return a JSON: {{ "title": "short title in English", "topic": "brief description in English" }}
        """
        response = self.call_ollama(prompt)
        result = self.safe_parse(response, {"title": "Unknown Topic", "topic": "N/A"})
        return result

    # AGENTE 2: COPYWRITER (Viral & Benefit-Driven Style)
    def agent_copywriter(self, scout_data, category):
        print(f"[COPYWRITER] Writing: {scout_data['title']}")
        prompt = f"""
        You are the Chief Copywriter of INFOBYTE. Style: Viral Science.
        
        TOPIC: {scout_data['title']} (Category: {category})
        
        Return EXACTLY this JSON:
        {{
            "image_text_hook": "Short mystery hook (max 10 words)",
            "title": "CATCHY ALL CAPS TITLE 🔥",
            "story": "1 paragraph using analogies",
            "benefit1": "Benefit about health/well-being",
            "benefit2": "Benefit about environment/city",
            "benefit3": "Benefit about future/global",
            "question": "Engaging question for comments",
            "authority": "🔍 Scientific Backing: [Institution]",
            "hashtags": "#Tag1 #Tag2 #Tag3"
        }}
        """
        response = self.call_ollama(prompt)
        res = self.safe_parse(response, {
            "image_text_hook": "Scientists discovered something that changes everything.",
            "title": scout_data.get('title', 'Breaking Discovery').upper(),
            "story": "This discovery changes our understanding of the world.",
            "benefit1": "Improves your health awareness.",
            "benefit2": "Protects your local environment.",
            "benefit3": "Ensures a sustainable future.",
            "question": "What do you think?",
            "authority": "🔍 Source: Science",
            "hashtags": "#Science #News"
        })
        
        # Ensamblar postEN en Python (Evita errores de JSON)
        post_en = f"{res.get('title','')}\n\n{res.get('story','')}\n\n"
        post_en += f"HOW DOES THIS AFFECT YOUR LIFE?\n"
        post_en += f"✅ {res.get('benefit1','')}\n"
        post_en += f"✅ {res.get('benefit2','')}\n"
        post_en += f"✅ {res.get('benefit3','')}\n\n"
        post_en += f"{res.get('question','')}\n\n"
        post_en += f"{res.get('authority','')}\n\n"
        post_en += f"{res.get('hashtags','')}"
        
        res['postEN'] = post_en
        return res

    # AGENTE 3: COMPLIANCE
    def agent_compliance(self, post_content):
        print("[COMPLIANCE] Auditing safety...")
        prompt = f"""
        You are a Facebook content auditor. Review this post: {post_content.get('postEN', '')}
        Return a JSON: {{"safe": true/false, "reason": "OK", "fixed_post": ""}}
        """
        response = self.call_ollama(prompt)
        return self.safe_parse(response, {"safe": True, "reason": "OK", "fixed_post": ""})

    # AGENTE 3B: TRANSLATOR (Español para lectura personal)
    def agent_translate(self, post_en_text):
        print("[TRADUCTOR] Generando versión en español...")
        prompt = f"""
        Translate the following Facebook post to natural, fluent Spanish. Keep emojis and hashtags.
        Return a JSON: {{"post_es": "full Spanish translation"}}
        
        Post: {post_en_text}
        """
        response = self.call_ollama(prompt)
        result = self.safe_parse(response, {"post_es": post_en_text})
        return result.get('post_es', post_en_text)

    # AGENTE 4: VISUAL ARTIST (National Geographic Style)
    def agent_visual(self, post_content):
        print("[VISUAL] Designing realistic documentary prompt...")
        prompt = f"""
        You are the Photography Director of INFOBYTE. Style: STRICT DOCUMENTARY REALISM.
        
        TOPIC: {post_content.get('postEN', '')[:100]}...
        
        RULES:
        - SUBJECT: Must be related to the news topic.
        - STYLE: National Geographic / Magnum Photos.
        - CAMERA: Mention Sony A7R IV or Canon EOS R5.
        - NO TEXT, NO FANTASY, NO GLOWING ORBS.
        - Composition: Bottom 30% clean for text.
        
        Example of STYLE (but adapt to the TOPIC): "A high-detail documentary shot of a scientist's weathered hands working in the field. Natural light, sharp textures, professional. Shot on Sony A7R IV."
        
        Return EXACTLY this JSON: {{"image_prompt": "Your detailed realistic prompt here", "video_prompt": "Slow cinematic pan"}}
        """
        response = self.call_ollama(prompt)
        return self.safe_parse(response, {
            "image_prompt": "Documentary photography, realistic, natural lighting, 8k, raw photo.",
            "video_prompt": "Slow cinematic zoom."
        })

def main():
    engine = InfobyteEngine()
    final_posts = []
    
    # Cargar histórico
    historico = []
    if os.path.exists(engine.historico_file):
        with open(engine.historico_file, 'r', encoding='utf-8') as f:
            historico = [line.strip() for line in f.readlines() if line.strip()]
            
    count = 2
    CATEGORIES = engine.categories
    
    for i in range(count):
        print(f"\n--- Processing Post {i+1}/{count} ---")
        
        # 1. SCOUT
        is_unique = False
        attempts = 0
        scout_data = {}
        current_cat = ""
        
        while not is_unique and attempts < 5:
            current_cat = random.choice(CATEGORIES)
            scout_data = engine.agent_scout(current_cat, "\n".join(historico))
            title = scout_data.get('title', 'Untitled')
            
            if title.lower().strip() not in [t.lower().strip() for t in historico]:
                is_unique = True
                historico.append(title)
            else:
                print(f"[SCOUT] Duplicate avoided: {title}. Retrying...")
                attempts += 1

        # 2. Copywriter
        copy = engine.agent_copywriter(scout_data, current_cat)
        
        # 3. Compliance
        audit = engine.agent_compliance(copy)
        if not audit.get('safe', True):
            copy['postEN'] = audit.get('fixed_post', copy.get('postEN', ''))
        
        # 4. Translation to Spanish (for personal reading only)
        post_en_full = copy.get('postEN', '')
        post_es = engine.agent_translate(post_en_full)
        # 5. Visual
        visual = engine.agent_visual(copy)
        
        final_posts.append({
            "id": i + 1,
            "category": current_cat,
            "title": scout_data.get('title', 'No Title'),
            "image_text_hook": copy.get('image_text_hook', ''),
            "postES": post_es,
            "postEN": copy.get('postEN', ''),
            "prompt": visual.get('image_prompt', 'Documentary photography, natural lighting, 8k, raw photo.'),
            "animationPrompt": visual.get('video_prompt', 'Slow cinematic zoom')
        })

    # Save
    data_to_save = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "posts": final_posts
    }
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    # Update history
    with open('historico_noticias.txt', 'a', encoding='utf-8') as f:
        for p in final_posts:
            f.write(f"{p['title']}\n")

    print(f"\n[SUCCESS] {count} fresh posts generated in posts_content.json")

if __name__ == "__main__":
    main()
