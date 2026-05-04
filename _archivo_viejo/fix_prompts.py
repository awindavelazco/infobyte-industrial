import json
import urllib.request

def fix_prompts():
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, item in enumerate(data):
        prompt = item.get('prompt', '')
        if len(prompt) < 25:
            print(f"Fixing prompt {item['id']}...")
            req_prompt = f"Write a short photorealistic image generation prompt in English (1 sentence) for a news article titled: '{item['title']}'. ONLY output the prompt, nothing else. No intro."
            
            payload = {
                "model": "llama3",
                "prompt": req_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
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
        
    print("Prompts fixed.")

if __name__ == '__main__':
    fix_prompts()
