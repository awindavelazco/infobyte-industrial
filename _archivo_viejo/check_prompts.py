import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('posts_content.json', encoding='utf-8'))
for i in d:
    title = i.get('title', '')[:50]
    prompt = i.get('prompt', '')
    print(f"ID:{i['id']} | PROMPT:{len(prompt)} chars | {title}")
