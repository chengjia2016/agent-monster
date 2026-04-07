from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class Nature(Enum):
    HARDY = ("attack", "attack")
    LONELY = ("attack", "defense")
    BRAVE = ("attack", "speed")
    ADAMANT = ("attack", "sp_atk")
    NAUGHTY = ("attack", "sp_def")
    BOLD = ("defense", "attack")
    DOCILE = ("defense", "defense")
    RELAXED = ("defense", "speed")
    IMPISH = ("defense", "sp_atk")
    LAX = ("defense", "sp_def")
    TIMID = ("speed", "attack")
    HASTY = ("speed", "defense")
    JOLLY = ("speed", "sp_atk")
    NAIVE = ("speed", "sp_def")
    MODEST = ("sp_atk", "attack")
    MILD = ("sp_atk", "defense")
    QUIET = ("sp_atk", "speed")
    GENTLE = ("sp_atk", "sp_def")
    SASSY = ("sp_def", "attack")
    CAREFUL = ("sp_def", "sp_atk")
    RASH = ("sp_def", "speed")
    QUIRKY = ("sp_def", "sp_def")


TYPE_CHART = {
    ("Low-Level", "Scripting"): 2.0,
    ("Low-Level", "Logic"): 0.5,
    ("Low-Level", "Automation"): 1.0,
    ("Scripting", "Low-Level"): 0.5,
    ("Scripting", "Logic"): 2.0,
    ("Scripting", "Automation"): 1.0,
    ("Logic", "Low-Level"): 2.0,
    ("Logic", "Scripting"): 0.5,
    ("Logic", "Automation"): 1.0,
    ("Automation", "Logic"): 2.0,
    ("Automation", "Scripting"): 0.5,
    ("Automation", "Low-Level"): 1.0,
    ("Web", "Data"): 2.0,
    ("Web", "System"): 0.5,
    ("Data", "System"): 2.0,
    ("Data", "Web"): 0.5,
    ("System", "Network"): 2.0,
    ("System", "Security"): 0.5,
    ("Network", "Security"): 2.0,
    ("Network", "System"): 0.5,
    ("Security", "Low-Level"): 2.0,
    ("Security", "Network"): 0.5,
    ("Metal", "Glass"): 2.0,
    ("Metal", "Logic"): 0.5,
    ("Glass", "Metal"): 0.5,
    ("Glass", "Web"): 2.0,
}

ABILITIES = {
    "Recycle": {
        "desc": "使用攻击技能后，30%几率回复10%HP",
        "trigger": "after_attack",
        "effect": "heal_10_percent",
    },
    "Multithread": {
        "desc": "速度属性前3回合翻倍",
        "trigger": "first_3_turns",
        "effect": "speed_x2",
    },
    "OpenSource": {
        "desc": "同属性对战时，双方攻击+50%",
        "trigger": "same_type",
        "effect": "atk_boost",
    },
    "ExceptionCatch": {
        "desc": "致命一击时强制保留1HP（每场一次）",
        "trigger": "fatal_damage",
        "effect": "survive_1hp",
    },
    "CloudSync": {
        "desc": "每回合回复5%最大HP",
        "trigger": "every_turn",
        "effect": "regen_5_percent",
    },
    "VersionControl": {
        "desc": "受到伤害时，20%几率完全闪避",
        "trigger": "on_damage",
        "effect": "evade_chance",
    },
    "LazyLoad": {
        "desc": "SP.Atk和SP.Def交换数值",
        "trigger": "stat_calc",
        "effect": "swap_sp",
    },
    "Memoize": {
        "desc": "首次受到同类型攻击时，伤害-50%",
        "trigger": "repeat_attack",
        "effect": "memory_reduce",
    },
    "Pipeline": {
        "desc": "技能伤害+20%",
        "trigger": "damage_calc",
        "effect": "dmg_boost",
    },
    "HotReload": {
        "desc": "速度-30%，但攻击+50%",
        "trigger": "stat_calc",
        "effect": "trade_speed_atk",
    },
}

MOVES = {
    "Zero-Day_Exploit": {
        "type": "Security",
        "category": "special",
        "power": 120,
        "accuracy": 90,
        "pp": 5,
        "effect": "ignore_50_def",
    },
    "Hotfix": {
        "type": "Automation",
        "category": "status",
        "power": 0,
        "accuracy": 100,
        "pp": 10,
        "effect": "heal_25_percent",
    },
    "Refactor_Storm": {
        "type": "Low-Level",
        "category": "physical",
        "power": 100,
        "accuracy": 85,
        "pp": 10,
        "effect": "multi_hit",
    },
    "Memory_Dump": {
        "type": "System",
        "category": "special",
        "power": 80,
        "accuracy": 95,
        "pp": 15,
        "effect": "sp_atk_debuff",
    },
    "Buffer_Shield": {
        "type": "Data",
        "category": "status",
        "power": 0,
        "accuracy": 100,
        "pp": 20,
        "effect": "def_boost",
    },
    "API_Gateway": {
        "type": "Web",
        "category": "special",
        "power": 90,
        "accuracy": 100,
        "pp": 10,
        "effect": "speed_debuff",
    },
    "SQL_Injection": {
        "type": "Security",
        "category": "special",
        "power": 110,
        "accuracy": 80,
        "pp": 5,
        "effect": "poison",
    },
    "Docker_Container": {
        "type": "System",
        "category": "status",
        "power": 0,
        "accuracy": 100,
        "pp": 10,
        "effect": "sp_def_boost",
    },
}


@dataclass
class Monster:
    monster_id: str
    name: str
    type: List[str]
    nature: str
    ability: str
    base_stats: Dict[str, int]
    ivs: Dict[str, int]
    evs: Dict[str, int]
    level: int = 5
    moves: List[str] = field(default_factory=list)


def calculate_stat(base: int, iv: int, ev: int, level: int, nature_mod: float) -> int:
    return int((((2 * base + iv + int(ev / 4)) * level / 100) + 5) * nature_mod)


def calculate_hp(base: int, iv: int, ev: int, level: int) -> int:
    return int(((2 * base + iv + int(ev / 4)) * level / 100) + level + 10)


def get_nature_modifier(nature: str, stat: str) -> float:
    try:
        n = Nature[nature.upper()]
        if n.value[0] == stat:
            return 1.1
        elif n.value[1] == stat:
            return 0.9
        return 1.0
    except (KeyError, ValueError):
        return 1.0


def get_type_effectiveness(attack_type: str, defender_types: List[str]) -> float:
    multiplier = 1.0
    for def_type in defender_types:
        key = (attack_type, def_type)
        if key in TYPE_CHART:
            multiplier *= TYPE_CHART[key]
    return multiplier


def calculate_stats(monster: Monster) -> Dict[str, int]:
    stats = {}
    for stat in ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]:
        nature_mod = get_nature_modifier(monster.nature, stat)
        if stat == "hp":
            stats[stat] = calculate_hp(
                monster.base_stats[stat],
                monster.ivs[stat],
                monster.evs[stat],
                monster.level,
            )
        else:
            stats[stat] = calculate_stat(
                monster.base_stats[stat],
                monster.ivs[stat],
                monster.evs[stat],
                monster.level,
                nature_mod,
            )
    return stats


def calculate_level_from_exp(exp: int) -> int:
    if exp < 0:
        return 1
    for lvl in range(1, 101):
        if exp < lvl**3:
            return lvl
    return 100


def calculate_exp_needed(current_level: int, target_level: int) -> int:
    return sum(i**3 for i in range(current_level + 1, target_level + 1))


def render_radar_chart(stats: Dict[str, int], max_val: int = 255) -> str:
    labels = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]
    keys = ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]
    values = [stats.get(k, 0) for k in keys]

    lines = []
    max_bar = 12

    for ring in range(5, 0, -1):
        ring_val = int(max_val * ring / 5)
        line = f"{ring_val:3}│"
        for i, val in enumerate(values):
            char = "█" if val >= ring_val else "░"
            if i == 0:
                line += f"  {char}  │"
            else:
                line += f" {char} │"
        lines.append(line)

    lines.append(f"    ├────┼────┼────┼────┼────┼────┤")

    stat_vals = [stats[k] for k in keys]
    avg = sum(stat_vals) / len(stat_vals)

    result = [
        "",
        "           六维雷达图 (Radar Chart)",
        "         ╔═══════════════════════╗",
    ]

    for i, (label, val) in enumerate(zip(labels, values)):
        bar_len = min(int(val / max_val * 15), 15)
        bar = "█" * bar_len + "░" * (15 - bar_len)
        arrow = "→" if val >= avg else "←"
        result.append(f"  {label:4} │ {bar} │ {val:3} {arrow}")

    result.extend(
        ["         ╚═══════════════════════╝", f"         Average: {avg:.1f}", ""]
    )

    return "\n".join(result)


def print_monster_stats(monster: Monster):
    stats = calculate_stats(monster)

    print(f"\n{'═' * 50}")
    print(f"  {monster.name} (Lv.{monster.level})")
    print(f"  ID: {monster.monster_id}")
    print(f"  Type: {' / '.join(monster.type)}")
    print(f"  Nature: {monster.nature}")
    print(f"  Ability: {monster.ability}")
    print(f"{'═' * 50}")

    print("\n┌─ BASE STATS ──────────────────────────────────────┐")
    stat_names = [
        ("HP", "hp"),
        ("Attack", "attack"),
        ("Defense", "defense"),
        ("Sp.Atk", "sp_atk"),
        ("Sp.Def", "sp_def"),
        ("Speed", "speed"),
    ]

    for label, key in stat_names:
        base = monster.base_stats[key]
        iv = monster.ivs[key]
        ev = monster.evs[key]
        final = stats[key]

        bar = "█" * int(final / 20) + "░" * (12 - int(final / 20))
        print(f"│ {label:8} │ Base:{base:3} IV:{iv:2} EV:{ev:3} │ {bar} {final:3} │")

    print("└────────────────────────────────────────────────────┘")

    print("\n┌─ MOVES ───────────────────────────────────────────┐")
    for move in monster.moves[:4]:
        if move in MOVES:
            m = MOVES[move]
            print(f"│ {move:20} [{m['type']:10}] PWR:{m['power']:3} PP:{m['pp']:2} │")
    print("└────────────────────────────────────────────────────┘")


if __name__ == "__main__":
    bit_rex = Monster(
        monster_id="0xabcdef1234567890",
        name="Bit-Rex",
        type=["Low-Level", "Metal"],
        nature="Adamant",
        ability="Multithread",
        base_stats={
            "hp": 80,
            "attack": 135,
            "defense": 110,
            "sp_atk": 60,
            "sp_def": 95,
            "speed": 105,
        },
        ivs={
            "hp": 31,
            "attack": 28,
            "def": 25,
            "sp_atk": 10,
            "sp_def": 20,
            "speed": 31,
        },
        evs={"hp": 0, "attack": 252, "def": 0, "sp_atk": 0, "sp_def": 4, "speed": 252},
        level=50,
    )

    print_monster_stats(bit_rex)

    print("\n\n=== TYPE EFFECTIVENESS TEST ===")
    print(
        f"Low-Level vs Scripting: {get_type_effectiveness('Low-Level', ['Scripting'])}x"
    )
    print(
        f"Security vs Low-Level: {get_type_effectiveness('Security', ['Low-Level'])}x"
    )
