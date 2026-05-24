"""
=============================================================================
  PIPELINE DE PRODUCCION DE VIDEOS — INFOBYTE
  Ejecuta el generador elegido y lanza el auditor QA automaticamente.

  REGLA DE ORO: No modifica ningun script existente.
  Solo orquesta: genera -> audita -> reporta -> decide.

  Uso:
    python pipeline_videos.py viral       # genera videos_content.json + audita
    python pipeline_videos.py cartoon     # genera video_moda_cartoon.json + audita
    python pipeline_videos.py solo_auditar  # solo corre el auditor (sin generar)
=============================================================================
"""

import subprocess
import sys
import os
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON   = sys.executable  # usa el mismo Python que lanzo este script

# =============================================================================
# MAPA DE GENERADORES
# =============================================================================

GENERADORES = {
    "viral":   {
        "script":  "crear_video_viral.py",
        "label":   "Videos Virales Fotorrealistas (crear_video_viral.py)",
        "output":  "videos_content.json",
    },
    "cartoon": {
        "script":  "crear_moda_cartoon.py",
        "label":   "Cartoon Hero — Lumina (crear_moda_cartoon.py)",
        "output":  "video_moda_cartoon.json",
    },
}

AUDITOR_SCRIPT = "auditor_videos.py"

SEP = "=" * 72

# =============================================================================
# EJECUCION
# =============================================================================

def run_step(label: str, script_path: str) -> int:
    """Ejecuta un script Python y retorna su codigo de salida."""
    print(f"\n{SEP}")
    print(f"  PASO: {label}")
    print(f"  Script: {os.path.basename(script_path)}")
    print(f"  Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print(SEP)

    result = subprocess.run(
        [PYTHON, script_path],
        cwd=BASE_DIR,
        # Hereda stdout/stderr para que se vea en tiempo real
    )

    print(f"\n  Fin: {datetime.now().strftime('%H:%M:%S')} | Codigo de salida: {result.returncode}")
    return result.returncode


def check_output_exists(filename: str) -> bool:
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        print(f"\n  [WARN] El archivo de salida '{filename}' no fue creado.")
        return False
    size = os.path.getsize(path)
    print(f"\n  [OK] Archivo '{filename}' generado ({size:,} bytes).")
    return True


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "help"

    print(f"\n{SEP}")
    print(f"  PIPELINE DE PRODUCCION DE VIDEOS — INFOBYTE")
    print(f"  Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Modo: {mode.upper()}")
    print(SEP)

    # ── MODO: solo auditar (sin generar) ─────────────────────────────────────
    if mode == "solo_auditar":
        print("\n  Ejecutando solo el Auditor de Calidad (sin generacion)...\n")
        auditor_path = os.path.join(BASE_DIR, AUDITOR_SCRIPT)
        run_step("Auditoria de Calidad de Prompts", auditor_path)
        return

    # ── MODO: generar + auditar ───────────────────────────────────────────────
    if mode not in GENERADORES:
        print(f"\n  [ERROR] Modo '{mode}' no reconocido.")
        print("  Modos disponibles:")
        print("    python pipeline_videos.py viral")
        print("    python pipeline_videos.py cartoon")
        print("    python pipeline_videos.py solo_auditar")
        sys.exit(1)

    cfg = GENERADORES[mode]
    gen_script = os.path.join(BASE_DIR, cfg["script"])
    auditor_path = os.path.join(BASE_DIR, AUDITOR_SCRIPT)

    # ── PASO 1: Verificar que el generador existe ────────────────────────────
    if not os.path.exists(gen_script):
        print(f"\n  [ERROR] Generador no encontrado: {gen_script}")
        sys.exit(1)

    # ── PASO 2: Ejecutar el Generador ────────────────────────────────────────
    gen_exit = run_step(f"Generacion — {cfg['label']}", gen_script)

    if gen_exit != 0:
        print(f"\n  [ATENCION] El generador termino con codigo {gen_exit}.")
        print("  Puede haber errores de API. Revisando si hay output para auditar...")

    output_ok = check_output_exists(cfg["output"])

    # ── PASO 3: Auditoría Automática (siempre corre, aunque haya error) ──────
    print(f"\n{SEP}")
    print("  AUDITORIA AUTOMATICA DE CALIDAD")
    print("  (El auditor NUNCA modifica archivos. Solo lee y reporta.)")
    print(SEP)

    if not os.path.exists(auditor_path):
        print(f"\n  [ERROR] Auditor no encontrado: {auditor_path}")
        print("  Ejecutar primero: el archivo auditor_videos.py debe existir.")
        sys.exit(1)

    run_step("Auditoria de Calidad de Prompts", auditor_path)

    # ── PASO 4: Resumen del Pipeline ─────────────────────────────────────────
    print(f"\n{SEP}")
    print("  RESUMEN DEL PIPELINE")
    print(SEP)
    print(f"  Generador:   {cfg['script']}")
    print(f"  Output:      {cfg['output']} ({'creado' if output_ok else 'NO creado'})")
    print(f"  Auditoria:   Completada (ver reporte arriba)")
    print()
    print("  PROXIMOS PASOS SEGUN EL VEREDICTO DEL AUDITOR:")
    print("  [OK] APROBADO    -> Copiar prompts a Flow AI / Luma / Kling.")
    print("  [!!] REVISION    -> Revisar las notas del auditor y corregir manualmente.")
    print("  [XX] RECHAZADO   -> Volver a ejecutar el generador con Gemini.")
    print()
    print("  Para regenerar: python pipeline_videos.py " + mode)
    print("  Para solo auditar: python pipeline_videos.py solo_auditar")
    print(SEP + "\n")


if __name__ == "__main__":
    main()
