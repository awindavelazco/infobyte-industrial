import json
import os

def cleanup():
    if not os.path.exists('posts_content.json'):
        return
        
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Filtrar: quedarnos con las 23 originales y la 30 (que era la buena)
    # IDs 24-29 eran pruebas fallidas
    data = [p for p in data if p['id'] <= 23 or p['id'] == 30]
    
    # Re-asignar IDs secuenciales
    for i, p in enumerate(data):
        p['id'] = i + 1
        
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Limpieza completada. Ahora hay {len(data)} noticias de alta calidad.")

if __name__ == "__main__":
    cleanup()
