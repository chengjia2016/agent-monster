import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

GITHUB_MAP_CONFIG = {
    "level_thresholds": [0, 10, 50, 100, 250, 500, 1000, 2500, 5000, 10000],
    "exp_per_line": 0.5,
    "exp_per_test": 2.0,
    "exp_per_doc": 0.3,
    "en_regen_base": 10,
    "green_ratio_threshold": 0.7,
    "defense_coverage_cap": 80,
    "defense_bonus_per_percent": 0.5,
    "accuracy_linter_cap": 95,
    "accuracy_bonus_per_percent": 0.3,
    "skill_unlock_stars": [10, 50, 100],
    "evolution_merge_threshold": 5,
    "conflict_resolution_bonus": 15,
}


@dataclass
class GitHubMetrics:
    total_commits: int = 0
    recent_commits_7d: int = 0
    green_ratio: float = 0.0
    test_coverage: float = 0.0
    linter_accuracy: float = 100.0
    repo_stars: int = 0
    tech_stack: List[str] = field(default_factory=list)
    fix_keywords_count: int = 0
    major_version_commits: int = 0


def get_git_config(key: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "config", "--get", key], capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def run_git_command(args: List[str], cwd: str = ".") -> str:
    try:
        result = subprocess.run(
            ["git"] + args, capture_output=True, text=True, timeout=30, cwd=cwd
        )
        return result.stdout.strip()
    except Exception:
        return ""


def calculate_level(total_commits: int) -> Tuple[int, int, int]:
    thresholds = GITHUB_MAP_CONFIG["level_thresholds"]
    for i, thresh in enumerate(thresholds):
        if total_commits < thresh:
            current_level = max(1, i)
            exp_current = thresholds[i - 1] if i > 0 else 0
            exp_next = thresh
            exp_have = total_commits - exp_current
            exp_need = exp_next - exp_current
            return current_level, exp_have, exp_need
    return len(thresholds), 0, 0


def calculate_en_regen(green_ratio: float) -> int:
    base = GITHUB_MAP_CONFIG["en_regen_base"]
    if green_ratio >= GITHUB_MAP_CONFIG["green_ratio_threshold"]:
        return int(base * (1 + (green_ratio - 0.7) * 2))
    return base


def calculate_defense_from_coverage(coverage: float) -> float:
    base_defense = 50.0
    capped = min(coverage, GITHUB_MAP_CONFIG["defense_coverage_cap"])
    bonus = (capped / GITHUB_MAP_CONFIG["defense_coverage_cap"]) * 20
    return base_defense + bonus


def calculate_accuracy_from_linter(accuracy: float) -> float:
    base_accuracy = 70.0
    capped = min(accuracy, GITHUB_MAP_CONFIG["accuracy_linter_cap"])
    bonus = (capped / GITHUB_MAP_CONFIG["accuracy_linter_cap"]) * 15
    return base_accuracy + bonus


def analyze_commit_history(days: int = 7) -> GitHubMetrics:
    metrics = GitHubMetrics()

    all_commits = run_git_command(["rev-list", "--all", "--count"])
    metrics.total_commits = int(all_commits) if all_commits else 0

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = run_git_command(["log", f"--since={since}", "--oneline"])
    metrics.recent_commits_7d = len(recent.split("\n")) if recent else 0

    commit_dates = run_git_command(
        [
            "log",
            f"--since={(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')}",
            "--format=%ad",
            "--date=short",
        ]
    )
    if commit_dates:
        dates = [d for d in commit_dates.split("\n") if d]
        unique_days = len(set(dates))
        metrics.green_ratio = min(unique_days / days, 1.0)

    fix_pattern = re.compile(r"\b(fix|bug|fix|repair|patch|hack|workaround)\b", re.I)
    fix_output = run_git_command(["log", f"--all", "--grep=fix", "--oneline"])
    if fix_output:
        metrics.fix_keywords_count = len([l for l in fix_output.split("\n") if l])

    major_pattern = re.compile(r"^v?([0-9]+)\.", re.I)
    tags = run_git_command(["tag", "-l", "v*"])
    if tags:
        for tag in tags.split("\n"):
            if major_pattern.search(tag):
                metrics.major_version_commits += 1

    return metrics


def detect_tech_stack() -> List[str]:
    stack = []

    files = os.listdir(".")
    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cpp": "C++",
        ".rb": "Ruby",
        ".php": "PHP",
        ".swift": "Swift",
        ".kt": "Kotlin",
    }

    counts = {}
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in ext_map:
            lang = ext_map[ext]
            counts[lang] = counts.get(lang, 0) + 1

    sorted_langs = sorted(counts.items(), key=lambda x: -x[1])
    stack = [lang for lang, _ in sorted_langs[:3]]

    if "package.json" in files:
        stack.append("npm")
    if "Cargo.toml" in files:
        stack.append("Cargo")
    if "requirements.txt" in files:
        stack.append("pip")
    if "go.mod" in files:
        stack.append("GoModules")
    if "Gemfile" in files:
        stack.append("RubyGems")

    return stack


def calculate_exp_from_diff(diff_output: str) -> Dict[str, int]:
    exp = {"code": 0, "test": 0, "docs": 0, "config": 0}

    if not diff_output:
        return exp

    lines = diff_output.split("\n")
    for line in lines:
        if line.startswith("+") and not line.startswith("+++"):
            if any(x in line for x in ["test_", "tests/", "_test.", "spec_"]):
                exp["test"] += 1
            elif any(x in line for x in [".md", "docs/", "README"]):
                exp["docs"] += 1
            elif any(
                x in line for x in [".yml", ".yaml", ".json", "config", "Dockerfile"]
            ):
                exp["config"] += 1
            else:
                exp["code"] += 1

    return exp


def generate_evolution_sprite(
    name: str, level: int, tech_stack: List[str], stage: int
) -> str:
    stage_1_ascii = r"""
         ╭───╮
        │ ◕  │
        ╰───╯
       ╭──────╮
      │  ♪ ♪  │
      ╰──────╯
    """
    stage_2_ascii = r"""
      ╭───────────╮
     │   ╭═══╮   │
     │  ◕  ◕  │ 
     │   ╰═══╯   │
     ╰───────────╯
    ╭─────────────╮
   │   ══════════│
  ╰───────────────╯
    """
    stage_3_ascii = r"""
      ╭═══════════════════╮
     │   ╭═══════════╮   │
     │  │ ╭═══════╮ │   │
     │  │ │ ◕  ◕ │ │   │
     │  │ ╰═══════╯ │   │
     │   ╰═══════════╯   │
     ╰═══════════════════╯
    ╭═════════════════════╮
   │ ════════════════════ │
  ╰═══════════════════════╯
    """

    sprites = {1: stage_1_ascii, 2: stage_2_ascii, 3: stage_3_ascii}
    return sprites.get(stage, sprites[1])


def apply_evolution(monster: Dict, metrics: GitHubMetrics) -> Dict:
    level = monster.get("level", 1)
    old_stage = monster.get("evolution_stage", 1)

    new_stage = 1
    if level >= 50:
        new_stage = 3
    elif level >= 20:
        new_stage = 2

    if new_stage > old_stage:
        monster["evolution_stage"] = new_stage
        monster["avatar"] = generate_evolution_sprite(
            monster.get("name", "Pet"), level, metrics.tech_stack, new_stage
        )

        for stat in ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]:
            if stat in monster.get("base_stats", {}):
                monster["base_stats"][stat] = int(monster["base_stats"][stat] * 1.2)

    return monster


def calculate_fusion(
    main_stats: Dict, feature_stats: Dict, conflicts_resolved: int
) -> Dict:
    new_stats = {}
    for stat in ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]:
        main_val = main_stats.get(stat, 50)
        feat_val = feature_stats.get(stat, 50)
        new_stats[stat] = int(main_val * 0.6 + feat_val * 0.4)

    bonus = conflicts_resolved * GITHUB_MAP_CONFIG["conflict_resolution_bonus"]
    new_stats["hp"] += bonus

    return new_stats


class SpiritCommands:
    GRIT_KEYWORDS = ["fix", "bug", "repair", "patch", "hotfix", "resolve"]
    VALOR_TRIGGERS = ["major", "release", "breaking", "v2.", "v3."]

    @staticmethod
    def check_grit(commit_history: str) -> bool:
        count = sum(
            1
            for kw in SpiritCommands.GRIT_KEYWORDS
            if kw.lower() in commit_history.lower()
        )
        return count >= 3

    @staticmethod
    def check_valor(current_message: str) -> bool:
        return any(
            trigger in current_message.lower()
            for trigger in SpiritCommands.VALOR_TRIGGERS
        )

    @staticmethod
    def activate_grit(current_hp: float, max_hp: float) -> bool:
        return current_hp <= max_hp * 0.25

    @staticmethod
    def activate_valor() -> bool:
        tags = run_git_command(["tag", "-l", "v[2-9].*"])
        return bool(tags)


def generate_battle_report_text(winner: str, rounds: List[Dict]) -> str:
    lines = [
        "╔══════════════════════════════════════╗",
        "║      BATTLE REPORT - 战斗战报          ║",
        "╠══════════════════════════════════════╣",
    ]

    for i, r in enumerate(rounds[:10], 1):
        lines.append(
            f"║ Round {i:2}: {r.get('attacker', '?'):10} → {r.get('damage', 0):3} DMG"
        )

    lines.extend(
        [
            "╠══════════════════════════════════════╣",
            f"║ WINNER: {winner:30} ║",
            "╚══════════════════════════════════════╝",
        ]
    )

    return "\n".join(lines)


def save_pre_commit_hook(path: str = ".git/hooks/pre-commit"):
    content = r"""#!/bin/bash
MONSTER_DIR=".monster"
SOUL_FILE="$MONSTER_DIR/pet.soul"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🦖 Agent Monster: Analyzing your commit...${NC}"

if [ ! -f "$SOUL_FILE" ]; then
    echo -e "${YELLOW}⚠ No pet found. Run egg_incubator.py first!${NC}"
    exit 0
fi

STATS=$(git diff --stat HEAD~1 HEAD 2>/dev/null | tail -1)
LINES=$(echo "$STATS" | grep -oP '\d+(?= insertion)' || echo 0)

EXP=$((LINES / 2))
echo "📈 +$EXP EXP from $LINES changed lines"

python3 -c "
import json
with open('$SOUL_FILE', 'r') as f:
    data = json.load(f)
    data['exp'] = data.get('exp', 0) + $EXP
    if 'stats' in data and 'hp' in data['stats']:
        data['stats']['hp']['exp'] += $EXP
with open('$SOUL_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pet grew stronger!${NC}"
else
    echo -e "${RED}❌ Failed to update pet!${NC}"
fi
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    os.chmod(path, 0o755)


def save_issue_duel_action(path: str = ".github/workflows/arena-duel.yml"):
    content = r"""name: Arena Duel
on:
  issue_comment:
    types: [created]

jobs:
  duel:
    if: contains(github.event.comment.body, 'duel start')
    runs-on: ubuntu-latest
    steps:
      - name: Parse Challenge
        run: |
          TARGET=$(echo "${{ github.event.comment.body }}" | grep -oP '@\K[0-9a-f]+')
          echo "target=$TARGET" >> $GITHUB_OUTPUT
      
      - name: Fetch Monsters
        run: |
          curl -s https://api.github.com/repos/${{ github.repository }}/contents/.monster/pet.soul
      
      - name: Run Battle
        run: |
          node battle_engine.js
      
      - name: Post Result
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '⚔️ Battle Complete! [View Report]'
            })
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def save_cron_updater(path: str = ".github/workflows/monster-status.yml"):
    content = r"""name: Monster Status Update
on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Analyze Git Activity
        run: |
          python3 stat_calculator.py --analyze
      
      - name: Update README
        run: |
          python3 -c "
          import re
          with open('README.md', 'r') as f:
             content = f.read()
          content = re.sub(r'!\[Monster\].*', '![Monster](.monster/badge.svg)', content)
          with open('README.md', 'w') as f:
             f.write(content)
          "
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    print("📊 GitHub Metrics Analysis")
    print("=" * 50)

    metrics = analyze_commit_history(7)
    tech_stack = detect_tech_stack()
    metrics.tech_stack = tech_stack

    print(f"Total Commits: {metrics.total_commits}")
    print(f"Recent 7d: {metrics.recent_commits_7d}")
    print(f"Green Ratio: {metrics.green_ratio:.1%}")
    print(f"Fix Keywords: {metrics.fix_keywords_count}")
    print(f"Tech Stack: {', '.join(tech_stack)}")

    level, exp_have, exp_need = calculate_level(metrics.total_commits)
    print(f"\n_level: {level}")
    print(f"EXP: {exp_have} / {exp_need}")

    en_regen = calculate_en_regen(metrics.green_ratio)
    print(f"\n⚡ EN Regen: {en_regen}/turn")

    if SpiritCommands.check_valor("Release v2.0.0"):
        print("🔥 VALOR ACTIVE: Major version in progress!")
