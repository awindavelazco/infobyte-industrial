# BITACORA DE ERRORES Y ESTADO DEL SISTEMA — INFOBYTE INDUSTRIAL
# LECTURA OBLIGATORIA AL INICIO DE CADA SESION DE DESARROLLO
# Ultima actualizacion: 2026-05-09

---
## ESTADO ACTUAL DEL SISTEMA (RESUMEN PARA NUEVO CHAT)

### 🔴 ESTADO DE API KEYS (al 2026-05-09 ~6pm EST)
- **news_keys:** 6 llaves — TODAS AGOTADAS (429 Rate Limit diario)
- **video_keys:** 6 llaves — TODAS AGOTADAS (429 Rate Limit diario)
- **Causa:** Se ejecutaron crear_video_viral.py (5 videos) y crear_frase_viral.py (7 frases) en la misma sesion con prompts de alto consumo de tokens. Ver ERROR #009.
- **Reinicio:** Las cuotas se reinician aprox. a las 3am EST / midnight PST.
- **Accion obligatoria al inicio de sesion:** Ejecutar auditoria de llaves ANTES de cualquier generacion.

### 📁 SCRIPTS ACTIVOS Y SU FUNCION
| Script | Funcion | Lote | Estado |
|---|---|---|---|
| `engine_agentes.py` | Motor principal de noticias (posts de ciencia/salud) | Variable | OK |
| `crear_frase_viral.py` | Posts de frases/reflexiones (Soul Notes / Infobyte) | 7/semana | MODIFICADO HOY |
| `crear_video_viral.py` | Guiones de video 4x8s para Flow AI (Reels 32s) | 5/semana | MODIFICADO HOY |
| `crear_quiz_viral.py` | Quizzes interactivos | 2/semana | Sin cambios |
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

### ⚙️ CAMBIOS REALIZADOS EN ESTA SESION (2026-05-09)
1. **crear_video_viral.py** — Rediseado con tecnica Continuidad 4x8s para Flow AI (32s Reels). Prompt mas largo (650 tokens). **PENDIENTE OPTIMIZACION** (ver ERROR #009).
2. **crear_frase_viral.py** — Nuevo prompt con Curiosity Gap, imagenes de personas reales, lote reducido a 7/semana.
3. **crear_video_seedboy.py** — Creado desde cero para concurso Cartoon Hero x Seedboy.
4. **BITACORA** — Actualizacion con ERROR #008 y #009.
5. **Backup** — Carpeta `backup_20260509_1452` con todos los scripts antes de cambios.

### ⚠️ FIXES PENDIENTES DE APROBACION (NO ejecutar sin OK del usuario)
1. Reducir prompt de `crear_video_viral.py` a max 300 tokens.
2. Cambiar logica de retry: rotar llave inmediatamente al primer 429.
3. Si todas las llaves fallan → detener proceso, NO caer a Ollama en produccion.
4. Agregar validacion: si generated_by == "Ollama", excluir del dashboard automaticamente.

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
FIN DE BITACORA
