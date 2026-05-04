import json
import sys

# Forzar salida UTF-8 para evitar errores de consola en Windows
sys.stdout.reconfigure(encoding='utf-8')

def audit_file(filepath, key_list, type_label):
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get(key_list, [])
    print(f"\n=== AUDITORÍA {type_label.upper()} ({len(items)} items) ===")
    for i, item in enumerate(items):
        id_val = item.get('id', i+1)
        headline = item.get('headline', item.get('hook_text', 'SIN HOOK'))
        prompt = item.get('visual_prompt', 'SIN PROMPT')
        postEN = item.get('postEN', '')
        postES = item.get('postES', '')
        
        # Simplificar visualización de posts
        postEN_summary = (postEN[:100].replace('\n', ' ') + '...') if len(postEN) > 100 else postEN.replace('\n', ' ')
        postES_summary = (postES[:100].replace('\n', ' ') + '...') if len(postES) > 100 else postES.replace('\n', ' ')
        
        print(f"ID #{id_val:02d} | HOOK: {headline}")
        print(f"      | PROMPT: {prompt[:80]}...")
        print(f"      | TEXT EN: {postEN_summary}")
        print(f"      | TEXT ES: {postES_summary}")
        print("-" * 30)

audit_file('quizzes_content.json', 'quizzes', 'Quizzes')
audit_file('frases_content.json', 'phrases', 'Spirit')
