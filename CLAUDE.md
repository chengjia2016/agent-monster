# Agent Monster MCP Server

将你的 GitHub 仓库变成一个数字宠物，与其他开发者进行代码对战！

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Claude Code

将以下配置添加到你的 `~/.claude/settings.json` 文件中：

### Windows 配置

```json
{
  "mcpServers": {
    "agent-monster": {
      "command": "python",
      "args": ["mcp_server.py", "mcp"],
      "cwd": "C:/Users/Administrator/agentmonster"
    }
  }
}
```

### Linux/macOS 配置

```json
{
  "mcpServers": {
    "agent-monster": {
      "command": "python3",
      "args": ["mcp_server.py", "mcp"],
      "cwd": "/path/to/agentmonster"
    }
  }
}
```

**或者**使用绝对路径：

```json
{
  "mcpServers": {
    "agent-monster": {
      "command": "python3",
      "args": ["/absolute/path/to/agentmonster/mcp_server.py", "mcp"]
    }
  }
}
```

## 可用工具

配置完成后，Claude Code 将自动加载以下工具：

| 工具 | 描述 |
|------|------|
| `monster_init` | 初始化当前仓库的 Agent Monster 宠物 |
| `monster_status` | 查看宠物状态（等级、属性、进化） |
| `monster_duel` | 挑战其他仓库的宠物进行对战 |
| `monster_analyze` | 分析仓库活动并更新宠物属性 |
| `monster_traps` | 扫描代码中的逻辑陷阱 |

## 使用方法

### 方式 1: 自然语言命令

在 Claude Code 中直接使用自然语言：

```
- "初始化我的宠物"
- "查看我的怪物状态"
- "分析这个仓库的代码活动"
- "扫描代码中的陷阱"
- "向对方仓库发起挑战"
```

### 方式 2: /monster 斜杠命令

输入 `/monster <command>` 来快速执行：

```
/monster init       - 初始化你的代码宠物
/monster status     - 查看宠物状态
/monster analyze    - 分析仓库活动
/monster traps      - 扫描代码陷阱
/monster duel       - 发起对战挑战
```

## 依赖项

确保已安装以下 Python 依赖：

```bash
pip install pyyaml
```

## 测试 MCP 服务器

手动测试 MCP 服务器是否正常工作：

```bash
# 测试初始化
echo '{"jsonrpc":"2.0","id":1,"method":"initialize"}' | python mcp_server.py mcp

# 测试工具列表
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python mcp_server.py mcp
```

## 文件结构

```
.monster/
├── pet.soul          # 宠物数据
├── vault.json        # 经验值存储
├── guard.yaml        # 防守配置
└── opponent_pet.soul # 对手数据（测试用）
```
