import os
import glob
import json
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Configuración de Rutas Absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Fonts')

def get_latest_image(download_folder):
    list_of_files = glob.glob(os.path.join(download_folder, '*.[jp][pn]*')) 
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def cargar_textos(tipo='noticias'):
    if tipo == 'frases':
        filename = 'frases_content.json'
        key = 'phrases'
    elif tipo == 'quizzes':
        filename = 'quizzes_content.json'
        key = 'quizzes'
    else:
        filename = 'posts_content.json'
        key = 'posts'
        
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data.get(key, [])
            return {i+1: item for i, item in enumerate(items)}
    except Exception as e:
        print(f"X Error al cargar {path}: {e}")
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

def create_viral_card(image_path, text, output_path, tipo='noticias', options=None):
    target_width = 1080
    target_height = 1350

    if tipo == 'frases':
        # --- NUEVO DISEÑO: APUNTES DEL ALMA (Imagen de Fondo Zen + Texto) ---
        if image_path and os.path.exists(image_path):
            base = Image.open(image_path).convert("RGBA")
            # Redimensionar y recortar (Pinterest style 4:5)
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
                base = base.crop((left, top, left + target_width, top + target_height))
        else:
            # Fallback a fondo crema si no hay imagen
            base = Image.new('RGB', (target_width, target_height), (249, 248, 246)).convert("RGBA")
        
        # Capa de oscurecimiento suave para legibilidad
        overlay = Image.new('RGBA', base.size, (0, 0, 0, 80)) # 80/255 opacidad
        base = Image.alpha_composite(base, overlay)
        draw = ImageDraw.Draw(base)
        
        def get_font(name, size):
            try:
                return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)
            except:
                return ImageFont.load_default()

        font_title = get_font("georgia.ttf", 60)
        font_body = get_font("arial.ttf", 45)
        font_action = get_font("arialbd.ttf", 55)
        font_logo = get_font("arial.ttf", 30)

        # Dibujar marca de agua arriba
        marca = "A P U N T E S   D E L   A L M A"
        bbox_marca = draw.textbbox((0,0), marca, font=font_logo)
        w_marca = bbox_marca[2] - bbox_marca[0]
        draw.text(((target_width - w_marca)/2, 100), marca, font=font_logo, fill=(255, 255, 255, 180))
        draw.line([((target_width - w_marca)/2 - 50, 140), ((target_width + w_marca)/2 + 50, 140)], fill=(255, 255, 255, 100), width=2)

        # --- TEXTO CENTRADO CON SOMBRA (Sin caja negra) ---
        wrapped_text = wrap_text(text, font_title, target_width - 160, draw)
        
        # Calcular altura total
        total_text_h = 0
        for line in wrapped_text:
            bbox = draw.textbbox((0,0), line, font=font_title)
            total_text_h += (bbox[3] - bbox[1]) + 20
            
        current_y = (target_height - total_text_h) // 2
        
        # Dibujar texto envuelto con sombra suave
        for line in wrapped_text:
            bbox = draw.textbbox((0,0), line, font=font_title)
            w = bbox[2] - bbox[0]
            
            # Sombra
            draw.text(((target_width - w) / 2 + 3, current_y + 3), line, font=font_title, fill=(0, 0, 0, 180))
            # Texto principal
            draw.text(((target_width - w) / 2, current_y), line, font=font_title, fill=(255, 255, 255, 255))
            
            current_y += (bbox[3] - bbox[1]) + 20
    else:
        # --- DISEÑO PREMIUM: GOLD & BLACK CON OPACIDAD (Logo central + Caja Opaca + Texto Dorado) ---
        if not image_path:
            print("X Se necesita una imagen de fondo para las noticias.")
            return
            
        base = Image.open(image_path).convert("RGBA")
        
        # 1. REDIMENSIONAR IMAGEN
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
            base = base.crop((left, top, left + target_width, top + target_height))
        
        draw = ImageDraw.Draw(base)

        # 2. DEFINIR FUENTE
        def get_font_main(name, size):
            try:
                return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)
            except:
                return ImageFont.load_default()

        font_main = get_font_main("arialbd.ttf", 45)

        # APLICAR DISEÑO SEGÚN TIPO
        if tipo == 'noticias':
            # --- DISEÑO GOLD & BLACK (NOTICIAS) ---
            # 2. CALCULAR TEXTO
            wrapped = textwrap.wrap(text.upper(), width=32)
            line_heights = [draw.textbbox((0,0), line, font=font_main)[3] - draw.textbbox((0,0), line, font=font_main)[1] for line in wrapped]
            total_text_height = sum(line_heights) + (len(wrapped)-1)*15
            
            # 3. DIBUJAR FRANJA NEGRA CON OPACIDAD (180/255) - FULL WIDTH
            rect_y_start = target_height - total_text_height - 140
            
            overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle([0, rect_y_start, target_width, target_height], fill=(0, 0, 0, 180))
            base = Image.alpha_composite(base, overlay)
            draw = ImageDraw.Draw(base)

            # 4. INTEGRAR LOGO CENTRADO
            log_h = 0
            logo_path = os.path.join(BASE_DIR, "infobyte_logo.png")
            if os.path.exists(logo_path):
                logo = Image.open(logo_path).convert("RGBA")
                log_w = 220
                log_h = int(logo.height * (log_w / logo.width))
                logo = logo.resize((log_w, log_h), Image.Resampling.LANCZOS)
                logo_x = (target_width - log_w) // 2
                logo_y = rect_y_start - (log_h // 2)
                base.paste(logo, (logo_x, logo_y), logo)

            # 5. DIBUJAR TEXTO DORADO
            color_oro = (212, 175, 55, 255)
            y_text = rect_y_start + (log_h // 2) + 20 if log_h > 0 else rect_y_start + 40
            for line in wrapped:
                bbox = draw.textbbox((0,0), line, font=font_main)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                x_text = (target_width - w) / 2
                draw.text((x_text, y_text), line, font=font_main, fill=color_oro)
                y_text += h + 15

        elif tipo == 'quizzes':
            # --- DISEÑO INTERACTIVO (QUIZ) ---
            # 2. CALCULAR TÍTULO (ARRIBA)
            wrapped = textwrap.wrap(text.upper(), width=35)
            line_heights = [draw.textbbox((0,0), line, font=font_main)[3] - draw.textbbox((0,0), line, font=font_main)[1] for line in wrapped]
            total_text_height = sum(line_heights) + (len(wrapped)-1)*15
            
            # Franja superior para la pregunta
            rect_y_end = total_text_height + 80
            overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle([0, 0, target_width, rect_y_end], fill=(0, 0, 0, 200))
            
            # --- NUEVA FRANJA INFERIOR CALIBRADA ---
            inferior_h = 220
            overlay_draw.rectangle([0, target_height - inferior_h, target_width, target_height], fill=(0, 0, 0, 180))
            
            base = Image.alpha_composite(base, overlay)
            draw = ImageDraw.Draw(base)

            # Dibujar Pregunta arriba
            y_text = 40
            for line in wrapped:
                bbox = draw.textbbox((0,0), line, font=font_main)
                w = bbox[2] - bbox[0]
                x_text = (target_width - w) / 2
                draw.text((x_text, y_text), line, font=font_main, fill=(255, 255, 255, 255))
                y_text += (bbox[3] - bbox[1]) + 15

            # 3. LOGO EN LA PARTE INFERIOR (CENTRADO)
            logo_path = os.path.join(BASE_DIR, "infobyte_logo.png")
            if os.path.exists(logo_path):
                logo = Image.open(logo_path).convert("RGBA")
                log_w = 150
                log_h_quiz = int(logo.height * (log_w / logo.width))
                logo = logo.resize((log_w, log_h_quiz), Image.Resampling.LANCZOS)
                logo_x = (target_width - log_w) // 2
                logo_y = target_height - inferior_h + 15
                base.paste(logo, (logo_x, logo_y), logo)

            # 4. DIBUJAR NÚMEROS Y NOMBRES PEQUEÑOS (DENTRO DE LA FRANJA)
            circle_y = target_height - 55
            spacing = target_width // 5
            color_oro = (212, 175, 55, 255)
            
            try:
                font_num = ImageFont.truetype("arialbd.ttf", 35)
                font_label = ImageFont.truetype("arial.ttf", 22)
            except:
                font_num = font_main
                font_label = font_main

            for i in range(1, 5):
                x = spacing * i
                
                if options and len(options) >= i:
                    opt_text = str(options[i-1])
                    # Limpiar prefijo "N. " de forma segura para cualquier número
                    if '. ' in opt_text: opt_text = opt_text.split('. ', 1)[1]
                    
                    opt_wrapped = textwrap.wrap(opt_text.upper(), width=14)
                    y_opt = circle_y - 85 # Más cerca del círculo para no chocar con el logo
                    for line in opt_wrapped:
                        l_bbox = draw.textbbox((0,0), line, font=font_label)
                        l_w = l_bbox[2] - l_bbox[0]
                        draw.text((x - l_w//2, y_opt), line, font=font_label, fill=(255, 255, 255, 255))
                        y_opt += 22

                # Círculo más pequeño
                r = 40
                draw.ellipse([x-r, circle_y-r, x+r, circle_y+r], outline=color_oro, width=4)
                # Número
                n_str = str(i)
                n_bbox = draw.textbbox((0,0), n_str, font=font_num)
                n_w = n_bbox[2] - n_bbox[0]
                n_h = n_bbox[3] - n_bbox[1]
                draw.text((x - n_w//2, circle_y - n_h//2 - 5), n_str, font=font_num, fill=color_oro)

    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    base.convert("RGB").save(output_path, quality=95)
    print(f"OK Tarjeta guardada en: {output_path}")

def main():
    print("="*60)
    print(" 🚀 INFOBYTE — GENERADOR DE TARJETAS VIRALES ")
    print("="*60)

    while True:
        print("\n ¿Qué tipo de contenido vas a publicar?")
        print("  [N] Noticias (Titulares Virales)")
        print("  [F] Frases Maestras (Apuntes del Alma)")
        print("  [Q] Quiz (Retos Psicológicos Virales)")
        tipo_choice = input("Elige (N/F/Q): ").strip().lower()
        
        latest_img = None
        if tipo_choice in ['n', 'q']:
            user_dir = os.path.expanduser('~')
            downloads_dir = os.path.join(user_dir, 'Downloads')
            print(f"\n🔍 Buscando la imagen más reciente en: {downloads_dir}")
            latest_img = get_latest_image(downloads_dir)
            
            if not latest_img:
                print("X No se encontraron imágenes en la carpeta de descargas.")
                break
                
            print(f"   Encontrada: {os.path.basename(latest_img)}")
            confirm = input("¿Usar esta imagen? (Enter para confirmar / N para cancelar): ")
            if confirm.lower() == 'n':
                print("Operación cancelada.")
                break
        
        # 1. Obtener datos
        tipo_choice_full = 'noticias'
        if tipo_choice == 'f': tipo_choice_full = 'frases'
        elif tipo_choice == 'q': tipo_choice_full = 'quizzes'
        
        data_items = cargar_textos(tipo_choice_full)
        
        print(f"\n Opciones de {tipo_choice_full.capitalize()} disponibles:")
        for nid, item in data_items.items():
            cat = item.get('category', 'General')
            title = item.get('title', 'Sin Título')
            txt = ""
            if tipo_choice == 'f': txt = item.get('hook_text', '')
            elif tipo_choice == 'q': txt = item.get('headline', '')
            else: txt = item.get('image_text_hook', '')
            
            print(f"      [{nid}] [{cat}] -> {title}")
            print(f"          Texto: {txt[:100]}...")
        
        choice = input("\nElige una opción (número): ").strip()
        
        if choice.isdigit() and int(choice) in data_items:
            item_selected = data_items[int(choice)]
            if tipo_choice == 'f': hook_text = item_selected.get('hook_text', '')
            elif tipo_choice == 'q': hook_text = item_selected.get('headline', '')
            else: hook_text = item_selected.get('image_text_hook', '')
            
            # Solo buscar imagen del JSON para Noticias; Frases ya tiene imagen confirmada
            json_img = item_selected.get('image_path', '')
            if json_img and not os.path.isabs(json_img):
                json_img = os.path.join(BASE_DIR, json_img)

            if tipo_choice != 'f' and json_img and os.path.exists(json_img):
                latest_img = json_img
            elif not latest_img or not os.path.exists(latest_img):
                user_dir = os.path.expanduser('~')
                downloads_dir = os.path.join(user_dir, 'Downloads')
                latest_img = get_latest_image(downloads_dir)
        else:
            print("X Opción inválida.")
            continue

        if not hook_text:
            print("X El texto no puede estar vacío.")
            continue

        output_dir = os.path.join(BASE_DIR, 'fb_images_ready')
        if latest_img and os.path.exists(latest_img):
            base_name = os.path.splitext(os.path.basename(latest_img))[0]
            out_path = os.path.join(output_dir, f"{base_name}_viral.jpg")
        else:
            # Fallback total
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(output_dir, f"infobyte_{timestamp}.jpg")
        
        print("\n Generando tarjeta...")
        opts = item_selected.get('options', []) if tipo_choice == 'q' else None
        create_viral_card(latest_img, hook_text, out_path, tipo=tipo_choice_full, options=opts)

        os.startfile(output_dir)

        print("\n" + "─"*60)
        otra = input("¿Deseas crear otra tarjeta? (Enter para continuar / N para salir): ")
        if otra.lower() == 'n':
            print("\n✨ ¡Sesión finalizada! Hasta la próxima.")
            break
        print("\n" + "="*60)

if __name__ == "__main__":
    main()
