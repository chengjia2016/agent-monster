import json
import os
import sys

os.chdir("C:/Users/Administrator/agentmonster")
MONSTER_DIR = ".monster"

print("=" * 60)
print("       AGENT MONSTER - COMPREHENSIVE TEST SUITE")
print("=" * 60)

# Load test data
with open(f"{MONSTER_DIR}/pet.soul", "r", encoding="utf-8") as f:
    attacker = json.load(f)

with open(f"{MONSTER_DIR}/opponent_pet.soul", "r", encoding="utf-8") as f:
    defender = json.load(f)

from battle_logic import BattleSimulator, LogicTrapDetector, VictorySettlement

print("\n[TEST 1] Battle with different attack sequences")
print("-" * 60)

test_cases = [
    {"name": "Balanced", "stack": ["scan", "buffer_overflow", "refactor_storm"]},
    {"name": "Aggressive", "stack": ["deadlock", "sql_injection", "refactor_storm"]},
    {"name": "Defensive", "stack": ["scan", "scan", "memory_leak"]},
]

for tc in test_cases:
    sim = BattleSimulator(attacker, defender, "seed123")
    result = sim.run_battle(tc["stack"], [], "tank", 5)
    print(
        f"  {tc['name']:12} -> Winner: {result['winner']:8} | Turns: {result['turns']}"
    )

print("\n[TEST 2] Battle with different defense modes")
print("-" * 60)

defense_modes = ["aggressive", "tank", "evasive"]

for mode in defense_modes:
    sim = BattleSimulator(attacker, defender, "seed456")
    result = sim.run_battle(["scan", "buffer_overflow"], [], mode, 5)
    print(f"  Defense: {mode:12} -> Winner: {result['winner']:8}")

print("\n[TEST 3] Battle with trap effects")
print("-" * 60)

from battle_logic import TrapEffect, TrapType

traps = [
    TrapEffect(trap_type=TrapType.LOOP, source_file="test.py", duration=3, power=0.5),
    TrapEffect(
        trap_type=TrapType.DEPENDENCY, source_file="main.js", duration=2, power=0.3
    ),
]

sim = BattleSimulator(attacker, defender, "seed789")
result = sim.run_battle(["buffer_overflow"], traps, "aggressive", 3)
print(f"  Traps active: {len(traps)}")
print(f"  Winner: {result['winner']}")
sample = result["battle_log"][0] if result["battle_log"] else "N/A"
safe_sample = sample.encode("ascii", "replace").decode("ascii")
print(f"  Sample log: {safe_sample[:50]}...")

print("\n[TEST 4] Victory settlement")
print("-" * 60)

settlement = VictorySettlement.process_victory(
    "attacker", attacker, defender, "test/repo"
)
print(f"  Winner: {settlement['winner']}")
print(f"  Actions: {len(settlement['actions'])}")
for action in settlement["actions"]:
    print(f"    - {action['type']}: {action.get('description', 'N/A')}")

print("\n[TEST 5] Trap detection (scan current files)")
print("-" * 60)

traps_found = LogicTrapDetector.scan_for_traps(".")
print(f"  Traps found: {len(traps_found)}")

print("\n[TEST 6] Stat calculation comparison")
print("-" * 60)


def calc_stat(base, iv, ev, lvl, is_hp=False):
    if is_hp:
        return int(((2 * base + iv + int(ev / 4)) * lvl / 100) + lvl + 10)
    return int(((2 * base + iv + int(ev / 4)) * lvl / 100) + 5)


print("  CodeRex (Attacker):")
for stat in ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]:
    is_hp = stat == "hp"
    base = attacker["base_stats"][stat]
    iv = attacker["ivs"][stat]
    ev = attacker["evs"][stat]
    lvl = attacker["level"]
    val = calc_stat(base, iv, ev, lvl, is_hp)
    print(f"    {stat.upper():8}: Base={base:3} IV={iv:2} EV={ev:3} -> {val}")

print("\n  PyPuff (Defender):")
for stat in ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]:
    is_hp = stat == "hp"
    base = defender["base_stats"][stat]
    iv = defender["ivs"][stat]
    ev = defender["evs"][stat]
    lvl = defender["level"]
    val = calc_stat(base, iv, ev, lvl, is_hp)
    print(f"    {stat.upper():8}: Base={base:3} IV={iv:2} EV={ev:3} -> {val}")

print("\n[TEST 7] Type effectiveness matrix")
print("-" * 60)

from stat_calculator import get_type_effectiveness

attack_types = ["Low-Level", "Scripting", "Logic", "Automation", "Security", "Metal"]
defender_types = [
    ["Low-Level", "Metal"],
    ["Scripting", "Glass"],
    ["Logic", "Automation"],
]

print("Attack \\ Def | LowL/Met | Scp/Gls | Log/Auto")
print("-" * 50)
for atk in attack_types:
    row = f"  {atk:12} |"
    for def_types in defender_types:
        effect = get_type_effectiveness(atk, def_types)
        row += f" {effect:5.2f}x |"
    print(row)

print("\n" + "=" * 60)
print("       ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
