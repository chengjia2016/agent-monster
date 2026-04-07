#!/usr/bin/env python3
"""
Monster CLI Wrapper - MCP Server Mode
Provides STDIO interface for Agent integration

🍪 agent_monster cookie 0xtest1234567890ab
"""

import json
import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MONSTER_DIR = SCRIPT_DIR / ".monster"
CONFIG_FILE = MONSTER_DIR / "config.json"
SOUL_FILE = MONSTER_DIR / "pet.soul"


def load_json(path):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_json(path, data):
    MONSTER_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def cmd_init():
    result = subprocess.run(
        ["python3", "egg_incubator.py"], capture_output=True, text=True
    )
    return result.stdout


def cmd_status(json_mode=False):
    soul = load_json(SOUL_FILE)
    if not soul:
        if json_mode:
            return json.dumps({"error": "No monster found, run init first"})
        else:
            print("No monster found, run: python monster.py init")
            return None

    if json_mode:
        return json.dumps(soul, indent=2)

    avatar = soul.get("avatar", "")
    safe_avatar = (
        avatar.encode("ascii", "replace").decode("ascii")
        if avatar
        else "[No Avatar]"
    )

    output = []
    output.append(f"\n{safe_avatar}")
    output.append("=" * 50)
    output.append(f"  {soul.get('name', 'Unknown')} (Lv.{soul.get('level', 1)})")
    output.append(f"  ID: {soul.get('monster_id', 'N/A')}")
    output.append(f"  Type: {'/'.join(soul.get('type', []))}")
    output.append(
        f"  Nature: {soul.get('nature', 'N/A')} | Ability: {soul.get('ability', 'N/A')}"
    )
    output.append("=" * 50)

    stats = soul.get("base_stats", {})
    output.append("\n[STATS]")
    for stat, val in stats.items():
        bar = "#" * (val // 20) + "-" * (12 - val // 20)
        output.append(f"  {stat.upper():8}: {val:3} [{bar}]")

    output.append(
        f"\n[INFO] EXP: {soul.get('exp', 0)} | Battles: {len(soul.get('battle_history', []))}"
    )

    return "\n".join(output)


def cmd_analyze(days=7):
    from github_integration import analyze_commit_history, detect_tech_stack

    metrics = analyze_commit_history(days)
    return {
        "total_commits": metrics.total_commits,
        "recent_7d": metrics.recent_commits_7d,
        "green_ratio": metrics.green_ratio,
        "tech_stack": metrics.tech_stack,
        "fix_count": metrics.fix_keywords_count,
    }


def cmd_traps(path="."):
    from battle_logic import LogicTrapDetector

    traps = LogicTrapDetector.scan_for_traps(path)
    return {
        "traps": [
            {"type": t.trap_type.value, "file": t.source_file, "power": t.power}
            for t in traps
        ],
        "count": len(traps),
    }


def cmd_duel(target, attack_stack=None):
    from battle_logic import BattleSimulator

    attacker = load_json(SOUL_FILE)
    if not attacker:
        return {"error": "No monster found, run init first"}

    defender = {
        "monster_id": "opponent",
        "name": "Opponent",
        "base_stats": {
            "hp": 100,
            "attack": 80,
            "defense": 80,
            "sp_atk": 80,
            "sp_def": 80,
            "speed": 80,
        },
    }

    simulator = BattleSimulator(attacker, defender, "seed123")
    result = simulator.run_battle(
        attack_stack or ["scan", "buffer_overflow", "refactor_storm"], [], "tank", 5
    )
    return result


def mcp_loop():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            req = json.loads(line.strip())
            method = req.get("method", "")
            params = req.get("params", {})

            resp = {"jsonrpc": "2.0"}

            if method == "initialize":
                resp["result"] = {"protocolVersion": "0.1.0", "capabilities": {}}

            elif method == "tools/list":
                resp["result"] = {
                    "tools": [
                        {
                            "name": "monster_init",
                            "description": "Initialize a new Agent Monster pet for the current repository by analyzing git commit history",
                            "inputSchema": {"type": "object", "properties": {}, "required": []},
                        },
                        {
                            "name": "monster_status",
                            "description": "Show the current status of your Agent Monster (level, stats, evolution)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "json": {"type": "boolean", "description": "Output in JSON format"}
                                },
                                "required": []
                            },
                        },
                        {
                            "name": "monster_duel",
                            "description": "Challenge another repository's monster to battle",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "target": {"type": "string", "description": "Target repository URL or monster ID"},
                                    "attack_sequence": {"type": "array", "items": {"type": "string"}, "description": "Attack sequence"}
                                },
                                "required": ["target"]
                            },
                        },
                        {
                            "name": "monster_analyze",
                            "description": "Analyze repository activity and update monster stats",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "days": {"type": "integer", "description": "Days to analyze (default: 7)"}
                                },
                                "required": []
                            },
                        },
                        {
                            "name": "monster_traps",
                            "description": "Scan code for defensive traps (@monster-trap comments)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string", "description": "Path to scan (default: current directory)"}
                                },
                                "required": []
                            },
                        },
                    ]
                }

            elif method == "tools/call":
                tool = params.get("name", "")
                args = params.get("arguments", {})

                if tool == "monster_init":
                    out = cmd_init()
                    resp["result"] = {"content": [{"type": "text", "text": out}]}
                elif tool == "monster_status":
                    out = cmd_status(args.get("json", True))
                    resp["result"] = {"content": [{"type": "text", "text": out or ""}]}
                elif tool == "monster_duel":
                    result = cmd_duel(
                        args.get("target", ""), args.get("attack_sequence")
                    )
                    resp["result"] = {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                elif tool == "monster_analyze":
                    result = cmd_analyze(args.get("days", 7))
                    resp["result"] = {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                elif tool == "monster_traps":
                    result = cmd_traps(args.get("path", "."))
                    resp["result"] = {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                else:
                    resp["error"] = {"code": -32601, "message": f"Unknown tool: {tool}"}

            else:
                resp["error"] = {"code": -32600, "message": "Invalid Request"}

            print(json.dumps(resp), flush=True)

        except Exception as e:
            print(
                json.dumps({"error": {"code": -32603, "message": str(e)}}), flush=True
            )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        mcp_loop()
    elif len(sys.argv) > 1:
        if sys.argv[1] == "init":
            print(cmd_init())
        elif sys.argv[1] == "status":
            cmd_status("--json" in sys.argv)
        elif sys.argv[1] == "analyze":
            print(json.dumps(cmd_analyze(), indent=2))
        elif sys.argv[1] == "traps":
            print(
                json.dumps(
                    cmd_traps(sys.argv[2] if len(sys.argv) > 2 else "."), indent=2
                )
            )
        elif sys.argv[1] == "duel":
            target = sys.argv[2] if len(sys.argv) > 2 else ""
            print(json.dumps(cmd_duel(target), indent=2))
    else:
        print("Monster CLI v0.1.0")
        print("Usage: monster.py <command>")
        print("Commands: init, status, analyze, traps, duel")
