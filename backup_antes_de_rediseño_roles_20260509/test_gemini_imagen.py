"""
TEST DE GENERACIÓN DE IMÁGENES — Pollinations.ai (100% GRATUITO)
=================================================================
Sin API Key. Sin billing. Sin límites estrictos.
Genera 3 variaciones del mismo prompt y las guarda en /test_imagenes/
"""

import urllib.request
import urllib.parse
import os
import random
from datetime import datetime

# ── CONFIGURACIÓN ──────────────────────────────────────────────────────────────
OUTPUT_FOLDER = "test_imagenes"
IMAGE_WIDTH   = 1080
IMAGE_HEIGHT  = 1080
IMAGE_MODEL   = "flux"   # opciones: flux, turbo, flux-realism

# ── PROMPT DE PRUEBA ───────────────────────────────────────────────────────────
TEST_PROMPT = (
    "A swirling vortex of iridescent colors and microscopic lifeforms surrounds "
    "a glowing crystal-like nucleus, cool blue bioluminescent lighting with glowing "
    "particles suspended in air, ultra-detailed textures of polished obsidian and "
    "brushed titanium, extreme depth of field with soft bokeh, 8k resolution, "
    "National Geographic cover style. "
    "no text, no letters, no watermark, no overlay, clean image only."
)

# ── MAIN ───────────────────────────────────────────────────────────────────────
def test_image_generation():
    print("=" * 55)
    print("  INFOBYTE — 3 Variaciones (Pollinations.ai - FREE)")
    print("=" * 55)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"[INFO] Carpeta creada: {OUTPUT_FOLDER}/")

    print(f"\n[MODELO] {IMAGE_MODEL} | {IMAGE_WIDTH}x{IMAGE_HEIGHT}px")
    print(f"[PROMPT] {TEST_PROMPT[:70]}...")
    print("[INFO] Generando 3 variaciones — espera 30-90 segundos...\n")

    seeds = [random.randint(1, 99999) for _ in range(3)]
    exitosas = 0

    for i, seed in enumerate(seeds, 1):
        print(f"[VARIACION {i}/3] seed={seed} ...")
        encoded_prompt = urllib.parse.quote(TEST_PROMPT)
        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}"
            f"&model={IMAGE_MODEL}&nologo=true&enhance=true&seed={seed}"
        )

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as response:
                image_data = response.read()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_FOLDER}/variacion_{i}_seed{seed}_{timestamp}.jpg"

            with open(filename, "wb") as f:
                f.write(image_data)

            size_kb = os.path.getsize(filename) / 1024
            print(f"  [✅] Guardada: {filename} ({size_kb:.1f} KB)")
            exitosas += 1

        except Exception as e:
            print(f"  [❌] Error: {e}")

    print(f"\n[RESULTADO] {exitosas}/3 imágenes generadas exitosamente.")
    print(f"[INFO] Revisa la carpeta: {OUTPUT_FOLDER}/")
    print("=" * 55)

if __name__ == "__main__":
    test_image_generation()
