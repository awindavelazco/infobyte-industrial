"""
SISTEMA MULTI-AGENTE DE NOTICIAS PARA FACEBOOK
================================================
AGENTE 1 - Redactor: Genera el artículo (ES + EN)
AGENTE 2 - Imagen:   Crea el prompt fotorealista basado en tendencias de FB
AGENTE 3 - Cumplimiento: Verifica reglas de Facebook
AGENTE 4 - Verificador: Comprueba que la noticia sea veraz y respaldada
"""

import urllib.request
import json
import re
import sys
import argparse
import os

sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────
# HASHTAGS FIJOS POR CATEGORÍA (100% fiables)
# ─────────────────────────────────────────────
HASHTAGS = {
    "Moda y Diseño":         "#Moda #Diseño #FashionDesign #Tendencias #AltaCostura",
    "Tecnología en la Moda": "#FashionTech #RopaInteligente #Innovacion #TextilesDelFuturo #Wearables",
    "Salud y Medicina":      "#Salud #Medicina #Biotecnologia #Bienestar #Ciencia",
    "Dinero y Economía":     "#Economia #Finanzas #Negocios #Emprendimiento #Dinero",
    "Tecnología General":    "#Tecnologia #Innovacion #InteligenciaArtificial #Futuro #Tech",
    "Historia Oculta":       "#Historia #Arqueologia #MisteriosDelMundo #CivilizacionesAntiguas #Descubrimientos",
    "Datos Insólitos":       "#DatosInsolitos #Curiosidades #Asombroso #SabiasQue #Increible",
    "Sostenibilidad":        "#Sostenibilidad #MedioAmbiente #EcologiaModa #ReciclajeTextil #PlanetaVerde",
    "Innovación y Futuro":   "#Innovacion #Futuro #Robotica #TecnologiaDelFuturo #SmartLife",
    "Bienestar y Psicología":"#Bienestar #SaludMental #Psicologia #Mindfulness #Autoestima"
}

# ─────────────────────────────────────────────
# ESTILOS VISUALES TRENDING EN FACEBOOK (base de datos interna)
# ─────────────────────────────────────────────
ESTILOS_FACEBOOK = {
    "Moda y Diseño":         "editorial fashion photography, professional model in studio, soft natural light, clean background",
    "Tecnología en la Moda": "close-up of smart fabric texture, person wearing innovative clothing, lifestyle photography",
    "Salud y Medicina":      "doctor and patient consultation in modern clinic, warm natural light, candid documentary style",
    "Dinero y Economía":     "young professional working on laptop in coffee shop, candid street photography, natural light",
    "Tecnología General":    "person using laptop or smartphone in everyday setting, candid documentary photography",
    "Historia Oculta":       "ancient stone ruins or archaeological site, dramatic natural light, wide angle photography",
    "Datos Insólitos":       "close-up macro photography of unusual natural or man-made object, vivid colors, sharp focus",
    "Sostenibilidad":        "person sorting recycled clothing in bright workshop, natural daylight, documentary style",
    "Innovación y Futuro":   "modern smart home interior with natural light, minimalist design, lifestyle photography",
    "Bienestar y Psicología":"woman applying makeup in natural light mirror, candid lifestyle photography, warm tones"
}

# ─────────────────────────────────────────────
# 10 TEMAS ÚNICOS - UNO POR SLOT (nunca se repiten dentro de un bloque de 10)
# ─────────────────────────────────────────────
TEMAS = [
    {"cat": "Moda y Diseño",
     "angulo": "El software de diseño 3D que permite crear patrones y colecciones completas sin usar tela física, reduciendo costos y desperdicio en la industria."},
    {"cat": "Tecnología en la Moda",
     "angulo": "Las prendas termocromáticas que cambian de color según la temperatura corporal y emociones del usuario, ya disponibles en el mercado."},
    {"cat": "Salud y Medicina",
     "angulo": "La nutrigenómica: ciencia que diseña dietas personalizadas basadas en el ADN de cada persona, reemplazando las dietas genéricas de moda."},
    {"cat": "Dinero y Economía",
     "angulo": "Creadores de contenido que generan ingresos de 6 cifras anuales: las plataformas, estrategias y nichos más rentables del mercado actual."},
    {"cat": "Tecnología General",
     "angulo": "Los nuevos chips de memoria cuántica que almacenan más datos que todos los centros de datos del mundo en el tamaño de una moneda."},
    {"cat": "Historia Oculta",
     "angulo": "La ciudad subterránea de Derinkuyu en Turquía: 18 pisos bajo tierra, capaz de albergar a 20,000 personas, construida sin tecnología moderna."},
    {"cat": "Datos Insólitos",
     "angulo": "El verde de París del siglo XIX: el pigmento más popular de la historia de la moda que contenía arsénico y causó miles de muertes silenciosas."},
    {"cat": "Sostenibilidad",
     "angulo": "Empresas que convierten ropa vieja en fibras textiles nuevas sin agua ni químicos: la economía circular que está rescatando la industria de la moda."},
    {"cat": "Innovación y Futuro",
     "angulo": "Los primeros hogares 100% autónomos que gestionan solos su energía, agua y temperatura sin intervención humana, ya habitables en 2024."},
    {"cat": "Bienestar y Psicología",
     "angulo": "El efecto paradójico del maquillaje en redes sociales: por qué las mujeres que muestran más make-up online reportan mayor ansiedad fuera de pantalla."},
]


def llamar_ollama(prompt_text, max_tokens=2000):
    """Llama al modelo Ollama local y devuelve la respuesta."""
    data = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False,
        "options": {"temperature": 0.8, "num_predict": max_tokens}
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode('utf-8')
    )
    req.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(req, timeout=300)
    result = json.loads(response.read().decode('utf-8'))
    return result['response']


def extract(marker, text):
    """Extrae el contenido entre marcadores [[MARKER]] y el siguiente [[."""
    pattern = rf"\[\[{marker}\]\][\s\*:]*(.*?)(?=\[\[|\Z)"
    match = re.search(pattern, text, re.S | re.I)
    return match.group(1).strip("* \n\t") if match else ""


# ─────────────────────────────────────────────
# AGENTE 1: REDACTOR DE NOTICIAS
# ─────────────────────────────────────────────
def agente_redactor(tema, titulos_anteriores):
    """Genera el artículo en ES e EN con estructura clara."""
    no_repetir = ""
    if titulos_anteriores:
        no_repetir = "NO repitas ninguno de estos temas ya publicados:\n" + "\n".join(f"- {t}" for t in titulos_anteriores[-20:])

    prompt = f"""Eres un periodista experto de alto nivel. Escribe UN ÚNICO reportaje profundo y original.

CATEGORÍA: {tema['cat']}
TEMA ESPECÍFICO: {tema['angulo']}

ESTRUCTURA OBLIGATORIA (usa EXACTAMENTE estos marcadores):
[[TITLE]]: Título impactante en español (máximo 12 palabras).
[[POST_ES]]: Reportaje en ESPAÑOL. Mínimo 400 palabras. Estructura: gancho inicial poderoso → 3 párrafos de contexto profundo con datos concretos → impacto en la vida real → pregunta filosófica al final. Usa emojis de forma natural en el texto.
[[POST_EN]]: Exact same article in ENGLISH. Minimum 400 words. Same structure and depth.
[[END_STORY]]

{no_repetir}
IMPORTANTE: Escribe SOLO el contenido dentro de los marcadores. No agregues introducción ni explicación fuera de ellos."""

    raw = llamar_ollama(prompt, 3000)
    return {
        "title": extract("TITLE", raw),
        "postES": extract("POST_ES", raw),
        "postEN": extract("POST_EN", raw),
        "raw": raw
    }


# ─────────────────────────────────────────────
# AGENTE 2: CREADOR DE PROMPT DE IMAGEN
# ─────────────────────────────────────────────
def agente_imagen(titulo, categoria, postES_resumen):
    """Genera un prompt de imagen fotorealista en inglés basado en tendencias de FB."""
    estilo_base = ESTILOS_FACEBOOK.get(categoria, "documentary photography, natural light, candid style")
    resumen = postES_resumen[:300] if postES_resumen else titulo

    prompt = f"""You are a professional photography art director specializing in viral Facebook content.

Create ONE image prompt in English for this news article:
Title: {titulo}
Summary: {resumen}
Visual style to follow: {estilo_base}

STRICT RULES:
- The image must look like a REAL photograph, not AI-generated art
- NO futuristic elements, NO holograms, NO sci-fi
- NO text, letters, or titles overlaid on image
- Must be relevant to the specific article topic
- Use natural lighting, real people or real places
- Style: documentary, editorial or lifestyle photography

Output ONLY the image prompt in one or two sentences. Nothing else."""

    raw = llamar_ollama(prompt, 200)
    # Limpiar el resultado
    prompt_img = raw.strip().strip('"\'').split('\n')[0].strip()
    return prompt_img


# ─────────────────────────────────────────────
# AGENTE 3: VERIFICADOR DE REGLAS DE FACEBOOK
# ─────────────────────────────────────────────
def agente_compliance(titulo, postES):
    """Verifica que el contenido cumpla las políticas de Facebook."""
    resumen = postES[:500] if postES else titulo

    prompt = f"""You are a Facebook Community Standards compliance expert.

Review this Spanish-language article and check if it violates Facebook policies:
Title: {titulo}
Content excerpt: {resumen}

Facebook key rules to check:
1. No misinformation about health (fake cures, dangerous medical advice)
2. No sensationalist clickbait that misleads users
3. No hate speech or discrimination
4. No content that promotes dangerous products
5. No violent or graphic content
6. Evergreen content (no specific unverified dates/events)

Respond with ONLY one of these two options:
APPROVED - Brief reason why it complies
WARNING: [specific issue found]"""

    raw = llamar_ollama(prompt, 200)
    resultado = raw.strip().split('\n')[0].strip()
    aprobado = resultado.upper().startswith("APPROVED")
    return aprobado, resultado


# ─────────────────────────────────────────────
# AGENTE 4: VERIFICADOR DE VERACIDAD
# ─────────────────────────────────────────────
def agente_verificador(titulo, postES):
    """Verifica que la noticia sea veraz, plausible y con respaldo real."""
    resumen = postES[:500] if postES else titulo

    prompt = f"""You are a professional fact-checker for a major news organization.

Evaluate this Spanish article for factual accuracy:
Title: {titulo}
Content: {resumen}

Check:
1. Is this topic real and documented by credible sources?
2. Are the facts plausible and scientifically sound?
3. Does it make claims that are completely fabricated or impossible?
4. Is the topic evergreen (not tied to unverifiable breaking news)?

Respond with ONLY:
VERIFIED - [brief reason it's credible]
NEEDS_REVIEW - [specific concern]"""

    raw = llamar_ollama(prompt, 200)
    resultado = raw.strip().split('\n')[0].strip()
    verificado = resultado.upper().startswith("VERIFIED")
    return verificado, resultado


# ─────────────────────────────────────────────
# FUNCIÓN DE ACTUALIZACIÓN DE script.js
# ─────────────────────────────────────────────
def actualizar_scriptjs():
    try:
        with open('posts_content.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        with open('script.js', 'r', encoding='utf-8') as f:
            content = f.read()
        parts = content.split('const newsData = [', 1)
        if len(parts) == 2:
            tail_parts = parts[1].split('];', 1)
            js_objects = []
            for item in posts:
                pes = json.dumps(item.get('postES', ''), ensure_ascii=False)
                pen = json.dumps(item.get('postEN', ''), ensure_ascii=False)
                cat = json.dumps(item.get('category', ''), ensure_ascii=False)
                tit = json.dumps(item.get('title', ''), ensure_ascii=False)
                prm = json.dumps(item.get('prompt', ''), ensure_ascii=False)
                obj_str = f'  {{\n    id: {item["id"]},\n    category: {cat},\n    title: {tit},\n    postES: {pes},\n    postEN: {pen},\n    prompt: {prm}\n  }}'
                js_objects.append(obj_str)
            new_content = parts[0] + 'const newsData = [\n' + ',\n'.join(js_objects) + '\n];' + tail_parts[1]
            with open('script.js', 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"🌐 script.js actualizado con {len(posts)} noticias.")
    except Exception as e:
        print(f"❌ Error actualizando script.js: {e}")


# ─────────────────────────────────────────────
# MAIN: ORQUESTADOR DE AGENTES
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cantidad', type=int, help='Número de noticias a generar')
    parser.add_argument('--clean', action='store_true', help='Borrar noticias actuales y empezar de cero')
    args = parser.parse_args()

    if args.clean:
        with open('posts_content.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        with open('new_prompts_to_generate.txt', 'w', encoding='utf-8') as f:
            f.write("")
        print("🧹 App limpiada. Listo para noticias frescas.")

    if args.cantidad == 0:
        actualizar_scriptjs()
        return

    # Leer títulos ya publicados para evitar repetición
    titulos_anteriores = []
    if os.path.exists('historico_noticias.txt'):
        with open('historico_noticias.txt', 'r', encoding='utf-8') as f:
            titulos_anteriores = [l.strip().lstrip('- ').strip() for l in f.readlines() if l.strip()]

    generadas = 0
    intentos_totales = 0
    max_intentos = args.cantidad * 2  # máximo 2 intentos por noticia

    i = 0
    while generadas < args.cantidad and intentos_totales < max_intentos:
        slot = i % len(TEMAS)
        tema = TEMAS[slot]
        i += 1
        intentos_totales += 1

        print(f"\n{'='*50}")
        print(f"📰 Noticia {generadas + 1}/{args.cantidad} | Categoría: {tema['cat']}")
        print(f"{'='*50}")

        try:
            # ── AGENTE 1: Redactar ──────────────────────────
            print("  ✍️  Agente 1 (Redactor) trabajando...")
            articulo = agente_redactor(tema, titulos_anteriores)

            if not articulo['title'] or not articulo['postES']:
                print("  ⚠️  Agente 1: Contenido vacío. Reintentando...")
                continue

            print(f"  ✅ Título: {articulo['title'][:60]}...")

            # ── AGENTE 3: Verificar cumplimiento FB ─────────
            print("  🔍 Agente 3 (Compliance Facebook) verificando...")
            aprobado_fb, razon_fb = agente_compliance(articulo['title'], articulo['postES'])
            if not aprobado_fb:
                print(f"  ⚠️  Agente 3: Contenido rechazado → {razon_fb}. Saltando...")
                continue
            print(f"  ✅ Compliance: {razon_fb[:60]}")

            # ── AGENTE 4: Verificar veracidad ───────────────
            print("  🔬 Agente 4 (Verificador) comprobando...")
            verificado, razon_ver = agente_verificador(articulo['title'], articulo['postES'])
            if not verificado:
                print(f"  ⚠️  Agente 4: Noticia cuestionable → {razon_ver}. Saltando...")
                continue
            print(f"  ✅ Verificación: {razon_ver[:60]}")

            # ── AGENTE 2: Crear prompt de imagen ────────────
            print("  🖼️  Agente 2 (Imagen) creando prompt visual...")
            prompt_img = agente_imagen(articulo['title'], tema['cat'], articulo['postES'])
            print(f"  ✅ Prompt imagen: {prompt_img[:60]}...")

            # ── Construir noticia final ──────────────────────
            hashtags = HASHTAGS.get(tema['cat'], "#Innovacion #Tecnologia #Futuro #Ciencia #Actualidad")
            cta_es = "\n\n📖 ¡Lee el artículo completo y déjanos tu opinión en los comentarios! 👇"

            noticia = {
                "category": tema['cat'],
                "title": articulo['title'],
                "postES": articulo['postES'] + cta_es + "\n\n" + hashtags,
                "postEN": articulo['postEN'] + "\n\n" + hashtags,
                "prompt": prompt_img
            }

            # ── Guardar en JSON ──────────────────────────────
            with open('posts_content.json', 'r', encoding='utf-8') as f:
                posts = json.load(f)
            next_id = max([p['id'] for p in posts]) + 1 if posts else 1
            noticia['id'] = next_id
            posts.append(noticia)
            with open('posts_content.json', 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)

            # ── Actualizar histórico ─────────────────────────
            with open('historico_noticias.txt', 'a', encoding='utf-8') as f:
                f.write(f"- {articulo['title']}\n")
            titulos_anteriores.append(articulo['title'])

            # ── Log de prompts de imagen ─────────────────────
            with open('new_prompts_to_generate.txt', 'a', encoding='utf-8') as f:
                f.write(f"=== NOTICIA {next_id}: {articulo['title']} ===\n")
                f.write(f"CATEGORÍA: {tema['cat']}\n")
                f.write(f"PROMPT IMAGEN (para Google Flow / Midjourney):\n{prompt_img}\n\n")

            generadas += 1
            print(f"  💾 Noticia {next_id} guardada con éxito.")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n🏁 Proceso finalizado. {generadas}/{args.cantidad} noticias generadas.")
    actualizar_scriptjs()
    print("🚀 ¡Listo! Revisa 'new_prompts_to_generate.txt' para tus imágenes.")


if __name__ == "__main__":
    main()
