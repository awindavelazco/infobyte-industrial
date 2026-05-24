import json, os, re
from crear_tarjeta_viral import create_viral_card

d = json.load(open('frases_content.json', encoding='utf-8'))

def deep_clean(text):
    # Solo permite letras (incluyendo acentos), numeros, espacios y puntuacion basica
    cleaned = re.sub(r"[^\w\s\.,;:\!\?'\"\-\(\)áéíóúÁÉÍÓÚñÑüÜ]", "", text)
    # Limpia multiples espacios
    return re.sub(r' +', ' ', cleaned).strip()

for p in d['phrases']:
    p['hook_text'] = deep_clean(p.get('hook_text', ''))

json.dump(d, open('frases_content.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

imgs = [
    '1_inner_sanctuary.jpeg', '2_rise_above.jpeg', '3_inner_harmony.jpeg', 
    '4_authentic_self.jpeg', '5_true_potential.jpeg', '6_nelson_mandela.jpeg', 
    '7_colors_of_soul.jpeg'
]

for i in range(7):
    texto = d['phrases'][i].get('hook_text', '')
    img_path = 'assets/spirit/' + imgs[i]
    if os.path.exists(img_path):
        create_viral_card(img_path, texto, 'fb_images_ready/SPIRIT_'+str(i+1)+'.jpg', tipo='frases')
        print(f'SPIRIT_{i+1} regenerada a la perfeccion.')
