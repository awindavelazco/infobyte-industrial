# 🎬 Guía Maestra de Cinematografía Universal para Videos IA

Este documento establece las reglas generales para generar libretos y prompts de video de alta gama (Cinematic Ads). Aplica para **cualquier tipo de video** (moda, documentales, ciencia, narrativa, productos), evitando el "look de IA" genérico.

## 1. Arquitectura del Libreto (El "Director's Script")

Nunca pidas a la IA "un video sobre X". El libreto debe estructurarse como un storyboard técnico de Hollywood.

*   **Secuenciación de Tensión (Micro-clips de 3 a 5s):** Divide la narrativa en planos cortos. Clips largos en la IA actual generan deformaciones (morphing) y alucinaciones.
*   **La Anatomía del Prompt (Contexto Maestro + Línea de Tiempo):**
    Los prompts profesionales no son un párrafo largo. Se dividen en dos bloques estrictos:
    1. **El Bloque de Contexto Global:** Establece el mundo y sus reglas *antes* de animar nada. Debe incluir siempre en este orden: `FORMAT` (ej. 15s / 6 SHOTS), `SUBJECT`, `WARDROBE`, `SECONDARY SUBJECTS`, `ENVIRONMENT`, `MOOD` (ej. Tense, restrained, then explosive), `MUSIC` (ej. Low sub bass drone), `COLOR LOGIC` (ej. Desaturated steel blues and blacks), `STYLE` (ej. Ultra-Realistic, cinematic action film look), `RULES` (restricciones lógicas vitales), y un fuerte `NEGATIVE PROMPT` (ej. "cheesy sparkle VFX, extra limbs").
    2. **El Bloque de Tomas (Shot List):** Aquí se usa la jerarquía visual `[TAMAÑO DE PLANO] + [ACCIÓN FÍSICA] + [LÚZ/ESTILO]` aplicando la sintaxis estricta de tiempo explicada en la sección 5.
*   **Física Descriptiva (No Emocional):** La IA de video no entiende "está triste". Entiende: *"Mira al suelo, hombros caídos, exhalación lenta"*. Describe siempre el movimiento físico.


## 2. Dinamismo y Ángulos de Cámara

Para evitar el "zoom digital lento" genérico, especifica el movimiento físico de una cámara virtual:

*   **Tipos de Plano (Framing):**
    *   **Extreme Close-Up (Macro):** Para el inicio (Hook). Texturas, ojos, mecanismos. Atrapa la atención en 1 segundo.
    *   **Low Angle (Contrapicado):** Hace al sujeto verse poderoso o heroico. Ideal para momentos de impacto o revelación.
    *   **High Angle (Picado):** Hace al sujeto verse vulnerable o pequeño frente a su entorno.
*   **Movimientos de Cámara (Camera Motion):**
    *   **Dolly Push-in:** La cámara avanza físicamente hacia el sujeto. Genera tensión e intimidad.
    *   **Handheld Tracking (Cámara en Mano):** Añade *"slight natural camera shake"*. Esto introduce imperfección humana y elimina instantáneamente el aspecto sintético/plástico de la IA.
    *   **Orbit / Arc Shot:** Paneo circular alrededor del sujeto. Perfecto para mostrar transformaciones completas o entornos 3D.
    *   **Slow Pull-back Reveal:** Comienza cerrado en un detalle y retrocede lentamente para revelar un entorno masivo o un giro de trama.
*   **Coreografía de Cortes (Multi-Ángulo):**
    *   **Shot / Reverse Shot (De Frente y de Espalda):** El mayor error es dejar la cámara quieta. Para crear tensión (como en escenas de persecución o diálogo), genera dos clips separados: uno con *"Frontal medium shot, subject looking at camera"* y el siguiente con *"Over-the-shoulder shot from behind the subject"*. Este corte abrupto de 180 grados rompe la monotonía instantáneamente.
    *   **Match on Action (Montaje Cinético Rápido):** Para secuencias de altísima energía, encadena ángulos y tamaños de plano de forma extrema (saltando de general a detalle) manteniendo un flujo de movimiento físico. Ejemplo de micro-montaje de 5 segundos: *"Macro close up of hand grabbing tray"* -> *"Wide shot from above of subject running down stairs"* -> *"Over-the-shoulder shot from behind opening a door"* -> *"Profile close-up of face reacting"*. Este bombardeo de planos retiene la atención del espectador al 100%.

## 3. Estilos de Iluminación Cinematográfica

La iluminación separa el contenido amateur del profesional. Evita la luz frontal plana.

*   **El Triángulo de Oro (3-Point Lighting):**
    *   **Key Light (Luz Principal):** Usa *"45-degree dramatic side-lighting"* o *"Rembrandt lighting"*. Esculpe el rostro o el objeto con sombras (claroscuro).
    *   **Rim Light / Backlight (Luz de Contorno):** *"Strong neon backlight"* o *"Golden hour rim light"*. Separa al sujeto del fondo. Es **crítico en la IA** para evitar que el sujeto se fusione con el fondo durante el movimiento.
*   **Texturización del Ambiente:**
    *   **Volumetric Fog / Atmospheric Haze:** "Niebla volumétrica". Permite que los rayos de luz (God rays) sean visibles e interactúen con la lente, ocultando imperfecciones del fondo.
    *   **Highlight Rolloff:** "Soft highlight rolloff" evita que las áreas blancas se vean "quemadas", dándole un acabado de película cara.
*   **Consistencia de Color (Color Grading):**
    Mantén el "Color Grade" constante en todos los clips de un mismo video para anclar la identidad visual (Ej: *"Teal and Orange color grade"*, *"Muted cinematic tones"*, *"Cyberpunk neon palette"*).
*   **Control de Efectos Visuales y Saturación:**
    *   No abuses de destellos (lens flares), partículas o dispersión de luz ("light scatter"). Pídele explícitamente a la IA que los use *solo en zonas necesarias*.
    *   La imagen no debe estar sobrecargada de detalles que la desequilibren. Menos es más en la cinematografía de alta gama. Usa frases como: *"Cinematográfico, alta calidad, fotorrealista, iluminación de estudio profesional, lentes de cine, ARRI Alexa"*.

## 4. Estabilización Avanzada (Transiciones y Consistencia Absoluta)

Independientemente de si el video es de un humano fotorrealista, un paisaje de ciencia ficción o un producto comercial, estas técnicas garantizan cero alucinaciones de la IA:

*   **El "Character Book" (La Biblia Visual del Personaje):**
    Para mantener a un sujeto idéntico en múltiples escenas, NO basta con describirlo en texto. El primer paso absoluto antes de animar es generar un *Character Book* o *Hoja de Referencia Maestro*. Este documento visual debe contener:
    1. **Rostro:** El sujeto visto de frente, perfil y 3/4.
    2. **Cuerpo Entero:** Outfit detallado de frente y de espaldas.
    3. **Poses Clave:** Lenguaje corporal predefinido.
    4. **Paleta de Color y Props:** Colores exactos y accesorios (ej. audífonos, cámara).
    Al usar esta "Biblia" como imagen de entrada (Image-to-Video) o como ancla en el modelo, la IA absorbe la geometría 3D completa del personaje, garantizando que su rostro, ropa o accesorios no "muten" o desaparezcan cuando la cámara gire.
*   **El Flujo "Start & End Frame" (Interpolación Perfecta):**
    Para crear transiciones perfectas entre clips, o controlar un movimiento muy específico (ej: una caja abriéndose), nunca confíes solo en el texto. Pasa a la IA un *Starting Frame* (inicio) y un *Ending Frame* (final) diseñados previamente. La IA funcionará como un interpolador perfecto entre el punto A y el B, eliminando parpadeos y fallos lógicos.
*   **Separación de Fases (El Modelo Híbrido):**
    Nunca intentes generar un sujeto complejo directamente en video. 
    1.  **Fase de Set-Up (Creación del Character Book):** Abre cualquier modelo de generación de imágenes de alta fidelidad. Sube 1 o 2 imágenes de referencia humana si es necesario, y usa este Prompt Base:
        *"Para que la IA de video tenga una referencia clara, necesito que crees un 'Character Book' de mi personaje. [INSERTA ESTILO, ej. Es una artista K-pop]. Tiene que tener: [LISTA DE ROPA Y ACCESORIOS, ej. vestido plateado, descalza, pulsera, colores neón]. En el character book debes especificar cómo es facialmente: Plano frontal, plano lateral y plano de detalle facial."*
    2.  **Fase de Cinematografía:** Carga el *Character Book* generado en el modelo de animación de video que elijas. En el prompt de texto de animación, **elimina la descripción física del sujeto** y enfócate única y exclusivamente en dictar el movimiento de cámara y la interacción física, permitiendo que la herramienta use la imagen ancla para resolver el 3D sin alucinaciones.

## 5. Optimización de Flujo de Trabajo (Ahorro de Créditos)

Generar videos cuesta dinero/créditos. Para no desperdiciarlos, los agentes deben seguir estas reglas:

*   **Timeline Prompting (Sintaxis Estricta Multi-shot):** Si vas a crear una secuencia larga, estructura el prompt pensando en la línea de tiempo usando una sintaxis técnica. El formato obligatorio para cada toma debe ser:
    `SHOT [X] — [INICIO]-[FIN]s — [TAMAÑO DE PLANO], [LENTE mm], [MOVIMIENTO DE CÁMARA]`
    *Ejemplo:*
    `SHOT 1 — 0:00-0:02 — MCU, 50mm, locked. Bustling mansion kitchen...`
    `SHOT 2 — 0:02-0:04 — WS, 35mm, slow tracking. She ascends the stairs...`
    `SHOT 3 — 0:04-0:06 — MS, 50mm, over-shoulder. Security guard glances...`
    Esto obliga a la IA a procesar el video como un director de fotografía real, respetando los cortes físicos y la longitud exacta de cada acción.
*   **Fase de Testeo en Baja Resolución:** Siempre que sea posible, el agente o usuario debe realizar una prueba del render en **baja resolución (ej. 480p)** y con bajo framerate para validar que el movimiento de cámara y la física son correctos. Solo cuando el *test render* sea aprobado, se hace el upscale o render final en 1080p/4K.
    *   **Referencia de costo:** Un test a 480p suele costar una fracción mínima de créditos por clip de 8s. Jamás gastar créditos de alta resolución sin aprobar el test primero.

*   **El Pipeline de 3 Herramientas (Flujo Profesional Completo):**
    Este es el workflow end-to-end que separa la producción amateur de la profesional:
    1. **Herramienta de Imagen** (cualquier generador de imágenes de alta fidelidad): Genera el *Character Book* del personaje.
    2. **Agente Co-Director** (cualquier LLM avanzado con capacidad de razonamiento): Recibe el briefing en lenguaje humano más el Character Book. Entrega el Shot List técnico completo (lente, plano, movimiento, lipsync, sincronización con la canción). **El cerebro es el sistema, no un generador de prompts.**
    3. **Herramienta de Video** (cualquier generador de video IA con soporte Image-to-Video): Recibe la imagen ancla + el prompt técnico. Solo se aprieta el botón.

## 6. Técnicas de Videoclip Musical (Lipsync + Beat Sync)

Cuando el video tiene música con letra, el movimiento de cámara debe estar anclado a momentos musicales específicos. No es opcional, es lo que separa un videoclip de calidad de un experimento amateur:

*   **Lipsync de Precisión (Sincronización de Labios):**
    En el prompt, se especifica el instante exacto de la canción que el personaje está cantando. La descripción debe ser física y literal, nunca emocional:
    *Ej: "mouth open, clearly mouthing the words, maximum lip separation". Nunca: "cantando emocionada".*

*   **CRASH ZOOM en el Beat (Corte de Impacto):**
    Cuando una palabra clave o acorde de impacto llega en la canción (ej. al segundo 4.5, ella dice "CRACKS"), el prompt debe ejecutar un movimiento de cámara agresivo que coincida. Ejemplo:
    *"At exactly second 4.5, execute a RAPID CINEMATIC CRASH ZOOM directly into her face — fast, aggressive, instant impact. No slow pull."*
    El Crash Zoom debe sentirse cinematográfico, **nunca digital o brusco**.

*   **Bokeh Arquitectónico (Profundidad de Campo con Entorno):**
    Para evitar fondos plásticos y generar profundidad real, usa los elementos del entorno como técnica de bokeh. Ejemplo:
    *"Columns blur into vertical silver bokeh. Lens flare from ceiling strip light. Real-time speed."*
    Esto convierte el escenario en un activo cinematográfico que enmarca al sujeto, en lugar de competir con él.

*   **Halo de Contraluz (Silhouette Backlight):**
    Al final de un clip o en el clímax de la canción, el personaje camina hacia la cámara con una luz de fondo potente que crea un halo alrededor de su silueta. Ejemplo:
    *"Final 1.5 seconds: white backlight creates a halo around her silhouette. Confident stride toward camera."*

## 7. Directorio de Estilos Visuales Adaptativos

El estilo visual debe complementar la temática de la noticia o contenido. Usa estos "bloques de estilo" al principio de tu prompt (como vimos en la Jerarquía Universal) para dictar la atmósfera:

*   **Ciencia y Medicina (Anatomía, Biología, Tecnología pura):**
    *   **Prompt Base:** *"Clean clinical precision, subtle glowing microscopic details, cold blue and sterile white tones, macro scientific photography, high-tech documentary style."*
    *   **Uso:** Ideal para noticias serias de descubrimientos, salud o tecnología de punta.

*   **Psicología, Emociones y Relaciones Humanas:**
    *   **Prompt Base:** *"Muted cinematic tones, soft diffuse lighting, 35mm film grain, intimate portraiture, earthy color palette, naturalistic documentary feel."*
    *   **Uso:** Ideal para temas de salud mental, comportamiento humano o sociología.

*   **Fantasía, Moda o Futurismo Comercial:**
    *   **Prompt Base:** *"Vibrant neon palette, high-fashion editorial photography, glossy reflections, dramatic rim lighting, hyper-stylized 3D rendering, surrealism."*
    *   **Uso:** Concursos, historias ficticias o contenido altamente visual enfocado en estética.

*   **Marketing Digital, Productos y UI/UX (Alta Precisión):**
    *   **Prompt Base:** *"Clean flat design aesthetics, vibrant vector-like colors, modern UI mockup, professional studio product lighting, 4K crisp details, accurate typography."*
    *   **Uso:** Ideal para crear material promocional, prototipos de apps, o mostrar interfaces/productos de forma ultra-nítida.

*   **AI Influencers y Lifestyle (Redes Sociales):**
    *   **Prompt Base:** *"Candid smartphone photography, social media influencer style, highly detailed facial features, casual modern outfits, natural golden hour lighting, slight depth of field, photorealistic 8k."*
    *   **Uso:** Ideal para simular fotos "reales" capturadas con un smartphone, generando confianza y cercanía en el feed.

*   **Acción y Tensión Cinematográfica (Heist / Thriller):**
    *   **Prompt Base:** *"Gritty cinematic action, dynamic high-speed motion blur, moody low-key lighting, stark color contrast, handheld camera shake, intense suspenseful atmosphere, anamorphic lens flare, 4K."*
    *   **Uso:** Perfecto para historias de alto impacto, documentales de crimen real (True Crime) o narrativas aceleradas que necesitan adrenalina visual.

*   **Videoclip Musical (K-Pop / Coreografía Dinámica):**
    *   **Prompt Base:** *"High-energy music video aesthetic, vibrant neon lighting, dynamic tracking shots, perfect choreography sync, multiple rapid camera cuts, glossy 4K, stylish pop idols, futuristic LED wall background."*
    *   **Uso:** Especializado para secuencias de baile intenso, sincronización musical y estéticas de conciertos hiper-estilizadas.

*(Esta sección es un documento vivo y debe enriquecerse cada vez que descubramos un nuevo estilo visual potente).*
