#!/usr/bin/env python3
"""
Agent Monster - Egg Incubator (Phase 1)
72小时行为感知与"蛋"的孵化器
分析 git 提交历史，生成初始基因权重
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
MONSTER_DIR = PROJECT_ROOT / ".monster"
SOUL_FILE = MONSTER_DIR / "pet.soul"

# 基因类型定义
GENE_TYPES = {
    "logic": ["go", "rs", "py", "java", "cpp", "c", "ts", "js"],  # 代码行/复杂算法
    "creative": ["md", "css", "html", "scss", "vue", "jsx", "tsx"],  # 文档/注释/UI
    "speed": ["sh", "yml", "yaml", "json", "toml", "sql"],  # 脚本/配置/API
}

# 语言到基因类型的映射
LANGUAGE_GENE_MAP = {}
for gene_type, langs in GENE_TYPES.items():
    for lang in langs:
        LANGUAGE_GENE_MAP[lang] = gene_type


def get_git_config(key):
    """获取 git 配置"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", key], capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def get_commit_history(hours=72, limit=50):
    """获取最近 N 小时的提交历史"""
    try:
        since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d")
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={since}",
                f"-n{limit}",
                "--pretty=format:%H|%an|%ae|%at|%s",
                "--",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=PROJECT_ROOT,
        )
        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 5:
                commits.append(
                    {
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "timestamp": int(parts[3]),
                        "message": parts[4],
                    }
                )
        return commits
    except Exception as e:
        print(f"Warning: Could not read git history: {e}")
        return []


def analyze_commit_diffs(commits):
    """分析提交的 diff 特征，统计语言分布"""
    language_counts = defaultdict(int)
    gene_weights = defaultdict(float)

    for commit in commits:
        try:
            result = subprocess.run(
                ["git", "show", "--stat", "--format=", commit["hash"]],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=PROJECT_ROOT,
            )

            for line in result.stdout.strip().split("\n"):
                # 统计文件扩展名
                for ext in LANGUAGE_GENE_MAP:
                    if f".{ext}" in line.lower():
                        lang = ext
                        gene_type = LANGUAGE_GENE_MAP.get(lang, "logic")
                        language_counts[lang] += 1
                        gene_weights[gene_type] += 1
                        break
        except Exception:
            continue

    return language_counts, gene_weights


def calculate_ivs(commits):
    """计算个体值 (IVs) - 基于提交特征的随机种子"""
    import hashlib

    if not commits:
        # 默认值
        return {
            stat: 15 for stat in ["hp", "attack", "defense", "speed", "armor", "quota"]
        }

    # 使用所有提交 hash 的组合作为种子
    seed_data = "".join(c["hash"] for c in commits[:10])
    seed = int(hashlib.md5(seed_data.encode()).hexdigest()[:8], 16)

    ivs = {}
    stat_names = ["hp", "attack", "defense", "speed", "armor", "quota"]
    for i, stat in enumerate(stat_names):
        ivs[stat] = (seed >> (i * 5)) % 32

    return ivs


def generate_initial_soul(commits, language_counts, gene_weights, owner_email):
    """生成初始的 pet.soul 文件"""

    total_commits = len(commits)
    if total_commits == 0:
        total_commits = 1

    # 归一化基因权重
    total_weight = sum(gene_weights.values()) or 1
    normalized_genes = {
        gene: weight / total_weight for gene, weight in gene_weights.items()
    }

    # 确定物种类型
    if normalized_genes.get("logic", 0) > 0.5:
        species = "Logic"
    elif normalized_genes.get("creative", 0) > 0.5:
        species = "Creative"
    elif normalized_genes.get("speed", 0) > 0.5:
        species = "Speed"
    else:
        species = "Hybrid"

    # 生成基础属性 (基于基因权重)
    base_stats = {
        "hp": 50 + int(normalized_genes.get("logic", 0.33) * 50),
        "attack": 50 + int(normalized_genes.get("speed", 0.33) * 50),
        "defense": 50 + int(normalized_genes.get("logic", 0.33) * 30),
        "speed": 50 + int(normalized_genes.get("speed", 0.33) * 50),
        "armor": 30 + int(normalized_genes.get("creative", 0.33) * 40),
        "quota": 100 + int(normalized_genes.get("creative", 0.33) * 100),
    }

    # 计算 IVs
    ivs = calculate_ivs(commits)

    # 构建 soul 数据结构
    soul = {
        "metadata": {
            "name": f"CodePet-{datetime.now().strftime('%Y%m%d')}",
            "species": species,
            "birth_time": datetime.now().isoformat(),
            "owner": owner_email,
            "generation": 1,
            "evolution_stage": 1,
            "avatar": get_ascii_avatar(1),
        },
        "stats": {},
        "genes": {
            "logic": {
                "weight": normalized_genes.get("logic", 0.33),
                "source_commits": [],
            },
            "creative": {
                "weight": normalized_genes.get("creative", 0.33),
                "source_commits": [],
            },
            "speed": {
                "weight": normalized_genes.get("speed", 0.33),
                "source_commits": [],
            },
        },
        "battle_history": [],
        "signature": {
            "algorithm": "RSA-SHA256",
            "value": "",
            "keyid": get_git_config("user.signingkey") or "",
        },
    }

    # 构建 stats
    for stat_name, base in base_stats.items():
        soul["stats"][stat_name] = {
            "base": base,
            "iv": ivs.get(stat_name, 15),
            "ev": 0,
            "exp": 0,
        }

    # 添加基因来源提交
    for commit in commits[:10]:
        gene_type = LANGUAGE_GENE_MAP.get("py", "logic")  # 默认
        for lang, gt in LANGUAGE_GENE_MAP.items():
            if lang in commit.get("message", "").lower():
                gene_type = gt
                break
        soul["genes"][gene_type]["source_commits"].append(commit["hash"])

    return soul


def get_ascii_avatar(stage):
    """获取 ASCII 头像"""
    avatars = {
        1: r"""
     ╭───╮
    │ ◕  │
    ╰───╯
   ╭──────╮
  │  ♪ ♪  │
  ╰──────╯
        """,
        2: r"""
    ╭───────────╮
   │   ╭═══╮   │
   │  ◕  ◕  │ 
   │   ╰═══╯   │
   ╰───────────╯
  ╭─────────────╮
 │   ══════════│
╰───────────────╯
        """,
        3: r"""
    ╭═══════════════════╮
   │   ╭═══════════╮   │
   │  │ ╭═══════╮ │   │
   │  │ │ ◕  ◕ │ │   │
   │  │ ╰═══════╯ │   │
   │   ╰═══════════╯   │
   ╰═══════════════════╯
  ╭═════════════════════╮
 │ ════════════════════ │
╰════════───────────────╯
        """,
    }
    return avatars.get(stage, avatars[1])


def main():
    """主函数"""
    # Windows 控制台 Unicode 兼容
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("🥚 Agent Monster - Egg Incubator")
    print("=" * 40)

    # 确保 .monster 目录存在
    MONSTER_DIR.mkdir(exist_ok=True)

    # 获取用户信息
    owner_email = get_git_config("user.email") or "unknown@localhost"
    print(f"Owner: {owner_email}")

    # 获取提交历史
    commits = get_commit_history(hours=72, limit=50)
    print(f"Analyzing {len(commits)} commits (last 72h)...")

    # 分析语言分布
    language_counts, gene_weights = analyze_commit_diffs(commits)

    print("\nLanguage Distribution:")
    for lang, count in sorted(language_counts.items(), key=lambda x: -x[1]):
        gene = LANGUAGE_GENE_MAP.get(lang, "logic")
        print(f"  {lang:8} -> {gene:8} : {count}")

    print("\nGene Weights:")
    for gene, weight in sorted(gene_weights.items(), key=lambda x: -x[1]):
        bar = "#" * int(weight * 10)
        print(f"  {gene:8}: {weight:.2%} {bar}")

    # 生成 soul 文件
    soul = generate_initial_soul(commits, language_counts, gene_weights, owner_email)

    # 写入文件
    with open(SOUL_FILE, "w", encoding="utf-8") as f:
        json.dump(soul, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Created: {SOUL_FILE}")
    print(f"   Species: {soul['metadata']['species']}")
    print(f"   Stage: {soul['metadata']['evolution_stage']}")

    print("\n" + soul["metadata"]["avatar"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
