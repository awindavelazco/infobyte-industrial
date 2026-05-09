# KNOWLEDGE BASE — CURSO CARTOON HERO x SEEDBOY AI
# Ultima actualizacion: 2026-05-09
# Fuente: 5 carpetas de video descargadas de Google Drive (16 modulos totales)
# Proposito: Guia permanente para implementar las tecnicas del curso en los agentes de Infobyte

---

## INDICE
1. Resumen del Curso por Modulo
2. Tecnicas Clave Aprendidas
3. Herramientas del Arsenal
4. Plan de Distribucion en Agentes
5. Reglas de Oro para Prompts de Video
6. Flujo de Produccion Completo

---

## 1. RESUMEN DEL CURSO POR MODULO

### CARPETA 1 — Fundamentos (Zero to Hero)
**Modulos:** Bienvenida, Herramientas, Mapa de Aventura, Fogata Comun

**Lo mas importante:**
- El curso se basa en la idea de que cualquier persona puede crear animaciones de calidad profesional usando IA, sin saber dibujar.
- Filosofia: Velocidad + Experimentacion > Perfeccion tecnica.
- Dos tipos de video que debes dominar:
  * **Single-Shot:** Una sola escena animada. Rapido, pero limitado narrativamente.
  * **Multi-Shot:** Varias escenas conectadas que cuentan una historia completa. Es el formato que produce videos virales.
- Herramientas base del ecosistema: Midjourney / DALL-E (imagen base), Morphic/Nano Banana (consistencia de personaje), Seedance/Luma/Kling/Flow (animacion), CapCut (edicion), Suno (musica).

---

### CARPETA 2 — Tecnicas Avanzadas y Personajes
**Modulos:** Crear Personaje con FLUX Kontext, 20 Casos de Uso Nano Banana, Prompt Sheet PDF, Seedance Single-Shot, CapCut Arena, Suno Canciones

**Lo mas importante:**

#### FLUX Kontext (Creacion de Personaje Base)
- Usa FLUX Kontext para crear la imagen de origen del personaje.
- La imagen de origen es el ACTIVO MAS VALIOSO. Si la imagen base es mala, todo lo que venga despues sera malo.
- La imagen debe tener: fondo neutro o simple, iluminacion clara, expresion neutra, ropa representativa del personaje.

#### Morphic / Nano Banana (Consistencia de Personaje) — LAS 20 TECNICAS
Esta es la pieza mas critica del curso. Permite modificar la imagen base manteniendo al mismo personaje.
Tecnicas disponibles segun el Prompt Sheet oficial:

| # | Tecnica | Uso en contenido |
|---|---|---|
| 1 | Cambiar angulo de camara | Pasar de plano frontal a plano cenital o perfil |
| 2 | Cambiar hora del dia | Misma escena pero de noche / al amanecer |
| 3 | Cambiar clima | Sol → lluvia → nieve en la misma ubicacion |
| 4 | Cambiar ropa | Mantener personaje con nuevo outfit |
| 5 | Cambiar expresion facial | Feliz → triste → sorprendido |
| 6 | Cambiar fondo/ubicacion | Mismo personaje, diferente escenario |
| 7 | Zoom progresivo | Acercarse al personaje en la misma pose |
| 8 | Crear Spritesheet | Hoja de poses del personaje para animacion |
| 9 | Cambiar a persona real | Reemplazar personaje animado por foto real |
| 10 | Envejecer / rejuvenecer | El mismo personaje en diferentes edades |
| 11 | Cambiar genero | Mantener estilo pero cambiar genero |
| 12 | Agregar un objeto | Mismo personaje ahora sosteniendo algo |
| 13 | Agregar otro personaje | Poner un segundo personaje en la escena |
| 14 | Cambiar estilo artistico | Mismo personaje en Anime, Pixar, comic, etc. |
| 15 | Vista microscopica | Zoom extremo a un detalle del personaje |
| 16 | Plano Over-the-shoulder | Camara detras del personaje viendo lo que el ve |
| 17 | Plano Insert | Detalle de un objeto importante (ej: manos, objeto) |
| 18 | Vista aerea (Aerial) | Camara desde arriba mostrando el entorno |
| 19 | Close-up emocional | Primer plano del rostro para mostrar emocion |
| 20 | Steadicam / Dolly shot | Camara que sigue al personaje moviendose |

#### Seedance (Animacion Single-Shot)
- Seedance genera videos de hasta 10 segundos por clip con alta fidelidad al personaje.
- Para un video fluido, el prompt debe describir exactamente:
  * El movimiento de camara (lento, rapido, paneo)
  * La emocion del personaje
  * La accion que ocurre en esos segundos
- Ventaja sobre Luma/Kling: Mantiene mejor la consistencia del personaje entre frames.

#### CapCut Arena (Edicion Final)
- Herramienta para ensamblar los clips generados.
- Permite agregar: texto animado, transiciones, efectos de sonido, musica de fondo.
- El flujo correcto es: Generar clips en Flow/Seedance → Descargar → Importar a CapCut → Ensamblar → Exportar 1080p.

#### Suno AI (Musica Tematica)
- Crea una cancion tematica para el personaje/marca con un prompt de descripcion del genero y mood.
- Para Infobyte: Estilo recomendado = "Ambient electronic, inspirational, documentary feel, no vocals, 30 seconds loop".
- Para Seedboy: Estilo = "Upbeat children cartoon theme, playful, educational, 30 seconds".

---

### CARPETA 3 — Produccion Cinematografica
**Modulos:** El secreto de los angulos de camara, Multi-Shot Magic Seedance, Walkthrough completo Isle of Secrets, Efectos de Sonido

**Lo mas importante:**

#### Los 4 Angulos Fundamentales (El "secreto" del curso)
Usar siempre estos 4 angulos en orden para crear un video Multi-Shot profesional:

1. **HOOK — Close-up Shot (0-8s):** Primer plano del rostro o detalle impactante. Captura la atencion en los primeros 3 segundos.
2. **TENSION — Over the Shoulder / Medium Shot (8-16s):** Camara detras del personaje o a media altura. Muestra el problema o conflicto.
3. **REVELATION — Insert Shot / Pull Back (16-24s):** Plano detalle del objeto/elemento clave O alejamiento para revelar el contexto completo.
4. **IMPACT — Aerial View / Slow Motion Close-Up (24-32s):** Vista cenital epica O primer plano en camara lenta para el final emocional.

#### Multi-Shot con Seedance (la tecnica de continuidad)
- Generar clips de 8-10 segundos cada uno.
- Cada prompt de clip siguiente debe referenciar el frame final del clip anterior.
- Prefijo obligatorio para clips 2, 3, 4: "Continuing from previous clip —"
- Esto crea la ilusion de un video largo fluido sin saltos visuales.

#### Efectos de Sonido — El Arma Definitiva
- Los efectos de sonido son el 40% de la percepcion de calidad de un video.
- Sin efectos de sonido, el video parece de bajo presupuesto aunque las imagenes sean perfectas.
- Fuentes gratuitas: Pixabay Sound Effects, Freesound.org, Epidemic Sound (pago).
- Tipos de efectos criticos:
  * Whoosh/Swoosh: para transiciones entre escenas.
  * Heartbeat o breathing: para escenas de tension.
  * Chime/Bell: para momentos de revelacion.
  * Ambient nature: para finales tranquilos.

---

### CARPETA 4 — Produccion Completa (Walkthroughs)
**Modulos:** The Last Throne Parte 1, Parte 2, Final Polish 1080p Upscale

**Lo mas importante:**

#### Flujo de Produccion Completo (de imagen a video publicable)
El walkthrough "The Last Throne" demuestra el proceso de principio a fin:
1. Crear imagen de origen con FLUX Kontext (personaje base).
2. Modificar con Nano Banana para las 4 escenas del video.
3. Animar cada escena con Seedance (8-10s por clip).
4. Descargar clips y ensamblar en CapCut.
5. Agregar voiceover (grabado o generado con ElevenLabs).
6. Agregar efectos de sonido (Freesound).
7. Agregar musica de fondo generada en Suno (volumen al 20-30%).
8. Exportar en 1080p con CapCut.
9. **PASO FINAL CRITICO: Upscale a 1080p** con Topaz Video AI o similar.

#### Por que el Upscale es critico
- Los generadores de video de IA producen en 720p por defecto.
- Facebook y Instagram penalizan videos de baja resolucion en el algoritmo.
- El upscale a 1080p puede aumentar el alcance organico hasta 3x.
- Herramienta gratuita para upscale: Kapwing (online) o DaVinci Resolve (local).

---

### CARPETA 5 — Bonus: Imagenes de Origen
**Modulos:** Como crear buena imagen de origen, Caza del Heroe, 4 Reglas Clave

**Lo mas importante:**

#### Las 4 Reglas de Oro para la Imagen de Origen
1. **Regla del Fondo Simple:** El fondo debe ser neutro (color solido, gradiente suave, o escenario muy simple). Fondos complejos confunden a los generadores de video.
2. **Regla de la Luz Frontal:** La iluminacion debe venir de frente o ligeramente lateral. La sombra del personaje no debe tapar partes importantes.
3. **Regla del Espacio de Accion:** Dejar espacio vacio alrededor del personaje para que el generador pueda animarlo sin cortar partes del cuerpo.
4. **Regla de la Expresion Neutra:** La imagen base debe tener expresion neutra/ligera. Es mas facil para la IA modificar una expresion neutra hacia cualquier emocion que partir de una expresion exagerada.

#### Donde encontrar imagenes de origen rapidamente
- Adobe Stock (buscar "character, white background, full body")
- Unsplash (para personas reales en situaciones cotidianas)
- Generar con FLUX Kontext o Midjourney
- Para Infobyte: Buscar "person daily life, candid, 35mm photography"

---

## 2. TECNICAS CLAVE APRENDIDAS (Resumen para Agentes)

### Tecnica A: Continuidad de 4 Clips (ya implementada en crear_video_viral.py)
- 4 clips x 8 segundos = 32 segundos (Reel ideal)
- Estructura: Hook → Tension → Revelation → Impact
- Cada clip empieza con "Continuing from previous clip —"
- Un "character_description_en" global garantiza consistencia visual

### Tecnica B: Angulos de Camara por Clip
- Clip 1: Close-up / Macro
- Clip 2: Medium Shot / Over-the-shoulder
- Clip 3: Insert Shot / Pull Back
- Clip 4: Aerial View / Slow Motion Close-up

### Tecnica C: Curiosity Gap (ya implementada en crear_frase_viral.py)
- Primeras 2 lineas del post = Gancho de curiosidad irresistible
- Estructura: Dato sorprendente + Pregunta que genera FOMO
- Siempre cerrar con pregunta binaria o personal para invitar comentarios

### Tecnica D: Imagen de Origen de Alta Calidad
- Persona real + situacion cotidiana + iluminacion cinematica
- Prohibido: fractales, nebulosas, figuras abstractas
- Formato: 1080x1350 (vertical para Facebook/Instagram)

---

## 3. HERRAMIENTAS DEL ARSENAL

| Herramienta | Funcion | Costo | Integrado en Agente? |
|---|---|---|---|
| **Gemini 2.0 Flash** | Generacion de texto y prompts | Gratis (limite diario) | SI — todos los scripts |
| **Ollama (Llama3)** | Fallback local | Gratis | SI — pero NO produccion |
| **Flow AI** | Animacion de clips 8s | Pago/Freemium | NO — uso manual |
| **Seedance 1.0** | Animacion Single/Multi-Shot | Pago/Freemium | NO — uso manual |
| **Morphic/Nano Banana** | Consistencia de personaje | Pago/Freemium | NO — uso manual |
| **FLUX Kontext** | Imagen base del personaje | Pago/Freemium | NO — uso manual |
| **CapCut** | Edicion final del video | Gratis | NO — uso manual |
| **Suno AI** | Musica tematica | Gratis (limite) | NO — uso manual |
| **Pollinations.ai** | Generacion de imagenes fijas | Gratis | SI — crear_frase_viral.py |
| **ElevenLabs** | Voiceover / Text-to-Speech | Freemium | NO — uso manual |
| **Freesound.org** | Efectos de sonido | Gratis | NO — uso manual |
| **Kapwing** | Upscale a 1080p | Freemium | NO — uso manual |

---

## 4. PLAN DE DISTRIBUCION EN AGENTES

### AGENTE 1: crear_frase_viral.py (Posts de Imagen Fija)
**Tecnicas del curso integradas:**
- [x] Curiosity Gap en primeras 2 lineas
- [x] Imagen de personas reales (no abstractas)
- [x] Iluminacion cinematica en prompt de imagen (Golden Hour, ventana dramatica)
- [x] Angulo de camara especificado (Close-up, medium shot, over-the-shoulder)
- [x] Pregunta de interaccion al final
- [ ] PENDIENTE: Validacion anti-Ollama (excluir si generated_by == Ollama)

**Parametros actuales:** 7 posts/semana | Pollinations.ai para imagenes | Gemini 2.0 Flash

---

### AGENTE 2: crear_video_viral.py (Videos Reels 32s para Infobyte)
**Tecnicas del curso integradas:**
- [x] Continuidad 4x8s para Flow AI
- [x] Estructura Hook → Tension → Revelation → Impact
- [x] character_description_en para consistencia visual
- [x] Movimientos de camara especificados por clip
- [x] Curiosity Gap en post caption
- [ ] PENDIENTE: Reducir prompt a max 300 tokens (ERROR #009)
- [ ] PENDIENTE: Rotar llave inmediatamente en 429
- [ ] PENDIENTE: Detener proceso si todas las llaves fallan (no caer a Ollama)

**Parametros actuales:** 5 videos/semana | Flow AI (manual) | Gemini 2.0 Flash

---

### AGENTE 3: crear_quiz_viral.py (Quizzes Interactivos)
**Tecnicas del curso integradas:**
- [ ] PENDIENTE: Agregar imagen tipo "persona en situacion cotidiana relacionada al quiz"
- [ ] PENDIENTE: Agregar Curiosity Gap en el enunciado del quiz

**Parametros actuales:** 2 quizzes/semana (Lun y Jue 7pm EST)

---

### AGENTE 4: crear_video_seedboy.py (Videos Concurso Cartoon Hero)
**Tecnicas del curso integradas:**
- [x] Estructura narrativa 5 pasos del concurso (Enganche, Investigacion, POV Semillas, Diagnostico, Desenlace)
- [x] 6 escenas x 5 segundos = 30 segundos
- [x] Estilo 3D Animation (Pixar/Dreamworks)
- [x] Personajes: Seedboy + vecino + semillas con humor
- [ ] PENDIENTE: Migrar a formato 4x8s con Flow AI (en lugar de 6x5s para Luma/Kling)
- [ ] PENDIENTE: Agregar descripcion de efectos de sonido por escena

**Parametros actuales:** 2 guiones/ejecucion | Luma/Kling (manual) | Gemini 2.0 Flash

---

### AGENTE 5: engine_agentes.py (Motor Principal de Noticias)
**Tecnicas del curso integradas:**
- [ ] PENDIENTE: Agregar prompt de imagen con angulos cinematicos
- [ ] PENDIENTE: Cambiar estilo visual de abstracto a personas reales en situacion cotidiana

**Parametros actuales:** Noticias de ciencia/salud | Gemini 2.0 Flash

---

## 5. REGLAS DE ORO PARA PROMPTS DE VIDEO

Estas reglas son resultado directo del curso y deben seguirse SIEMPRE:

### Para clips de Flow AI / Seedance:
```
FORMATO OBLIGATORIO:
"[CAMARA MOVEMENT]. [SUBJECT] [ACTION]. [LIGHTING]. [EMOTION]. Photorealistic, cinematic, 4K."

EJEMPLO CORRECTO:
"Slow zoom in on face. A tired 30-year-old woman stares at her phone at 3am, 
dark circles visible, blue screen light illuminating her face. Soft ambient 
darkness, single lamp glow. Expression of exhaustion and loneliness. 
Photorealistic, cinematic, 4K."

EJEMPLO INCORRECTO (nunca usar):
"A woman looking at phone. Sci-fi background with neon lights and fractals."
```

### Para prompts de imagen fija (Pollinations.ai):
```
FORMATO OBLIGATORIO:
"[PERSON DESCRIPTION] [SITUATION/ACTION], [LOCATION], [LIGHTING], [CAMERA ANGLE], 
[EMOTIONAL TONE]. Photorealistic, cinematic, 4K, no text, no watermark."

EJEMPLO CORRECTO:
"A 40-year-old man sitting alone at a kitchen table at dawn, holding a coffee mug 
with both hands, looking out the window with a thoughtful expression, warm golden 
morning light, medium shot from the side, mood of quiet introspection. 
Photorealistic, cinematic, 4K, no text, no watermark."
```

---

## 6. FLUJO DE PRODUCCION COMPLETO

### Para Videos de Infobyte (crear_video_viral.py)
```
1. Ejecutar crear_video_viral.py
   → Genera videos_content.json con 5 guiones (4 clips cada uno)

2. Para cada video en videos_content.json:
   a. Copiar character_description_en → Crear imagen base en FLUX Kontext
   b. Copiar clip_1_hook_en → Pegar en Flow AI → Descargar clip 1 (8s)
   c. Copiar clip_2_tension_en → Pegar en Flow AI (imagen = ultimo frame clip 1) → Clip 2
   d. Copiar clip_3_revelation_en → Pegar en Flow AI (imagen = ultimo frame clip 2) → Clip 3
   e. Copiar clip_4_impact_en → Pegar en Flow AI (imagen = ultimo frame clip 3) → Clip 4

3. En CapCut: Importar clips 1+2+3+4 → Ensamblar → Agregar voiceover_en
4. Agregar efectos de sonido de Freesound.org
5. Agregar musica de Suno (volumen 20%)
6. Exportar 1080p → Upscale si es necesario
7. Publicar en Facebook segun calendario (8am EST, Lun/Mar/Mie/Vie/Sab)
```

### Para Posts de Imagen Fija (crear_frase_viral.py)
```
1. Ejecutar crear_frase_viral.py
   → Genera frases_content.json con 7 posts

2. VALIDACION OBLIGATORIA antes de publicar:
   a. Verificar que generated_by_text == "Gemini (Cloud)" (NO Ollama)
   b. Verificar que postES no diga "Resumen no disponible."
   c. Verificar que len(postEN) > 200 caracteres
   d. Verificar que el post NO termine con "Action Plan:" sin contenido

3. Para cada post aprobado:
   a. Copiar prompt de imagen → Generar en Pollinations.ai
   b. Descargar imagen 1080x1350
   c. Publicar postEN en Facebook segun calendario

4. Horarios: Martes 12:30pm, Viernes 12:30pm, Domingo 12:30pm (EST)
```

### Para Quizzes (crear_quiz_viral.py)
```
1. Ejecutar crear_quiz_viral.py
2. Publicar resultado en Facebook: Lunes 7pm y Jueves 7pm (EST)
```

---

## REGLA FINAL
Antes de ejecutar cualquier script de generacion:
1. Verificar cuota de llaves con el script de auditoria
2. Confirmar que es el UNICO script pesado del dia
3. Si las llaves estan agotadas → NO ejecutar (esperar reinicio o conseguir nuevas llaves)
4. Si el resultado es de Ollama → NO publicar sin revision manual

FIN DEL KNOWLEDGE BASE
