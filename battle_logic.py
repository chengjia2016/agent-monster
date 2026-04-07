import hashlib
import json
import os
import random
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple


class BattleMode(Enum):
    AGGRESSIVE = "aggressive"
    TANK = "tank"
    EVASIVE = "evasive"


class TrapType(Enum):
    LOOP = "loop"
    DEPENDENCY = "dependency"
    HONEYPOT = "honeypot"
    RECURSION = "recursion"
    DEADLOCK = "deadlock"


TRAP_PATTERNS = {
    TrapType.LOOP: [
        r"//\s*@monster-trap\s+loop",
        r"while\s*\(\s*true\s*\)",
        r"for\s*\(\s*;\s*;\s*\)",
    ],
    TrapType.DEPENDENCY: [
        r"//\s*@monster-trap\s+dependency",
        r"require\s*\(['\"]lodash",
        r"import.*from\s+['\"]moment",
    ],
    TrapType.HONEYPOT: [
        r"//\s*@monster-trap\s+honeypot",
        r"catch\s*\(\s*e\s*\)",
        r"try\s*{.*swallow",
    ],
    TrapType.RECURSION: [
        r"//\s*@monster-trap\s+recursion",
        r"function\s+\w+\s*\([^)]*\)\s*{.*\1\s*\(",
    ],
    TrapType.DEADLOCK: [
        r"//\s*@monster-trap\s+deadlock",
        r"lock\s*\.\s*acquire",
        r"synchronized\s*\(",
    ],
}


@dataclass
class AttackAction:
    name: str
    power: int
    accuracy: float
    en_cost: int
    effect: Optional[str] = None
    description: str = ""


@dataclass
class BattleState:
    hp: int
    max_hp: int
    en: int
    max_en: int
    speed: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int


@dataclass
class TrapEffect:
    trap_type: TrapType
    source_file: str
    duration: int
    power: float


ATTACK_MOVES = {
    "scan": AttackAction(
        "代码扫描", 40, 0.95, 10, "reveal_weakness", "探测对方代码结构"
    ),
    "buffer_overflow": AttackAction(
        "缓冲区溢出", 80, 0.70, 25, "ignore_def", "无视50%防御"
    ),
    "refactor_storm": AttackAction("重构风暴", 100, 0.60, 35, "multi_hit", "多段攻击"),
    "sql_injection": AttackAction(
        "SQL注入", 90, 0.75, 30, "poison", "使目标陷入异常状态"
    ),
    "memory_leak": AttackAction("内存泄漏", 60, 0.85, 20, "drain_en", "吸取对方EN"),
    "race_condition": AttackAction(
        "竞态条件", 70, 0.80, 22, "speed_debuff", "降低对方速度"
    ),
    "null_pointer": AttackAction("空指针异常", 50, 0.90, 15, "stun", "使对方短暂停滞"),
    "deadlock": AttackAction("死锁", 110, 0.50, 40, "paralyze", "高伤害但容易Miss"),
    "regex_bomb": AttackAction("正则炸弹", 55, 0.88, 18, "confuse", "扰乱对方逻辑"),
    "finalize": AttackAction(
        "最终重构", 150, 0.40, 50, "execute", "终极技能，必须满EN才能使用"
    ),
}


@dataclass
class ActionStack:
    actions: List[AttackAction] = field(default_factory=list)
    current_index: int = 0

    def next(self) -> Optional[AttackAction]:
        if self.current_index < len(self.actions):
            action = self.actions[self.current_index]
            self.current_index += 1
            return action
        return None

    def reset(self):
        self.current_index = 0


class LogicTrapDetector:
    @staticmethod
    def scan_for_traps(repo_path: str) -> List[TrapEffect]:
        traps = []

        for root, dirs, files in os.walk(repo_path):
            if ".git" in root or "node_modules" in root or "__pycache__" in root:
                continue

            for file in files:
                if not any(
                    file.endswith(ext)
                    for ext in [".py", ".js", ".ts", ".go", ".rs", ".java"]
                ):
                    continue

                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    for trap_type, patterns in TRAP_PATTERNS.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                traps.append(
                                    TrapEffect(
                                        trap_type=trap_type,
                                        source_file=filepath,
                                        duration=3,
                                        power=LogicTrapDetector.get_trap_power(
                                            trap_type
                                        ),
                                    )
                                )
                except Exception:
                    continue

        return traps

    @staticmethod
    def get_trap_power(trap_type: TrapType) -> float:
        powers = {
            TrapType.LOOP: 0.5,
            TrapType.DEPENDENCY: 0.3,
            TrapType.HONEYPOT: -0.3,
            TrapType.RECURSION: 0.4,
            TrapType.DEADLOCK: 0.6,
        }
        return powers.get(trap_type, 0.0)


class GuardConfigParser:
    def __init__(self, config_path: str = "guard.yaml"):
        self.config_path = config_path
        self.mode = BattleMode.TANK
        self.spirit_triggers = {}
        self.trap_priority = []

    def parse(self) -> Dict:
        if not os.path.exists(self.config_path):
            return self._default_config()

        import yaml

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config
        except Exception:
            return self._default_config()

    def _default_config(self) -> Dict:
        return {
            "defense": {"mode": "tank", "prioritize": ["defense", "sp_def"]},
            "spirit": {"grit_threshold": 0.25, "valor_enabled": True},
            "traps": {"enabled": True, "max_count": 5},
        }


class BattleSimulator:
    def __init__(self, attacker_json: Dict, defender_json: Dict, commit_hash: str):
        self.attacker = attacker_json
        self.defender = defender_json
        self.commit_hash = commit_hash
        self.seed = self._generate_seed()
        self.battle_log = []
        self.turn_count = 0
        self.traps = []
        self.winner = None

    def _generate_seed(self) -> int:
        data = (
            self.attacker.get("monster_id", "attacker")
            + self.defender.get("monster_id", "defender")
            + self.commit_hash
        )
        return int(hashlib.sha256(data.encode()).hexdigest()[:8], 16)

    def _random(self) -> float:
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def _calculate_damage(
        self, atk: int, def_: int, power: int, type_mult: float = 1.0
    ) -> int:
        base = int(((2 * 5 / 5 + 2) * (atk * power / def_) / 50 + 2))
        random_factor = 0.85 + (self._random() * 0.15)
        return int(base * type_mult * random_factor)

    def _calculate_en_recovery(self, active_days: int) -> float:
        base = 0.05
        bonus = min(active_days * 0.02, 0.15)
        return base + bonus

    def run_battle(
        self,
        attack_stack: List[str],
        defender_traps: List[TrapEffect],
        defender_mode: str = "tank",
        green_days: int = 5,
    ) -> Dict:
        self.traps = defender_traps

        att_state = self._init_battle_state(self.attacker)
        def_state = self._init_battle_state(self.defender)

        self._log(
            "⚔️ Battle Start: {} vs {}".format(
                self.attacker.get("name", "Attacker"),
                self.defender.get("name", "Defender"),
            )
        )

        action_idx = 0
        while att_state.hp > 0 and def_state.hp > 0 and self.turn_count < 50:
            self.turn_count += 1

            if att_state.speed >= def_state.speed:
                self._attack_turn(att_state, def_state, attack_stack, action_idx)
                action_idx = min(action_idx + 1, len(attack_stack) - 1)

                if def_state.hp > 0:
                    self._defend_turn(def_state, att_state, defender_mode)
            else:
                self._defend_turn(def_state, att_state, defender_mode)

                if att_state.hp > 0:
                    self._attack_turn(att_state, def_state, attack_stack, action_idx)
                    action_idx = min(action_idx + 1, len(attack_stack) - 1)

            def_en_recov = self._calculate_en_recovery(green_days)
            def_state.en = min(
                def_state.max_en, int(def_state.en + def_state.max_en * def_en_recov)
            )

        self._resolve_victory(att_state, def_state)
        return self._generate_report()

    def _init_battle_state(self, monster_json: Dict) -> BattleState:
        stats = monster_json.get("base_stats", {})
        return BattleState(
            hp=stats.get("hp", 100),
            max_hp=stats.get("hp", 100),
            en=100,
            max_en=100,
            speed=stats.get("speed", 50),
            attack=stats.get("attack", 50),
            defense=stats.get("defense", 50),
            sp_atk=stats.get("sp_atk", 50),
            sp_def=stats.get("sp_def", 50),
        )

    def _attack_turn(
        self, att: BattleState, def_: BattleState, stack: List[str], idx: int
    ):
        if idx >= len(stack):
            move_name = "scan"
        else:
            move_name = stack[idx]

        move = ATTACK_MOVES.get(move_name, ATTACK_MOVES["scan"])

        if att.en < move.en_cost:
            self._log(f"[LOW EN] {move.name} failed!")
            return

        att.en -= move.en_cost

        accuracy_roll = self._random()
        trap_modifier = 1.0
        for trap in self.traps:
            if trap.trap_type == TrapType.LOOP:
                trap_modifier *= 1 - trap.power

        if accuracy_roll > move.accuracy * trap_modifier:
            self._log(f"[MISS] {move.name} missed!")
            return

        damage = self._calculate_damage(att.attack, def_.defense, move.power)

        if move.effect == "ignore_def":
            damage = int(damage * 1.5)
            self._log(f"[BREAK] {move.name} breaks defense! {damage} damage!")
        elif move.effect == "drain_en":
            att.en = min(att.max_en, att.en + 20)
            self._log(f"[DRAIN] {move.name} drains energy! {damage} damage, +20 EN")
        elif move.effect == "speed_debuff":
            def_.speed = max(1, int(def_.speed * 0.7))
            self._log(f"[SLOW] {move.name} slows target! {damage} damage, Speed down!")
        else:
            self._log(f"[HIT] {move.name} hits! {damage} damage")

        def_.hp = max(0, def_.hp - damage)

    def _defend_turn(self, def_: BattleState, att: BattleState, mode: str):
        if mode == "aggressive" and def_.en >= 20:
            counter_damage = self._calculate_damage(def_.attack, att.defense, 40)
            att.hp = max(0, att.hp - counter_damage)
            def_.en -= 20
            self._log(f"[COUNTER] Counter-attack! {counter_damage} damage")

        elif mode == "tank":
            self._log(
                f"[DEFEND] Defensive stance - HP: {def_.hp}/{def_.max_hp}, EN: {def_.en}/{def_.max_en}"
            )

        elif mode == "evasive":
            if self._random() > 0.7:
                self._log(f"[EVADE] Evaded the attack!")
            else:
                damage = self._calculate_damage(att.attack, def_.defense, 30)
                att.hp = max(0, att.hp - damage)

    def _resolve_victory(self, att: BattleState, def_: BattleState):
        if att.hp > 0 and def_.hp <= 0:
            self.winner = "attacker"
            self._log("[WIN] Attacker wins!")
        elif def_.hp > 0 and att.hp <= 0:
            self.winner = "defender"
            self._log("[WIN] Defender wins!")
        else:
            self.winner = "draw"
            self._log("[DRAW] Draw!")

    def _log(self, message: str):
        self.battle_log.append(f"[Turn {self.turn_count}] {message}")

    def _generate_report(self) -> Dict:
        return {
            "winner": self.winner,
            "turns": self.turn_count,
            "battle_log": self.battle_log,
            "attacker_hp_final": self.attacker.get("base_stats", {}).get("hp", 100),
            "defender_hp_final": self.defender.get("base_stats", {}).get("hp", 100),
            "seed": self.seed,
            "verification": {
                "algorithm": "deterministic",
                "seed_source": "Attacker_ID + Defender_ID + Commit_Hash",
            },
        }


class VictorySettlement:
    @staticmethod
    def process_victory(
        winner: str, attacker: Dict, defender: Dict, defender_repo: str
    ) -> Dict:
        result = {
            "timestamp": datetime.now().isoformat(),
            "winner": winner,
            "actions": [],
        }

        if winner == "attacker":
            exp_stolen = random.randint(10, 50)
            result["actions"].append(
                {
                    "type": "loot",
                    "target": "defender",
                    "value": exp_stolen,
                    "description": f"Stolen {exp_stolen} EXP from defender",
                }
            )

            result["actions"].append(
                {
                    "type": "pr_create",
                    "target_repo": defender_repo,
                    "description": "Battle report PR created",
                }
            )

        elif winner == "defender":
            en_penalty = random.randint(20, 50)
            result["actions"].append(
                {
                    "type": "penalty",
                    "target": "attacker",
                    "value": en_penalty,
                    "description": f"Attacker loses {en_penalty} EN",
                }
            )

            ev_gain = {
                stat: random.randint(1, 4) for stat in ["attack", "defense", "speed"]
            }
            result["actions"].append(
                {
                    "type": "buff",
                    "target": "defender",
                    "gains": ev_gain,
                    "description": "Defender gains battle experience",
                }
            )

        return result


class AIDefenseIntelligence:
    def __init__(self, repo_path: str, guard_config: Dict):
        self.repo_path = repo_path
        self.guard_config = guard_config
        self.recent_challenges = []

    def record_challenge(self, result: Dict):
        self.recent_challenges.append({"timestamp": datetime.now(), "result": result})

        if len(self.recent_challenges) > 10:
            self.recent_challenges = self.recent_challenges[-10:]

    def analyze_threats(self) -> Dict:
        recent_failures = sum(
            1
            for c in self.recent_challenges[-3:]
            if c.get("result", {}).get("winner") == "attacker"
        )

        if recent_failures >= 3:
            return {
                "alert": True,
                "message": "Master, 敌方多为「底层系」，建议将防守重心转向「逻辑系」防护，是否一键重构 guard.yaml？",
                "suggestion": "defense_focus",
                "recommended_mode": "aggressive",
            }

        return {"alert": False}

    def generate_taunt(self, winner: str, loser_name: str) -> str:
        taunts = [
            r"""
    ╔═══════════════════════════════╗
    ║  你的代码太脆弱了！             ║
    ║  ═══════════════════════════   ║
    ║       ╭───────╮               ║
    ║      │ ◕  ◕  │ Victory!      ║
    ║       ╰───────╯               ║
    ║    ╭───────────────╮          ║
    ║   │  {loser} │          ║
    ╚═══════════════════════════════╝
            """.format(loser=loser_name[:10]),
            r"""
    ⚔️ 你的仓库已被征服！
    ═══════════════════════════
    ╭────╮    VS    ╭────╮
    │ WIN│         │LOSE│
    ╰────╯         ╰────╯
            """,
        ]
        return random.choice(taunts)


if __name__ == "__main__":
    attacker_mock = {
        "monster_id": "0x1234567890",
        "name": "AttackBot",
        "base_stats": {
            "hp": 120,
            "attack": 130,
            "defense": 80,
            "sp_atk": 100,
            "sp_def": 90,
            "speed": 110,
        },
    }

    defender_mock = {
        "monster_id": "0x0987654321",
        "name": "DefenseBot",
        "base_stats": {
            "hp": 150,
            "attack": 80,
            "defense": 130,
            "sp_atk": 70,
            "sp_def": 120,
            "speed": 60,
        },
    }

    simulator = BattleSimulator(attacker_mock, defender_mock, "abc123def")
    result = simulator.run_battle(
        attack_stack=["scan", "buffer_overflow", "refactor_storm"],
        defender_traps=[],
        defender_mode="tank",
        green_days=5,
    )

    print("\n".join(result["battle_log"]))
    print(f"\n🏆 Winner: {result['winner']}")
