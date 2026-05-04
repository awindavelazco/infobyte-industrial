import json
import time

with open('quizzes_content.json', encoding='utf-8') as f:
    data = json.load(f)

quizzes = data.get('quizzes', [])

# Detectar y eliminar duplicados por headline
seen = set()
unicos = []
for q in quizzes:
    key = q.get('headline', '').strip().lower()
    if key not in seen:
        seen.add(key)
        unicos.append(q)
    else:
        print(f"DUPLICADO ELIMINADO: {q.get('headline','')}")

# Renumerar
for i, q in enumerate(unicos):
    q['id'] = i + 1

print(f"\nTotal final: {len(unicos)} quizzes únicos")
for q in unicos:
    print(f"  {q['id']:02d}. {q.get('headline','')}")

data['quizzes'] = unicos
data['generated_at'] = time.strftime("%Y-%m-%d %H:%M:%S")

with open('quizzes_content.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nOK: Duplicados eliminados. Sin usar API.")
