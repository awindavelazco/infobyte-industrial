import json
import urllib.request

def regenerate_prompts():
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, item in enumerate(data):
        print(f"Regenerando prompt para noticia {item['id']}...")
        req_prompt = f"""Escribe UNA SOLA ORACIÓN en INGLÉS que describa una fotografía periodística altamente realista para ilustrar la siguiente noticia: '{item['title']}'.
REGLAS:
1. DEBE ser una escena del mundo actual, cotidiana y real.
2. PROHIBIDO usar las palabras "futuristic", "sci-fi", "cyberpunk", "hologram" o "glowing".
3. NO incluyas texto ni letras.
Solo devuelve el prompt en inglés, nada más."""
        
        payload = {
            "model": "llama3",
            "prompt": req_prompt,
            "stream": False,
            "options": {
                "temperature": 0.5,
                "num_predict": 100
            }
        }
        
        try:
            req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(payload).encode('utf-8'))
            req.add_header("Content-Type", "application/json")
            response = urllib.request.urlopen(req, timeout=30)
            result = json.loads(response.read().decode('utf-8'))
            new_prompt = result['response'].strip(' \n"\'')
            print(f"  New prompt: {new_prompt}")
            item['prompt'] = new_prompt
        except Exception as e:
            print(f"  Error: {e}")
                
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Prompts regenerados.")

if __name__ == '__main__':
    regenerate_prompts()
