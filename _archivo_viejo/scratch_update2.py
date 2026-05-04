import json
import os

print("Starting update script...")

# 1. Update posts_content.json
try:
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
except Exception as e:
    print(f"Error loading posts_content.json: {e}")
    posts = []

try:
    with open('new_11.json', 'r', encoding='utf-8') as f:
        new_posts = json.load(f)
except Exception as e:
    print(f"Error loading new_11.json: {e}")
    new_posts = []

posts.extend(new_posts)

try:
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print("posts_content.json updated successfully!")
except Exception as e:
    print(f"Error saving posts_content.json: {e}")

# 2. Update script.js
print("Updating script.js...")
try:
    with open('script.js', 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('];', 1)
    if len(parts) == 2:
        js_objects = []
        for item in new_posts:
            # We construct the JS object carefully
            cat = item['category'].replace('"', '\\"')
            tit = item['title'].replace('"', '\\"')
            pes = json.dumps(item['postES'], ensure_ascii=False)
            pen = json.dumps(item['postEN'], ensure_ascii=False)
            prm = item['prompt'].replace('"', '\\"')
            
            obj_str = f'''  {{
    category: "{cat}",
    title: "{tit}",
    postES: {pes},
    postEN: {pen},
    prompt: "{prm}"
  }}'''
            js_objects.append(obj_str)
        
        first_part = parts[0].rstrip()
        if not first_part.endswith(','):
            first_part += ','
        
        new_content = first_part + '\n' + ',\n'.join(js_objects) + '\n];' + parts[1]
        
        with open('script.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("script.js updated successfully!")
    else:
        print("Failed to find ]; in script.js")
except Exception as e:
    print(f"Error updating script.js: {e}")

print("Done!")
