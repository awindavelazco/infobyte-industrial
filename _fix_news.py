import json
import time

with open('posts_content.json', encoding='utf-8') as f:
    data = json.load(f)

# Hashtags temáticos por noticia (basados en el título)
hashtag_map = {
    1:  ("#Neuroplasticity #BrainHealth #DefaultModeNetwork #Neuroscience #MindScience",
         "#Neuroplasticidad #SaludCerebral #Neurociencia #MenteSana #CienciaDelCerebro"),
    2:  ("#MarineBiology #OceanScience #Bioinformatics #SeaLife #MarineResearch",
         "#BiologiaMarina #CienciaDelOceano #VidaMarina #Bioinformatica #OceanosVivos"),
    3:  ("#AstronomyFacts #SpaceScience #Cosmology #Universe #ScienceDaily",
         "#AstronomiaCosmica #CienciaDelEspacio #Universo #Cosmologia #DescubrimientosEspaciales"),
    5:  ("#NaturalRemedies #HolisticHealth #WellnessScience #HerbalMedicine #NaturalHealing",
         "#RemediosNaturales #SaludHolistica #MedicinaHerbal #BienestarNatural #CuracionNatural"),
    13: ("#Robotics #AIInnovation #Technology #FutureOfTech #MachineIntelligence",
         "#Robotica #IntelenciaArtificial #Tecnologia #FuturoTecnologico #Innovacion"),
    16: ("#MedicalBreakthrough #HealthScience #Research #Medicine #BioTech",
         "#AvancesMedicos #CienciaDeLaSalud #Medicina #Investigacion #Biotecnologia"),
    18: ("#BrainComputerInterface #Neurology #FutureTech #BCITechnology #Neuroscience",
         "#InterfazCerebro #Neurologia #TecnologiaFutura #Neurociencia #CienciaAvanzada"),
}

for p in data.get('posts', []):
    pid = p.get('id')
    if pid in hashtag_map:
        tags_en, tags_es = hashtag_map[pid]
        post_en = p.get('postEN', '')
        post_es = p.get('postES', '')

        if '#' not in post_en:
            p['postEN'] = post_en.rstrip() + f"\n\n{tags_en}\n📡 INFOBYTE — Science. Verified."
            print(f"News #{pid}: Hashtags EN añadidos.")

        if '#' not in post_es:
            p['postES'] = post_es.rstrip() + f"\n\n{tags_es}\n📡 INFOBYTE — Ciencia. Verificada."
            print(f"News #{pid}: Hashtags ES añadidos.")

data['generated_at'] = time.strftime("%Y-%m-%d %H:%M:%S")

with open('posts_content.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nOK: Hashtags añadidos. Sin usar API.")
