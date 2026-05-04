import json
import os
import shutil
import glob

# 1. Update script.js exactly
try:
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

    with open('script.js', 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('const newsData = [', 1)
    if len(parts) == 2:
        tail_parts = parts[1].split('];', 1)
        if len(tail_parts) == 2:
            js_objects = []
            for item in posts:
                cat = item.get('category', '').replace('"', '\\"')
                tit = item.get('title', '').replace('"', '\\"')
                pes = json.dumps(item.get('postES', ''), ensure_ascii=False)
                pen = json.dumps(item.get('postEN', ''), ensure_ascii=False)
                prm = item.get('prompt', '').replace('"', '\\"')
                
                obj_str = f'''  {{
    category: "{cat}",
    title: "{tit}",
    postES: {pes},
    postEN: {pen},
    prompt: "{prm}"
  }}'''
                js_objects.append(obj_str)
            
            new_content = parts[0] + 'const newsData = [\n' + ',\n'.join(js_objects) + '\n];' + tail_parts[1]
            
            with open('script.js', 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('script.js completely synced with posts_content.json!')
except Exception as e:
    print("Error syncing:", e)

# 2. Move images 11 to 15
artifact_dir = r"c:\Users\Awinda\.gemini\antigravity\brain\e5836229-fea2-4ef5-91c5-16ee4b71dfaa"
dest_dir = r"c:\Users\Awinda\MisProyectos\facebook_post_assistant\fb_images"

for i in range(11, 16):
    pattern = os.path.join(artifact_dir, f"post_{i}_*.png")
    matches = glob.glob(pattern)
    if matches:
        src = matches[0]
        dst = os.path.join(dest_dir, f"post_{i}.png")
        shutil.copy2(src, dst)
        print(f"Moved {src} to {dst}")
    else:
        print(f"No image found for post {i}")
