#!/usr/bin/env python3
"""
MCP Server Connection Stability Fix
处理 OpenCode 的连接问题
"""

import sys
import json
import os
import signal
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# 导入原始 MCP 服务器
import mcp_server

def safe_mcp_loop():
    """改进的 MCP 循环，更好地处理连接问题"""
    import sys
    
    # 设置信号处理
    def signal_handler(signum, frame):
        """优雅地处理信号"""
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # 设置 stderr 和 stdout 为非缓冲
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)
    
    # 运行原始 mcp_loop
    try:
        mcp_server.mcp_loop()
    except BrokenPipeError:
        # OpenCode 连接关闭，正常退出
        sys.exit(0)
    except Exception as e:
        # 记录错误但继续
        print(json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32603, "message": f"Server error: {str(e)}"}
        }), flush=True)
        sys.exit(1)

if __name__ == "__main__":
    if not mcp_server.check_dependencies():
        sys.exit(1)
    
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        safe_mcp_loop()
    else:
        # 代理到原始服务器处理其他命令
        sys.argv.pop(0)  # 移除脚本名称
        if sys.argv and sys.argv[0] == "mcp":
            safe_mcp_loop()
        else:
            # 运行原始脚本的命令处理
            if sys.argv:
                if sys.argv[0] == "init":
                    print(mcp_server.cmd_init())
                elif sys.argv[0] == "status":
                    print(mcp_server.cmd_status("--json" in sys.argv))
                elif sys.argv[0] == "analyze":
                    print(json.dumps(mcp_server.cmd_analyze(), indent=2))
                elif sys.argv[0] == "traps":
                    target = sys.argv[1] if len(sys.argv) > 1 else "."
                    print(json.dumps(mcp_server.cmd_traps(target), indent=2))
                elif sys.argv[0] == "duel":
                    target = sys.argv[1] if len(sys.argv) > 1 else ""
                    print(json.dumps(mcp_server.cmd_duel(target), indent=2))
            else:
                print("Agent Monster CLI v0.1.0")
                print("Usage: python3 mcp_server.py <command>")
                print("Commands: init, status, analyze, traps, duel, mcp")
