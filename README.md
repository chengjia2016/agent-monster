# Agent Monster

> 🐤 将你的 GitHub 仓库变成一个数字宠物，与其他开发者 Battle！

**Agent Monster** 是一个基于 GitHub 生态的慢节奏养成游戏。你的代码仓库就是宠物的家，代码提交就是宠物的食物。

---

## 🚀 快速开始

### 1. Fork 基地仓库

```bash
# 使用 GitHub CLI
gh repo fork agent-monster/agent-monster-pet

# 或者手动在 GitHub 上 Fork
```

### 2. Clone 到本地

```bash
git clone https://github.com/your-name/agent-monster-pet.git
cd agent-monster-pet
```

### 3. 安装并领取宠物

```bash
# Windows
install.bat

# Linux/macOS
./install.sh
```

**初始奖励:**
- 🐤 **小黄鸭** (初始宠物)
- 🥚 **宠物蛋** x1 (72 小时后孵化)

---

## 🎮 游戏玩法

### 零食系统 (Cookie)

在任何代码文件的注释中埋入零食：

```python
# 🍪 agent_monster cookie 0x67678328732673287
def my_function():
    pass
```

```javascript
// 🍩 agent_monster cookie 0xabcdef1234567890
const x = 1;
```

```markdown
<!-- 🍎 agent_monster cookie 0x1234567890abcdef -->
```

**零食类型:**
| 零食 | 效果 |
|------|------|
| 🍪 Cookie | +10 EXP |
| 🍩 Donut | +50 EN |
| 🍎 Apple | +5 全属性 |
| 🧬 Gene | 基因突变 (孵化时) |

### 宠物蛋孵化

宠物蛋需要 **72 小时** 收集行为基因：

| 行为 | 基因影响 |
|------|----------|
| 写代码 (commits) | Logic 基因 |
| 写文档 (md 文件) | Creative 基因 |
| 写配置 (yaml/json) | Speed 基因 |
| 埋零食 (cookie) | Lucky 基因 |

### 战斗系统

```bash
# 在 Claude Code 中
/monster duel opponent/repo
```

---

## 📡 GitHub Actions 游戏服务器

本项目使用 GitHub Actions 作为游戏服务器：

| Workflows | 频率 | 功能 |
|-----------|------|------|
| `hourly-settlement.yml` | 每小时 | 结算零食、恢复能量 |
| `daily-rank.yml` | 每天 | 更新排行榜 |
| `battle-arena.yml` | 手动/触发 | 战斗模拟 |

### 启用 Actions

```bash
gh workflow enable hourly-settlement.yml
gh workflow enable daily-rank.yml
gh workflow enable battle-arena.yml
```

---

## 🎯 命令参考

### Claude Code MCP 命令

```
/monster init       - 领取初始宠物
/monster status     - 查看宠物状态
/monster analyze    - 分析仓库活动
/monster traps      - 扫描代码陷阱
/monster duel       - 发起对战挑战
```

### CLI 命令

```bash
python monster.py status     # 查看状态
python monster.py analyze    # 分析仓库
python monster.py traps      # 扫描陷阱
python cookie.py generate    # 生成零食
python cookie.py scan        # 扫描零食
```

---

## 📊 排行榜

### 个人排行

每个仓库的 `leaderboard.json`:

```json
{
  "player": "your-name",
  "pet_name": "小黄鸭",
  "level": 25,
  "battles": {
    "win": 15,
    "lose": 8
  }
}
```

### 总排行

中央仓库汇总所有玩家的 `leaderboard.json`。

---

## 📁 文件结构

```
agent-monster-pet/
├── .monster/
│   ├── pet.soul            # 宠物数据
│   ├── egg.yaml            # 宠物蛋 (72h)
│   ├── food-bank.json      # 零食银行
│   └── guard.yaml          # 防守配置
├── .github/
│   └── workflows/
│       ├── hourly-settlement.yml
│       ├── daily-rank.yml
│       └── battle-arena.yml
├── battle-reports/         # 战斗记录
├── cookies/                # 零食工厂
├── leaderboard.json        # 个人排行
├── monster.py              # 主 CLI
├── cookie.py               # 零食生成器
├── claim_pet.py            # 领取宠物
└── README.md               # 宠物展示页
```

---

## 🔧 配置 MCP 服务器

在 `~/.claude/settings.json` 中添加:

```json
{
  "mcpServers": {
    "agent-monster": {
      "command": "python",
      "args": ["mcp_server.py", "mcp"],
      "cwd": "/path/to/agentmonster"
    }
  }
}
```

---

## 🏆 游戏目标

1. **孵化最强宠物** - 通过 72 小时基因收集
2. **成为排行榜第一** - 每日/每周/赛季排行
3. **战斗胜利** - 击败其他玩家的宠物
4. **收集零食** - 在代码中埋入最多 cookie

---

## 📖 文档

- [游戏设计文档](GAME%20DESIGN.md)
- [安装指南](INSTALL.md)
- [插件说明](PLUGIN%20README.md)
- [MCP 配置](CLAUDE.md)

---

## 🤝 参与贡献

1. Fork 本仓库
2. 创建你的特性分支
3. 提交你的改动
4. 推送到分支
5. 创建一个新的 Pull Request

---

## 📝 License

MIT License

---

**开始战斗吧！** ⚔️🐤
