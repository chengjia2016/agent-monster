#!/usr/bin/env python3
"""
Agent Monster - 初始宠物领取
领取初始宠物 (小黄鸭) 和宠物蛋
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

MONSTER_DIR = Path(".monster")
PET_SOUL_FILE = MONSTER_DIR / "pet.soul"
EGG_FILE = MONSTER_DIR / "egg.yaml"
FOOD_BANK_FILE = MONSTER_DIR / "food-bank.json"


def get_git_config(key):
    """获取 git 配置"""
    try:
        import subprocess

        result = subprocess.run(
            ["git", "config", "--get", key], capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def create_initial_pet():
    """创建初始宠物 - 小黄鸭"""

    owner_email = get_git_config("user.email") or "unknown@localhost"
    owner_name = get_git_config("user.name") or "unknown"

    pet = {
        "monster_id": "0x" + os.urandom(8).hex(),
        "name": "小黄鸭",
        "species": "Duck",
        "type": ["Creative", "Speed"],
        "nature": "Relaxed",
        "ability": "Quack Quack",
        "base_stats": {
            "hp": 80,
            "attack": 60,
            "defense": 70,
            "sp_atk": 50,
            "sp_def": 60,
            "speed": 90,
        },
        "ivs": {
            "hp": 20,
            "attack": 15,
            "defense": 18,
            "sp_atk": 12,
            "sp_def": 15,
            "speed": 25,
        },
        "evs": {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "sp_atk": 0,
            "sp_def": 0,
            "speed": 0,
        },
        "level": 1,
        "exp": 0,
        "evolution_stage": 1,
        "moves": ["scan", "quack", "feather_dance"],
        "exp": 0,
        "evolution_stage": 1,
        "avatar": r"""
     ╭───╮
    │ ◕  │  小黄鸭
    ╰───╯
   ╭─────╮
  │  🦆  │
  ╰─────╯
        """,
        "metadata": {
            "birth_time": datetime.now().isoformat(),
            "owner": owner_email,
            "owner_name": owner_name,
            "generation": 1,
            "source": "initial_gift",
        },
        "battle_history": [],
        "signature": {
            "algorithm": "RSA-SHA256",
            "value": "",
            "keyid": get_git_config("user.signingkey") or "",
        },
    }

    return pet


def create_egg():
    """创建宠物蛋"""

    egg_yaml = f"""# 宠物蛋配置
# 72 小时孵化机制

egg:
  # 孵化状态：incubating, ready, hatched
  status: incubating

  # 开始时间 (ISO 8601)
  start_time: {datetime.now().isoformat()}

  # 孵化所需时间 (小时)
  incubation_hours: 72

  # 剩余时间 (由 Actions 每小时更新)
  remaining_hours: 72

# 基因收集
genes:
  # Logic 基因：代码提交
  logic:
    weight: 0.0
    source_commits: []

  # Creative 基因：文档/注释
  creative:
    weight: 0.0
    source_files: []

  # Speed 基因：配置/脚本
  speed:
    weight: 0.0
    source_files: []

  # Lucky 基因：零食 cookie
  lucky:
    weight: 0.0
    cookies_found: 0

# 孵化后的宠物属性预测
predicted_stats:
  hp: null
  attack: null
  defense: null
  speed: null
  sp_atk: null
  sp_def: null

# 里程碑
milestones:
  - hour: 24
    reached: false
    description: "24 小时 - 基因初步形成"
  - hour: 48
    reached: false
    description: "48 小时 - 宠物轮廓显现"
  - hour: 72
    reached: false
    description: "72 小时 - 孵化完成!"
"""

    return egg_yaml


def create_food_bank():
    """创建零食银行"""

    food_bank = {
        "player_id": get_git_config("user.email") or "unknown",
        "last_updated": datetime.now().isoformat(),
        "cookies": [],
        "summary": {
            "total": 0,
            "by_type": {},
        },
        "consumed": [],
    }

    return food_bank


def main():
    """主函数"""
    # Windows 控制台 Unicode 兼容
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("Agent Monster - 初始宠物领取")
    print("=" * 50)

    # 确保 .monster 目录存在
    MONSTER_DIR.mkdir(exist_ok=True)

    # 检查是否已经有宠物
    if PET_SOUL_FILE.exists():
        print("你已经有宠物了!")
        with open(PET_SOUL_FILE, encoding="utf-8") as f:
            pet = json.load(f)
        print(f"   宠物名：{pet.get('name', 'Unknown')}")
        print(f"   等级：{pet.get('level', 1)}")
        return 1

    # 创建初始宠物
    pet = create_initial_pet()
    with open(PET_SOUL_FILE, "w", encoding="utf-8") as f:
        json.dump(pet, f, indent=2, ensure_ascii=False)

    print(f"领取成功!")
    print(f"   宠物名：{pet['name']}")
    print(f"   物种：{pet['species']}")
    print(f"   等级：{pet['level']}")
    print(f"   属性：{pet['type']}")

    # 创建宠物蛋
    egg_yaml = create_egg()
    with open(EGG_FILE, "w", encoding="utf-8") as f:
        f.write(egg_yaml)

    print(f"\n宠物蛋已领取!")
    print(f"   孵化时间：72 小时")
    print(f"   开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   预计孵化：{(datetime.now() + timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')}")

    # 创建零食银行
    food_bank = create_food_bank()
    with open(FOOD_BANK_FILE, "w", encoding="utf-8") as f:
        json.dump(food_bank, f, indent=2, ensure_ascii=False)

    print(f"\n零食银行已创建!")
    print(f"   在代码中埋入零食 cookie 来给宠物增加能量")
    print(f"   格式：# agent_monster cookie 0x...")

    # 显示宠物
    print("\n" + pet["avatar"])

    print("\n下一步:")
    print("   1. 在代码中埋入零食 cookie")
    print("   2. 等待 72 小时让宠物蛋孵化")
    print("   3. 使用 /monster status 查看状态")
    print("   4. 参与战斗和排行")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
