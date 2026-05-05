# BITACORA DE ERRORES — INFOBYTE INDUSTRIAL
# LECTURA OBLIGATORIA AL INICIO DE CADA SESION DE DESARROLLO
# Ultima actualizacion: 2026-05-04

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
FIN DE BITACORA
