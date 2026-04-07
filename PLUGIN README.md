# Agent Monster - Claude Code Plugin

将你的 GitHub 仓库变成一个数字宠物，与其他开发者进行代码对战！

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启用 MCP 服务器

在项目根目录已有 `.mcp.json` 文件，Claude Code 会自动检测并提示启用。

或者手动在 `~/.claude/settings.json` 中添加：

```json
{
  "enabledMcpServers": ["agent-monster"]
}
```

### 3. 使用 /monster 命令

启用后，在 Claude Code 中输入：

```
/monster init       - 初始化你的代码宠物
/monster status     - 查看宠物状态
/monster analyze    - 分析仓库活动
/monster traps      - 扫描代码陷阱
/monster duel       - 发起对战挑战
```

## 游戏说明

### 宠物孵化

运行 `/monster init` 孵化你的代码宠物：
- 分析最近 72 小时的 Git 提交
- 根据代码语言分布生成基因权重
- 创建初始六维属性值

### 属性系统

| 属性 | 含义 |
|------|------|
| HP | 战斗能量上限 |
| Attack | 攻击力 |
| Defense | 防御力 |
| Speed | 速度 |
| Sp.Atk | 特殊攻击 |
| Sp.Def | 特殊防御 |

### 属性克制

- **Low-Level** (C/C++/Rust) 克制 **Scripting** (Python/JS)
- **Scripting** 克制 **Logic** (SQL/Lisp)
- **Logic** 克制 **Low-Level**

### 对战技能

| 技能 | 威力 | 命中率 | 效果 |
|------|------|--------|------|
| scan | 40 | 95% | 探测弱点 |
| buffer_overflow | 80 | 70% | 无视 50% 防御 |
| refactor_storm | 100 | 60% | 多段攻击 |
| sql_injection | 90 | 75% | 中毒状态 |
| memory_leak | 60 | 85% | 吸取 EN |
| deadlock | 110 | 50% | 高伤害易 Miss |
| finalize | 150 | 40% | 终极技能 |

## 文件结构

```
agentmonster/
├── mcp_server.py          # MCP 服务器入口
├── monster.py             # 怪物 CLI（兼容模式）
├── egg_incubator.py       # 宠物孵化器
├── battle_logic.py        # 对战引擎
├── .mcp.json              # MCP 配置
├── .claude/
│   └── commands/
│       └── monster.md     # /monster 命令定义
├── .monster/
│   ├── pet.soul           # 宠物数据
│   ├── vault.json         # 经验值存储
│   └── guard.yaml         # 防守配置
└── CLAUDE.md              # 使用文档
```

## MCP 工具 API

| 工具 | 描述 | 参数 |
|------|------|------|
| `monster_init` | 初始化宠物 | 无 |
| `monster_status` | 查看状态 | `json?: boolean` |
| `monster_analyze` | 分析仓库 | `days?: number` |
| `monster_traps` | 扫描陷阱 | `path?: string` |
| `monster_duel` | 发起对战 | `target: string, attack_sequence?: string[]` |

## 许可证

MIT
