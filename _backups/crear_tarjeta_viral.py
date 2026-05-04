import os
import glob
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont

def get_latest_image(download_folder):
    list_of_files = glob.glob(os.path.join(download_folder, '*.[jp][pn]*')) 
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def cargar_textos(tipo='noticias'):
    if tipo == 'frases':
        path = 'frases_content.json'
        key = 'phrases'
        text_field = 'text'
    else:
        path = 'posts_content.json'
        key = 'posts'
        text_field = 'title'
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data.get(key, [])
            return {i+1: item.get(text_field, '') for i, item in enumerate(items)}
    except Exception as e:
        print(f"❌ Error al cargar {path}: {e}")
        return {}

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0,0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def create_viral_card(image_path, text, output_path, es_frase=False):
    base = Image.open(image_path).convert("RGBA")
    
    target_width = 1080
    target_height = 1350
    if base.size != (target_width, target_height):
        base_ratio = base.width / base.height
        target_ratio = target_width / target_height
        if base_ratio > target_ratio:
            new_height = target_height
            new_width = int(new_height * base_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / base_ratio)
        base = base.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (base.width - target_width) / 2
        top = (base.height - target_height) / 2
        right = (base.width + target_width) / 2
        bottom = (base.height + target_height) / 2
        base = base.crop((left, top, right, bottom))
    
    draw = ImageDraw.Draw(base)

    overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    shadow_height = int(target_height * 0.45)
    for y in range(shadow_height):
        alpha = int(255 * (y / shadow_height) ** 1.5)
        overlay_draw.line([(0, target_height - shadow_height + y), (target_width, target_height - shadow_height + y)], fill=(0, 0, 0, alpha))
        
    top_shadow_height = 200
    for y in range(top_shadow_height):
        alpha = int(180 * (1 - (y / top_shadow_height)))
        overlay_draw.line([(0, y), (target_width, y)], fill=(0, 0, 0, alpha))

    base = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(base)

    try:
        font_logo = ImageFont.truetype("arialbd.ttf", 35)
        if es_frase:
            # Estilo Poético/Manuscrito para Frases
            try: font_main = ImageFont.truetype("georgiai.ttf", 55) # Georgia Italic
            except: font_main = ImageFont.truetype("timesi.ttf", 55) # Times Italic backup
        else:
            # Estilo Noticia Viral
            font_main = ImageFont.truetype("arialbd.ttf", 65)
    except:
        print("Advertencia: No se encontraron fuentes TTF. Usando default.")
        font_main = ImageFont.load_default()
        font_logo = ImageFont.load_default()

    if es_frase:
        marca = "APUNTES DEL ALMA"
        color_marca = (245, 245, 220, 220)  # Beige
        color_linea = (245, 245, 220, 150)
    else:
        marca = "INFOBYTE SCIENCE"
        color_marca = (0, 255, 255, 220)    # Cian Neón
        color_linea = (0, 255, 255, 150)

    bbox_marca = draw.textbbox((0,0), marca, font=font_logo)
    w_marca = bbox_marca[2] - bbox_marca[0]
    draw.text(((target_width - w_marca)/2, 60), marca, font=font_logo, fill=color_marca)
    draw.line([((target_width - w_marca)/2 - 50, 110), ((target_width + w_marca)/2 + 50, 110)], fill=color_linea, width=3)

    if es_frase:
        # Para frases, fuente pequeña y elegante que no compita con la imagen
        try: font_main = ImageFont.truetype("georgiai.ttf", 38)
        except: 
            try: font_main = ImageFont.truetype("timesi.ttf", 38)
            except: pass
        wrapped = wrap_text(f'"{text}"', font_main, target_width - 150, draw)
    else:
        # Para noticias, siempre UPPERCASE y grande
        if len(text) > 80: 
            try: font_main = ImageFont.truetype("arialbd.ttf", 55)
            except: pass
        wrapped = wrap_text(text.upper(), font_main, target_width - 120, draw)
    
    total_text_height = sum([draw.textbbox((0,0), line, font=font_main)[3] - draw.textbbox((0,0), line, font=font_main)[1] for line in wrapped]) + (len(wrapped)-1)*20
    
    # Empujar el texto mucho más abajo (Margen de 50px en lugar de 120px)
    margen_inferior = 50 if es_frase else 120
    y_text = target_height - total_text_height - margen_inferior

    for line in wrapped:
        bbox = draw.textbbox((0,0), line, font=font_main)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x_text = (target_width - w) / 2
        
        shadow_offset = 3 if es_frase else 4
        # Sombra negra dura
        draw.text((x_text + shadow_offset, y_text + shadow_offset), line, font=font_main, fill=(0, 0, 0, 255))
        # Color del texto (Blanco para noticias, crema/dorado tenue para frases)
        color_texto = (255, 250, 240, 255) if es_frase else (255, 255, 255, 255)
        draw.text((x_text, y_text), line, font=font_main, fill=color_texto)
        
        y_text += h + 20

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    base.convert("RGB").save(output_path, quality=95)
    print(f"✅ Tarjeta guardada en: {output_path}")

def main():
    print("="*60)
    print(" 🚀 INFOBYTE — GENERADOR DE TARJETAS VIRALES ")
    print("="*60)

    while True:
        user_dir = os.path.expanduser('~')
        downloads_dir = os.path.join(user_dir, 'Downloads')
        
        print(f"\n🔍 Buscando la imagen más reciente en: {downloads_dir}")
        latest_img = get_latest_image(downloads_dir)
        
        if not latest_img:
            print("❌ No se encontraron imágenes en la carpeta de descargas.")
            break
            
        print(f"   Encontrada: {os.path.basename(latest_img)}")
        confirm = input("¿Usar esta imagen? (Enter para confirmar / N para cancelar): ")
        if confirm.lower() == 'n':
            print("Operación cancelada.")
            break

        print("\n📚 ¿Qué tipo de contenido vas a publicar?")
        print("  [N] Noticias (Titulares Virales)")
        print("  [F] Frases Maestras (Bitácora del Genio)")
        tipo_choice = input("Elige (N/F): ").strip().lower()
        
        tipo_data = 'frases' if tipo_choice == 'f' else 'noticias'
        textos = cargar_textos(tipo_data)
        
        print(f"\n📝 Opciones de Texto para el Gancho ({tipo_data.capitalize()}):")
        print("  [1-10] Escribe el número para usar ese texto.")
        print("  [C]    Escribe tu propio texto personalizado.")
        
        print(f"\n  📰 {tipo_data.capitalize()} disponibles:")
        for nid, txt in textos.items():
            preview = txt if len(txt) < 80 else txt[:77] + '...'
            print(f"      [{nid}] {preview}")
        
        choice = input("\nElige una opción: ").strip().lower()
        
        hook_text = ""
        if choice == 'c':
            hook_text = input("\nEscribe el texto impactante para la imagen:\n> ")
        elif choice.isdigit() and int(choice) in textos:
            hook_text = textos[int(choice)]
            print(f"\nUsando texto {choice}:\n'{hook_text}'")
        else:
            print("❌ Opción inválida. Escribe tu propio texto:")
            hook_text = input("> ")

        if not hook_text:
            print("❌ El texto no puede estar vacío.")
            continue

        output_dir = os.path.join(os.getcwd(), 'fb_images_ready')
        base_name = os.path.splitext(os.path.basename(latest_img))[0]
        out_path = os.path.join(output_dir, f"{base_name}_viral.jpg")
        
        print("\n🎨 Generando tarjeta...")
        # Pasamos es_frase=True si el usuario eligió 'f'
        create_viral_card(latest_img, hook_text, out_path, es_frase=(tipo_choice == 'f'))

        os.startfile(output_dir)

        print("\n" + "─"*60)
        otra = input("¿Deseas crear otra tarjeta? (Enter para continuar / N para salir): ")
        if otra.lower() == 'n':
            print("\n✨ ¡Sesión finalizada! Hasta la próxima.")
            break
        print("\n" + "="*60)

if __name__ == "__main__":
    main()
