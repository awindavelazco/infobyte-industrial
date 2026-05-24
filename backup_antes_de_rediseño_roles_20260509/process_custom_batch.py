import os
import json
import time
from engine_agentes import InfobyteEngine

def run_custom_batch():
    agentes = InfobyteEngine()
    
    # 21 Temas Existentes (para regenerar texto sin 'Ever felt')
    existing_topics = [
        {"category": "Teoría del Color y Psicología Visual", "title": "Chimerical Colors: Unveiling the Brain's 'Impossible' Hues", "topic": "Phenomenon where the brain perceives 'forbidden' colors beyond the normal spectrum."},
        {"category": "Dinero y Cómo Multiplicarlo", "title": "Invisible Hand: Behavioral Nudges in FinTech", "topic": "How FinTech apps use behavioral economics to nudge users towards better financial habits."},
        {"category": "Materiales e Innovación en la Moda", "title": "Bio-Fashion Unleashed: Lab-Grown Leather & Silk for Luxury", "topic": "Cellular agriculture creating molecularly identical leather and silk in labs without animals."},
        {"category": "Economía y Finanzas Personales", "title": "Neuro-Financial AI: Predicting Market Moods with Brainwaves", "topic": "Using AI to analyze aggregate brainwave data to predict market sentiment shifts."},
        {"category": "Remedios Naturales Comprobados", "title": "Ocean's Bio-Pharmacy: Marine Compounds for Novel Cures", "topic": "Discovering unique bioactive compounds from marine organisms for new medical treatments."},
        {"category": "Entomología", "title": "Cyborg Beetles: Remotely Controlled Bio-Robots", "topic": "Live beetles equipped with electronic backpacks for search and rescue missions."},
        {"category": "Moda y Tendencias Actuales", "title": "Chameleon Couture: The Dawn of Dye-Free Structural Color Textiles", "topic": "Textiles that change color using microscopic structures instead of chemical dyes."},
        {"category": "Alimentación Sana y Nutrición", "title": "Phage Therapy: Precision Gut Microbiome Tuning", "topic": "Using bacteriophages to specifically target harmful gut bacteria for personalized nutrition."},
        {"category": "Salud Natural y Bienestar", "title": "Metabolomics Unveiled: Decoding Your Unique Health Blueprint", "topic": "Analyzing metabolites to create a chemical footprint of an individual's health and lifestyle."},
        {"category": "Noticias Sociales y Virales", "title": "AI Empathy: The Rise of Emotional Support Companions", "topic": "AI algorithms designed to interpret emotional cues and provide support, reducing isolation."},
        {"category": "Robótica e IA", "title": "AI Architect: Robots Designing Themselves", "topic": "Generative design systems allowing robots to evolve their own physical forms for task efficiency."},
        {"category": "Biología Marina", "title": "Invisible Compass: How Marine Animals Navigate Earth's Magnetic Field", "topic": "Magnetoreception in sea turtles, sharks, and salmon for epic ocean migrations."},
        {"category": "Neurociencia", "title": "Your Brain's Nightly Detox: The Glymphatic System Revealed", "topic": "How the glymphatic system flushes metabolic waste during deep sleep to prevent neurodegeneration."},
        {"category": "Salud Natural y Bienestar", "title": "Fascia's Hidden Power: Unlocking Whole-Body Wellness", "topic": "The role of connective tissue (fascia) in mobility, pain relief, and overall structural health."},
        {"category": "Dinero y Cómo Multiplicarlo", "title": "Tokenized Assets: The New Frontier of Digital Wealth", "topic": "Fractional ownership of physical assets (real estate, art) through blockchain technology."},
        {"category": "Teoría del Color y Psicología Visual", "title": "Unseen Rainbows: How Animal Vision Reshapes Color Theory", "topic": "How animals perceive UV and polarized light, revealing a world hidden to human eyes."},
        {"category": "Salud Natural y Bienestar", "title": "Barefoot Benefits: The Electroceutical Power of Earthing", "topic": "The science of grounding (earthing) to reduce inflammation and improve sleep via electron transfer."},
        {"category": "Política General y Tendencias Globales", "title": "Algorithmic Sovereignty: AI's Rise in Global Governance", "topic": "Automation of public decision-making via AI and its implications for accountability."},
        {"category": "Biología Marina", "title": "Ocean's Puppet Masters: Parasites Manipulating Marine Life", "topic": "Parasites that hijack the nervous systems of marine animals to ensure their own life cycles."},
        {"category": "Remedios Naturales Comprobados", "title": "Phytomicrobiome Engineering: Unlocking Medicinal Plant Potential", "topic": "Manipulating plant microbiomes to boost production of therapeutic compounds."},
        {"category": "Teoría del Color y Psicología Visual", "title": "Synesthesia's Spectrum: When Sounds Have Color", "topic": "Neurological phenomenon where senses intertwine, allowing one to 'see' music or 'taste' words."}
    ]

    # 7 Temas Nuevos (Inspiración del usuario)
    new_topics = [
        {"category": "Robótica e IA", "title": "China's 50-Year Nuclear Battery: The Future of Endless Energy", "topic": "Successful start of mass production for a betavoltaic nuclear battery that lasts 50 years without charging."},
        {"category": "Remedios Naturales Comprobados", "title": "The Secret of Ricinoleic Acid: Castor Oil for Gut and Eye Health", "topic": "Ancient wisdom validated by science: how castor oil (aceite de ricino) supports intestine regeneration and eye health."},
        {"category": "Salud Natural y Bienestar", "title": "Energy Management: Science-Backed Habits to Revitalize Your Body", "topic": "A comparative guide on habits that drain energy versus those that boost vitality and cellular regeneration."},
        {"category": "Remedios Naturales Comprobados", "title": "Maca Root: The Inca Warrior Fuel and Adrenal Regulator", "topic": "Ancient root used by Inca warriors, now scientifically documented as a powerful adrenal and hormonal regulator."},
        {"category": "Salud Natural y Bienestar", "title": "Clove (Clavo de Olor): The Molecular Purger Against Parasites", "topic": "How eugenol in cloves acts as a 'molecular purger' to eliminate parasites and restore gut health."},
        {"category": "Robótica e IA", "title": "Wireless Electricity: Finland's Wireless Power Transmission Breakthrough", "topic": "Scientists in Finland successfully transmitted electric power through open air without physical wires or cables."},
        {"category": "Remedios Naturales Comprobados", "title": "Cartilage Regeneration: The German 'Holy Grail' for Joint Health", "topic": "Natural wisdom from the Black Forest regarding ginger and herbs for regenerating knee cartilage without surgery."}
    ]

    full_batch = existing_topics + new_topics
    all_posts = []

    for i, item in enumerate(full_batch):
        print(f"\n[SISTEMA] Procesando Noticia {i+1}/28: {item['title']}")
        
        # AGENTE COPYWRITER (Nuevo prompt sin repetición)
        copy_data = agentes.agent_copywriter(item, item['category'])
        
        # AGENTE VISUAL (Nuevo prompt de alta gama)
        visual_prompt = agentes.agent_visual(item)
        
        post_final = {
            "id": i + 1,
            "category": item['category'],
            "title": item['title'],
            "image_text_hook": copy_data['image_text_hook'],
            "postES": copy_data['postES'],
            "postEN": copy_data['postEN'],
            "generated_by_text": "Gemini (Cloud)",
            "generated_by_visual": "Gemini (Cloud)",
            "prompt": visual_prompt,
            "animationPrompt": "cinematic zoom",
            "image_path": ""
        }
        all_posts.append(post_final)
        
        # Guardado incremental para seguridad
        output_data = {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "posts": all_posts
        }
        with open('posts_content.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("\n[ÉXITO] Lote de 28 noticias completado y guardado en 'posts_content.json'")

if __name__ == "__main__":
    run_custom_batch()
