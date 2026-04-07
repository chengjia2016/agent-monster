#!/usr/bin/env python3
"""
Agent Monster Cookie Generator
生成零食 cookie 代码注释，可以插入到任何代码文件中
"""

import hashlib
import random
import string
from pathlib import Path
from datetime import datetime

# 零食模板
COOKIE_TEMPLATES = {
    "cookie": {
        "emoji": "🍪",
        "name": "Cookie",
        "exp_bonus": 10,
        "en_bonus": 0,
    },
    "donut": {
        "emoji": "🍩",
        "name": "Donut",
        "exp_bonus": 20,
        "en_bonus": 50,
    },
    "apple": {
        "emoji": "🍎",
        "name": "Apple",
        "exp_bonus": 15,
        "en_bonus": 25,
    },
    "gene": {
        "emoji": "🧬",
        "name": "Gene",
        "exp_bonus": 50,
        "en_bonus": 0,
    },
}

# 代码注释格式
COMMENT_FORMATS = {
    ".py": "# {emoji} agent_monster cookie {cookie_id}\n",
    ".js": "// {emoji} agent_monster cookie {cookie_id}\n",
    ".ts": "// {emoji} agent_monster cookie {cookie_id}\n",
    ".go": "// {emoji} agent_monster cookie {cookie_id}\n",
    ".rs": "// {emoji} agent_monster cookie {cookie_id}\n",
    ".java": "// {emoji} agent_monster cookie {cookie_id}\n",
    ".md": "<!-- {emoji} agent_monster cookie {cookie_id} -->\n",
    ".html": "<!-- {emoji} agent_monster cookie {cookie_id} -->\n",
    ".yaml": "# {emoji} agent_monster cookie {cookie_id}\n",
    ".yml": "# {emoji} agent_monster cookie {cookie_id}\n",
    ".json": "// {emoji} agent_monster cookie {cookie_id}\n",
}


def generate_cookie_id(player_id: str = None) -> str:
    """生成唯一的 cookie ID"""
    timestamp = datetime.now().isoformat()
    random_seed = "".join(random.choices(string.hexdigits, k=16))
    data = f"{player_id or 'anonymous'}:{timestamp}:{random_seed}"
    return "0x" + hashlib.sha256(data.encode()).hexdigest()[:16]


def generate_cookie(
    file_ext: str = ".py",
    cookie_type: str = "cookie",
    player_id: str = None,
) -> str:
    """生成零食 cookie 注释"""
    cookie_data = COOKIE_TEMPLATES.get(cookie_type, COOKIE_TEMPLATES["cookie"])
    cookie_id = generate_cookie_id(player_id)
    comment = COMMENT_FORMATS.get(file_ext, COMMENT_FORMATS[".py"])
    return comment.format(emoji=cookie_data["emoji"], cookie_id=cookie_id)


def scan_file_for_cookies(filepath: str) -> list:
    """扫描文件中的零食 cookie"""
    cookies = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 匹配 cookie 模式
        import re

        pattern = r"([🍪🍩🍎🧬])\s*agent_monster\s+cookie\s+(0x[0-9a-fA-F]{16})"
        matches = re.findall(pattern, content)

        for emoji_match, cookie_id in matches:
            cookie_type = "cookie"
            if "🍩" in emoji_match:
                cookie_type = "donut"
            elif "🍎" in emoji_match:
                cookie_type = "apple"
            elif "🧬" in emoji_match:
                cookie_type = "gene"

            cookies.append(
                {
                    "type": cookie_type,
                    "cookie_id": cookie_id,
                    "file": filepath,
                }
            )
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")

    return cookies


def scan_directory_for_cookies(directory: str) -> list:
    """扫描目录下所有文件中的零食"""
    all_cookies = []
    for root, dirs, files in os.walk(directory):
        # 跳过特定目录
        if any(skip in root for skip in [".git", "node_modules", "__pycache__"]):
            continue

        for file in files:
            filepath = os.path.join(root, file)
            cookies = scan_file_for_cookies(filepath)
            all_cookies.extend(cookies)

    return all_cookies


def create_food_bank(cookies: list, player_id: str) -> dict:
    """创建零食银行数据"""
    food_bank = {
        "player_id": player_id,
        "last_updated": datetime.now().isoformat(),
        "cookies": [],
        "summary": {
            "total": len(cookies),
            "by_type": {},
        },
    }

    for cookie in cookies:
        food_bank["cookies"].append(
            {
                "cookie_id": cookie["cookie_id"],
                "type": cookie["type"],
                "file": cookie["file"],
                "claimed": False,
            }
        )

        # 统计
        cookie_type = cookie["type"]
        if cookie_type not in food_bank["summary"]["by_type"]:
            food_bank["summary"]["by_type"][cookie_type] = 0
        food_bank["summary"]["by_type"][cookie_type] += 1

    return food_bank


if __name__ == "__main__":
    import json
    import os
    import sys
    import io

    # Windows 控制台 Unicode 兼容
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        # 生成零食
        file_ext = sys.argv[2] if len(sys.argv) > 2 else ".py"
        cookie_type = sys.argv[3] if len(sys.argv) > 3 else "cookie"
        player_id = sys.argv[4] if len(sys.argv) > 4 else None

        cookie = generate_cookie(file_ext, cookie_type, player_id)
        print(cookie)

    elif len(sys.argv) > 1 and sys.argv[1] == "scan":
        # 扫描零食
        directory = sys.argv[2] if len(sys.argv) > 2 else "."
        player_id = sys.argv[3] if len(sys.argv) > 3 else "unknown"

        cookies = scan_directory_for_cookies(directory)
        food_bank = create_food_bank(cookies, player_id)

        print(json.dumps(food_bank, indent=2))

    else:
        print("Agent Monster Cookie Generator")
        print("Usage:")
        print("  cookie.py generate [ext] [type] [player_id]")
        print("  cookie.py scan [directory] [player_id]")
        print("")
        print("Examples:")
        print("  cookie.py generate .py cookie player123")
        print("  cookie.py scan . player123")
