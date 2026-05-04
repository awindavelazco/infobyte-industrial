import json

with open('posts_content.json', encoding='utf-8') as f:
    data = json.load(f)

print("=== AUDITORÍA PROFUNDA DE COHERENCIA (NOTICIAS 1-21) ===")
for p in data.get('posts', []):
    id_num = p.get('id', '??')
    title = p.get('title', 'SIN TÍTULO')
    hook = p.get('headline', p.get('image_text_hook', 'SIN HOOK'))
    print(f"#{id_num:02d} | TÍTULO: {title}")
    print(f"    | HOOK  : {hook}")
    print("-" * 50)
