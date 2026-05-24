# 🎬 PIPELINE DE PRODUCCIÓN: VIDEO CINEMÁTICO DE ALTA CONSISTENCIA (I2V)

Este documento contiene la arquitectura completa para la creación del video de la mujer Latina, diseñada para maximizar la consistencia del personaje y evitar "alucinaciones" de la IA en Flow AI.

---

## 🛠️ ESTRATEGIA TÉCNICA: CADENA DE KEYFRAMES (I2V)
Para evitar que Flow AI cambie el rostro o el vestuario, se utiliza la técnica de **Start Frame $\rightarrow$ End Frame**.

**Flujo de trabajo:**
1. **Paso 0:** Generar Character Sheet (ADN Visual).
2. **Paso 1:** Generar 6 Imágenes Clave (Keyframes) usando el Character Sheet como referencia.
3. **Paso 2:** Crear 5 Clips de video mediante la transición entre imágenes.

---

## 🔒 1. EL ANCLA MAESTRA (Identidad Total)
*Copia y pega este bloque en TODA generación de imagen para mantener el personaje y el vestuario.*

**Prompt de Identidad:**
> A beautiful and magnetic 26-year-old Latina woman with deep highly expressive brown eyes, medium tan skin, long dark slightly wavy hair flowing naturally, elegant realistic facial features. WARDROBE: wearing a sleek, minimalist high-collar matte black architectural bodysuit with a subtle futuristic texture. Intelligent and emotionally intense appearance, radiating emotional strength. Ultra realistic skin texture, cinematic gaze, premium Netflix-style cinematic character design.

---

## 🎨 2. PASO 0: EL CHARACTER SHEET (La Biblia Visual)
*Generar primero para establecer la referencia de frente, lado y espalda.*

**Prompt:**
> Character sheet of [ANCLA MAESTRA]. Full body orthographic views: front view, side profile view, and back view. All views showing the same character with identical facial features, long dark wavy hair and the sleek minimalist high-collar matte black architectural bodysuit. Simple neutral grey background, studio lighting, photorealistic, 8K resolution, cinematic character design, symmetric composition, high detail, 9:16.

---

## 🖼️ 3. PASO 1: GENERACIÓN DE KEYFRAMES (Imágenes)
*Sube la hoja de personaje como "Character Reference" y genera estas 6 imágenes.*

| Imagen | Prompt de Generación (Añadir [ANCLA MAESTRA] al inicio) |
| :--- | :--- |
| **Img A** | Extreme macro close-up of her brown eyes reflecting flashing red emergency lights, dark futuristic elevator background, hyper-realistic iris detail, cinematic lighting, 9:16. |
| **Img B** | Medium shot, standing motionless inside a dark futuristic elevator, aggressive red lighting, the environment is starting to glitch and collapse into geometric shards, psychological thriller aesthetic, 9:16. |
| **Img C** | Full body shot, walking under rain in a futuristic cyberpunk city, neon blue and magenta reflections on wet pavement, giant screens in the background showing fragmented echoes of her face, cinematic depth of field, 9:16. |
| **Img D** | Floating in zero-gravity inside a dark minimalist void, red emotional energy waves flowing through her body and nervous system, hypnotic atmosphere, cinematic neuroscience aesthetic, 9:16. |
| **Img E** | Close-up of her face, eyes just opening, golden hour sunlight hitting her skin, futuristic rooftop background, wind moving her hair and the black fabric of her suit, soft lens flares, epic emotional atmosphere, 9:16. |
| **Img F** | Wide shot, small silhouette of her standing on an infinite surreal white salt flat landscape, bright ethereal sky reflecting perfectly on the ground, absolute peace, minimalist epic composition, 9:16. |

---

## 🎬 4. PASO 2: PROMPTS DE MOVIMIENTO (Transiciones I2V)
*Sube la imagen de inicio y la de fin, y aplica el prompt de movimiento.*

| Clip | Imágenes | Motion Prompt (Transición) |
| :--- | :--- | :--- |
| **Clip 1** | A $\rightarrow$ B | Extreme macro zoom-out from eyes to medium shot. Fast orbit around the face. Red lights flickering aggressively. High-speed psychological collapse of the environment. Cinematic handheld shake. **[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]** |
| **Clip 2** | B $\rightarrow$ C | Seamless transition from elevator to cyberpunk rain. Fast lateral tracking shot. Movement through wet glass reflections. Ends with a spinning top-down camera rotation. Subtle speed ramps. **[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]** |
| **Clip 3** | C $\rightarrow$ D | Transition from city rain to zero-gravity void. Slow cinematic rotation. Red energy waves pulsing through the body. Transition from red glow to peaceful blue light particles. Hypnotic flow. **[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]** |
| **Clip 4** | D $\rightarrow$ E | Transition from void to sunrise rooftop. Slow-motion eye opening. Wind moving hair and clothing elegantly. Drone pull-back revealing the futuristic city skyline in golden hour. **[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]** |
| **Clip 5** | E $\rightarrow$ F | Transition from rooftop to infinite white salt flats. Cinematic side-profile close-up transitioning into a massive drone reveal. Extreme pull-back showing the vastness of the white landscape. Absolute peace. **[CRITICAL: NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN VISUAL ONLY]** |

---

## 🚀 NOTAS DE EJECUCIÓN FINAL:
1. **Sincronización:** Cada clip debe durar 6 segundos para completar el video de 30s.
2. **Sufijo Anti-Texto:** Siempre mantener el bloque `[CRITICAL: NO TEXT...]` para evitar que la IA invente letras en el fondo.
3. **Referencia:** Si Flow permite "Character Reference", usa la Imagen del Character Sheet en TODOS los pasos.
