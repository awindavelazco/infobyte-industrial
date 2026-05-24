import json

with open('quizzes_content.json', encoding='utf-8') as f:
    d = json.load(f)

print(f"generated_at: {d.get('generated_at', 'SIN FECHA')}")
print(f"Total quizzes: {len(d.get('quizzes', []))}\n")
print("--- TITULOS ACTUALES ---")
for i, q in enumerate(d.get('quizzes', [])):
    print(f"{i+1:02d}. {q.get('headline', q.get('topic', 'SIN TITULO'))}")
