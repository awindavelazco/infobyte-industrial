"""
INFOBYTE - Watermark Automático
================================
Agrega el logo de Infobyte a las imágenes descargadas de Google Flow.

USO:
  1. Descarga la imagen de Flow (queda en tu carpeta de Descargas)
  2. Corre este script: python add_watermark.py
  3. El script detecta la imagen más reciente en Descargas,
     le agrega el logo y la guarda lista para Facebook en /fb_images_ready/

También puedes procesar una imagen específica:
  python add_watermark.py "C:/ruta/a/imagen.png"
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import glob

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
LOGO_PATH = "infobyte_logo.png"
OUTPUT_FOLDER = "fb_images_ready"
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")

# Tamaño del logo como % del ancho de la imagen
LOGO_SIZE_PERCENT = 0.25   # 25% del ancho de la imagen
LOGO_OPACITY = 210          # 0 = invisible, 255 = sólido
MARGIN = 20                 # Margen desde el borde en píxeles

# ─────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────

def get_latest_image_from_downloads():
    """Detecta la imagen más reciente descargada."""
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(DOWNLOADS_FOLDER, ext)))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def add_watermark(image_path, output_path):
    """Agrega el logo de Infobyte en la esquina inferior izquierda."""

    # Cargar imagen base
    base = Image.open(image_path).convert("RGBA")
    base_w, base_h = base.size

    # Cargar logo
    logo = Image.open(LOGO_PATH).convert("RGBA")
    
    # --- ELIMINAR EL FONDO OSCURO DEL LOGO ---
    # El logo generado tiene un fondo navy blue (#0B132B aprox RGB 11, 19, 43)
    datas = logo.getdata()
    newData = []
    for item in datas:
        # Si el pixel es oscuro (fondo), hacerlo 100% transparente
        if item[0] < 50 and item[1] < 50 and item[2] < 70:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    logo.putdata(newData)
    # -----------------------------------------

    # Escalar logo al 25% del ancho de la imagen
    logo_w = int(base_w * LOGO_SIZE_PERCENT)
    logo_ratio = logo_w / logo.width
    logo_h = int(logo.height * logo_ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    # Aplicar opacidad al logo
    r, g, b, a = logo.split()
    a = a.point(lambda x: min(x, LOGO_OPACITY) if x > 0 else 0)
    logo = Image.merge("RGBA", (r, g, b, a))

    # Posicionar en esquina inferior izquierda
    pos_x = MARGIN
    pos_y = base_h - logo_h - MARGIN

    # Componer imagen final
    transparent = Image.new("RGBA", base.size, (0, 0, 0, 0))
    transparent.paste(logo, (pos_x, pos_y), logo)
    watermarked = Image.alpha_composite(base, transparent)

    # Guardar como RGB (sin transparencia para Facebook)
    final = watermarked.convert("RGB")
    final.save(output_path, quality=95)
    return output_path


def process_image(image_path):
    """Procesa una imagen y guarda el resultado."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_infobyte.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    print(f"\n📸 Procesando: {filename}")
    result = add_watermark(image_path, output_path)
    print(f"✅ Logo agregado → Guardado en: {output_path}")
    print(f"📐 Lista para Facebook (formato original preservado)")
    return result


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  📡 INFOBYTE — Watermark Automático")
    print("=" * 50)

    # Verificar que el logo existe
    if not os.path.exists(LOGO_PATH):
        print(f"❌ ERROR: No se encontró el logo en '{LOGO_PATH}'")
        print("   Asegúrate de que 'infobyte_logo.png' esté en esta carpeta.")
        sys.exit(1)

    # Modo 1: Imagen específica como argumento
    if len(sys.argv) > 1:
        image_path = sys.argv[1].strip('"')
        if not os.path.exists(image_path):
            print(f"❌ No se encontró la imagen: {image_path}")
            sys.exit(1)
        process_image(image_path)

    # Modo 2: Detectar automáticamente la más reciente en Descargas
    else:
        print(f"\n🔍 Buscando imagen más reciente en: {DOWNLOADS_FOLDER}")
        latest = get_latest_image_from_downloads()
        if not latest:
            print("❌ No se encontró ninguna imagen en la carpeta de Descargas.")
            print("   Descarga una imagen de Flow e intenta de nuevo.")
            sys.exit(1)
        print(f"   Encontrada: {os.path.basename(latest)}")
        confirm = input("\n¿Usar esta imagen? (Enter para confirmar / N para cancelar): ").strip().lower()
        if confirm == 'n':
            print("Cancelado.")
            sys.exit(0)
        process_image(latest)

    print("\n🚀 ¡Imagen lista para subir a Facebook!")
