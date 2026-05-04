import json
import urllib.request
import re
import random
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN GENERADOR DE FRASES "BITÁCORA DEL GENIO"
# =============================================================================

class GeniusJournalEngine:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3"

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

    def generate_phrases(self, count=10):
        print(f"[CEREBRO] Generando {count} frases maestras...")
        prompt = f"""
        You are an expert psychologist and persuasive copywriter for Facebook. Write deep, reflective posts for the category 'Notes from the Soul' (Apuntes del Alma).
        Generate {count} posts that connect universally with life, resilience, and emotions.
        
        CRITICAL RULES - STRICT ADHERENCE REQUIRED:
        1. ALL FIELDS MUST BE IN ENGLISH, EXCEPT 'postES' WHICH MUST BE IN SPANISH.
        2. DO NOT USE SPANISH in the quotes, hooks, titles, or body paragraphs.
        
        STRUCTURE FOR EACH POST:
        
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
        {{ "phrases": [
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
        ] }}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result.get('phrases', []) if result else []

    def create_visual_prompt(self, phrase_data):
        print(f"[ARTE] Diseñando visual para: {phrase_data.get('hook_quote', '')[:30]}...")
        prompt = f"""
        Crea un prompt de imagen minimalista para la categoría 'Apuntes del Alma'.
        ESTILO: 'White Background / Minimalist Quote'.
        
        REGLA DE ORO: El diseño debe parecer una nota clínica, un poema o un tweet elegante. Fondo blanco o blanco hueso puro.
        
        ELEMENTOS OBLIGATORIOS:
        - Debe estar escrito el texto: "{phrase_data.get('hook_quote', '')}" y luego las reglas "{', '.join(phrase_data.get('hook_instructions', []))}".
        - Estilo visual limpio, tipografía negra elegante sobre fondo claro, sin distracciones, diseño estéril y profesional.
        
        Devuelve un JSON: {{ "image_prompt": "prompt detallado en inglés para generar esta imagen minimalista con texto" }}
        """
        response = self.call_ollama(prompt)
        result = self.extract_json(response)
        return result.get('image_prompt', '') if result else 'Minimalist white background quote card'

def main():
    engine = GeniusJournalEngine()
    
    # 1. Generar Frases
    phrases = engine.generate_phrases(10)
    
    final_data = []
    for p in phrases:
        # 2. Generar Arte para cada frase
        art_prompt = engine.create_visual_prompt(p)
        
        # Ensamblar post completo en inglés
        post_completo_en = f"{p.get('post_title','')}\n\n{p.get('post_reframe','')}\n\n{p.get('post_science','')}\n\n{p.get('post_psychology','')}\n\n{p.get('post_benefits','')}\n\nAction Plan:\n{p.get('post_action_plan','')}"
        
        final_data.append({
            "hook_text": f"{p.get('hook_quote','')}\n" + "\n".join(p.get('hook_instructions',[])) + f"\n{p.get('hook_action','')}",
            "postES": p.get('postES', 'Resumen no disponible.'),
            "postEN": post_completo_en,
            "prompt": art_prompt
        })
    
    # 3. Guardar con Timestamp
    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phrases": final_data
    }
    
    with open('frases_content.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    print("\n[ÉXITO] 10 Frases Maestras generadas en frases_content.json")

if __name__ == "__main__":
    main()
