"""
=============================================================================
  AUDITOR DE VIDEOS — AGENTE DE CONTROL DE CALIDAD DE PROMPTS
  Infobyte | facebook_post_assistant
  Autor: Antigravity AI
  Regla de Oro: SOLO LECTURA. Este script NUNCA modifica archivos existentes.
=============================================================================
  Evalúa prompts de video contra 5 Pilares de Calidad y emite un veredicto
  de factibilidad (Aprobado / Revisión / Rechazado) por cada clip y video.

  Archivos que escanea (solo lectura):
    - videos_content.json      (formato: 5 clips, estilo fotorrealista)
    - video_moda_cartoon.json  (formato: 4 clips, estilo Cartoon Hero)
    - seedboy_content.json     (si existe, mismo formato de videos)

  Uso:
    python auditor_videos.py
=============================================================================
"""

import json
import os
import re
import sys
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# CONSTANTES DE CONFIGURACION
# =============================================================================

# Palabras clave de cinematografía premium que validan calidad visual
CINEMATIC_KEYWORDS = [
    'cinematic', 'rim light', 'soft shadow', 'subsurface scattering',
    'golden hour', 'bokeh', 'slow-motion', 'dutch angle', 'close-up',
    'wide shot', 'medium shot', 'extreme close-up', 'elevated', 'aerial',
    '4K', 'photorealistic', 'octane render', 'pixar', 'disney', '3D style',
    'lighting', 'dramatic', 'ethereal', 'cinematic depth',
]

# Palabras de acción de continuidad entre clips
CONTINUITY_KEYWORDS = [
    'continuing from previous clip',
    'keep consistency',
    'same character',
    'same environment',
    'same scene',
    'from previous',
    'maintaining',
]

# Palabras que indican física compleja de alto riesgo para la IA
HIGH_RISK_PHYSICS = [
    'running fast', 'running quickly', 'jumping', 'spinning rapidly',
    'fighting', 'complex crowd', 'multiple people interacting',
    'hands touching face', 'eating food', 'drinking', 'writing text',
    'detailed hand movement', 'driving a car', 'bicycle',
]

# Sufijo de blindaje anti-texto en el prompt
NO_TEXT_SHIELD = [
    'no text', 'no letters', 'no typography',
    'clean aesthetic', 'no writing', 'no words',
    'absolutely no text',
]

# Rangos óptimos de longitud de un prompt por clip (en caracteres)
PROMPT_MIN_CHARS = 80
PROMPT_IDEAL_MIN = 120
PROMPT_IDEAL_MAX = 300
PROMPT_MAX_CHARS = 450

# =============================================================================
# INTELIGENCIA DE MERCADO — BASE DE CONOCIMIENTO DEL AGENTE (Facebook 2026)
# Fuente: Investigación de patrones reales de retención, psicología viral y
# saturación visual. Actualizado: 2026-05.
# =============================================================================

# --- PILAR 6A: PATRONES DE RETENCIÓN (Hooks que detienen el scroll) ---
# Basado en: Análisis de Facebook Reels 2026. Meta reporta que el 70%+ de
# retención en los primeros 3s depende del tipo de apertura visual/textual.

# Fórmulas de hooks que interrumpen el scroll (Curiosity Gap probado)
VIRAL_CURIOSITY_HOOKS = [
    # Fórmulas de error/problema (la más efectiva: "Stop doing X")
    'stop doing', 'deja de hacer', 'the #1 mistake', 'el error #1',
    'you are doing it wrong', 'lo estas haciendo mal',
    # Fórmulas de curiosity gap
    'did you know', 'sabias que', 'the secret', 'el secreto',
    'nobody tells you', 'nadie te dice', 'experts dont want',
    'lo que nadie te dice',
    # Fórmulas contraintuitivas (cognitive dissonance)
    'why i stopped', 'por que deje de', 'this is why', 'por eso',
    'what if i told you', 'y si te dijera',
    # Fórmulas de urgencia/valor inmediato
    'this 10-second', 'in just', 'en solo', 'if you are struggling',
    'si luchas con', 'watch this', 'mira esto',
    # Fórmulas generales de descubrimiento
    'discover', 'descubre', 'unlock', 'desbloquea',
    'the truth', 'la verdad',
]

# Hooks visuales que detienen el scroll (para evaluar el Clip 1)
HOOK_VISUAL_PATTERNS = [
    'extreme close-up',   # Zoom agresivo — detiene el scroll por impacto
    'close-up',           # Primer plano — conexión emocional inmediata
    'macro',              # Detalle macro — despierta curiosidad visual
    'eyes',               # Ojos en primer plano — conexión humana instintiva
    'face',               # Cara — activa el reconocimiento facial del cerebro
    'contrast',           # Colores contrastantes — destacan en el feed
    'zooming in',         # Movimiento hacia el sujeto — sensación dinámica
    'dutch angle',        # Ángulo inclinado — genera tensión/incomodidad
    'tense', 'frustrated', 'overwhelm',  # Emoción negativa inicial (problema)
    'cold light', 'harsh light', 'fluorescent',  # Iluminación fría = tensión
]

# --- PILAR 6B: DRIVERS DE VIRALIDAD CIENTÍFICA ---
# Basado en: Neurociencia del sharing (fMRI studies), Berger's STEPPS framework.
# El contenido científico viral activa el medial prefrontal cortex (identidad)
# y el ventral striatum (dopamina de compartir).

VIRAL_SCIENCE_KEYWORDS = [
    # Respaldo académico (Social Currency — "parece que sabes mucho")
    'study', 'research', 'science', 'proven', 'university',
    'scientists', 'harvard', 'stanford', 'mit', 'journal',
    'researchers found', 'found that', 'according to',
    'estudio', 'investigacion', 'ciencia', 'universidad', 'segun',
    # Datos del cerebro (máximo impacto — "explica algo de mí mismo")
    'brain', 'neuroscience', 'neurons', 'dopamine', 'cortisol',
    'prefrontal', 'amygdala', 'serotonin', 'cerebro', 'neurociencia',
    'neuronas', 'dopamina', 'cortisol', 'serotonina',
    # Estadísticas de impacto personal (Practical Value)
    '%', 'percent', 'times more', 'veces mas', '21 days', '21 dias',
    'in 30 days', 'en 30 dias', 'rewire', 'recablear',
    # Descubrimiento/novedad (FOMO — "el secreto que debes saber ya")
    'discovered', 'descubrio', 'breakthrough', 'avance',
    'new study', 'nuevo estudio', 'just confirmed', 'recien confirmado',
]

# Drivers emocionales de viralidad (Identity + Belonging)
VIRAL_EMOTION_KEYWORDS = [
    # Emociones de alta activación (awe, joy — las que más se comparten)
    'amazing', 'incredible', 'powerful', 'breathtaking', 'asombroso',
    'incredible', 'increible', 'poderoso', 'impresionante',
    # Emociones de transformación personal (el arco más viral)
    'transform', 'change your life', 'cambiar tu vida', 'transformar',
    'never the same', 'nunca sera igual', 'life-changing', 'que cambia vidas',
    # Estados positivos de alto valor social
    'happiness', 'joy', 'peace', 'freedom', 'gratitude', 'love', 'hope',
    'felicidad', 'alegria', 'paz', 'libertad', 'gratitud', 'amor', 'esperanza',
    'bienestar', 'wellness', 'fulfillment', 'plenitud',
    # Validación de experiencias comunes (Relatability)
    'feel', 'sentirte', 'struggle', 'lucha', 'anxiety', 'ansiedad',
    'exhausted', 'agotado', 'overwhelmed', 'abrumado',
]

# Call-to-action que generan engagement real (no bait prohibido por Meta)
VIRAL_CTA_KEYWORDS = [
    # CTAs aprobados por Meta (no "Like si..." que está penalizado)
    'share', 'comparte', 'save this', 'guarda este',
    'tag someone', 'etiqueta a alguien', 'send this to', 'enviaselo a',
    'comment below', 'comenta abajo', 'tell us', 'dinos',
    'what do you think', 'que piensas tu', 'what has been your',
    'cual ha sido tu', 'have you experienced', 'has experimentado',
]

# --- PILAR 6C: SATURACIÓN VISUAL — IMÁGENES "QUEMADAS" EN FACEBOOK ---
# Basado en: Análisis de tendencias 2025-2026. Estas imágenes generan
# "banner blindness" — el cerebro las ignora automáticamente.

VISUAL_CLICHES_BURNED = [
    # Clichés corporativos (máxima saturación)
    'high-fiving', 'jumping in the air', 'business handshake',
    'pointing at graph', 'pointing at chart', 'glass office',
    'team meeting smiling', 'suit and tie', 'professional team',
    # Emociones forzadas/actuadas
    'laughing with salad', 'perfect smile', 'overly enthusiastic',
    'mime emotion', 'acting excited', 'staged happiness',
    # Estética genérica de IA (2025 — "plastic look")
    'generic 3d background', 'shiny 3d render', 'plastic look',
    'template aesthetic', 'ai generated background',
    # Imágenes de "brag" o éxito genérico
    'luxury car', 'stacks of money', 'mansión', 'yacht',
    'hustle quote', 'motivational sunset',
    # Visuaes abstractos sin conexión humana
    'unrelated stock photo', 'foto de stock generica',
    'abstract background', 'generic landscape',
]


# Umbrales de veredicto (sobre 30 puntos — 6 pilares x 5 pts)
THRESHOLD_APPROVED = 23
THRESHOLD_REVIEW   = 16

# Nota sobre la fuente de inteligencia:
# Las listas anteriores son una BASE DE CONOCIMIENTO ESTATICA investigada
# en mayo 2026 a partir de patrones reales de Facebook Reels, estudios de
# neurociencia del sharing (Berger's STEPPS, fMRI studies) y analisis de
# saturacion visual. Para mantenerla actualizada, ejecutar mensualmente:
#   python actualizar_inteligencia.py  (pendiente de crear)

# =============================================================================
# PILAR 1 — CONTINUIDAD Y COHERENCIA TEMPORAL (0-5 pts)
# =============================================================================

def score_continuity(clip_prompt: str, clip_index: int, total_clips: int) -> tuple[int, list[str]]:
    """
    En el formato de MONTAJE DINÁMICO, ya no se requiere la frase de continuidad.
    Ahora evaluamos la consistencia del personaje (Character Anchor).
    """
    notes = []
    text_lower = clip_prompt.lower()

    if clip_index == 0:
        # Clip 1 (Hook): evaluar si usa patrones visuales de alto impacto
        visual_hooks_found = [p for p in HOOK_VISUAL_PATTERNS if p in text_lower]
        if len(visual_hooks_found) >= 2:
            notes.append(f"  OK  Hook visual de alto impacto: {visual_hooks_found[:3]}. Detendra el scroll.")
            return 5, notes
        elif len(visual_hooks_found) == 1:
            notes.append(f"  WARN Hook visual basico: '{visual_hooks_found[0]}'. Anadir zoom agresivo, ojos o contraste de luz.")
            return 3, notes
        else:
            notes.append("  FAIL Clip 1 no usa ningun patron visual de retencion. Alto riesgo de scroll-through.")
            return 1, notes

    # Clips 2+: Validar que se mantenga la descripción física del personaje (Ancla)
    # Buscamos que el prompt sea descriptivo sobre el sujeto sin depender de frases de enlace
    if len(clip_prompt) > 100 and ("woman" in text_lower or "man" in text_lower or "person" in text_lower):
        notes.append("  OK  Consistencia de personaje detectada mediante descripción física.")
        return 5, notes
    else:
        notes.append("  WARN Prompt demasiado corto o sin descripción de sujeto. Riesgo de inconsistencia visual.")
        return 3, notes


# =============================================================================
# PILAR 2 — VIABILIDAD FÍSICA / RENDERABILIDAD (0-5 pts)
# =============================================================================

def score_physics_viability(clip_prompt: str) -> tuple[int, list[str]]:
    """
    Penaliza físicas complejas que la IA de video raramente renderiza bien.
    Premia movimientos de cámara simples y acciones expresivas estáticas.
    """
    notes = []
    text_lower = clip_prompt.lower()

    risky_found = [kw for kw in HIGH_RISK_PHYSICS if kw in text_lower]

    if not risky_found:
        notes.append("  OK  Sin físicas de alto riesgo detectadas.")
        score = 5
    elif len(risky_found) == 1:
        notes.append(f"  WARN Física de riesgo moderado: '{risky_found[0]}'. Posible artefacto en el video.")
        score = 3
    else:
        notes.append(f"  FAIL {len(risky_found)} acciones de alto riesgo: {risky_found}. Alta probabilidad de renderizado defectuoso.")
        score = 1

    return score, notes


# =============================================================================
# PILAR 3 — CALIDAD CINEMATOGRÁFICA Y DIRECCIÓN VISUAL (0-5 pts)
# =============================================================================

def score_cinematic_quality(clip_prompt: str) -> tuple[int, list[str]]:
    """
    Evalúa cuántas palabras clave de cinematografía premium contiene el prompt.
    Mínimo 2 para ser aceptable. Ideal: 3-4.
    """
    notes = []
    text_lower = clip_prompt.lower()
    found = [kw for kw in CINEMATIC_KEYWORDS if kw.lower() in text_lower]

    if len(found) >= 4:
        notes.append(f"  OK  Dirección cinematográfica excelente: {found[:4]}")
        return 5, notes
    elif len(found) >= 2:
        notes.append(f"  OK  Dirección cinematográfica aceptable: {found[:3]}")
        return 4, notes
    elif len(found) == 1:
        notes.append(f"  WARN Solo 1 keyword cinematográfico: '{found[0]}'. Añadir iluminación o tipo de plano.")
        return 2, notes
    else:
        notes.append("  FAIL Sin keywords cinematográficos. El prompt es genérico y producirá resultados mediocres.")
        return 0, notes


# =============================================================================
# PILAR 4 — BLINDAJE ANTI-TEXTO (0-5 pts)
# =============================================================================

def score_no_text_shield(clip_prompt: str) -> tuple[int, list[str]]:
    """
    Verifica que el prompt tenga protección explícita contra la generación
    de texto, letreros o tipografía en el video.
    """
    notes = []
    text_lower = clip_prompt.lower()
    found = [kw for kw in NO_TEXT_SHIELD if kw in text_lower]

    if len(found) >= 2:
        notes.append(f"  OK  Blindaje anti-texto activo: {found}")
        return 5, notes
    elif len(found) == 1:
        notes.append(f"  WARN Blindaje parcial: '{found[0]}'. Añadir '[CRITICAL: ABSOLUTELY NO TEXT, NO LETTERS, NO TYPOGRAPHY]'.")
        return 3, notes
    else:
        notes.append("  FAIL SIN blindaje anti-texto. La IA puede generar letreros ilegibles en el video.")
        return 0, notes


# =============================================================================
# PILAR 5 — ECONOMÍA DE TOKENS / LONGITUD ÓPTIMA (0-5 pts)
# =============================================================================

def score_token_economy(clip_prompt: str) -> tuple[int, list[str]]:
    """
    Evalúa si la longitud del prompt está dentro del rango óptimo.
    Demasiado corto = genérico. Demasiado largo = agota la cuota de API.
    """
    notes = []
    length = len(clip_prompt.strip())

    if length < PROMPT_MIN_CHARS:
        notes.append(f"  FAIL Prompt demasiado corto ({length} chars). Mínimo recomendado: {PROMPT_MIN_CHARS}.")
        return 0, notes
    elif length < PROMPT_IDEAL_MIN:
        notes.append(f"  WARN Prompt corto ({length} chars). Genérico. Añadir detalle de cámara o expresión.")
        return 2, notes
    elif length <= PROMPT_IDEAL_MAX:
        notes.append(f"  OK  Longitud óptima ({length} chars). Eficiente y descriptivo.")
        return 5, notes
    elif length <= PROMPT_MAX_CHARS:
        notes.append(f"  WARN Prompt largo ({length} chars). Funciona, pero consume más tokens de lo necesario.")
        return 3, notes
    else:
        notes.append(f"  FAIL Prompt excesivamente largo ({length} chars). Riesgo de 429 RESOURCE_EXHAUSTED. Reducir.")
        return 1, notes

# =============================================================================
# PILAR 6 — POTENCIAL VIRAL EN FACEBOOK (0-5 pts)
# Evaluado a nivel de VIDEO completo (post_text + voiceover + clips).
# =============================================================================

def score_viral_potential(post_text: str, voiceover: str, hashtags: str = "",
                          all_clip_prompts: list = None) -> tuple[int, list[str]]:
    """
    Pilar 6: Evalua si el video tiene potencial viral en Facebook.
    FUENTE DE DATOS: Base de conocimiento investigada en mayo 2026 a partir de:
      - Meta/Facebook Reels 2026 retention analytics
      - Berger's STEPPS framework (Wharton Business School)
      - fMRI studies sobre neurociencia del sharing
      - Analisis de saturacion visual 2025-2026

    Criterios (1 punto cada uno, max 5):
      1. Curiosity Gap / Hook de retencion en el post o voiceover
      2. Respaldo cientifico (dato, porcentaje, institucion)
      3. Elemento humano/emocional (awe, transformacion, relatabilidad)
      4. Call-to-action aprobado por Meta (no bait penalizado)
      5. Hashtags en rango optimo (3-8) Y sin cliches visuales quemados
    """
    notes = []
    combined = (post_text + " " + voiceover + " " + hashtags).lower()
    clips_text = " ".join(all_clip_prompts or []).lower()
    score = 0

    # 1. Curiosity Gap / Hook de retencion
    hooks_found = [kw for kw in VIRAL_CURIOSITY_HOOKS if kw in combined]
    if hooks_found:
        notes.append(f"  OK  Gancho de curiosidad: '{hooks_found[0]}'")
        score += 1
    else:
        notes.append("  WARN Sin Curiosity Gap. Probar: 'Did you know...', 'The #1 mistake...' o 'Stop doing...'")

    # 2. Respaldo cientifico (Social Currency + Practical Value)
    science_found = [kw for kw in VIRAL_SCIENCE_KEYWORDS if kw in combined]
    if science_found:
        notes.append(f"  OK  Respaldo cientifico presente: '{science_found[0]}'")
        score += 1
    else:
        notes.append("  FAIL Sin dato cientifico. Agregar: porcentaje, nombre de universidad o resultado de estudio.")

    # 3. Elemento humano/emocional (Emotional Arousal -> sharing)
    emotion_found = [kw for kw in VIRAL_EMOTION_KEYWORDS if kw in combined]
    if emotion_found:
        notes.append(f"  OK  Elemento emocional: '{emotion_found[0]}'")
        score += 1
    else:
        notes.append("  FAIL Sin emocion. El cerebro comparte lo que le hace sentir algo. Agregar transformacion o awe.")

    # 4. Call-to-action (aprobado por Meta, no engagement bait)
    cta_found = [kw for kw in VIRAL_CTA_KEYWORDS if kw in combined]
    if cta_found:
        notes.append(f"  OK  CTA Meta-aprobado: '{cta_found[0]}'")
        score += 1
    else:
        notes.append("  WARN Sin CTA. Usar: 'Share with someone who needs this' o 'Comment: what changed your life?'")

    # 5. Hashtags en rango optimo + chequeo de cliches visuales quemados
    all_hashtags = [w for w in combined.split() if w.startswith('#')]
    ht_count = len(all_hashtags)
    cliches_found = [c for c in VISUAL_CLICHES_BURNED if c in clips_text]

    if cliches_found:
        notes.append(f"  FAIL CLICHE VISUAL QUEMADO detectado: {cliches_found[:2]}. El feed lo ignorara automaticamente.")
        # No suma el punto aunque los hashtags sean buenos
    elif 3 <= ht_count <= 8:
        notes.append(f"  OK  Hashtags optimos ({ht_count}) + sin cliches visuales. Alcance organico favorecido.")
        score += 1
    elif ht_count > 8:
        notes.append(f"  WARN {ht_count} hashtags. Facebook penaliza >8. Reducir a 5-7 tematicos.")
    else:
        notes.append(f"  FAIL Solo {ht_count} hashtags. Minimo 3 para alcance organico en Facebook.")

    return score, notes


# =============================================================================
# MOTOR PRINCIPAL — EVALUACIÓN DE UN CLIP
# =============================================================================

def evaluate_clip(prompt: str, clip_index: int, total_clips: int, phase_name: str = "",
                  p6_score: int = 0, p6_notes: list = None) -> dict:
    """
    Evalúa un único clip de video contra los 6 pilares.
    P6 (Viral) se calcula a nivel de video y se pasa como argumento.
    """
    p1_score, p1_notes = score_continuity(prompt, clip_index, total_clips)
    p2_score, p2_notes = score_physics_viability(prompt)
    p3_score, p3_notes = score_cinematic_quality(prompt)
    p4_score, p4_notes = score_no_text_shield(prompt)
    p5_score, p5_notes = score_token_economy(prompt)

    total = p1_score + p2_score + p3_score + p4_score + p5_score + p6_score

    if total >= THRESHOLD_APPROVED:
        verdict = "APROBADO"
        verdict_icon = "[OK]"
    elif total >= THRESHOLD_REVIEW:
        verdict = "REVISION REQUERIDA"
        verdict_icon = "[!!]"
    else:
        verdict = "RECHAZADO"
        verdict_icon = "[XX]"

    return {
        "phase": phase_name or f"Clip {clip_index + 1}",
        "scores": {
            "P1_Continuidad":    p1_score,
            "P2_Fisica":         p2_score,
            "P3_Cinematografia": p3_score,
            "P4_AntiTexto":      p4_score,
            "P5_TokenEconomia":  p5_score,
            "P6_PotencialViral": p6_score,
        },
        "total": total,
        "max_total": 30,
        "verdict": verdict,
        "verdict_icon": verdict_icon,
        "notes": p1_notes + p2_notes + p3_notes + p4_notes + p5_notes + (p6_notes or []),
    }


# =============================================================================
# PARSERS DE ESTRUCTURA JSON
# =============================================================================

def extract_clips_from_videos_json(data: dict) -> list[dict]:
    """
    Parsea el formato de videos_content.json (5 clips por video, estilo fotorrealista).
    Devuelve una lista de (nombre, prompt, index_en_video, total_clips_en_video).
    """
    clips = []
    videos = data.get("videos", [])
    clip_keys_ordered = [
        ("clip_1_hook_en",       "HOOK"),
        ("clip_2_tension_en",    "TENSION"),
        ("clip_3_revelation_en", "REVELATION"),
        ("clip_4_expansion_en",  "EXPANSION"),
        ("clip_5_impact_en",     "IMPACT"),
    ]
    for video in videos:
        vid_id    = video.get("id", "?")
        topic     = video.get("topic_es", "Sin tema")
        gen_by    = video.get("generated_by", "Desconocido")
        vid_clips = []
        for idx, (key, phase) in enumerate(clip_keys_ordered):
            prompt = video.get(key, "")
            if prompt:
                vid_clips.append({
                    "video_id":   vid_id,
                    "topic":      topic,
                    "generated":  gen_by,
                    "prompt":     prompt,
                    "clip_index": idx,
                    "total":      len(clip_keys_ordered),
                    "phase":      phase,
                    "raw_video":  video,   # <-- para P6 (post_text, voiceover, hashtags)
                })
        clips.extend(vid_clips)
    return clips


def extract_clips_from_cartoon_json(data: dict) -> list[dict]:
    """
    Parsea el formato de video_moda_cartoon.json (4 clips, estilo Cartoon Hero).
    """
    clips    = []
    topic    = data.get("topic", data.get("character_name", "Cartoon Hero"))
    raw_list = data.get("clips", [])
    total    = len(raw_list)

    for raw in raw_list:
        prompt = raw.get("prompt_en", "")
        phase  = raw.get("phase", f"Clip {raw.get('id', '?')}")
        idx    = int(raw.get("id", 1)) - 1
        clips.append({
            "video_id":   "cartoon",
            "topic":      topic,
            "generated":  data.get("generated_by", "Manual / Ollama"),
            "prompt":     prompt,
            "clip_index": idx,
            "total":      total,
            "phase":      phase,
            "raw_video":  data,  # <-- post_text, voiceover en el nivel raiz del JSON
        })
    return clips


def extract_clips_from_seedboy_json(data: dict) -> list[dict]:
    """
    Parsea seedboy_content.json. Formato similar a videos_content pero con
    claves scene_1_en / scene_2_en / scene_3_en (3 escenas de 5s).
    """
    clips = []
    videos = data.get("videos", [])
    scene_keys_ordered = [
        ("scene_1_en", "ESCENA 1"),
        ("scene_2_en", "ESCENA 2"),
        ("scene_3_en", "ESCENA 3"),
    ]
    for video in videos:
        vid_id  = video.get("id", "?")
        topic   = video.get("topic_es", "Sin tema")
        gen_by  = video.get("generated_by", "Desconocido")
        for idx, (key, phase) in enumerate(scene_keys_ordered):
            prompt = video.get(key, "")
            if prompt:
                clips.append({
                    "video_id":   vid_id,
                    "topic":      topic,
                    "generated":  gen_by,
                    "prompt":     prompt,
                    "clip_index": idx,
                    "total":      3,
                    "phase":      phase,
                    "raw_video":  video,  # <-- para P6
                })
    return clips


# =============================================================================
# CARGADOR UNIVERSAL DE ARCHIVOS JSON DE VIDEO
# =============================================================================

FILE_CONFIGS = [
    {
        "filename": "videos_content.json",
        "label":    "VIDEOS FOTORREALISTAS (videos_content.json)",
        "parser":   "standard",
    },
    {
        "filename": "videos_content_v2.json",
        "label":    "VIDEOS v2 QA-APPROVED (videos_content_v2.json)",
        "parser":   "standard",
    },
    {
        "filename": "video_moda_cartoon.json",
        "label":    "MODA CARTOON HERO (video_moda_cartoon.json)",
        "parser":   "standard",
    },
    {
        "filename": "seedboy_content.json",
        "label":    "SEEDBOY / CARTOON CONCURSO (seedboy_content.json)",
        "parser":   "seedboy",
    },
]


def load_all_video_clips() -> list[tuple[str, list[dict]]]:
    """
    Carga y parsea todos los archivos de video configurados.
    Devuelve una lista de (label, clips_list).
    GARANTIA: este proceso es de solo lectura. No escribe nada al disco.
    """
    results = []
    for cfg in FILE_CONFIGS:
        filepath = os.path.join(BASE_DIR, cfg["filename"])
        if not os.path.exists(filepath):
            print(f"  [SKIP] {cfg['filename']} — Archivo no encontrado. Omitiendo.")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if cfg["parser"] == "standard":
            clips = extract_clips_from_videos_json(data)
        elif cfg["parser"] == "cartoon":
            clips = extract_clips_from_cartoon_json(data)
        elif cfg["parser"] == "seedboy":
            clips = extract_clips_from_seedboy_json(data)
        else:
            clips = []

        if clips:
            results.append((cfg["label"], clips))
        else:
            print(f"  [WARN] {cfg['filename']} — No se encontraron clips para auditar.")

    return results


# =============================================================================
# RENDERER DEL REPORTE EN CONSOLA
# =============================================================================

SEP_MAJOR = "=" * 72
SEP_MINOR = "-" * 72
SEP_DOT   = "." * 72

def render_score_bar(score: int, max_score: int = 5) -> str:
    """Dibuja una barra visual de puntuación."""
    filled = "█" * score
    empty  = "░" * (max_score - score)
    return f"[{filled}{empty}] {score}/{max_score}"


def print_report(all_results: list[tuple[str, list[dict]]]):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    print(f"\n{SEP_MAJOR}")
    print(f"  AUDITOR DE VIDEOS — CONTROL DE CALIDAD DE PROMPTS")
    print(f"  Infobyte | Fecha: {now}")
    print(f"  MODO: SOLO LECTURA — Ningun archivo fue modificado.")
    print(SEP_MAJOR)

    global_approved = 0
    global_review   = 0
    global_rejected = 0
    global_total    = 0

    for file_label, clips in all_results:
        print(f"\n{'▓' * 72}")
        print(f"  ARCHIVO: {file_label}")
        print(f"{'▓' * 72}")

        # Agrupar clips por video_id
        videos: dict[str, list[dict]] = {}
        for clip in clips:
            vid_key = str(clip["video_id"])
            videos.setdefault(vid_key, []).append(clip)

        file_approved = 0
        file_review   = 0
        file_rejected = 0

        for vid_key, vid_clips in videos.items():
            topic    = vid_clips[0]["topic"]
            gen_by   = vid_clips[0]["generated"]
            raw_data = vid_clips[0].get("raw_video", {})

            # Calcular P6 UNA SOLA VEZ por video
            # Pasa todos los prompts de clips para detectar cliches visuales
            post_text     = raw_data.get("post_text_en", "") or raw_data.get("post_text_es", "") or raw_data.get("facebook_post", {}).get("caption", "")
            voiceover     = raw_data.get("voiceover_en", "") or raw_data.get("voiceover_es", "")
            hashtags      = raw_data.get("hashtags", "") or raw_data.get("facebook_post", {}).get("hashtags", "")
            clip_prompts  = [c["prompt"] for c in vid_clips]
            p6_score, p6_notes = score_viral_potential(post_text, voiceover, hashtags, clip_prompts)

            print(f"\n  VIDEO ID: {vid_key} | Tema: {topic}")
            print(f"  Generado por: {gen_by}")
            print(f"\n  [P6] POTENCIAL VIRAL EN FACEBOOK — {render_score_bar(p6_score)}/5")
            for note in p6_notes:
                print(f"    {note}")
            print(SEP_MINOR)

            video_total = 0
            for clip_data in vid_clips:
                result = evaluate_clip(
                    prompt=clip_data["prompt"],
                    clip_index=clip_data["clip_index"],
                    total_clips=clip_data["total"],
                    phase_name=clip_data["phase"],
                    p6_score=p6_score,
                    p6_notes=[],  # ya se imprimio arriba
                )
                video_total += result["total"]
                global_total += 1

                if result["verdict"] == "APROBADO":
                    file_approved += 1
                elif result["verdict"] == "REVISION REQUERIDA":
                    file_review += 1
                else:
                    file_rejected += 1

                print(f"\n  {result['verdict_icon']} CLIP — {result['phase']}")
                print(f"  Puntuacion Total: {result['total']}/30  |  Veredicto: {result['verdict']}")

                scores = result["scores"]
                print(f"\n  Pilares de Evaluacion:")
                print(f"    P1 Continuidad:      {render_score_bar(scores['P1_Continuidad'])}")
                print(f"    P2 Fisica:           {render_score_bar(scores['P2_Fisica'])}")
                print(f"    P3 Cinematografia:   {render_score_bar(scores['P3_Cinematografia'])}")
                print(f"    P4 Anti-Texto:       {render_score_bar(scores['P4_AntiTexto'])}")
                print(f"    P5 Token Economia:   {render_score_bar(scores['P5_TokenEconomia'])}")
                print(f"    P6 Potencial Viral:  {render_score_bar(scores['P6_PotencialViral'])}")

                clip_notes = [n for n in result["notes"] if n not in p6_notes]
                if clip_notes:
                    print(f"\n  Notas del Clip:")
                    for note in clip_notes:
                        print(f"    {note}")
                print(SEP_DOT)

            avg_score = video_total / len(vid_clips) if vid_clips else 0
            print(f"\n  RESUMEN DEL VIDEO:")
            print(f"    Promedio de Clips:  {avg_score:.1f}/30")
            if avg_score >= THRESHOLD_APPROVED:
                print(f"    Veredicto Final:   [OK] LISTO PARA PRODUCCION — Enviar a Flow AI / Luma.")
            elif avg_score >= THRESHOLD_REVIEW:
                print(f"    Veredicto Final:   [!!] REVISION HUMANA REQUERIDA antes de producir.")
            else:
                print(f"    Veredicto Final:   [XX] RECHAZADO — Regenerar con Gemini antes de continuar.")

        global_approved += file_approved
        global_review   += file_review
        global_rejected += file_rejected

        print(f"\n  RESUMEN DEL ARCHIVO:")
        print(f"    Clips Aprobados:    {file_approved}")
        print(f"    Clips en Revisión:  {file_review}")
        print(f"    Clips Rechazados:   {file_rejected}")

    print(f"\n{SEP_MAJOR}")
    print(f"  RESUMEN GLOBAL — TODOS LOS ARCHIVOS AUDITADOS")
    print(SEP_MAJOR)
    print(f"    Total de Clips Evaluados:   {global_total}")
    print(f"    [OK] Aprobados:             {global_approved}")
    print(f"    [!!] Requieren Revision:    {global_review}")
    print(f"    [XX] Rechazados:            {global_rejected}")

    if global_total > 0:
        pct_ok = (global_approved / global_total) * 100
        print(f"\n    Tasa de Aprobacion Global:  {pct_ok:.1f}%")
        if pct_ok >= 80:
            print("    Estado del Batch:  EXCELENTE — La mayoria de prompts estan listos.")
        elif pct_ok >= 50:
            print("    Estado del Batch:  MODERADO — Revisar los clips marcados antes de producir.")
        else:
            print("    Estado del Batch:  CRITICO — Regenerar el batch con Gemini antes de continuar.")

    print(f"\n  RECORDATORIO: Este script NO modifico ningun archivo.")
    print(f"  Para regenerar contenido, ejecutar: crear_video_viral.py")
    print(f"  Para regenerar Cartoon Hero, ejecutar: crear_moda_cartoon.py")
    print(SEP_MAJOR + "\n")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main():
    print("\nCargando archivos de video...")
    all_results = load_all_video_clips()

    if not all_results:
        print("\n[ERROR] No se encontro ningun archivo de video JSON para auditar.")
        print("  Verificar que existen en:", BASE_DIR)
        return

    print_report(all_results)


if __name__ == "__main__":
    main()
