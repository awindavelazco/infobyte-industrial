def limpiar_historial(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # Eliminar duplicados manteniendo el orden (los mas recientes al final)
        vistos = set()
        unicos = []
        for line in reversed(lines):
            if line.lower() not in vistos:
                vistos.add(line.lower())
                unicos.insert(0, line)
        
        # Quedarnos con los ultimos 60 para que el prompt no sea gigante
        final = unicos[-60:]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final) + '\n')
        
        print(f"Historial {filename} limpiado. De {len(lines)} a {len(final)} temas únicos.")
    except Exception as e:
        print(f"Error limpiando {filename}: {e}")

limpiar_historial('historico_noticias.txt')
limpiar_historial('historico_quizzes.txt')
