# BITACORA DE ERRORES Y ESTADO DEL SISTEMA — INFOBYTE INDUSTRIAL
# LECTURA OBLIGATORIA AL INICIO DE CADA SESION DE DESARROLLO
# Ultima actualizacion: 2026-05-16

---
## ESTADO ACTUAL DEL SISTEMA (RESUMEN PARA NUEVO CHAT)

### 🔴 ESTADO DE API KEYS (al 2026-05-13 ~8pm EST)
- **news_keys:** 6 llaves — OK (Reiniciadas)
- **video_keys:** 6 llaves — OK (Reiniciadas)
- **Acción hoy:** Se priorizó el uso de **Ollama + Claude (Local)** para evitar el agotamiento de cuotas de Antigravity.
- **Nota:** Ollama + Claude local presenta lentitud extrema en procesamiento de prompts complejos.

### 📁 SCRIPTS ACTIVOS Y SU FUNCION
| Script | Funcion | Lote | Estado |
|---|---|---|---|
| `engine_agentes.py` | Motor principal de noticias (posts de ciencia/salud) | Variable | OK |
| `crear_frase_viral.py` | Posts de frases/reflexiones (Soul Notes / Infobyte) | 7/semana | MODIFICADO HOY |
| `crear_video_viral.py` | Guiones de video 4x8s para Flow AI (Reels 32s) | 5/semana | MODIFICADO HOY |
| `crear_quiz_viral.py` | Quizzes interactivos | 2/semana | Sin cambios |
| `actualizar_inteligencia.py` | Refresco mensual de tendencias Facebook para QA | Mensual | NUEVO |
| `crear_video_seedboy.py` | Guiones para concurso Cartoon Hero x Seedboy | 2 por ejecucion | Sin cambios |
| `generar_nueva_semana.py` | Generador semanal completo (noticias) | Semanal | Sin cambios |

### 📊 ARCHIVOS DE DATOS Y SUS CLAVES JSON
| Archivo | Clave raiz esperada | Lo lee |
|---|---|---|
| `posts_content.json` | "posts" | script.js (Dashboard) |
| `quizzes_content.json` | "quizzes" | script.js (Dashboard) |
| `frases_content.json` | "phrases" | script.js (Dashboard) |
| `videos_content.json` | "videos" | Manual (copiar prompts a Flow AI) |
| `seedboy_content.json` | "videos" | Manual (copiar prompts a Luma/Kling) |

### 📅 CALENDARIO DE PUBLICACION APROBADO (Horario EST para audiencia USA)
| Dia | 8:00 AM | 12:30 PM | 7:00 PM |
|---|---|---|---|
| Lunes | VIDEO | — | QUIZ |
| Martes | VIDEO | Soul Notes | — |
| Miercoles | VIDEO | — | — |
| Jueves | Post Ciencia | — | QUIZ |
| Viernes | VIDEO | — | — |
| Sabado | VIDEO | — | — |
| Domingo | — | Soul Notes | Post Curiosidad |

### ⚙️ CAMBIOS REALIZADOS EN ESTA SESIÓN (2026-05-14)
1. **Ollama + Claude**: Configuración exitosa del motor local para evitar el agotamiento de Antigravity.
2. **crear_moda_cartoon.py**: Nuevo script de moda futurista siguiendo la técnica Cartoon Hero (4x8s).
3. **video_moda_cartoon.json**: Generado el primer guion de la serie "Lumina" (Diseñadora de Luz).
4. **Dashboard Filter**: Implementado filtro en `script.js` para ocultar contenido de Ollama (Fix #4).
5. **BITÁCORA**: Actualización de progreso y tareas pendientes.

### ⚠️ FIXES PENDIENTES DE APROBACION (NO ejecutar sin OK del usuario)
1. Reducir prompt de `crear_video_viral.py` a max 300 tokens.
2. Cambiar logica de retry: rotar llave inmediatamente al primer 429.
3. Si todas las llaves fallan → detener proceso, NO caer a Ollama en produccion.
4. **COMPLETADO:** Agregar validacion: si generated_by == "Ollama", excluir del dashboard automaticamente.

### 🚫 CONTENIDO NO PUBLICABLE (generado hoy por Ollama)
- `frases_content.json` actual: **NO PUBLICAR** — posts incompletos y estadisticas falsas.
- `videos_content.json` actual: **USAR CON PRECAUCION** — revisar datos antes de publicar.
- Regenerar ambos maniana cuando se reinicien las llaves con Gemini.

### ✅ LO QUE FUNCIONA CORRECTAMENTE
- Rotacion de llaves API (cuando hay cuota disponible)
- Fallback a Ollama (tecnicamente funciona, pero calidad no es apta para produccion)
- Dashboard en GitHub Pages (rama: main)
- Estructura JSON validada antes de escribir al disco (ERROR #001 corregido)
- Backup automatico de scripts antes de modificaciones

---

## 🚀 GUÍA DE ACCESO RÁPIDO AL DASHBOARD (LOCAL)
Si estás perdida y no sabes cómo ver el proyecto:

### Opción A: La más fácil (Archivo Automático)
1. Ve a la carpeta `facebook_post_assistant`.
2. Busca el archivo llamado `iniciar_dashboard.bat`.
3. Haz doble clic en él. Se abrirá una ventana negra y automáticamente tu navegador en `http://localhost:8000`.
4. **No cierres la ventana negra** mientras estés usando el dashboard.

### Opción B: Manual (Desde la Terminal)
1. Abre una terminal en la carpeta del proyecto.
2. Escribe y pulsa Enter: `python -m http.server 8000`
3. Abre tu navegador y ve a: `http://localhost:8000`

---

## DIRECTIVA PRIMA — DOCUMENTACION EN TIEMPO REAL
Esta regla esta por encima de todas las demas:

1. CADA VEZ que ocurra un error durante el desarrollo, sin importar que tan pequenio
   sea, debe documentarse en esta bitacora INMEDIATAMENTE, antes de continuar con
   cualquier otra tarea.

2. No se permite terminar una sesion de trabajo sin actualizar esta bitacora si
   hubo algun error, comportamiento inesperado o decision de diseno importante.

3. El formato minimo obligatorio para cada entrada es:
   - Numero secuencial (ERROR #XXX)
   - Fecha
   - Archivo culpable
   - Descripcion del error
   - Sintoma visible para el usuario
   - Fix aplicado
   - Regla permanente para no repetirlo

4. Despues de documentar, hacer commit con mensaje:
   "bitacora: add ERROR #XXX - descripcion breve"

5. Esta bitacora es el PRIMER archivo que debe leer la IA al iniciar cualquier
   sesion de trabajo en este proyecto. Sin excepcion.

RAZON: La IA no tiene memoria entre sesiones. Esta bitacora ES su memoria.
Si no se documenta aqui, el error se repetira.

---

## REGLA GENERAL
Antes de tocar cualquier archivo de este proyecto, leer esta bitacora completa.
Cada error aqui documentado ya costo tiempo y cuota de API. No repetirlo.

---

## ERROR #001 — ESCRITURA DE JSON SIN VALIDAR SCHEMA
**Fecha:** 2026-05-04
**Archivo culpable:** generar_test_10.py (tambien aplica a generar_nueva_semana.py)
**Descripcion:** El script abria el archivo con modo 'w' (borrando el contenido anterior)
y luego llamaba a Gemini. Si Gemini devolvia un JSON con claves diferentes a las esperadas
(ej: 'quiz' en vez de 'quizzes'), el archivo quedaba vacio o con estructura incorrecta.
El Dashboard no mostraba nada en las pestanas Quizzes y Spirit.

**Sintoma visible:** Pestanas de Quizzes y Spirit en blanco. Archivo con 15 bytes: {"quizzes": []}

**FIX APLICADO:**
Antes de escribir al disco, SIEMPRE validar:
```python
if data and isinstance(data.get('quizzes'), list) and len(data['quizzes']) > 0:
    # escribir al disco
else:
    # NO sobreescribir. Conservar archivo anterior. Loguear el error.
```

**REGLA PERMANENTE:**
- NUNCA abrir un archivo con 'w' antes de confirmar que los datos nuevos son validos.
- SIEMPRE conservar el archivo anterior si el nuevo tiene estructura incorrecta.

---

## ERROR #002 — EMOJIS EN PROMPTS DE IA
**Fecha:** Multiple sesiones
**Archivo culpable:** engine_agentes.py (prompts del Copywriter y Scout)
**Descripcion:** Se incluyeron emojis directamente dentro de los prompts que se mandan
a Gemini como instrucciones de formato o estructura. Algunos editores de texto,
parsers JSON y sistemas de logging no interpretan bien los emojis y generan
caracteres invalidos, errores de encoding o respuestas mal formateadas.

**Sintoma visible:** Respuestas de Gemini con caracteres extranios, JSON invalido,
o instrucciones ignoradas por el modelo.

**REGLA PERMANENTE:**
- PROHIBIDO usar emojis dentro de las instrucciones/prompts que se mandan a Gemini.
- Los emojis SOLO se permiten en el CONTENIDO GENERADO (postEN, postES), nunca en
  las instrucciones de formato o schema que le decimos al modelo que siga.
- Correcto: "Generate a JSON with keys: title, body, hashtags"
- Incorrecto: "Generate a JSON like: {title: ..." with emojis in the structure"

---

## ERROR #003 — CSS TOAST SIN ESTADO OCULTO POR DEFECTO
**Fecha:** 2026-05-04
**Archivo culpable:** style.css
**Descripcion:** El elemento .toast no tenia definido opacity:0 ni transform de
ocultamiento en su estado base. Solo tenia el estado .toast.active definido.
Esto causaba que el texto "Mensaje de sistema" apareciera visible en la pagina
al cargar, confundiendo al usuario.

**FIX APLICADO:**
```css
.toast {
    position: fixed;
    opacity: 0;
    transform: translate(-50%, 100px);
    pointer-events: none;
    transition: all 0.3s ease;
}
.toast.active {
    opacity: 1;
    transform: translate(-50%, 0);
}
```

**REGLA PERMANENTE:**
- Todo elemento de notificacion/toast/popup debe tener su estado OCULTO definido
  explicitamente en CSS, no solo el estado visible.

---

## ERROR #004 — SINTAXIS && EN POWERSHELL
**Fecha:** 2026-05-04
**Sistema:** Windows PowerShell
**Descripcion:** Se uso el operador && para encadenar comandos git (bash syntax).
PowerShell no reconoce && como separador de instrucciones valido.

**FIX APLICADO:** Usar ; en PowerShell para encadenar comandos:
```powershell
git add .; git commit -m "mensaje"; git push origin gh-pages
```

**REGLA PERMANENTE:**
- En este proyecto el shell es PowerShell (Windows), NO bash.
- Separador de comandos: ; (punto y coma), NO &&

---

## ERROR #005 — GENERACION SIN PAUSA ENTRE LLAMADAS A API
**Fecha:** Multiple sesiones
**Descripcion:** Llamadas consecutivas a Gemini sin pausa generan error 429
(RESOURCE_EXHAUSTED). Esto agota la cuota de todas las llaves API rapidamente.

**REGLA PERMANENTE:**
- SIEMPRE incluir time.sleep(2) entre llamadas a Gemini en loops.
- El pool de llaves tiene 6 llaves. Rotar en orden, nunca al azar.
- Si todas las llaves fallan con 429, detener el proceso. NO reintentar en loop infinito.

---

## ARQUITECTURA DE ARCHIVOS CRITICOS
| Archivo               | Clave JSON esperada | Quien la lee     |
|-----------------------|---------------------|------------------|
| posts_content.json    | "posts"             | script.js        |
| quizzes_content.json  | "quizzes"           | script.js        |
| frases_content.json   | "phrases"           | script.js        |

NOTA: Si la clave raiz no coincide exactamente con lo de arriba, el Dashboard
mostrara vacio. Gemini a veces devuelve "quiz", "phrase", "data" — SIEMPRE validar.

---

## COMO ACTUALIZAR ESTA BITACORA
Cuando se descubra un error nuevo:
1. Agregar entrada con numero secuencial (ERROR #006, etc.)
2. Documentar: Fecha, Archivo culpable, Descripcion, Sintoma, Fix, Regla permanente.
3. Hacer commit con mensaje: "bitacora: add ERROR #XXX - descripcion breve"

---

## ERROR #006 — COMMIT PARCIAL DEJA ARCHIVOS JSON FUERA DE GITHUB PAGES
**Fecha:** 2026-05-04
**Causa:** Se hicieron commits individuales (solo style.css, solo BITACORA.md) sin
incluir los archivos de datos (quizzes_content.json, frases_content.json).
GitHub Pages siempre sirve el ULTIMO commit. Si los JSON no estan en ese commit,
la web los ve vacios aunque existan localmente.

**Sintoma visible:** Quizzes y Spirit en blanco en la web. Localmente los archivos
tienen contenido correcto.

**Fix aplicado:** git add con todos los archivos de datos incluidos antes de push.

**REGLA PERMANENTE:**
- Antes de cualquier git push, verificar con "git status" que los 3 archivos de
  datos esten incluidos si hubo cambios en ellos:
    * quizzes_content.json
    * frases_content.json
    * posts_content.json
- NUNCA hacer push de solo CSS o solo scripts sin verificar el estado de los JSON.
- Comando de verificacion obligatorio antes de push:
  git diff --stat HEAD (debe mostrar los archivos de datos si cambiaron)

---

## ARQUITECTURA DE ARCHIVOS CRITICOS
| Archivo               | Clave JSON esperada | Quien la lee     |
|-----------------------|---------------------|------------------|
| posts_content.json    | "posts"             | script.js        |
| quizzes_content.json  | "quizzes"           | script.js        |
| frases_content.json   | "phrases"           | script.js        |

NOTA: Si la clave raiz no coincide exactamente con lo de arriba, el Dashboard
mostrara vacio. Gemini a veces devuelve "quiz", "phrase", "data" — SIEMPRE validar.

---

## COMO ACTUALIZAR ESTA BITACORA
Cuando se descubra un error nuevo:
1. Agregar entrada con numero secuencial (ERROR #006, etc.)
2. Documentar: Fecha, Archivo culpable, Descripcion, Sintoma, Fix, Regla permanente.
3. Hacer commit con mensaje: "bitacora: add ERROR #XXX - descripcion breve"

---

## ERROR #007 — PUSH A RAMA INCORRECTA (gh-pages vs main)
**Fecha:** 2026-05-05
**Causa:** Todos los commits con datos se hicieron a la rama "gh-pages" pero
GitHub Pages esta configurado para servir desde la rama "main". La web leia
siempre el "main" desactualizado con archivos vacios.

**Sintoma visible:** Quizzes y Spirit vacios en la web aunque git log mostraba
los datos en el historial de gh-pages.

**Verificacion que confirma el problema:**
  git show origin/main:quizzes_content.json  → devuelve {"quizzes": []}
  git show origin/gh-pages:quizzes_content.json → devuelve 10 quizzes

**Fix aplicado:**
  git push origin gh-pages:main
  (Sincroniza gh-pages hacia main de un solo comando)

**REGLA PERMANENTE:**
- SIEMPRE verificar que rama sirve GitHub Pages ANTES de hacer push.
- Comando de verificacion: leer github.com/[repo]/settings/pages
- En este proyecto GitHub Pages sirve desde: RAMA "main"
- El comando correcto de push es siempre: git push origin main
- Si se esta en rama gh-pages local, usar: git push origin gh-pages:main

---

## ERROR #008 — OLLAMA LOCAL NO APTO PARA CONTENIDO DE PRODUCCION
**Fecha:** 2026-05-09
**Archivo culpable:** crear_frase_viral.py, crear_video_viral.py (fallback a Ollama)
**Descripcion:** Cuando Gemini se agota (429), el sistema hace fallback a Ollama (Llama3 local).
Se detecto que Ollama genera contenido defectuoso que NO es publicable:
  - postES aparece como "Resumen no disponible." en 3 de 7 posts (posts #4, #5, #6).
  - postEN incompleto: termina con "Action Plan:" sin contenido (posts #4, #5).
  - Repite el mismo tema (memoria cerebral) en los 7 posts ignorando el pool de temas.
  - Los prompts de imagen siguen siendo paisajes abstractos, ignorando la instruccion de personas reales.
  - Inventa estadisticas falsas sin fuente: "stress erases 50% of neurons", "75% of people age faster".
  - Copia literalmente los ejemplos del prompt como si fueran contenido real.

**Sintoma visible:** frases_content.json con posts vacios e inutilizables. Videos con datos falsos
que si se publican daniarian la credibilidad de la pagina.

**FIX APLICADO:** Ninguno aun. Contenido de este lote NO publicado.

**REGLA PERMANENTE:**
- Ollama (local) es SOLO para emergencias tecnicas de prueba. NUNCA para produccion.
- Agregar validacion post-generacion: si generated_by == "Ollama (Local)", marcar el item
  como "requires_review: true" y excluirlo del dashboard hasta revision manual.
- Validacion minima antes de aceptar cualquier item:
  * postES != "Resumen no disponible."
  * len(postEN) > 200 caracteres
  * postEN no termina con "Action Plan:" sin contenido
- Si Gemini falla y Ollama genera basura, es MEJOR no generar nada que publicar contenido falso.

---

## ERROR #009 — PROMPT SOBRECARGADO AGOTO 12 LLAVES EN UNA SOLA SESION
**Fecha:** 2026-05-09
**Archivo culpable:** crear_video_viral.py (nuevo prompt de continuidad 4x8s)
**Descripcion:** Se rediseno el prompt de videos para incluir tecnica de Continuidad 4x8s para Flow AI.
El nuevo prompt_instruction paso de ~200 tokens a ~650 tokens. Combinado con:
  - 5 videos por lote (antes eran 3)
  - Sistema de reintentos que espera antes de rotar (agota tokens en cada intento)
  - Ejecucion de crear_video_viral.py + crear_frase_viral.py en la misma sesion
  Resultado: las 12 llaves (6 NEWS + 6 VIDEO) se agotaron en una sola sesion de trabajo.

**Auditoria confirmada:** 0/12 llaves activas. Todas con error 429 RESOURCE_EXHAUSTED.

**Sintoma visible:** Todos los scripts caen a Ollama local, generando contenido defectuoso (ver ERROR #008).

**FIX PENDIENTE DE APROBACION:**
  1. Reducir el prompt de videos a maximo 300 tokens sin perder estructura de continuidad.
  2. Cambiar logica de retry: al primer 429, rotar llave INMEDIATAMENTE (no esperar ni reintentar).
  3. Si todas las llaves fallan → detener proceso y mostrar mensaje claro. NO caer a Ollama en produccion.
  4. Separar horario de ejecucion: noticias/frases en la maniana, videos en la tarde.
  5. Nunca ejecutar dos scripts pesados en la misma sesion del mismo dia.

**REGLA PERMANENTE:**
- El tamano maximo de un prompt_instruction es 300 tokens (~220 palabras).
- Cada sesion de trabajo puede ejecutar SOLO UN script pesado por dia (o frases O videos, no ambos).
- Antes de ejecutar cualquier script, verificar el estado de las llaves con el script de auditoria.
- El script de auditoria de llaves se debe ejecutar PRIMERO, antes que cualquier generacion.

---

## 📅 PENDIENTE PARA MAÑANA (2026-05-14)
1. **Prompts de Imagen Base**: Crear los prompts para Midjourney de la diseñadora "Lumina" (Pelo de fibra óptica, estilo Pixar).
2. **Generación en Flow AI**: Usar el guion de `video_moda_cartoon.json` para crear los 4 clips.
3. **Debug Ollama**: Probar el modelo `llama3.1:8b` o `gemma:2b` si Claude local sigue siendo demasiado lento para el script automático.

---

## 🆕 SESIÓN 2026-05-17 — EVOLUCIÓN HACIA EL "MONTAJE DINÁMICO" Y QA
    
### 🚀 CAMBIOS IMPLEMENTADOS (Standard: CERO ABURRIMIENTO para Facebook)

1. **Rediseño de la Estructura de Video (Viral)**:
   - Migración de 4 clips de 8s (32s) $\rightarrow$ **5 clips de 6s (30s)**.
   - Eliminación de la "Continuidad Estática" (`Continuing from previous clip`).
   - Implementación de **"Dynamic Character Jump"**: El personaje es la constante, pero el entorno, la ropa y la luz EVOLUCIONAN en cada clip para representar un viaje de transformación.
   - **Nueva Secuencia de Ángulos**: Hook (Macro) $\rightarrow$ Tension (Medium) $\rightarrow$ Revelation (Insert) $\rightarrow$ Expansion (Wide) $\rightarrow$ Impact (Slow-mo).

2. **Upgrade de Inteligencia Visual**:
    - Implementación de la **"Técnica del Ancla" (Character Anchor)**: Descripción física detallada constante, pero con cambios dinámicos de outfit y escenario.
    - Priorización de modelos **Gemini 1.5 Pro** para la generación de prompts artísticos y psicológicos.
    - Inyección de terminología de alta gama (Arri Alexa, anamorphic flares, volumetric fog) basada en el curso Cartoon Hero.

3. **Actualización de Interfaz (Dashboard)**:
    *   `script.js` actualizado para soportar la visualización de 5 clips.
    *   Ajuste de etiquetas de tiempo (0-6s, 6-12s, etc.) y optimización de la cuadrícula de prompts.

4. **Sistema de Control de Calidad (QA Auditor)**:
    - Implementación de la lógica de **6 Pilares de Evaluación** (Continuidad, Física, Cinematografía, Anti-Texto, Tokens, Potencial Viral).
    - Definición de umbrales de veredicto: APROBADO ($\ge 23$), REVISIÓN ($16-22$), RECHAZADO ($< 16$).
    - Incorporación de la base de conocimiento de tendencias de Facebook 2026.

### 📁 ARCHIVOS MODIFICADOS
- `crear_video_viral.py`: Nueva lógica de montaje dinámico y 5 clips.
- `engine_agentes.py`: Prompt visual psicológico y prioridad modelo Pro.
- `script.js`: Soporte para 5 clips y tiempos de 6s.
- `auditor_videos.py`: Sincronización con el nuevo formato de montaje dinámico.
- `videos_content.json`: Ahora almacena el formato `5x6s_dynamic_montage`.

### ⚠️ NOTA DE SEGURIDAD
Se creó la carpeta `/obsoleto` con los backups de los scripts antes de la migración al estándar de 5 clips.

---

### 🧠 BASE DE CONOCIMIENTO DEL AGENTE QA (Resumen)
- **P1 Continuidad**: Validada ahora por consistencia de rasgos físicos (Ancla) y arco emocional, no por frases de enlace.
- **P4 Anti-Texto**: Uso obligatorio del sufijo `[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]`.
- **P6 Viralidad**: Hooks de curiosidad, respaldo científico, emoción de transformación y CTAs Meta-aprobados.

---

### 📅 PENDIENTES DE ESTA SESIÓN (2026-05-17)
1. **Corregir `video_moda_cartoon.json`**: Añadir anti-texto a los 4 clips y mejorar el P6 viral.
2. **Corregir `crear_moda_cartoon.py`**: Integrar las correcciones en el template del prompt.
3. **Crear `actualizar_inteligencia.py`**: Script mensual para refrescar tendencias de Facebook.
**COMPLETADO:** Sincronización Total: Ejecutar `auditor_videos.py` automáticamente tras cada generación de video.

---
---

## 🆕 SESIÓN 2026-05-18 — SEGMENTACIÓN DE VOZ Y CIERRE de QA

### 🚀 CAMBIOS IMPLEMENTADOS
1. **Segmentación de Voiceover (Timestamps)**: 
   - Implementado sistema de `voiceover_segments` en `videos_content_v2.json`.
   - Ahora la voz en off está dividida exactamente por clips (0-6s, 6-12s, etc.), facilitando el montaje en Flow AI.
   - Actualizado `crear_video_viral.py` para persistir este formato automáticamente.
2. **Verificación de Automatización QA**:
   - Confirmado que `auditor_videos.py` se ejecuta automáticamente al final de `crear_video_viral.py`.

---

FIN DE BITACORA


### ✅ RESUMEN DE LO CONSTRUIDO

Se diseñó y construyó desde cero un **Agente de Control de Calidad (QA Agent)** exclusivo para evaluar prompts de video antes de enviarlos a Flow AI / Luma / Kling.

**REGLA DE ORO DEL AGENTE: SOLO LECTURA. NUNCA modifica archivos existentes.**

---

### 📁 ARCHIVOS CREADOS (NUEVOS — no modifican nada existente)

| Archivo | Descripción |
|---|---|
| `auditor_videos.py` | Agente QA principal. Evalúa prompts contra 6 pilares. Solo lectura. |
| `videos_content_v2.json` | Versión mejorada del video "La Ciencia de la Gratitud" que pasa la auditoría. |

---

### 🏗️ ARQUITECTURA DEL AGENTE (`auditor_videos.py`)

#### Sistema de Evaluación: 6 Pilares (máx. 30 puntos)

| Pilar | Qué evalúa | Máx. |
|---|---|---|
| **P1 — Continuidad** | Clip 1 usa patrones visuales de alto impacto (ojos, zoom, contraste). Clips 2+ llevan frase de continuidad explícita ("Continuing from previous clip..."). | 5 pts |
| **P2 — Física/Renderabilidad** | Detecta acciones de alto riesgo que la IA renderiza mal (correr rápido, luchar, comer, escribir). | 5 pts |
| **P3 — Cinematografía** | Verifica presencia de keywords de dirección premium: rim light, cinematic, dutch angle, slow-motion, 4K, photorealistic, subsurface scattering. | 5 pts |
| **P4 — Blindaje Anti-Texto** | Verifica que el prompt incluya el sufijo de protección: `[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]`. | 5 pts |
| **P5 — Economía de Tokens** | Longitud óptima por clip: 120-300 chars. <80: genérico. >450: agota cuota API (riesgo 429). | 5 pts |
| **P6 — Potencial Viral Facebook** | Evaluado 1 vez por video (no por clip): Curiosity Gap + respaldo científico + emoción + CTA Meta-aprobado + hashtags 3-8 + sin clichés visuales quemados. | 5 pts |

#### Umbrales de Veredicto

| Puntuación | Veredicto | Acción |
|---|---|---|
| ≥ 23/30 | ✅ APROBADO | Enviar directo a Flow AI / Luma. |
| 16-22/30 | ⚠️ REVISIÓN | Guardar con `requires_review: true`, revisar manualmente. |
| < 16/30 | ❌ RECHAZADO | Regenerar con Gemini. No producir. |

#### Archivos que audita (solo lectura)
- `videos_content.json` — Videos fotorrealistas (5 clips)
- `videos_content_v2.json` — Videos fotorrealistas v2 QA-Approved
- `video_moda_cartoon.json` — Cartoon Hero / Lumina (4 clips)
- `seedboy_content.json` — Concurso Seedboy (3 escenas), si existe

---

### 🧠 BASE DE CONOCIMIENTO DEL AGENTE (Pilar 6)

El agente no inventa criterios: usa una **base de conocimiento estática** investigada el 2026-05-17 a partir de:

1. **Patrones de Retención de Facebook Reels 2026 (Meta Analytics)**
   - Hook visual de alto impacto en los primeros 3 segundos: extreme close-up de ojos, contraste de luz, emoción negativa inicial (problema).
   - Fórmulas de texto probadas: "Stop doing X", "The #1 mistake", "Did you know", "What if I told you".
   - Tasa de retención objetivo: 60%+ es bueno, 70%+ es excelente.

2. **Psicología Viral de Contenido Científico (Berger's STEPPS, fMRI studies)**
   - Social Currency: el dato científico hace que el que lo comparte "parezca que sabe mucho".
   - Practical Value: datos aplicables inmediatamente (porcentajes, días, estadísticas).
   - Emotional Arousal: las emociones de alta activación (asombro, alegría) generan más shares que las neutrales.
   - Identity: compartir contenido que valida experiencias propias (ansiedad, agotamiento) activa la región de identidad del cerebro (medial prefrontal cortex).

3. **Saturación Visual 2025-2026 (Banner Blindness)**
   - Clichés corporativos quemados: high-fiving teams, handshakes, pointing at graphs, glass offices.
   - Emociones actuadas/forzadas: "laughing with salad", perfect smiles, overly enthusiastic poses.
   - Estética genérica de IA: "plastic look", shiny 3D renders, template backgrounds.
   - "Brag visuals": luxury cars, stacks of money, hustle quotes.

**Nota importante**: Esta base de conocimiento fue investigada en mayo 2026. Para mantenerla actualizada, se debe crear `actualizar_inteligencia.py` que consulte Gemini 1 vez/mes con preguntas sobre tendencias actuales.

---

### 📊 RESULTADOS DE LA PRIMERA AUDITORÍA COMPLETA

| Archivo | Clips | ✅ OK | ⚠️ Revisión | ❌ Rechazado | Veredicto |
|---|---|---|---|---|---|
| `videos_content.json` (v1) | 5 | 0 | 1 | 4 | ❌ RECHAZADO (12.6/30) |
| `videos_content_v2.json` (v2) | 5 | 5 | 0 | 0 | ✅ APROBADO (27.8/30) |
| `video_moda_cartoon.json` (Lumina) | 4 | 0 | 4 | 0 | ⚠️ REVISIÓN (19.8/30) |

#### Diagnóstico del video v1 "La Ciencia de la Gratitud" (rechazado):
- Prompts de 500-583 chars (la descripción física completa del personaje se repite en CADA clip).
- Sin frases de continuidad entre clips (cada clip empieza desde cero).
- Sin blindaje anti-texto en ninguno de los 5 clips.

#### Correcciones aplicadas en v2:
- Técnica "Character Anchor": descripción del personaje definida 1 vez en `character_anchor_en`, clips 2-5 solo dicen "same woman" + detalle de la nueva escena.
- Continuidad explícita en clips 2-5: "Continuing from previous clip —".
- Anti-texto en los 5 clips: `[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]`.
- Post/Voiceover con: dato de Harvard (25% más felicidad), CTA "Share with someone", 5 hashtags temáticos.
- Resultado: 27.8/30 promedio. APROBADO para producción.

#### Diagnóstico de Lumina — Cartoon Hero (revisión requerida):
- P6 Viral: 1/5 — Falta curiosity gap, dato científico, emoción y CTA en el post.
- P4 Anti-texto: 0/5 en todos los clips — Falta el sufijo de blindaje.
- **PENDIENTE**: Corregir `video_moda_cartoon.json` y `crear_moda_cartoon.py`.

---

### ⚙️ REGLAS PERMANENTES ESTABLECIDAS EN ESTA SESIÓN

1. **TODO video nuevo debe pasar `auditor_videos.py` antes de enviarse a Flow AI/Luma.** Puntuación mínima para producción: 23/30.
2. **La descripción del personaje NO se repite en cada clip.** Usar técnica "Character Anchor": definir 1 vez, referenciar brevemente en clips 2+.
3. **El sufijo anti-texto es OBLIGATORIO en cada clip**: `[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]`.
4. **Los clips 2, 3, 4 y 5 DEBEN empezar con**: "Continuing from previous clip —".
5. **El post_text y voiceover deben incluir**: al menos 1 dato científico con fuente, 1 elemento emocional, 1 CTA Meta-aprobado, y 3-8 hashtags.
6. **CTAs prohibidos por Meta** (penalizan alcance): "Like si...", "Comparte si estás de acuerdo", "Comenta SÍ si...". Usar siempre: "Share with someone who needs this", "Comment: what changed your life?", "Tag someone who...".

---

### 📅 PENDIENTES DE ESTA SESIÓN (2026-05-17)

1. **Corregir `video_moda_cartoon.json`**: Añadir anti-texto a los 4 clips y mejorar el P6 viral (curiosity gap, dato científico, CTA).
2. **Corregir `crear_moda_cartoon.py`**: Integrar las correcciones en el template del prompt para que futuras generaciones de Lumina pasen la auditoría automáticamente.
3. **Crear `actualizar_inteligencia.py`**: Script mensual que consulta Gemini para refrescar la base de conocimiento del agente con las últimas tendencias de Facebook.
**COMPLETADO:** Integrar auditor en el flujo de producción: Ejecutar `auditor_videos.py` automáticamente después de cada ejecución de `crear_video_viral.py` y `crear_moda_cartoon.py`.

---
---

## 🆕 SESIÓN 2026-05-18 — SEGMENTACIÓN DE VOZ Y CIERRE de QA

### 🚀 CAMBIOS IMPLEMENTADOS
1. **Segmentación de Voiceover (Timestamps)**: 
   - Implementado sistema de `voiceover_segments` en `videos_content_v2.json`.
   - Ahora la voz en off está dividida exactamente por clips (0-6s, 6-12s, etc.), facilitando el montaje en Flow AI.
   - Actualizado `crear_video_viral.py` para persistir este formato automáticamente.
2. **Verificación de Automatización QA**:
   - Confirmado que `auditor_videos.py` se ejecuta automáticamente al final de `crear_video_viral.py`.

---

FIN DE BITACORA

---
---

## 🆕 SESIÓN 2026-05-18 (Noche) — EL MOTOR CINEMATOGRÁFICO UNIVERSAL

### 🚀 CAMBIOS IMPLEMENTADOS

#### A) Guía Maestra (`CINEMATIC_AI_VIDEO_GUIDELINES.md`) — 7 Secciones
1. **Sec. 1 — Arquitectura del Libreto**: Anatomía del Prompt en 2 bloques (Contexto Maestro + Shot List). Etiquetas obligatorias: `FORMAT`, `SUBJECT`, `WARDROBE`, `ENVIRONMENT`, `MOOD`, `MUSIC`, `COLOR LOGIC`, `STYLE`, `RULES`, `NEGATIVE PROMPT`.
2. **Sec. 2 — Dinamismo y Cámara**: Planos (Macro, Contrapicado, Picado), Movimientos (Dolly, Handheld, Orbit), Coreografía de Cortes (Shot/Reverse Shot, Match on Action / Montaje Cinético Rápido).
3. **Sec. 3 — Iluminación**: Triángulo de Oro, Volumetric Fog, Color Grading, Control de Saturación (no abusar de destellos/partículas).
4. **Sec. 4 — Estabilización**: Character Book (Biblia Visual), Start & End Frame, Modelo Híbrido (imagen primero, video después).
5. **Sec. 5 — Optimización**: Timeline Prompting con sintaxis estricta (`SHOT X — TIMECODE — PLANO, LENTE, CÁMARA`), Testeo a 480p, Pipeline de 3 Herramientas (Imagen → Co-Director → Video).
6. **Sec. 6 — Videoclip Musical**: Lipsync de Precisión, CRASH ZOOM en el Beat, Bokeh Arquitectónico, Halo de Contraluz.
7. **Sec. 7 — Directorio de Estilos**: Ciencia, Psicología, Fantasía/Moda, Marketing/UI, Lifestyle, Thriller, K-Pop.

#### B) Scripts Modificados
- `crear_video_viral.py`: Nuevo JSON con `global_context_block_en` + sintaxis de tomas estricta.
- `crear_moda_cartoon.py`: Misma actualización de estructura de prompt.
- Ambos scripts leen `CINEMATIC_AI_VIDEO_GUIDELINES.md` dinámicamente en cada ejecución.

#### C) Test de Producción
- Se ejecutó `crear_video_viral.py` con la nueva arquitectura. Gemini generó correctamente el bloque de contexto maestro con MOOD, MUSIC y COLOR LOGIC. Auditoría QA: 100% clips aprobados (15/15).

#### D) Limpieza de Agnosticismo
- Se eliminaron TODAS las referencias a marcas específicas (ChatGPT, DALL-E, Claude, Gemini, Seedance, Midjourney, Luma, Kling, iPhone). El documento es 100% universal.

#### E) Videos Analizados (Fuentes de Conocimiento)
1. Video "Stop wasting Credits! Master Seedance 2.0" (Dan Kieft): Timeline Prompting, testeo 480p, secuencia Heist.
2. Video "Cómo crear un videoclip de Kpop con IA" (Duran Academy): Character Book, Pipeline de 3 herramientas, Lipsync, CRASH ZOOM, Bokeh Arquitectónico.

### ✅ TAREAS PENDIENTES RESUELTAS
- **COMPLETADO**: "Corregir `crear_moda_cartoon.py`: Integrar las correcciones en el template del prompt".
- **COMPLETADO**: "Expansión del Directorio de Estilos Visuales" (ahora tiene 7 estilos).

### 📅 PENDIENTE PARA MAÑANA (2026-05-19)
1. **Revisar el Documento Final**: Leer `CINEMATIC_AI_VIDEO_GUIDELINES.md` completo y validar coherencia de las 7 secciones.
2. **Revisar JSON Generado**: Validar `videos_content_v2.json` antes de pasar a producción.
3. **Generar Serie Lumina**: Correr `crear_moda_cartoon.py` para regenerar `video_moda_cartoon.json` bajo las nuevas reglas.
4. **Crear `actualizar_inteligencia.py`**: Script mensual para refrescar tendencias de Facebook.
