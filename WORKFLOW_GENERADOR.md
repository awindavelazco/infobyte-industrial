# REGLAS MAESTRAS - PROYECTO INFOBYTE
**Misión:** Automatización de página de Facebook de ciencia en EE. UU. orientada a la monetización mediante credibilidad y rigor científico.

## 1. Reglas de Generación de Texto (Ollama)
- **Tono y Público:** Periodístico, estilo revista "Wired" o "Science". Público objetivo: Estados Unidos.
- **Verificabilidad Obligatoria:** Toda noticia DEBE citar una Universidad o Institución real.
- **Sección Fact Check:** Al final del post en inglés (`postEN`) siempre debe ir: `🔍 Fact Check: Search for '[Término]'`.
- **Firma de Marca:** Todos los posts terminan con la firma fija: `📡 INFOBYTE — Science. Verified.` y un CTA para pedir *Likes*.
- **Auditoría Interna:** El texto en español (`postES`) debe ser estrictamente una **traducción literal y exacta** del `postEN`. No se debe extender ni inventar información, sirve para que el administrador valide qué se subirá.

## 2. Reglas del Prompt Visual (Para Flow AI)
- **Bloqueo Anti-Filtros (Regla Crítica):** ESTRICTAMENTE PROHIBIDO describir rostros humanos o características físicas (edad, raza, género). Esto dispara la alerta de "Famosos" en Google Flow.
- **Precisión Científica Visual (Regla Crítica):** El objeto central descrito en el prompt de la imagen DEBE ser el análogo visual exacto de la investigación. Ya sea astronomía (telescopios/lentes), medicina (tejidos/ADN/microscopios), o tecnología (chips/circuitos), la IA debe especificar la terminología técnica correcta del objeto para evitar que las herramientas de generación cometan errores de contexto.
- **Composición Visual (Para evitar Sci-Fi):** Las imágenes deben enfocarse en manos con guantes, planos macro (close-ups extremos) del objeto científico o biológico, y el entorno de laboratorio.
- **Estética Facebook:** Formato obligatorio 4:5 (portrait). Iluminación dramática, fría/fluorescente con contrastes, poca profundidad de campo (fondo borroso).

## 3. Reglas de Publicación y Marca
- **Cero Repetición:** El script `use_ollama.py` debe inyectar siempre el contenido de `historico_noticias.txt` en el prompt para evitar repetir titulares.
- **Marca de Agua:** Todas las imágenes generadas por Flow deben ser procesadas localmente con el script `add_watermark.py` para incrustar `infobyte_logo.png` con 25% de tamaño y opacidad semi-transparente en la esquina inferior izquierda.
- **Despliegue:** La fuente de la verdad para previsualizar el contenido generado es la web app en Vercel.
