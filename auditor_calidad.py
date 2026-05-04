import json
import os
from datetime import datetime

class InfobyteAuditor:
    def __init__(self):
        self.files = {
            'news': 'posts_content.json',
            'quizzes': 'quizzes_content.json',
            'spirit': 'frases_content.json'
        }
        self.report = []
        self.fixes_made = []
        
        # Diccionario de reemplazo seguro para evitar baneo
        self.safe_replacements = {
            'cure': 'support health in',
            'curar': 'apoyar el bienestar en',
            'miracle': 'breakthrough',
            'milagro': 'gran avance',
            'guaranteed': 'science-backed',
            'garantizado': 'respaldado por la ciencia',
            'magic': 'transformative',
            'mágico': 'transformativo',
            'lose weight': 'manage weight',
            'perder peso': 'gestionar el peso',
            'shocking': 'fascinating',
            'impactante': 'fascinante'
        }

    def auto_fix_text(self, text, lang='EN'):
        fixed_text = text
        for bad, good in self.safe_replacements.items():
            if bad in fixed_text.lower():
                # Reemplazo respetando mayúsculas básicas si es inicio de palabra
                fixed_text = fixed_text.replace(bad, good)
                fixed_text = fixed_text.replace(bad.capitalize(), good.capitalize())
                self.fixes_made.append(f"REPARADO: Se cambió '{bad}' por '{good}' para evitar baneo.")
        
        # Añadir Disclaimer si falta
        if lang == 'EN' and "consult" not in fixed_text.lower():
            fixed_text += "\n\n*Consult with a specialist for personalized advice."
            self.fixes_made.append("AVISO: Se añadió Disclaimer profesional en Inglés.")
        elif lang == 'ES' and "especialista" not in fixed_text.lower():
            fixed_text += "\n\n*Consulta con un especialista para asesoramiento personalizado."
            self.fixes_made.append("AVISO: Se añadió Disclaimer profesional en Español.")
            
        return fixed_text

    def clean_emojis_for_render(self, text, source_id):
        import re
        # Remover caracteres fuera del bloque común para evitar [missing glyphs] en Pillow
        cleaned = re.sub(r"[^\w\s\.,;:\!\?'\"\-\(\)áéíóúÁÉÍÓÚñÑüÜ]", "", text)
        cleaned = re.sub(r' +', ' ', cleaned).strip()
        if cleaned != text.strip():
            self.fixes_made.append(f"ESTERILIZACIÓN VISUAL: Emojis ocultos eliminados del texto en #{source_id}.")
        return cleaned

    def sanitize_visual_prompt(self, prompt, source_id):
        if not prompt or "SIN PROMPT" in prompt.upper() or len(prompt.strip()) < 10:
            self.report.append(f"ERROR CRITICO: #{source_id} — El prompt visual esta vacio o es invalido ('SIN PROMPT').")
            return "[ERROR: REQUIRES MANUAL PROMPT]"
            
        # Limpiar repeticiones del blindaje [NO TEXT]
        import re
        clean_prompt = re.sub(r"\[CRITICAL:.*?\]", "", prompt).replace("..", ".").strip()
        
        # Añadir siempre sufijo de blindaje una sola vez
        shielded_prompt = clean_prompt + ". [CRITICAL: ABSOLUTELY NO TEXT, NO LETTERS, NO TYPOGRAPHY. CLEAN AESTHETIC ONLY]."
        return shielded_prompt

    def audit_news(self):
        print(">>> Auditando y Reparando Noticias...")
        if not os.path.exists(self.files['news']): return
        
        with open(self.files['news'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            posts = data.get('posts', [])
        
        modified = False
        for p in posts:
            id_card = p.get('id', 'N/A')
            
            # ── REGLA 0: Sanear Prompt Visual ──────────────────────────────
            old_vp = p.get('visual_prompt', '')
            new_vp = self.sanitize_visual_prompt(old_vp, f"News {id_card}")
            if old_vp != new_vp:
                p['visual_prompt'] = new_vp
                modified = True
                
            # ── REGLA 0.5: Limpiar Título para Pillow ──────────────────────
            old_head = p.get('headline', '')
            new_head = self.clean_emojis_for_render(old_head, f"News {id_card} Headline")
            if old_head != new_head:
                p['headline'] = new_head
                modified = True
            
            # Obtener textos EN y ES
            post_en_data = p.get('postEN', '')
            if isinstance(post_en_data, dict):
                text_en = post_en_data.get('content', '') or str(post_en_data)
                authority = post_en_data.get('post_authority', '') or post_en_data.get('authority', '')
            else:
                text_en = str(post_en_data)
                authority = ''
            text_es = str(p.get('postES', ''))

            # ── REGLA 1: Fix de Texto (vocabulario prohibido + disclaimers) ─
            new_en = self.auto_fix_text(text_en, 'EN')
            if text_en != new_en:
                p['postEN'] = new_en if not isinstance(post_en_data, dict) else post_en_data
                if isinstance(post_en_data, dict): p['postEN']['content'] = new_en
                modified = True
            
            new_es = self.auto_fix_text(text_es, 'ES')
            if text_es != new_es:
                p['postES'] = new_es
                modified = True

            # ── REGLA 2: Completitud del Español vs Inglés ─────────────────
            len_en = len(new_en.split())
            len_es = len(new_es.split())
            if len_en > 0 and len_es > 0:
                ratio = len_es / len_en
                if ratio < 0.6:
                    self.report.append(
                        f"CALIDAD: News #{id_card} — El texto ES ({len_es} palabras) es menos del 60% del EN ({len_en} palabras). Revision recomendada."
                    )

            # ── REGLA 3: Prompt de Imagen — ¿Existe y tiene calidad? ────────
            vp_final = p.get('visual_prompt', '')
            if not vp_final or len(vp_final.strip()) < 40:
                self.report.append(f"ALERTA: News #{id_card} — SIN PROMPT VISUAL o muy corto. Debe generarse manualmente.")
            elif len(vp_final.strip()) < 120:
                self.report.append(f"CALIDAD: News #{id_card} — Prompt visual demasiado generico ({len(vp_final)} car.). Se recomienda mas detalle cinematico.")

            # ── REGLA 4: Hashtags en ambos idiomas ─────────────────────────
            if '#' not in new_en:
                self.report.append(f"ALERTA: News #{id_card} — Post EN no tiene HASHTAGS. Necesita al menos 3.")
            if '#' not in new_es:
                self.report.append(f"ALERTA: News #{id_card} — Post ES no tiene HASHTAGS. Necesita al menos 3.")

            # ── REGLA 5: Fuente / Autoridad / Referencia ───────────────────
            source_keywords = ['university', 'institute', 'journal', 'research', 'study', 'according', 'fact check', 'infobyte']
            has_source = any(kw in new_en.lower() for kw in source_keywords)
            if not has_source and not authority:
                self.report.append(f"ALERTA: News #{id_card} — Sin Fuente/Autoridad ni referencia academica detectada en el post EN.")

            # ── REGLA 6: Coherencia Título de Enganche vs Noticia ──────────
            # El headline (texto que va en la imagen) debe estar relacionado
            # con la noticia. Numeración correcta 1-28.
            news_title   = p.get('title', '')
            hook_text    = p.get('headline', '') or p.get('image_text_hook', '')

            # 6a. El hook debe existir y tener longitud razonable para la tarjeta
            if not hook_text or len(hook_text.strip()) < 5:
                self.report.append(
                    f"ALERTA: News #{id_card} (Imagen {id_card}/28) — SIN TITULO DE ENGANCHE para la imagen. Agregar campo 'headline'."
                )
            elif len(hook_text) > 60:
                self.report.append(
                    f"CALIDAD: News #{id_card} (Imagen {id_card}/28) — Titulo de enganche muy largo ({len(hook_text)} car.). "
                    f"Recortar a max 60 caracteres para que quepa en la tarjeta."
                )

            # 6b. Coherencia semántica: al menos 1 palabra clave del título
            #     debe aparecer en el hook (ignorando palabras comunes)
            import re
            stop_words = {'the','a','an','of','in','on','at','to','for','and','or','is',
                          'are','how','why','what','new','your','our','its','with','by','as'}
            title_words = {w.lower() for w in re.findall(r'\b\w+\b', news_title) if w.lower() not in stop_words and len(w) > 3}
            hook_lower  = hook_text.lower()
            matched     = [w for w in title_words if w in hook_lower]

            if news_title and hook_text and len(title_words) > 0 and len(matched) == 0:
                self.report.append(
                    f"COHERENCIA: News #{id_card} (Imagen {id_card}/28) — El enganche '{hook_text}' "
                    f"no comparte ninguna palabra clave con la noticia '{news_title}'. "
                    f"Posible desconexion imagen-contenido."
                )

        # ── REGLA 7: VARIEDAD DE GANCHOS (ANTI-REPETICIÓN) ─────────────
        all_hooks_es = [p.get('postES', '')[:40].lower() for p in posts]
        for start_phrase in set(all_hooks_es):
            count = all_hooks_es.count(start_phrase)
            if count > 2 and len(start_phrase.strip()) > 5:
                self.report.append(
                    f"ERROR CRITICO: REPETICION DETECTADA. La frase '{start_phrase.strip()}...' "
                    f"se repite en {count} noticias. El auditor RECHAZA este batch por falta de variedad."
                )


        if modified:
            with open(self.files['news'], 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("FIX: Se han auto-reparado problemas en Noticias.")


    def audit_quizzes(self):
        print(">>> Auditando y Reparando Quizzes (Reglas de Diseño)...")
        if not os.path.exists(self.files['quizzes']): return
        
        with open(self.files['quizzes'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            quizzes = data.get('quizzes', [])
        
        modified = False
        for i, q in enumerate(quizzes):
            quiz_num = i + 1
            
            # 0. Sanear Prompt Visual (Agente Auditor Visual)
            old_vp = q.get('visual_prompt', '')
            new_vp = self.sanitize_visual_prompt(old_vp, f"Quiz {quiz_num}")
            if old_vp != new_vp:
                q['visual_prompt'] = new_vp
                modified = True
                
            # 0.5. Limpiar Título para Pillow (Agente Anti-Missing Glyphs)
            old_head = q.get('headline', '')
            new_head = self.clean_emojis_for_render(old_head, f"Quiz {quiz_num} Headline")
            if old_head != new_head:
                q['headline'] = new_head
                modified = True
            
            # 1. Auditoría de Texto (Facebook Policy + Ghost Translations)
            old_en = q.get('postEN', '')
            if "disponible" in old_en.lower() or len(old_en) < 20:
                self.report.append(f"ERROR CRITICO: Quiz #{quiz_num} — El texto EN parece invalido o incompleto.")

            new_en = self.auto_fix_text(old_en, 'EN')
            if old_en != new_en:
                q['postEN'] = new_en
                modified = True
            
            old_es = q.get('postES', '')
            if "disponible" in old_es.lower() or len(old_es) < 20:
                self.report.append(f"ERROR CRITICO: Quiz #{quiz_num} — El texto ES tiene error de traduccion ('no disponible').")

            new_es = self.auto_fix_text(old_es, 'ES')
            if old_es != new_es:
                q['postES'] = new_es
                modified = True

            # 2. AUDITORÍA VISUAL (Etiquetas de Imagen)
            options = q.get('options', [])
            new_options = []
            for opt in options:
                # Asegurar Mayúsculas para Look Premium
                opt_fixed = opt.upper()
                
                # Validar Longitud para evitar que choquen sobre los círculos
                if len(opt_fixed) > 15:
                    self.report.append(f"Quiz #{quiz_num}: Opción '{opt_fixed}' es muy larga (>15 car.). Puede chocar en la imagen.")
                
                new_options.append(opt_fixed)
            
            # 3. AUDITORÍA DE COHERENCIA (Imagen vs. Post)
            for idx, opt in enumerate(new_options):
                num_label = f"{idx+1}"
                # Buscar si la palabra clave de la imagen está en el post del mismo número
                search_pattern = f"{num_label}"
                post_text = new_en.upper()
                
                # Verificamos si la opción (keyword) existe cerca de su número en el post
                if opt not in post_text:
                    self.report.append(f"COHERENCIA: Quiz #{quiz_num} - La opción '{opt}' no aparece en el texto del Post EN. ¡Posible confusión!")
                
                # Verificamos el post en español también
                post_text_es = new_es.upper()
                # Para español buscamos una coincidencia aproximada o alertamos para revisión
                if opt not in post_text_es:
                    # No es obligatorio que sea idéntico en ES pero sí recomendado
                    pass 

        if modified:
            with open(self.files['quizzes'], 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("FIX: Se han auto-reparado problemas visuales y de texto en Quizzes.")

    def audit_spirit(self):
        print(">>> Auditando y Reparando Apuntes del Alma (Spirit)...")
        if not os.path.exists(self.files['spirit']): return
        
        with open(self.files['spirit'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            phrases = data.get('phrases', [])
        
        modified = False
        for p in phrases:
            id_p = p.get('id', 'N/A')
            
            # 0. Sanear Prompt Visual
            old_vp = p.get('visual_prompt', '')
            new_vp = self.sanitize_visual_prompt(old_vp, f"Spirit {id_p}")
            if old_vp != new_vp:
                p['visual_prompt'] = new_vp
                modified = True
                
            # 0.5 Limpiar emojis del hook text para Pillow
            old_hook = p.get('hook_text', '')
            new_hook = self.clean_emojis_for_render(old_hook, f"Spirit {id_p} Hook")
            if old_hook != new_hook:
                p['hook_text'] = new_hook
                modified = True
            
            # 1. Validar Hook (Longitud + Formato Anti-Lista)
            hook = p.get('hook_text', '')
            if hook.count('\n') > 2:
                self.report.append(f"ERROR ESTRUCTURA: Spirit #{id_p} — El hook es una lista, no una frase. Reduciendo a la primera linea.")
                p['hook_text'] = hook.split('\n')[0].strip()
                modified = True
            elif len(hook) > 220:
                self.report.append(f"Spirit #{id_p}: Mensaje Gancho muy largo ({len(hook)} car.). Podría salirse de la caja de legibilidad.")
            
            # 2. Asegurar Disclaimer + Ghost Translations
            post_en = p.get('postEN', '')
            if "disponible" in post_en.lower():
                self.report.append(f"ERROR CRITICO: Spirit #{id_p} — Texto EN invalido.")

            new_en = self.auto_fix_text(post_en, 'EN')
            if post_en != new_en:
                p['postEN'] = new_en
                modified = True

            post_es = p.get('postES', '')
            if "disponible" in post_es.lower():
                self.report.append(f"ERROR CRITICO: Spirit #{id_p} — Traduccion ES invalida ('no disponible').")
                
        if modified:
            with open(self.files['spirit'], 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("FIX: Se han auto-reparado problemas en Spirit.")

    def run_full_audit(self):
        self.audit_news()
        self.audit_quizzes()
        self.audit_spirit()
        
        print("\n" + "="*70)
        print(f"REPORTE DE ACCIONES DEL AUDITOR - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("="*70)
        
        if self.fixes_made:
            print("LOG DE REPARACIONES (Auto-Fix):")
            for fix in set(self.fixes_made): 
                # Limpiar emojis para la terminal de Windows
                import re
                clean_fix = re.sub(r'[^\x00-\x7F]+', '', fix)
                print(f"- {clean_fix}")
        else:
            print("OK: No se requirieron reparaciones automaticas.")
            
        if self.report:
            print("\nPENDIENTE POR REVISION HUMANA:")
            for item in self.report:
                import re
                clean_item = re.sub(r'[^\x00-\x7F]+', '', item)
                print(f"! {clean_item}")
        
        print("="*70)



if __name__ == "__main__":
    auditor = InfobyteAuditor()
    auditor.run_full_audit()
