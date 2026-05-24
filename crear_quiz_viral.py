import os
import json
import requests
import time
from datetime import datetime

class QuizEngine:
    def __init__(self):
        # POOL DE LLAVES (Leídas de api_keys.json de forma segura)
        self.api_keys = []
        keys_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_keys.json")
        if os.path.exists(keys_path):
            with open(keys_path, "r", encoding="utf-8") as f:
                self.api_keys = json.load(f).get("news_keys", [])
        
        if not self.api_keys:
            self.api_keys = ["LLAVE_DE_RESPALDO_AQUI"]
        self.current_key_index = 0
        self.ollama_url = "http://localhost:11434/api/generate"
        self.output_file = "quizzes_content.json"

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"[SISTEMA] Rotando a la llave API #{self.current_key_index + 1}...")

    def generate_quiz(self, topic="Psychological Archetypes"):
        print(f"[QUIZ] Generando Reto Psicológico/Científico Viral (USA Style)...")
        
        # PROMPT DE SISTEMA: EL AGENTE DE ENGAGEMENT CIENTÍFICO (Versión Blindada)
        sys_prompt = f"""
        You are the 'Infobyte Viral Agent', a specialist in creating psychological and scientific challenges 
        for the US market. Your goal is to maximize comments and authority.

        STRICT RULES:
        1. CONTENT: Must be based on real science (neuroscience, biology, physics, psychology).
        2. STRUCTURE: Headline, impact hook, 4 numbered psychological options, and scientific explanations.
        3. VIRAL POST (postEN): Must include high-impact emojis, at least 5 strategic hashtags, and a MANDATORY provocative question at the end to force reader interaction (e.g., 'Which one are you? Drop your number below!').
        4. LANGUAGE: Native, sophisticated American English.
        5. CONSISTENCY: The 'visual_prompt' MUST be a perfect 1:1 logical representation of the Topic and Headline.
        6. SAFETY: Never use elements that might trigger social media flags. Use neutral, luxury elements.
        7. JSON FORMAT: Return ONLY a valid JSON object with the exact keys: topic, headline, hook_question, options (list), explanations (dict), postEN, postES, visual_prompt.
        8. TRANSLATION: The 'postES' field MUST BE a FULL and EXACT translation of 'postEN' to Spanish (do not summarize).

        TOPIC: {topic}
        """

        # --- INTENTO CON GEMINI (Primary) ---
        attempts = 0
        while attempts < len(self.api_keys):
            try:
                key = self.api_keys[self.current_key_index]
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
                
                payload = {
                    "contents": [{"parts": [{"text": sys_prompt}]}],
                    "generationConfig": {"response_mime_type": "application/json"}
                }
                
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                    return json.loads(raw_text)
                elif res.status_code == 429:
                    print(f"[QUIZ] Fallo con Gemini #{self.current_key_index+1}: 429 RESOURCE_EXHAUSTED.")
                    self.rotate_key()
                    attempts += 1
                else:
                    print(f"[QUIZ] Error API: {res.status_code}")
                    self.rotate_key()
                    attempts += 1
            except Exception as e:
                print(f"[QUIZ] Error conexión: {e}")
                self.rotate_key()
                attempts += 1

        # --- FALLBACK A OLLAMA ---
        print(f"[QUIZ] Activando Redactor Local (Ollama)...")
        try:
            payload = {
                "model": "llama3",
                "prompt": sys_prompt + "\nResponse in JSON format.",
                "stream": False,
                "format": "json"
            }
            res = requests.post(self.ollama_url, json=payload, timeout=60)
            if res.status_code == 200:
                raw_text = res.json()['response']
                result = json.loads(raw_text)
                
                # VALIDACIÓN: Si Ollama devolvió opciones numéricas, corregirlas
                if result and isinstance(result.get('options'), list):
                    explanations = result.get('explanations', {})
                    fixed_options = []
                    for i, opt in enumerate(result['options']):
                        if isinstance(opt, (int, float)):
                            # Usar la primera parte de la explicación como nombre
                            exp = explanations.get(str(i+1), f'Option {i+1}')
                            name = exp.split(':')[0].strip()[:30]
                            fixed_options.append(f"{i+1}. {name}")
                        else:
                            fixed_options.append(opt)
                    result['options'] = fixed_options
                
                # VALIDACIÓN: Si no hay visual_prompt, generar uno básico
                if result and not result.get('visual_prompt'):
                    topic = result.get('topic', 'science and psychology')
                    result['visual_prompt'] = f"High-end cinematic collage representing 4 aspects of {topic}. Luxury photography, 8k, sharp focus, no text, no watermark."
                
                print(f"[OK] Quiz generado con Ollama")
                return result
        except Exception as e:
            print(f"[ERROR] Fallo total del sistema: {e}")
            return None

    def save_quizzes(self, quizzes_data):
        if not quizzes_data: return
        
        all_data = {"quizzes": quizzes_data}
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        print(f"[SISTEMA] {len(quizzes_data)} Quizzes guardados en {self.output_file} (SOBREESCRITO)")

if __name__ == "__main__":
    engine = QuizEngine()
    topics = [
        "Fascinating Brain Facts and Personality",
        "The Psychology of Colors and Emotions",
        "Subconscious Mind and Decision Making",
        "Enclothed Cognition and Style",
        "Neuroscience of Healthy Eating",
        "Emotional Intelligence Archetypes",
        "Body Language Secrets"
    ]
    
    import random
    selected_topics = random.choices(topics, k=28)
    final_quizzes = []
    
    for i, t in enumerate(selected_topics):
        print(f"\n--- Generando Quiz {i+1}/28 ---")
        quiz = engine.generate_quiz(t)
        if quiz:
            quiz['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            quiz['generated_by'] = "Gemini"
            final_quizzes.append(quiz)
        time.sleep(3) # Pausa de seguridad API
            
    engine.save_quizzes(final_quizzes)
