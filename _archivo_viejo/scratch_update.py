import json
import re
import os

new_posts = [
    {
        'id': 11,
        'category': 'Transporte',
        'title': 'Taxis Voladores: eVTOLs',
        'postES': '🚁✨ ¡EL CIELO ES LA VÍA: Los taxis voladores ya son realidad! ✨🚁\n\nSe ha verificado que múltiples misiones de prueba de aviones eléctricos de despegue y aterrizaje vertical (eVTOL) han sido un éxito. Para el final de la década, viajar en un dron gigante de pasajeros sobre ciudades como Dubai o París será algo cotidiano.\n\n🌐 Cero Emisiones: Estos vehículos funcionan 100% con baterías eléctricas, reduciendo drásticamente el ruido y la contaminación frente a los helicópteros tradicionales.\n\n💬 FUTURO: ¿Te subirías a un taxi volador autónomo para ir al trabajo y evitar el tráfico?\n\n#Transporte #eVTOL #Futuro #Tecnologia #CiudadesInteligentes #Innovacion',
        'postEN': '🚁✨ THE SKY IS THE ROAD: Flying taxis are now a reality! ✨🚁\n\nElectric Vertical Takeoff and Landing (eVTOL) vehicles have passed critical tests. Traveling in a giant passenger drone over cities like Dubai or Paris will soon be an everyday commute. Zero emissions, zero traffic.\n\n💬 QUESTION: Would you ride an autonomous flying taxi to avoid morning traffic?\n\n#Transport #eVTOL #FutureTech #SmartCities #Innovation',
        'prompt': 'A sleek futuristic quadcopter flying taxi soaring over a glowing futuristic metropolis at sunset. TITLE: THE SKY COMMUTE.'
    },
    {
        'id': 12,
        'category': 'Sostenibilidad',
        'title': 'Madera de Laboratorio: MIT',
        'postES': '🌳🔬 ¡FIN A LA DEFORESTACIÓN: Crean madera en el laboratorio sin talar árboles! 🔬🌳\n\nInvestigadores del MIT han verificado el éxito del crecimiento de tejidos vegetales en formas concretas (como mesas o sillas) utilizando células de la planta Zinnia. Esto significa que podemos cultivar muebles igual que cultivamos carne de laboratorio.\n\n🍃 Impacto Verde: Este proceso revolucionario permite crear madera con la forma final deseada, sin generar residuos y conservando nuestros bosques nativos intactos.\n\n💬 NATURALEZA: ¿Comprarías una mesa de madera real que fue cultivada en un laboratorio sin tocar ningún árbol?\n\n#Sostenibilidad #MIT #InnovacionVerde #Ciencia #Naturaleza #DeforestacionZero',
        'postEN': '🌳🔬 END TO DEFORESTATION: MIT creates lab-grown wood! 🔬🌳\n\nMIT researchers successfully grew plant tissues into specific shapes using Zinnia cells. We can now grow furniture like we grow lab meat. This zero-waste process produces real wood without cutting down a single tree.\n\n💬 QUESTION: Would you buy a real wood table grown entirely in a lab?\n\n#Sustainability #MIT #GreenTech #Science #Nature #ZeroDeforestation',
        'prompt': 'A glowing green laboratory flask where a solid piece of beautiful dark oak wood is naturally forming. TITLE: THE GROWN WOOD.'
    },
    {
        'id': 13,
        'category': 'Tecnología',
        'title': 'Baterías de Estado Sólido',
        'postES': '🔋🚗 ¡REVOLUCIÓN ELÉCTRICA: Baterías de estado sólido cambian el juego! 🚗🔋\n\nSe ha verificado un avance global: las nuevas baterías de estado sólido para vehículos eléctricos permiten cargas en menos de 10 minutos con autonomías que superan los 1,000 kilómetros. \n\n⚡ Adiós Litio Tradicional: Son más seguras (no se incendian), más compactas y resolverán por fin la ansiedad de rango de los coches eléctricos.\n\n💬 MOTOR: Con este avance, ¿cambiarías ya tu auto de gasolina por uno completamente eléctrico?\n\n#Evs #CochesElectricos #EstadoSolido #Baterias #Tecnologia #FuturoMotor',
        'postEN': '🔋🚗 ELECTRIC REVOLUTION: Solid-state batteries change the game! 🚗🔋\n\nA global breakthrough: solid-state batteries for EVs now allow 10-minute charging times and over 1,000 km of range. Safer, lighter, and finally ending range anxiety.\n\n💬 QUESTION: With this new battery tech, would you switch to an electric vehicle today?\n\n#EV #ElectricCars #SolidStateBattery #Technology #FutureMotor',
        'prompt': 'A futuristic transparent glowing vehicle battery radiating clean blue energy on a sleek dark surface. TITLE: THE ENDLESS CHARGE.'
    },
    {
        'id': 14,
        'category': 'Transporte',
        'title': 'Trenes de Hidrógeno',
        'postES': '🚄💧 ¡VAPOR DE AGUA: El primer tren que funciona solo con Hidrógeno! 💧🚄\n\nSe ha verificado la operación exitosa del Coradia iLint en Europa, el primer tren de pasajeros que funciona completamente con celdas de combustible de hidrógeno.\n\n🌍 Emisión Cero: El único escape de este tren gigante es puro vapor de agua condensada. Puede circular silenciosamente por vías sin electrificar, desplazando para siempre a los ruidosos y contaminantes trenes diésel.\n\n💬 VIAJES: ¿Te gustaría que los sistemas de transporte de tu ciudad respiraran solo vapor de agua?\n\n#Hidrogeno #TransporteSostenible #Trenes #InnovacionEco #FuturoCeroEmisiones',
        'postEN': '🚄💧 WATER VAPOR ONLY: The world\\'s first hydrogen-powered train! 💧🚄\n\nThe Coradia iLint is verified in Europe: a passenger train powered entirely by hydrogen fuel cells. Its only emission is pure water vapor. It silently replaces polluting diesel trains on non-electrified routes.\n\n💬 QUESTION: Would you like your city\\'s transit system to emit nothing but water vapor?\n\n#Hydrogen #SustainableTransit #Trains #EcoInnovation #ZeroEmissions',
        'prompt': 'A sleek white bullet train speeding past green mountains, leaving a trail of glowing blue water droplets. TITLE: THE HYDROGEN EXPRESS.'
    },
    {
        'id': 15,
        'category': 'Arquitectura',
        'title': 'Arquitectura Biomimética',
        'postES': '🏢🍃 ¡EDIFICIOS VIVOS: La arquitectura que imita a la naturaleza! 🍃🏢\n\nInspirados en termiteros y organismos celulares, nuevos rascacielos biomiméticos están demostrando poder autoregular su temperatura sin aire acondicionado, ahorrando hasta un 70% de energía.\n\n🌿 Ingeniería Natural: Adaptar el diseño de la naturaleza (biomímesis) para nuestras ciudades las convierte en ecosistemas más saludables y ultraeficientes. El concepto es simple: la naturaleza ya resolvió el problema.\n\n💬 CIUDADES: ¿Prefieres vivir en un rascacielos de cristal cerrado o en un edificio que respire como una planta?\n\n#Arquitectura #Biomimesis #DiseñoVerde #CiudadesDelFuturo #Sostenibilidad',
        'postEN': '🏢🍃 LIVING BUILDINGS: Architecture designed by nature! 🍃🏢\n\nInspired by termite mounds and cellular mechanics, biomimetic skyscrapers self-regulate temperatures without air conditioning, saving up to 70% of energy. Nature already solved our design problems; we just have to copy it.\n\n💬 QUESTION: Would you rather live in a closed glass skyscraper or an open building that breathes like a plant?\n\n#Architecture #Biomimicry #GreenDesign #FutureCities #Sustainability',
        'prompt': 'A towering futuristic skyscraper designed like an organic spiraling plant, glowing with green natural light. TITLE: THE LIVING TOWER.'
    },
    {
        'id': 16,
        'category': 'Agricultura',
        'title': 'Granjas Verticales con IA',
        'postES': '🥬🤖 ¡COSECHA DEL FUTURO: Granjas verticales impulsadas por IA! 🤖🥬\n\nSe ha verificado el rendimiento masivo de instalaciones agrícolas urbanas que cultivan alimentos hacia arriba, en estantes iluminados por LED, y manejados 100% por Inteligencia Artificial.\n\n💧 Ahorro: Utilizan 95% menos agua que la agricultura tradicional, no usan pesticidas y pueden producir 300 veces más comida por metro cuadrado.\n\n💬 COMIDA: ¿Consumirías verduras que nunca han tocado el sol ni la tierra tradicional, pero son perfectas y sanas?\n\n#GranjasVerticales #AgriTech #InteligenciaArtificial #ComidaDelFuturo #Sostenibilidad',
        'postEN': '🥬🤖 FUTURE HARVEST: AI-powered vertical farms! 🤖🥬\n\nUrban agricultural facilities stacking crops to the ceiling under LED lights and managed 100% by AI are yielding massive results. They use 95% less water, no pesticides, and produce 300x more food per square meter.\n\n💬 QUESTION: Would you eat perfect, healthy vegetables that have never touched traditional soil or the sun?\n\n#VerticalFarming #AgriTech #ArtificialIntelligence #FutureFood #Sustainability',
        'prompt': 'A futuristic indoor vertical farm bathed in glowing pink and purple ultraviolet LED lights growing lush green lettuce. TITLE: THE NEON HARVEST.'
    },
    {
        'id': 17,
        'category': 'Materiales',
        'title': 'Bioplástico de Algas Marinas',
        'postES': '🌊♻️ ¡FIN AL POLIETILENO: El plástico de algas marinas que puedes incluso comer! ♻️🌊\n\nSe ha verificado el éxito de un nuevo embalaje derivado de extracto de algas que desaparece de forma natural. Funciona exactamente igual que el plástico para empacar agua o alimentos, pero es biodegradable en semanas.\n\n🌍 Adiós a la Basura: Si este material termina en el océano, se disuelve o sirve de comida para los peces. La solución definitiva al microplástico.\n\n💬 AMBIENTE: ¿Cuánto más pagarías por un envase que sabes con certeza que no dañará el océano?\n\n#Bioplastico #Algas #MaterialesInnovadores #CeroResiduos #OceanosLimpios #Innovacion',
        'postEN': '🌊♻️ END OF PLASTIC: The seaweed packaging you can even eat! ♻️🌊\n\nA new seaweed extract packaging works just like plastic but biodegrades completely in weeks. If it ends up in the ocean, it naturally dissolves or becomes fish food. The ultimate solution to microplastics is verified.\n\n💬 QUESTION: Would you pay extra for packaging that you know for certain won\\'t harm the ocean?\n\n#Bioplastic #Seaweed #ZeroWaste #CleanOceans #EcoInnovation',
        'prompt': 'A futuristic transparent biodegradable capsule resembling a water orb resting on a clean white sandy beach. TITLE: THE WATER DROP.'
    },
    {
        'id': 18,
        'category': 'Medicina',
        'title': 'Primer Hospital de Inteligencia Artificial',
        'postES': '🏥🤖 ¡EL PRIMER HOSPITAL DE IA: Médicos virtuales que tratan miles de pacientes al día! 🤖🏥\n\nEn China se ha inaugurado el concepto \"Agent Hospital\", un entorno donde médicos y enfermeras dirigidos por modelos de IA pueden tratar hasta 10,000 pacientes simulados y reales en cuestión de días.\n\n💊 Precisión: Estos doctores de IA procesan historiales médicos complejos, diagnósticos y recetan con una precisión del 93%, superando a muchos especialistas novatos.\n\n💬 SALUD: ¿Confiarías tu diagnóstico médico 100% a una supercomputadora sin intervención médica humana?\n\n#SaludDigital #AgentHospital #InteligenciaArtificial #Medicina #FuturoMedico #Innovacion',
        'postEN': '🏥🤖 THE FIRST AI HOSPITAL: Virtual doctors treating thousands! 🤖🏥\n\nChina has introduced \"Agent Hospital\", where AI-driven doctors and nurses treat up to 10,000 patients in days. Processing massive medical histories, they diagnose and prescribe with 93% accuracy, surpassing many human specialists.\n\n💬 QUESTION: Would you trust your medical diagnosis entirely to a supercomputer without a human doctor?\n\n#DigitalHealth #AIHospital #ArtificialIntelligence #Medicine #FutureHealth',
        'prompt': 'A futuristic bright hospital corridor where a glowing digital hologram of a doctor examines floating medical charts. TITLE: THE AI CLINIC.'
    },
    {
        'id': 19,
        'category': 'Energía',
        'title': 'Récord de Fusión Nuclear',
        'postES': '☀️🔋 ¡UN SOL EN LA TIERRA: Nuevo récord mundial en Fusión Nuclear! 🔋☀️\n\nSe ha verificado un nivel récord de energía generada y sostenida utilizando reactores Tokamak (fusión). Este es el proceso físico que ilumina las estrellas.\n\n⚡ Energía Infinita: Al contrario de la fisión (las nucleares de hoy), la fusión no deja residuos radiactivos letales y funciona con agua. Estamos a un solo paso de obtener energía inagotable y completamente limpia para todo el planeta.\n\n💬 FUTURO: ¿Crees que la fusión nuclear salvará a la humanidad de la crisis climática?\n\n#FusionNuclear #EnergiaInfinita #Ciencia #Tokamak #Sostenibilidad #FuturoLimpio',
        'postEN': '☀️🔋 A SUN ON EARTH: New world record in Nuclear Fusion! 🔋☀️\n\nA new record for sustained energy generation using Tokamak fusion reactors has been verified. Unlike current nuclear fission, fusion creates no lethal radioactive waste and runs on water. Limitless, clean energy for the entire planet is approaching.\n\n💬 QUESTION: Do you believe nuclear fusion will save humanity from the climate crisis?\n\n#NuclearFusion #LimitlessEnergy #Science #Tokamak #CleanFuture',
        'prompt': 'A massive circular futuristic reactor glowing with a blinding golden ring of plasma simulating a captive sun. TITLE: THE CAPTIVE STAR.'
    },
    {
        'id': 20,
        'category': 'Salud',
        'title': 'Bioimpresión 3D de Órganos Humanos',
        'postES': '🫀🖨️ ¡LLEGAN LOS REPUESTOS: La Bioimpresión 3D celular ahora es realidad! 🖨️🫀\n\nInvestigadores han verificado la capacidad de usar \"tintas biológicas\" para imprimir por capas tejido cardíaco humano vivo que late de forma independiente.\n\n🩸 Fin a las Listas de Espera: En un futuro muy cercano, si necesitas un trasplante, los médicos imprimirán un corazón o un riñón de reemplazo usando tus propias células, reduciendo a cero el riesgo de rechazo.\n\n💬 CIENCIA: ¿Qué órgano te impresiona más pensar que el ser humano sea capaz de intentar \"imprimir\"?\n\n#Bioimpresion #Salud #Corazon3D #InnovacionMedica #Futuro #Biotecnologia',
        'postEN': '🫀🖨️ BODY PARTS ON DEMAND: 3D Bioprinting is reality! 🖨️🫀\n\nResearchers have verified the use of \"bio-inks\" to 3D print living human heart tissue that beats independently. In the near future, replacement organs will be printed using your own cells, ending organ waitlists and rejection risks.\n\n💬 QUESTION: Which human organ impresses you the most to think scientists can \"print\"?\n\n#BioPrinting #Health #3DHeart #MedicalInnovation #BioTech',
        'prompt': 'A precise futuristic glowing 3D bioprinter slowly building a luminous red human heart out of digital cells. TITLE: THE PRINTED HEART.'
    },
    {
        'id': 21,
        'category': 'Medio Ambiente',
        'title': 'Limpieza Oceánica Autónoma',
        'postES': '🌊🚢 ¡LOS MARES RESPIRAN: Mega-Sistemas autónomos recogen la basura del Pacífico! 🚢🌊\n\nEl proyecto \"The Ocean Cleanup\" ha verificado la rotunda eficacia de sus sistemas flotantes a gran escala para atrapar miles de toneladas de plásticos del Gran Parche de Basura del Pacífico.\n\n🐠 Tecnología Salvadora: Barreras masivas en forma de U concentran la contaminación mientras fuerzas marítimas naturales empujan la basura, evitando atrapar peces o fauna. La meta: Eliminar el 90% del plástico marino.\n\n💬 OCÉANOS: ¿Crees que lograremos un mundo con océanos de agua prístina para nuestras futuras generaciones?\n\n#TheOceanCleanup #MedioAmbiente #OceanosLibres #TecnologiaEcológica #Innovacion #MaresLimpios',
        'postEN': '🌊🚢 THE SEAS BREATHE: Mega-systems sweep the Pacific garbage patch! 🚢🌊\n\n“The Ocean Cleanup” verified the massive success of their large-scale autonomous floating systems, catching thousands of tons of plastic. Massive U-shaped barriers concentrate pollution safely. The goal: remove 90% of marine plastic.\n\n💬 QUESTION: Do you believe we will achieve a pristine ocean for future generations?\n\n#OceanCleanup #Environment #CleanSeas #EcoTechnology #SaveTheEarth',
        'prompt': 'A massive clean, glowing high-tech barrier floating on deep blue ocean waves scooping up pollution. TITLE: THE SEA CLEANSING.'
    }
]

# Read existing JSON
with open('posts_content.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Append to JSON
posts.extend(new_posts)
with open('posts_content.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

# Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the array `const newsData = [` and append our items before the closing `];`
parts = content.split('];', 1)
if len(parts) == 2:
    # Build JS string for the new objects
    js_objects = []
    for item in new_posts:
        obj_str = f'''  {{
    category: "{item['category']}",
    title: "{item['title']}",
    postES: {json.dumps(item['postES'], ensure_ascii=False)},
    postEN: {json.dumps(item['postEN'], ensure_ascii=False)},
    prompt: "{item['prompt']}"
  }}'''
    js_objects.append(obj_str)
    
    first_part = parts[0].rstrip()
    if not first_part.endswith(','):
        first_part += ','
    
    new_content = first_part + '\n' + ',\n'.join(js_objects) + '\n];' + parts[1]
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Files Updated Successfully!")
else:
    print("Failed to find ]; in script.js")
