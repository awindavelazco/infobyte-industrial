"""
=============================================================================
  ACTUALIZADOR DE INTELIGENCIA DE MERCADO — INFOBYTE
  facebook_post_assistant
  Autor: Antigravity AI

  Proposito: Consulta a la IA (via API) sobre las ultimas tendencias de
  Facebook Reels para refrescar la base de conocimiento del agente QA
  (auditor_videos.py). Ejecutar 1 vez al mes.

  Regla de Oro: NO modifica auditor_videos.py directamente. Genera un
  archivo inteligencia_mercado.json que sirve como fuente de verdad
  actualizada. El auditor puede leerlo opcionalmente.

  Uso:
    python actualizar_inteligencia.py
=============================================================================
"""

import json
import urllib.request
import urllib.parse
import time
import os
import sys
from datetime import datetime

# Fix Windows UTF-8 console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "inteligencia_mercado.json")
BACKUP_DIR = os.path.join(BASE_DIR, "obsoleto")

SEP = "=" * 72


# =============================================================================
# POOL DE LLAVES API (reutiliza video_keys de api_keys.json)
# =============================================================================

class IntelligenceEngine:
    def __init__(self):
        self.api_keys = []
        keys_path = os.path.join(BASE_DIR, "api_keys.json")
        if os.path.exists(keys_path):
            with open(keys_path, "r", encoding="utf-8") as f:
                self.api_keys = json.load(f).get("video_keys", [])

        if not self.api_keys:
            print("[ERROR] No se encontraron API keys en api_keys.json.")
            print("        Este script requiere al menos 1 llave activa.")
            sys.exit(1)

        self.current_key_index = 0
        self.model = "gemini-2.5-flash"

    def get_active_key(self):
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        print(f"  [SISTEMA] Rotando a llave API #{self.current_key_index + 1}...")

    def call_gemini(self, prompt):
        """Llama a Gemini con rotacion de llaves. Devuelve texto o None."""
        attempts = 0
        max_attempts = len(self.api_keys)

        while attempts < max_attempts:
            api_key = self.get_active_key()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"

            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048,
                }
            }

            try:
                req = urllib.request.Request(url, method='POST')
                req.add_header('Content-Type', 'application/json')
                response = urllib.request.urlopen(
                    req, json.dumps(payload).encode('utf-8'), timeout=60
                )
                result = json.loads(response.read().decode('utf-8'))
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text

            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"  [429] Llave #{self.current_key_index + 1} agotada. Rotando...")
                    self.rotate_key()
                    attempts += 1
                    time.sleep(2)
                else:
                    print(f"  [HTTP ERROR {e.code}] {e.reason}")
                    return None

            except Exception as e:
                print(f"  [ERROR] {e}")
                return None

        print("  [CRITICO] Todas las llaves agotadas. Intentar maniana.")
        return None

    def extract_json(self, text):
        """Extrae JSON de una respuesta de texto."""
        if not text:
            return None
        import re
        # Intentar parsear directamente
        try:
            return json.loads(text)
        except:
            pass
        # Buscar bloques JSON en la respuesta
        matches = re.findall(r'\{.*\}', text, re.DOTALL)
        for match in sorted(matches, key=len, reverse=True):
            try:
                return json.loads(match)
            except:
                continue
        # Buscar arrays JSON
        matches = re.findall(r'\[.*\]', text, re.DOTALL)
        for match in sorted(matches, key=len, reverse=True):
            try:
                return json.loads(match)
            except:
                continue
        return None


# =============================================================================
# PREGUNTAS DE INTELIGENCIA (Las 5 consultas mensuales)
# =============================================================================

INTELLIGENCE_QUERIES = [
    {
        "id": "hooks_retention",
        "label": "Hooks y Retencion",
        "prompt": """You are a Facebook Reels analytics expert. Based on current trends (mid-2026):

1. What are the TOP 10 text hook formulas that stop the scroll on Facebook Reels RIGHT NOW?
   (e.g., "Stop doing X", "The #1 mistake...", etc.)
2. What visual hooks (first 1-3 seconds) have the highest retention rate?
3. Any NEW hook patterns that emerged in the last 3 months?

Return ONLY a valid JSON object with this exact structure:
{
  "text_hooks": ["hook1", "hook2", ...],
  "visual_hooks": ["description1", "description2", ...],
  "new_patterns": ["pattern1", "pattern2", ...]
}"""
    },
    {
        "id": "viral_science",
        "label": "Ciencia Viral",
        "prompt": """You are a viral content strategist specializing in science/health content on Facebook.
Based on current trends (mid-2026):

1. What scientific topics are getting the MOST engagement on Facebook Reels right now?
2. What keywords or phrases trigger the most shares in science content?
3. What are the top 5 "social currency" triggers (things that make people look smart when sharing)?

Return ONLY a valid JSON object:
{
  "trending_science_topics": ["topic1", "topic2", ...],
  "high_share_keywords": ["keyword1", "keyword2", ...],
  "social_currency_triggers": ["trigger1", "trigger2", ...]
}"""
    },
    {
        "id": "visual_saturation",
        "label": "Saturacion Visual",
        "prompt": """You are a visual content analyst for social media. Based on current trends (mid-2026):

1. What visual styles/aesthetics are NOW considered OVERUSED or "burned" on Facebook/Instagram?
   (images the algorithm or users skip automatically)
2. What NEW visual aesthetics are performing well and feel FRESH?
3. What AI-generated visual styles are currently being penalized or ignored by users?

Return ONLY a valid JSON object:
{
  "burned_visuals": ["description1", "description2", ...],
  "fresh_visuals": ["description1", "description2", ...],
  "ai_penalized_styles": ["description1", "description2", ...]
}"""
    },
    {
        "id": "cta_engagement",
        "label": "CTAs y Engagement",
        "prompt": """You are a Meta/Facebook engagement specialist. Based on current platform rules (mid-2026):

1. What CTAs (Call-to-Action) are currently APPROVED by Meta and drive real engagement?
2. What CTAs are NOW PENALIZED or flagged as engagement bait by Meta's algorithm?
3. What comment-driving questions work best for science/health content?

Return ONLY a valid JSON object:
{
  "approved_ctas": ["cta1", "cta2", ...],
  "penalized_ctas": ["cta1", "cta2", ...],
  "best_comment_questions": ["question1", "question2", ...]
}"""
    },
    {
        "id": "cinematography_trends",
        "label": "Tendencias Cinematograficas IA",
        "prompt": """You are an AI video production expert. Based on current trends (mid-2026):

1. What camera movements and shot types are trending in AI-generated video content?
2. What NEW prompting techniques have emerged for AI video generators?
3. What common mistakes should be avoided when prompting AI video tools?
4. What visual styles or aesthetics are currently producing the BEST results in AI video?

Return ONLY a valid JSON object:
{
  "trending_camera_techniques": ["technique1", "technique2", ...],
  "new_prompting_techniques": ["technique1", "technique2", ...],
  "common_mistakes": ["mistake1", "mistake2", ...],
  "best_visual_styles": ["style1", "style2", ...]
}"""
    },
]


# =============================================================================
# EJECUCION PRINCIPAL
# =============================================================================

def main():
    print(f"\n{SEP}")
    print(f"  ACTUALIZADOR DE INTELIGENCIA DE MERCADO — INFOBYTE")
    print(f"  Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Frecuencia recomendada: 1 vez al mes")
    print(SEP)

    engine = IntelligenceEngine()

    # Backup del archivo anterior si existe
    if os.path.exists(OUTPUT_FILE):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        backup_name = f"inteligencia_mercado_backup_{timestamp}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            backup_data = f.read()
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(backup_data)
        print(f"\n  [OK] Backup del archivo anterior guardado en: {backup_name}")

    intelligence_report = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "version": "auto",
        "queries_completed": 0,
        "queries_failed": 0,
        "data": {}
    }

    total_queries = len(INTELLIGENCE_QUERIES)

    for i, query in enumerate(INTELLIGENCE_QUERIES, 1):
        print(f"\n  [{i}/{total_queries}] Consultando: {query['label']}...")

        response_text = engine.call_gemini(query["prompt"])

        if response_text:
            parsed = engine.extract_json(response_text)
            if parsed:
                intelligence_report["data"][query["id"]] = parsed
                intelligence_report["queries_completed"] += 1
                print(f"  [OK] {query['label']} — Datos recibidos y parseados.")
            else:
                intelligence_report["data"][query["id"]] = {"raw_response": response_text}
                intelligence_report["queries_failed"] += 1
                print(f"  [WARN] {query['label']} — Respuesta recibida pero no es JSON valido. Guardada en crudo.")
        else:
            intelligence_report["queries_failed"] += 1
            print(f"  [FAIL] {query['label']} — Sin respuesta. Llaves agotadas o error de red.")

        # Pausa entre llamadas (regla permanente: ERROR #005)
        if i < total_queries:
            print("  Esperando 3s antes de la siguiente consulta...")
            time.sleep(3)

    # Guardar el reporte
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(intelligence_report, f, ensure_ascii=False, indent=2)

    # Resumen final
    print(f"\n{SEP}")
    print(f"  RESUMEN DE ACTUALIZACION")
    print(SEP)
    print(f"    Consultas exitosas:  {intelligence_report['queries_completed']}/{total_queries}")
    print(f"    Consultas fallidas:  {intelligence_report['queries_failed']}/{total_queries}")
    print(f"    Archivo generado:    inteligencia_mercado.json")

    if intelligence_report["queries_completed"] == total_queries:
        print(f"\n  [OK] ACTUALIZACION COMPLETA.")
        print(f"       La base de conocimiento del auditor esta lista.")
    elif intelligence_report["queries_completed"] > 0:
        print(f"\n  [WARN] ACTUALIZACION PARCIAL.")
        print(f"         Algunas consultas fallaron. Reintentar maniana cuando se reinicien las llaves.")
    else:
        print(f"\n  [FAIL] ACTUALIZACION FALLIDA.")
        print(f"         Ninguna consulta fue exitosa. Verificar estado de las API keys.")

    print(f"\n  PROXIMO PASO: Revisar inteligencia_mercado.json y decidir")
    print(f"  si actualizar las listas del auditor (auditor_videos.py).")
    print(f"  Este script NO modifica el auditor automaticamente.")
    print(f"{SEP}\n")


if __name__ == "__main__":
    main()
