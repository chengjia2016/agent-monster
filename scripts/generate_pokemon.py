#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Pokemon pets for Agent Monster from static data
"""

import json
import os

# First 50 Pokemon with their stats
POKEMON_DATA = [
    {"id": "001", "name": "Bulbasaur", "name_zh": "妙蛙种子", "types": ["Grass", "Poison"], "stats": {"hp": 45, "attack": 49, "defense": 49, "speed": 45, "sp_attack": 65, "sp_defense": 65}},
    {"id": "002", "name": "Ivysaur", "name_zh": "妙蛙草", "types": ["Grass", "Poison"], "stats": {"hp": 60, "attack": 62, "defense": 63, "speed": 60, "sp_attack": 80, "sp_defense": 80}},
    {"id": "003", "name": "Venusaur", "name_zh": "妙蛙花", "types": ["Grass", "Poison"], "stats": {"hp": 80, "attack": 82, "defense": 83, "speed": 80, "sp_attack": 100, "sp_defense": 100}},
    {"id": "004", "name": "Charmander", "name_zh": "小火龙", "types": ["Fire"], "stats": {"hp": 39, "attack": 52, "defense": 43, "speed": 65, "sp_attack": 60, "sp_defense": 50}},
    {"id": "005", "name": "Charmeleon", "name_zh": "火恐龙", "types": ["Fire"], "stats": {"hp": 58, "attack": 64, "defense": 58, "speed": 80, "sp_attack": 80, "sp_defense": 65}},
    {"id": "006", "name": "Charizard", "name_zh": "喷火龙", "types": ["Fire", "Flying"], "stats": {"hp": 78, "attack": 84, "defense": 78, "speed": 100, "sp_attack": 109, "sp_defense": 85}},
    {"id": "007", "name": "Squirtle", "name_zh": "杰尼龟", "types": ["Water"], "stats": {"hp": 44, "attack": 48, "defense": 65, "speed": 43, "sp_attack": 50, "sp_defense": 64}},
    {"id": "008", "name": "Wartortle", "name_zh": "卡咪龟", "types": ["Water"], "stats": {"hp": 59, "attack": 63, "defense": 80, "speed": 58, "sp_attack": 65, "sp_defense": 80}},
    {"id": "009", "name": "Blastoise", "name_zh": "水箭龟", "types": ["Water"], "stats": {"hp": 79, "attack": 83, "defense": 100, "speed": 78, "sp_attack": 85, "sp_defense": 105}},
    {"id": "010", "name": "Caterpie", "name_zh": "绿毛虫", "types": ["Bug"], "stats": {"hp": 45, "attack": 30, "defense": 35, "speed": 45, "sp_attack": 20, "sp_defense": 20}},
    {"id": "011", "name": "Metapod", "name_zh": "铁甲蛹", "types": ["Bug"], "stats": {"hp": 50, "attack": 20, "defense": 55, "speed": 30, "sp_attack": 25, "sp_defense": 25}},
    {"id": "012", "name": "Butterfree", "name_zh": "巴大蝶", "types": ["Bug", "Flying"], "stats": {"hp": 60, "attack": 45, "defense": 50, "speed": 70, "sp_attack": 90, "sp_defense": 80}},
    {"id": "013", "name": "Weedle", "name_zh": "独角虫", "types": ["Bug", "Poison"], "stats": {"hp": 40, "attack": 35, "defense": 30, "speed": 50, "sp_attack": 20, "sp_defense": 20}},
    {"id": "014", "name": "Kakuna", "name_zh": "铁壳蛹", "types": ["Bug", "Poison"], "stats": {"hp": 45, "attack": 25, "defense": 50, "speed": 35, "sp_attack": 25, "sp_defense": 25}},
    {"id": "015", "name": "Beedrill", "name_zh": "大针蜂", "types": ["Bug", "Poison"], "stats": {"hp": 65, "attack": 90, "defense": 40, "speed": 75, "sp_attack": 45, "sp_defense": 80}},
    {"id": "016", "name": "Pidgey", "name_zh": "波波", "types": ["Normal", "Flying"], "stats": {"hp": 40, "attack": 45, "defense": 40, "speed": 56, "sp_attack": 35, "sp_defense": 35}},
    {"id": "017", "name": "Pidgeotto", "name_zh": "比比鸟", "types": ["Normal", "Flying"], "stats": {"hp": 63, "attack": 60, "defense": 55, "speed": 71, "sp_attack": 50, "sp_defense": 50}},
    {"id": "018", "name": "Pidgeot", "name_zh": "大比鸟", "types": ["Normal", "Flying"], "stats": {"hp": 83, "attack": 80, "defense": 75, "speed": 101, "sp_attack": 70, "sp_defense": 70}},
    {"id": "019", "name": "Rattata", "name_zh": "小拉达", "types": ["Normal"], "stats": {"hp": 30, "attack": 56, "defense": 35, "speed": 72, "sp_attack": 25, "sp_defense": 35}},
    {"id": "020", "name": "Raticate", "name_zh": "拉达", "types": ["Normal"], "stats": {"hp": 55, "attack": 81, "defense": 60, "speed": 97, "sp_attack": 50, "sp_defense": 70}},
    {"id": "021", "name": "Spearow", "name_zh": "烈雀", "types": ["Normal", "Flying"], "stats": {"hp": 40, "attack": 60, "defense": 30, "speed": 70, "sp_attack": 31, "sp_defense": 31}},
    {"id": "022", "name": "Fearow", "name_zh": "大嘴雀", "types": ["Normal", "Flying"], "stats": {"hp": 65, "attack": 90, "defense": 65, "speed": 100, "sp_attack": 61, "sp_defense": 61}},
    {"id": "023", "name": "Ekans", "name_zh": "阿柏蛇", "types": ["Poison"], "stats": {"hp": 35, "attack": 60, "defense": 44, "speed": 55, "sp_attack": 40, "sp_defense": 54}},
    {"id": "024", "name": "Arbok", "name_zh": "阿柏怪", "types": ["Poison"], "stats": {"hp": 60, "attack": 85, "defense": 69, "speed": 80, "sp_attack": 65, "sp_defense": 79}},
    {"id": "025", "name": "Pikachu", "name_zh": "皮卡丘", "types": ["Electric"], "stats": {"hp": 35, "attack": 55, "defense": 40, "speed": 90, "sp_attack": 50, "sp_defense": 50}},
    {"id": "026", "name": "Raichu", "name_zh": "雷丘", "types": ["Electric"], "stats": {"hp": 60, "attack": 90, "defense": 55, "speed": 110, "sp_attack": 90, "sp_defense": 80}},
    {"id": "027", "name": "Sandshrew", "name_zh": "穿山鼠", "types": ["Ground"], "stats": {"hp": 50, "attack": 75, "defense": 85, "speed": 40, "sp_attack": 20, "sp_defense": 30}},
    {"id": "028", "name": "Sandslash", "name_zh": "穿山王", "types": ["Ground"], "stats": {"hp": 75, "attack": 100, "defense": 110, "speed": 65, "sp_attack": 45, "sp_defense": 55}},
    {"id": "029", "name": "Nidoran-F", "name_zh": "尼多兰", "types": ["Poison"], "stats": {"hp": 55, "attack": 47, "defense": 52, "speed": 41, "sp_attack": 40, "sp_defense": 40}},
    {"id": "030", "name": "Nidorina", "name_zh": "尼多娜", "types": ["Poison"], "stats": {"hp": 70, "attack": 62, "defense": 67, "speed": 56, "sp_attack": 55, "sp_defense": 55}},
    {"id": "031", "name": "Nidoqueen", "name_zh": "尼多后", "types": ["Poison", "Ground"], "stats": {"hp": 90, "attack": 92, "defense": 87, "speed": 76, "sp_attack": 75, "sp_defense": 85}},
    {"id": "032", "name": "Nidoran-M", "name_zh": "尼多朗", "types": ["Poison"], "stats": {"hp": 46, "attack": 57, "defense": 40, "speed": 50, "sp_attack": 40, "sp_defense": 40}},
    {"id": "033", "name": "Nidorino", "name_zh": "尼多力诺", "types": ["Poison"], "stats": {"hp": 61, "attack": 72, "defense": 57, "speed": 65, "sp_attack": 55, "sp_defense": 55}},
    {"id": "034", "name": "Nidoking", "name_zh": "尼多王", "types": ["Poison", "Ground"], "stats": {"hp": 81, "attack": 102, "defense": 77, "speed": 85, "sp_attack": 85, "sp_defense": 75}},
    {"id": "035", "name": "Clefairy", "name_zh": "皮皮", "types": ["Fairy"], "stats": {"hp": 70, "attack": 45, "defense": 48, "speed": 35, "sp_attack": 60, "sp_defense": 65}},
    {"id": "036", "name": "Clefable", "name_zh": "皮可西", "types": ["Fairy"], "stats": {"hp": 95, "attack": 70, "defense": 73, "speed": 60, "sp_attack": 95, "sp_defense": 90}},
    {"id": "037", "name": "Vulpix", "name_zh": "六尾", "types": ["Fire"], "stats": {"hp": 38, "attack": 41, "defense": 40, "speed": 65, "sp_attack": 50, "sp_defense": 65}},
    {"id": "038", "name": "Ninetales", "name_zh": "九尾", "types": ["Fire"], "stats": {"hp": 73, "attack": 76, "defense": 75, "speed": 100, "sp_attack": 81, "sp_defense": 100}},
    {"id": "039", "name": "Jigglypuff", "name_zh": "胖丁", "types": ["Normal", "Fairy"], "stats": {"hp": 115, "attack": 45, "defense": 45, "speed": 20, "sp_attack": 45, "sp_defense": 25}},
    {"id": "040", "name": "Wigglytuff", "name_zh": "胖可丁", "types": ["Normal", "Fairy"], "stats": {"hp": 90, "attack": 70, "defense": 45, "speed": 45, "sp_attack": 85, "sp_defense": 70}},
    {"id": "041", "name": "Zubat", "name_zh": "超音蝠", "types": ["Poison", "Flying"], "stats": {"hp": 40, "attack": 45, "defense": 35, "speed": 55, "sp_attack": 30, "sp_defense": 40}},
    {"id": "042", "name": "Golbat", "name_zh": "大嘴蝠", "types": ["Poison", "Flying"], "stats": {"hp": 75, "attack": 80, "defense": 70, "speed": 90, "sp_attack": 65, "sp_defense": 75}},
    {"id": "043", "name": "Oddish", "name_zh": "走路草", "types": ["Grass", "Poison"], "stats": {"hp": 45, "attack": 50, "defense": 55, "speed": 30, "sp_attack": 75, "sp_defense": 65}},
    {"id": "044", "name": "Gloom", "name_zh": "臭臭花", "types": ["Grass", "Poison"], "stats": {"hp": 60, "attack": 65, "defense": 70, "speed": 40, "sp_attack": 85, "sp_defense": 75}},
    {"id": "045", "name": "Vileplume", "name_zh": "霸王花", "types": ["Grass", "Poison"], "stats": {"hp": 75, "attack": 80, "defense": 85, "speed": 50, "sp_attack": 100, "sp_defense": 90}},
    {"id": "046", "name": "Paras", "name_zh": "派拉斯", "types": ["Bug", "Grass"], "stats": {"hp": 35, "attack": 70, "defense": 55, "speed": 25, "sp_attack": 45, "sp_defense": 55}},
    {"id": "047", "name": "Parasect", "name_zh": "派拉斯特", "types": ["Bug", "Grass"], "stats": {"hp": 60, "attack": 95, "defense": 80, "speed": 30, "sp_attack": 60, "sp_defense": 80}},
    {"id": "048", "name": "Venonat", "name_zh": "毛球", "types": ["Bug", "Poison"], "stats": {"hp": 60, "attack": 55, "defense": 50, "speed": 45, "sp_attack": 40, "sp_defense": 55}},
    {"id": "049", "name": "Venomoth", "name_zh": "末入蛾", "types": ["Bug", "Poison"], "stats": {"hp": 70, "attack": 65, "defense": 60, "speed": 90, "sp_attack": 90, "sp_defense": 75}},
    {"id": "050", "name": "Diglett", "name_zh": "地鼠", "types": ["Ground"], "stats": {"hp": 10, "attack": 55, "defense": 25, "speed": 95, "sp_attack": 35, "sp_defense": 45}},
]

def get_gene_type(types):
    """Determine gene type based on Pokemon type"""
    if "Fire" in types:
        return "creative"
    elif "Grass" in types:
        return "logic"
    elif "Electric" in types:
        return "speed"
    elif "Water" in types:
        return "logic"
    elif "Fighting" in types:
        return "creative"
    elif "Bug" in types:
        return "logic"
    elif "Poison" in types:
        return "lucky"
    else:
        return "lucky"

def create_pet(pokemon):
    """Convert Pokemon to pet format"""
    stats = pokemon["stats"]
    gene_type = get_gene_type(pokemon["types"])
    
    pet = {
        "metadata": {
            "name": pokemon["name"],
            "species": pokemon["name"],
            "birth_time": "2026-04-07T00:00:00.000000",
            "owner": "pokedex@agent-monster",
            "generation": 1,
            "evolution_stage": 1,
            "avatar": f"\n  {pokemon['name']}\n ╭───╮\n│ ◕‿◕ │\n╰─────╯\n  {pokemon['name_zh']}\n"
        },
        "stats": {
            "hp": {"base": stats["hp"], "iv": 15, "ev": 0, "exp": 0},
            "attack": {"base": stats["attack"], "iv": 15, "ev": 0, "exp": 0},
            "defense": {"base": stats["defense"], "iv": 15, "ev": 0, "exp": 0},
            "speed": {"base": stats["speed"], "iv": 15, "ev": 0, "exp": 0},
            "armor": {"base": stats["sp_defense"], "iv": 15, "ev": 0, "exp": 0},
            "quota": {"base": stats["sp_attack"], "iv": 15, "ev": 0, "exp": 0}
        },
        "genes": {
            gene_type: {"weight": 0.5, "source_commits": []},
            "lucky": {"weight": 0.3, "source_commits": []},
            "logic": {"weight": 0.1, "source_commits": []},
            "speed": {"weight": 0.1, "source_commits": []}
        },
        "battle_history": [],
        "signature": {
            "algorithm": "RSA-SHA256",
            "value": "",
            "keyid": ""
        }
    }
    return pet

def main():
    output_dir = "/root/pet/agent-monster-pet/demos/pokemon"
    os.makedirs(output_dir, exist_ok=True)
    
    all_pokemon = []
    
    for p in POKEMON_DATA:
        pet = create_pet(p)
        
        output_file = os.path.join(output_dir, f"{p['id']}-{p['name']}.soul")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pet, f, indent=2, ensure_ascii=False)
        
        total = sum(p["stats"].values())
        print(f"Created: {p['id']}-{p['name']} ({'/'.join(p['types'])}) Total: {total}")
        
        all_pokemon.append({
            "id": p["id"],
            "name": p["name"],
            "name_zh": p["name_zh"],
            "types": p["types"],
            "total": total
        })
    
    with open(os.path.join(output_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(all_pokemon, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created {len(POKEMON_DATA)} Pokemon pets!")
    print(f"   Location: {output_dir}/")

if __name__ == "__main__":
    main()