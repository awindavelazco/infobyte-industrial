import os
import json
from crear_tarjeta_viral import create_viral_card

# Configuración
JSON_FILE = 'quizzes_content.json'
ASSETS_DIR = r'c:\Users\Awinda\MisProyectos\facebook_post_assistant\assets\quizzes'
OUTPUT_DIR = r'c:\Users\Awinda\MisProyectos\facebook_post_assistant\fb_images_ready'

def process_all_quizzes():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        quizzes = data.get('quizzes', [])

    print(f"Iniciando generacion masiva de {len(quizzes)} tarjetas de Quiz...")

    for i, q in enumerate(quizzes):
        num = i + 1
        headline = q.get('headline', '')
        options = q.get('options', [])
        topic = q.get('topic', 'quiz')
        
        # El nombre del archivo que creamos antes
        import re
        def slugify(text):
            text = text.lower()
            text = re.sub(r'[^a-z0-9]+', '_', text)
            return text.strip('_')
        
        image_name = f"{num}_{slugify(topic)}.jpg"
        image_path = os.path.join(ASSETS_DIR, image_name)

        if os.path.exists(image_path):
            output_path = os.path.join(OUTPUT_DIR, f"TARJETA_QUIZ_{num}.jpg")
            print(f"--- Procesando Quiz #{num}...")
            
            try:
                create_viral_card(
                    image_path=image_path, 
                    text=headline, 
                    output_path=output_path, 
                    tipo='quizzes', 
                    options=options
                )
            except Exception as e:
                print(f"X Error en Quiz #{num}: {e}")
        else:
            print(f"X Imagen no encontrada para Quiz #{num}: {image_name}")

    print("\n✅ ¡Proceso masivo completado! Revisa la carpeta 'fb_images_ready'.")

if __name__ == "__main__":
    process_all_quizzes()
