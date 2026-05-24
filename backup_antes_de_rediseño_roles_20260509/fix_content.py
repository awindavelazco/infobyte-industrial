
import json
import os
import time
from engine_agentes import agent_spirit

def fix_and_generate():
    print("--- 1. Generando 7 Frases Spirit ---")
    spirit_posts = agent_spirit(7)
    with open('frases_content.json', 'w', encoding='utf-8') as f:
        json.dump({"phrases": spirit_posts}, f, ensure_ascii=False, indent=2)
    print("✅ Spirit generado.")

    print("--- 2. Variando ganchos de Noticias ---")
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    hooks_es = [
        "¡Cuidado! Lo que creías saber sobre {topic} acaba de cambiar.",
        "¿Sabías que {topic} oculta un secreto que la ciencia acaba de revelar?",
        "Imagina un mundo donde {topic} ya no es un misterio. ¡Está pasando!",
        "La frontera entre la realidad y la ficción se borra con este hallazgo sobre {topic}.",
        "¡Urgente! Científicos reportan un avance sin precedentes en {topic}.",
        "Tu cerebro no está preparado para lo que vas a leer sobre {topic}.",
        "Pocas veces la ciencia nos regala un descubrimiento tan visual como este sobre {topic}.",
        "Atención: Este dato sobre {topic} cambiará tu forma de ver el mundo."
    ]
    
    hooks_en = [
        "Warning! Everything you knew about {topic} just changed.",
        "Did you know {topic} hides a secret science just revealed?",
        "Imagine a world where {topic} is no longer a mystery. It's happening!",
        "The line between sci-fi and reality is blurring with this {topic} discovery.",
        "Urgent! Scientists report an unprecedented breakthrough in {topic}.",
        "Your brain isn't ready for what you're about to read regarding {topic}.",
        "Rarely does science give us such a visual discovery as this one about {topic}.",
        "Attention: This fact about {topic} will change how you see the world."
    ]

    for i, post in enumerate(data['posts']):
        # Si el post empieza con "¿Alguna vez" o "Ever wonder", lo cambiamos
        if post['postES'].startswith("¿Alguna vez") or post['postES'].startswith("🤯 ¿Alguna vez"):
            topic = post['category']
            new_hook_es = hooks_es[i % len(hooks_es)].format(topic=topic)
            new_hook_en = hooks_en[i % len(hooks_en)].format(topic=topic)
            
            # Reemplazamos la primera oración o el inicio repetitivo
            post['postES'] = post['postES'].replace("¿Alguna vez te has preguntado", new_hook_es).replace("🤯 ¿Alguna vez te has preguntado", "🤯 " + new_hook_es)
            post['postEN'] = post['postEN'].replace("Ever wondered", new_hook_en).replace("🤯 Ever wondered", "🤯 " + new_hook_en)

    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ Ganchos variados.")

if __name__ == "__main__":
    fix_and_generate()
