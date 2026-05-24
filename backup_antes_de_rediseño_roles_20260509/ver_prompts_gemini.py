import json
import os
import sys

# Forzar UTF-8 en la consola de Windows para soportar emojis
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def ver_todo():
    print("="*60)
    print(" 🔍 INFOBYTE - VISUALIZADOR DE CONTENIDO Y PROMPTS ")
    print("="*60)

    # 1. VER NOTICIAS
    if os.path.exists('posts_content.json'):
        print("\n📰 [ NOTICIAS CIENTÍFICAS ]")
        with open('posts_content.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for post in data.get('posts', []):
                print(f"\nID: {post.get('id')} | Categoría: {post.get('category')}")
                print(f"Título: {post.get('title')}")
                print(f"Generado por: {post.get('generated_by_text')}")
                print(f"--- POST (EN) ---\n{post.get('postEN')}")
                print(f"--- POST (ES) ---\n{post.get('postES')}")
                print(f"--- IMAGE PROMPT ---\n{post.get('prompt')}")
                print("-" * 40)
    
    # 2. VER QUIZZES (RETO VIRAL)
    if os.path.exists('quizzes_content.json'):
        print("\n🧠 [ QUIZZES Y RETOS PSICOLÓGICOS ]")
        with open('quizzes_content.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, quiz in enumerate(data.get('quizzes', []), 1):
                print(f"\nID: {i} | Topic: {quiz.get('topic')}")
                print(f"Headline: {quiz.get('headline')}")
                print(f"--- POST (EN) ---\n{quiz.get('postEN')}")
                print(f"--- VISUAL PROMPT ---\n{quiz.get('visual_prompt')}")
                print("-" * 40)

    # 3. VER FRASES (MENSAJES DEL ALMA)
    if os.path.exists('frases_content.json'):
        print("\n✨ [ APUNTES DEL ALMA ]")
        with open('frases_content.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for frase in data.get('phrases', []):
                print(f"\nID: {frase.get('id')} | Generado por: {frase.get('generated_by_text')}")
                print(f"--- HOOK ---\n{frase.get('hook_text')}")
                print(f"--- POST (ES) ---\n{frase.get('postES')}")
                print(f"--- POST (EN) ---\n{frase.get('postEN')}")
                print(f"--- VISUAL PROMPT ---\n{frase.get('prompt')}")
                print("-" * 40)

if __name__ == "__main__":
    ver_todo()
