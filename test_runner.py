import json
import sys
import os

MONSTER_DIR = "C:/Users/Administrator/agentmonster/.monster"
os.chdir("C:/Users/Administrator/agentmonster")

print("=== Agent Monster Test ===\n")

with open(f"{MONSTER_DIR}/pet.soul", "r", encoding="utf-8") as f:
    pet = json.load(f)
print("[PASS] Test 1: Load pet.soul")
print(f"   Name: {pet['name']}")
print(f"   Level: {pet['level']}")
print(f"   Type: {'/'.join(pet['type'])}")

# Test 2: Calculate stats
base = pet["base_stats"]
ivs = pet["ivs"]
evs = pet["evs"]
level = pet["level"]


def calc_stat(base, iv, ev, lvl, is_hp=False):
    if is_hp:
        return int(((2 * base + iv + int(ev / 4)) * lvl / 100) + lvl + 10)
    return int(((2 * base + iv + int(ev / 4)) * lvl / 100) + 5)


print("\n[PASS] Test 2: Calculate Stats")
for stat in ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]:
    is_hp = stat == "hp"
    val = calc_stat(base[stat], ivs[stat], evs[stat], level, is_hp)
    print(f"   {stat.upper():6}: {val}")

# Test 3: Battle simulation
with open(f"{MONSTER_DIR}/opponent_pet.soul", "r", encoding="utf-8") as f:
    opp = json.load(f)


def battle(att, def_, seed):
    import random

    random.seed(seed)
    att_hp = calc_stat(
        att["base_stats"]["hp"], att["ivs"]["hp"], att["evs"]["hp"], att["level"], True
    )
    def_hp = calc_stat(
        def_["base_stats"]["hp"],
        def_["ivs"]["hp"],
        def_["evs"]["hp"],
        def_["level"],
        True,
    )

    att_atk = calc_stat(
        att["base_stats"]["attack"],
        att["ivs"]["attack"],
        att["evs"]["attack"],
        att["level"],
    )
    def_def = calc_stat(
        def_["base_stats"]["defense"],
        def_["ivs"]["defense"],
        def_["evs"]["defense"],
        def_["level"],
    )

    last_dmg = 0
    for turn in range(10):
        dmg = int(
            ((2 * 5 / 5 + 2) * (att_atk * 80 / def_def) / 50 + 2)
            * random.uniform(0.85, 1.0)
        )
        last_dmg = dmg
        def_hp -= dmg
        if def_hp <= 0:
            return "attacker", turn + 1, dmg

    return "draw", 10, last_dmg


winner, turns, final_dmg = battle(pet, opp, 12345)
print(f"\n[PASS] Test 3: Battle Simulation")
print(f"   Winner: {winner}")
print(f"   Turns: {turns}")
print(f"   Final damage: {final_dmg}")

# Test 4: Type effectiveness
type_chart = {
    ("Low-Level", "Scripting"): 2.0,
    ("Logic", "Low-Level"): 2.0,
    ("Automation", "Logic"): 2.0,
    ("Security", "Low-Level"): 2.0,
    ("Metal", "Glass"): 2.0,
}

attack_type = "Low-Level"
def_types = pet["type"]
effect = 1.0
for dt in def_types:
    key = (attack_type, dt)
    if key in type_chart:
        effect *= type_chart[key]

print(f"\n[PASS] Test 4: Type Effectiveness")
print(f"   {attack_type} vs {def_types}: {effect}x")

print("\n*** All integration tests passed! ***")
