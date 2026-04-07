#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pokemon to Agent Monster Converter
Converts Pokemon data to our pet.soul format
"""

import json
import urllib.request
import urllib.parse
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

POKEMON_NAMES = {
    "妙蛙种子": "Bulbasaur",
    "妙蛙草": "Ivysaur", 
    "妙蛙花": "Venusaur",
    "小火龙": "Charmander",
    "火恐龙": "Charmeleon",
    "喷火龙": "Charizard",
    "杰尼龟": "Squirtle",
    "卡咪龟": "Wartortle",
    "水箭龟": "Blastoise",
    "绿毛虫": "Caterpie",
    "铁甲蛹": "Metapod",
    "巴大蝶": "Butterfree",
    "独角虫": "Weedle",
    "铁壳蛹": "Kakuna",
    "大针蜂": "Beedrill",
    "波波": "Pidgey",
    "比比鸟": "Pidgeotto",
    "大比鸟": "Pidgeot",
    "小拉达": "Rattata",
    "拉达": "Raticate",
    "烈雀": "Spearow",
    "大嘴雀": "Fearow",
    "阿柏蛇": "Ekans",
    "阿柏怪": "Arbok",
    "皮卡丘": "Pikachu",
    "雷丘": "Raichu",
    "穿山鼠": "Sandshrew",
    "穿山王": "Sandslash",
    "尼多兰": "Nidoran-F",
    "尼多娜": "Nidorina",
    "尼多后": "Nidoqueen",
    "尼多朗": "Nidoran-M",
    "尼多力诺": "Nidorino",
    "尼多王": "Nidoking",
    "皮皮": "Clefairy",
    "皮可西": "Clefable",
    "六尾": "Vulpix",
    "九尾": "Ninetales",
    "胖丁": "Jigglypuff",
    "胖可丁": "Wigglytuff",
    "超音蝠": "Zubat",
    "大嘴蝠": "Golbat",
    "走路草": "Oddish",
    "臭臭花": "Gloom",
    "霸王花": "Vileplume",
    "派拉斯": "Paras",
    "派拉斯特": "Parasect",
    "毛球": "Venonat",
    "末入蛾": "Dugtrio",
    "烈烈马": "Magnemite",
}

TYPE_COLORS = {
    "一般": "Normal",
    "火": "Fire", 
    "水": "Water",
    "电": "Electric",
    "草": "Grass",
    "冰": "Ice",
    "格斗": "Fighting",
    "毒": "Poison",
    "地面": "Ground",
    "飞行": "Flying",
    "超能力": "Psychic",
    "虫": "Bug",
    "岩石": "Rock",
    "幽灵": "Ghost",
    "龙": "Dragon",
    "恶": "Dark",
    "钢": "Steel",
    "妖精": "Fairy",
}

def fetch_pokemon_data(pokedex_id):
    """Fetch Pokemon data from GitHub"""
    url = f"https://raw.githubusercontent.com/42arch/pokemon-dataset-zh/main/data/pokemon/{urllib.parse.quote(pokedex_id)}"
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept-Encoding', 'utf-8')
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {pokedex_id}: {e}")
        return None

def convert_to_pet(data):
    """Convert Pokemon data to our pet format"""
    name_zh = data.get("name_zh", "")
    name_en = data.get("name_en", "Unknown")
    pokedex_id = data.get("pokedex_id", "000")
    
    forms = data.get("forms", [{}])[0] if data.get("forms") else {}
    stats_data = data.get("stats", [{}])[0].get("data", {}) if data.get("stats") else {}
    
    types = forms.get("types", [])
    type_en = [TYPE_COLORS.get(t, t) for t in types] if types else ["Normal"]
    
    hp = int(stats_data.get("hp", 50))
    attack = int(stats_data.get("attack", 50))
    defense = int(stats_data.get("defense", 50))
    speed = int(stats_data.get("speed", 50))
    sp_attack = int(stats_data.get("sp_attack", 50))
    sp_defense = int(stats_data.get("sp_defense", 50))
    
    total = hp + attack + defense + speed + sp_attack + sp_defense
    
    description = data.get("description", "")[:200]
    
    gene_type = "speed"
    if "火" in types or "Fire" in type_en:
        gene_type = "creative"
    elif "草" in types or "Grass" in type_en:
        gene_type = "logic"
    elif "电" in types or "Electric" in type_en:
        gene_type = "speed"
    elif "水" in types or "Water" in type_en:
        gene_type = "logic"
    elif "格斗" in types or "Fighting" in type_en:
        gene_type = "creative"
    else:
        gene_type = "lucky"
    
    pet = {
        "metadata": {
            "name": f"{name_en}",
            "species": name_en,
            "birth_time": "2026-04-07T00:00:00.000000",
            "owner": f"pokedex@pokedex",
            "generation": 1,
            "evolution_stage": 1,
            "avatar": f"\n  {name_en[:8]}\n ╭───╮\n│ ◕‿◕ │\n╰─────╯\n  🦶\n"
        },
        "stats": {
            "hp": {"base": hp, "iv": 15, "ev": 0, "exp": 0},
            "attack": {"base": attack, "iv": 15, "ev": 0, "exp": 0},
            "defense": {"base": defense, "iv": 15, "ev": 0, "exp": 0},
            "speed": {"base": speed, "iv": 15, "ev": 0, "exp": 0},
            "armor": {"base": sp_defense, "iv": 15, "ev": 0, "exp": 0},
            "quota": {"base": sp_attack, "iv": 15, "ev": 0, "exp": 0}
        },
        "genes": {
            gene_type: {"weight": 0.6, "source_commits": []},
            "lucky": {"weight": 0.2, "source_commits": []},
            "logic": {"weight": 0.1, "source_commits": []}
        },
        "battle_history": [],
        "signature": {
            "algorithm": "RSA-SHA256",
            "value": "",
            "keyid": ""
        }
    }
    
    return pet, type_en, total, description

def main():
    output_dir = "/root/pet/agent-monster-pet/demos/pokemon"
    os.makedirs(output_dir, exist_ok=True)
    
    pokemon_list = [
        ("0001-妙蛙种子.json", "001-Bulbasaur"),
        ("0002-妙蛙草.json", "002-Ivysaur"),
        ("0003-妙蛙花.json", "003-Venusaur"),
        ("0004-小火龙.json", "004-Charmander"),
        ("0005-火恐龙.json", "005-Charmeleon"),
        ("0006-喷火龙.json", "006-Charizard"),
        ("0007-杰尼龟.json", "007-Squirtle"),
        ("0008-卡咪龟.json", "008-Wartortle"),
        ("0009-水箭龟.json", "009-Blastoise"),
        ("0010-绿毛虫.json", "010-Caterpie"),
        ("0011-铁甲蛹.json", "011-Metapod"),
        ("0012-巴大蝶.json", "012-Butterfree"),
        ("0013-独角虫.json", "013-Weedle"),
        ("0014-铁壳蛹.json", "014-Kakuna"),
        ("0015-大针蜂.json", "015-Beedrill"),
        ("0016-波波.json", "016-Pidgey"),
        ("0017-比比鸟.json", "017-Pidgeotto"),
        ("0018-大比鸟.json", "018-Pidgeot"),
        ("0019-小拉达.json", "019-Rattata"),
        ("0020-拉达.json", "020-Raticate"),
        ("0021-烈雀.json", "021-Spearow"),
        ("0022-大嘴雀.json", "022-Fearow"),
        ("0023-阿柏蛇.json", "023-Ekans"),
        ("0024-阿柏怪.json", "024-Arbok"),
        ("0025-皮卡丘.json", "025-Pikachu"),
        ("0026-雷丘.json", "026-Raichu"),
        ("0027-穿山鼠.json", "027-Sandshrew"),
        ("0028-穿山王.json", "028-Sandslash"),
        ("0029-尼多兰.json", "029-Nidoran-F"),
        ("0030-尼多娜.json", "030-Nidorina"),
        ("0031-尼多后.json", "031-Nidoqueen"),
        ("0032-尼多朗.json", "032-Nidoran-M"),
        ("0033-尼多力诺.json", "033-Nidorino"),
        ("0034-尼多王.json", "034-Nidoking"),
        ("0035-皮皮.json", "035-Clefairy"),
        ("0036-皮可西.json", "036-Clefable"),
        ("0037-六尾.json", "037-Vulpix"),
        ("0038-九尾.json", "038-Ninetales"),
        ("0039-胖丁.json", "039-Jigglypuff"),
        ("0040-胖可丁.json", "040-Wigglytuff"),
        ("0041-超音蝠.json", "041-Zubat"),
        ("0042-大嘴蝠.json", "042-Golbat"),
        ("0043-走路草.json", "043-Oddish"),
        ("0044-臭臭花.json", "044-Gloom"),
        ("0045-霸王花.json", "045-Vileplume"),
        ("0046-派拉斯.json", "046-Paras"),
        ("0047-派拉斯特.json", "047-Parasect"),
        ("0048-毛球.json", "048-Venonat"),
        ("0049-末入蛾.json", "049-Venomoth"),
        ("0050-地鼠.json", "050-Diglett"),
    ]
    
    all_pokemon = []
    
    for filename, output_name in pokemon_list:
        print(f"Processing {filename}...")
        data = fetch_pokemon_data(filename)
        if data:
            pet, types, total, desc = convert_to_pet(data)
            
            output_file = os.path.join(output_dir, f"{output_name}.soul")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(pet, f, indent=2, ensure_ascii=False)
            
            print(f"  Created: {output_name} ({types[0]}) Total: {total}")
            all_pokemon.append({
                "name": output_name,
                "types": types,
                "total": total
            })
    
    print(f"\n✅ Created {len(all_pokemon)} Pokemon pets!")
    print(f"   Location: {output_dir}/")
    
    with open(os.path.join(output_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(all_pokemon, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()