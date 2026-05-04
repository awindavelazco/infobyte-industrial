import json
import re

def update_hashtags():
    updates = [
        {
            "match": "economía de los Creadores",
            "tagsES": "\n\n#EconomiaDigital #CreadoresDeContenido #Negocios #Emprendimiento #Innovacion",
            "tagsEN": "\n\n#DigitalEconomy #ContentCreators #Business #Entrepreneurship #Innovation"
        },
        {
            "match": "tintes tóxicos del siglo XIX",
            "tagsES": "\n\n#HistoriaDeLaModa #Curiosidades #Textiles #SigloXIX #DatosInsolitos",
            "tagsEN": "\n\n#FashionHistory #Curiosities #Textiles #19thCentury #UnusualFacts"
        },
        {
            "match": "Hogares 100% Inteligentes",
            "tagsES": "\n\n#HogaresInteligentes #Domotica #Futuro #Innovacion #Tecnologia",
            "tagsEN": "\n\n#SmartHomes #HomeAutomation #Future #Innovation #Technology"
        },
        {
            "match": "revolución del vestido virtual",
            "tagsES": "\n\n#ModaDigital #Metaverso #RopaVirtual #Innovacion #TecnologiaEnLaModa",
            "tagsEN": "\n\n#DigitalFashion #Metaverse #VirtualClothing #Innovation #FashionTech"
        }
    ]
    
    with open('posts_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        title = item.get('title', '')
        for u in updates:
            if u["match"].lower() in title.lower():
                if "#" not in item.get('postES', ''):
                    item['postES'] = item.get('postES', '') + u["tagsES"]
                if "#" not in item.get('postEN', ''):
                    item['postEN'] = item.get('postEN', '') + u["tagsEN"]
                print(f"Hashtags añadidos a: {title.encode('ascii', 'ignore').decode('ascii')}")
                
    with open('posts_content.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    update_hashtags()
