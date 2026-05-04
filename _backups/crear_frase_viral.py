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

    def generate_phrases(self, count=10):
        print(f"[CEREBRO] Generando {count} frases maestras...")
        prompt = f"""
        Actúa como un sabio emocional y pensador motivacional contemporáneo.
        Genera {count} frases cortas, potentes, reflexivas y profundamente humanas.
        Las frases deben conectar universalmente con la experiencia de la vida, la resiliencia, el crecimiento personal, las emociones y los retos diarios. Evita términos técnicos o científicos, usa palabras que toquen el alma y generen empatía inmediata.
        
        EJEMPLOS DE TONO ("Apuntes del Alma"):
        - "A veces, el mayor acto de valentía es simplemente perdonarte y volver a intentarlo."
        - "No midas tu progreso con el reloj de otra persona."
        - "Hay silencios que curan más que mil palabras de consuelo."
        - "La vida no te rompe, te reorganiza para que descubras de qué estás hecho."
        
        Devuelve un JSON con este formato:
        {{ "phrases": [
            {{ "text": "frase en español", "author": "Nombre o 'Infobyte'" }}
        ] }}
        """
        response = self.call_ollama(prompt)
        return json.loads(response).get('phrases', [])

    def create_visual_prompt(self, phrase_data):
        print(f"[ARTE] Diseñando visual para: {phrase_data['text'][:30]}...")
        prompt = f"""
        Crea un prompt de imagen viral de ALTA GAMA para Google Flow o Stable Diffusion.
        ESTILO: 'Dark Academia / Vintage Luxury' (Apuntes del Alma).
        
        REGLA DE ORO: DEBES VARIAR EL ESCENARIO en cada prompt. Elige UNO de estos entornos al azar:
        - Una máquina de escribir antigua con un papel texturizado.
        - Un diario de cuero abierto junto a una taza de café humeante o té.
        - Una carta antigua sellada con cera sobre un escritorio de madera oscura.
        - Unas gafas de lectura elegantes sobre un libro clásico.
        
        ELEMENTOS OBLIGATORIOS:
        - La frase '{phrase_data['text']}' debe estar escrita en el objeto principal (papel, carta, etc.) con una caligrafía elegante.
        - Iluminación cinematográfica, luz cálida (volumetric warm light), soft bokeh, resolución 8k, hiperrealista.
        
        Devuelve un JSON: {{ "image_prompt": "prompt detallado en inglés" }}
        """
        response = self.call_ollama(prompt)
        return json.loads(response).get('image_prompt', '')

def main():
    engine = GeniusJournalEngine()
    
    # 1. Generar Frases
    phrases = engine.generate_phrases(10)
    
    final_data = []
    for p in phrases:
        # 2. Generar Arte para cada frase
        art_prompt = engine.create_visual_prompt(p)
        final_data.append({
            "text": p['text'],
            "author": p['author'],
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
