import json
import re

def clean_prompts():
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i in data:
        prompt = i.get('prompt', '')
        # Delete "Integrated bold typography..." and everything after it
        cleaned_prompt = re.sub(r'(?i)integrated\s+bold\s+typography.*', '', prompt).strip(' \n"\'.,')
        i['prompt'] = cleaned_prompt
        
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    clean_prompts()
