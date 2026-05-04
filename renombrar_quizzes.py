import json
import os
import shutil

# Configuración de rutas
JSON_FILE = 'quizzes_content.json'
SOURCE_DIR = r'C:\Users\Awinda\Downloads'
DEST_DIR = r'c:\Users\Awinda\MisProyectos\facebook_post_assistant\assets\quizzes'

def slugify(text):
    """Convierte un texto en un nombre de archivo seguro."""
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def rename_quizzes():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"Directorio creado: {DEST_DIR}")

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        quizzes = data.get('quizzes', [])

    print(f"Iniciando renombrado de {len(quizzes)} imágenes...")

    for i, q in enumerate(quizzes):
        num = i + 1
        source_name = f"{num}.jpeg"
        source_path = os.path.join(SOURCE_DIR, source_name)
        
        # Si no existe .jpeg, probar con .jpg
        if not os.path.exists(source_path):
            source_path = os.path.join(SOURCE_DIR, f"{num}.jpg")

        if os.path.exists(source_path):
            topic = q.get('topic', f'quiz_{num}')
            new_name = f"{num}_{slugify(topic)}.jpg"
            dest_path = os.path.join(DEST_DIR, new_name)
            
            shutil.copy2(source_path, dest_path)
            print(f"Copiado: {source_name} -> {new_name}")
        else:
            print(f"Advertencia: No se encontró la imagen {source_name} en Descargas.")

if __name__ == "__main__":
    rename_quizzes()
