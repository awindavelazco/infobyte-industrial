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
            "Economía y Finanzas Personales", "Moda y Tendencias Actuales",
            "Salud Natural y Bienestar", "Alimentación Sana y Nutrición",
            "Remedios Naturales Comprobados", "Noticias Sociales y Virales",
            "Dinero y Cómo Multiplicarlo", "Teoría del Color y Psicología Visual",
            "Tendencias en Decoración del Hogar", "Materiales e Innovación en la Moda",
            "Tecnología Aplicada al Consumidor", "Política General y Tendencias Globales",
            "Neurociencia", "Biología Marina", "Astrofísica", "Robótica e IA",
            "Genética", "Paleontología", "Ingeniería de Materiales", "Meteorología",
            "Física Cuántica", "Entomología", "Geología", "Biotecnología"
        ]

    def repair_json(self, text):
        if not text: return None
        text = text.strip()
        text = text.replace('\n', ' ').replace('\r', ' ')
        return text

    def call_ollama(self, prompt, format_json=True):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
        if format_json:
            data["format"] = "json"
            
        req = urllib.request.Request(self.url, data=json.dumps(data).encode('utf-8'))
        req.add_header("Content-Type", "application/json")
        try:
            response = urllib.request.urlopen(req, timeout=300)
            result = json.loads(response.read().decode('utf-8'))
            raw_response = result['response']
            return raw_response
        except Exception as e:
            print(f"Error en Ollama: {e}")
            return None

    # AGENTE 1: SCOUT (Selección de Tema Único)
    def agent_scout(self, category, historico_txt):
        print(f"[SCOUT] Buscando tema único en: {category}...")
        prompt = f"""
        Actúa como un Scout de Noticias Virales. Tu objetivo es encontrar un tema fascinante y poco común en: {category}.
        
        TEMAS YA PUBLICADOS (PROHIBIDO REPETIR):
        {historico_txt}
        
        Instrucciones:
        1. El tema debe ser real y científico/tecnológico.
        2. NO repitas temas de la lista. Busca algo FRESCO.
        3. Devuelve un JSON: {{ "title": "título corto en inglés", "topic": "breve descripción" }}
        """
        response = self.call_ollama(prompt)
        return json.loads(response)

    # AGENTE 2: COPYWRITER
    def agent_copywriter(self, scout_data, category):
        print(f"[COPYWRITER] Redactando: {scout_data['title']}")
        prompt = f"""
        Eres el Redactor Jefe de INFOBYTE. Escribe un post viral para Facebook sobre: {scout_data['title']} (Categoría: {category}).
        - 2 a 3 párrafos en inglés periodístico, atrapante.
        - Incluye la institución real del descubrimiento.
        - Incluye Fact Check y una pregunta final para los comentarios.
        - Añade 5-8 hashtags.
        
        ADEMÁS, diseña una ENCUESTA DE FACEBOOK (Poll) divertida o polémica relacionada con la noticia.
        - Una pregunta directa.
        - 2 a 4 opciones cortas (con emojis).
        
        Devuelve un JSON exacto con esta estructura: 
        {{
            "postEN": "texto completo con hashtags", 
            "postES": "traducción o resumen en español",
            "pollQuestion": "¿Pregunta de la encuesta?",
            "pollOptions": ["A) Opción 1", "B) Opción 2", "C) Opción 3"]
        }}
        """
        response = self.call_ollama(prompt)
        return json.loads(response)

    # AGENTE 3: COMPLIANCE
    def agent_compliance(self, post_content):
        print("[COMPLIANCE] Auditando seguridad...")
        prompt = f"""
        Eres el Auditor de Facebook. Revisa este post: {post_content['postEN']}
        Devuelve un JSON: {{"safe": true/false, "reason": "explicación", "fixed_post": "versión corregida"}}
        """
        response = self.call_ollama(prompt)
        return json.loads(response)

    # AGENTE 4: VISUAL ARTIST (Luxury Detail)
    def agent_visual(self, post_content):
        print("[VISUAL] Diseñando prompt de ALTO NIVEL...")
        prompt = f"""
        Eres el Director de Fotografía Senior de INFOBYTE. Tu misión es redactar un prompt de imagen viral de ALTA GAMA para ser usado en Google Flow.
        
        REGLA DE ORO: El prompt debe ser LARGO y EXTREMADAMENTE DETALLADO (Mínimo 60 palabras). No acepto frases cortas.
        
        DEBES incluir siempre estos 4 bloques de detalle:
        1. SUJETO Y ACCIÓN: Descripción detallada de lo que ocurre.
        2. ENTORNO Y TEXTURAS: Materiales (mármol de Carrara, vidrio, seda, metales), partículas en el aire, superficies.
        3. ILUMINACIÓN Y CÁMARA: Tipo de lente (Macro 100mm, Wide 35mm), iluminación (volumetric lighting, soft bokeh, cinematic teal and orange).
        4. ESTILO GEMINI: Elige entre (Laboratorio Moderno, Minimalista de Lujo, o Naturaleza Conceptual).
        
        EJEMPLO DE CALIDAD ESPERADA:
        "Extreme macro photography of a single glowing amber drop of herbal oil falling into a crystal clear pool of water, intricate ripples forming on the surface, soft volumetric lighting hitting the liquid, high-end laboratory background with blurred teal glass equipment, shot on 100mm macro lens, 8k resolution, hyper-realistic textures of the water and oil, cinematic atmosphere, no text."
        
        Noticia para la cual diseñarás el prompt: {post_content['postEN']}
        
        Devuelve un JSON exacto: {{"image_prompt": "EL PROMPT LARGO Y DETALLADO AQUÍ", "video_prompt": "descripción de movimiento"}}
        """
        response = self.call_ollama(prompt)
        return json.loads(response)

def main():
    engine = InfobyteEngine()
    final_posts = []
    
    # Cargar histórico
    historico = []
    if os.path.exists(engine.historico_file):
        with open(engine.historico_file, 'r', encoding='utf-8') as f:
            historico = [line.strip() for line in f.readlines() if line.strip()]
            
    count = 10
    CATEGORIES = engine.categories
    
    for i in range(count):
        print(f"\n--- Procesando Noticia {i+1}/{count} ---")
        
        # 1. SCOUT con Filtro Policial
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
                print(f"[SCOUT] Repetición evitada: {title}. Reintentando...")
                attempts += 1

        # 2. Redacción
        copy = engine.agent_copywriter(scout_data, current_cat)
        
        # 3. Seguridad
        audit = engine.agent_compliance(copy)
        if not audit.get('safe', True):
            copy['postEN'] = audit.get('fixed_post', copy['postEN'])
        
        # 4. Visual
        visual = engine.agent_visual(copy)
        
        # Ensamblar
        final_posts.append({
            "id": i + 1,
            "category": current_cat,
            "title": scout_data.get('title', 'Sin Título'),
            "postEN": copy.get('postEN', 'Error'),
            "postES": copy.get('postES', 'Traducción error'),
            "prompt": visual.get('image_prompt', 'Luxury photo, 8k'),
            "animationPrompt": visual.get('video_prompt', 'Slow cinematic zoom')
        })

    # Guardar
    if not os.path.exists('data'): os.mkdir('data')
    data_to_save = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "posts": final_posts
    }
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)
    
    # Actualizar histórico txt
    with open('historico_noticias.txt', 'a', encoding='utf-8') as f:
        for p in final_posts:
            f.write(f"{p['title']}\n")

    print(f"\n[ÉXITO] 10 Noticias FRESCAS generadas. {len(historico)} títulos en histórico.")

if __name__ == "__main__":
    main()
