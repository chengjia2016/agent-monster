# Agent Monster 游戏设计文档

## 游戏概述

**Agent Monster** 是一个基于 GitHub 生态的慢节奏养成游戏。你的代码仓库就是宠物的家，代码提交就是宠物的食物。

---

## 核心玩法

### 1. 开始游戏

```bash
# 1. Fork/Clone 基地仓库
git clone https://github.com/your-name/agent-monster-pet.git

# 2. 安装 CLI 工具
pip install -r requirements.txt

# 3. 领取初始宠物
python monster.py init
```

**初始奖励:**
- 🐤 小黄鸭 (初始宠物)
- 🥚 宠物蛋 x1 (72 小时后孵化)

### 2. 宠物蛋孵化机制

宠物蛋需要 **72 小时** 收集行为基因，然后孵化：

| 行为 | 基因影响 |
|------|----------|
| 写代码 (commits) | Logic 基因 |
| 写文档 (md 文件) | Creative 基因 |
| 写配置 (yaml/json) | Speed 基因 |
| 埋零食 (cookie) | Lucky 基因 |

### 3. 零食系统 (Cookie)

在任何 GitHub 仓库的代码注释中埋入零食：

```python
# 🍪 agent_monster cookie 0x67678328732673287
def my_function():
    pass
```

```javascript
// 🍪 agent_monster cookie 0xabcdef1234567890
const x = 1;
```

```markdown
<!-- 🍪 agent_monster cookie 0x1234567890abcdef -->
```

**零食类型:**
| 零食 | 效果 | 持续时间 |
|------|------|----------|
| 🍪 Cookie | +10 EXP | 即时 |
| 🍩 Donut | +50 EN | 1 小时 |
| 🍎 Apple | +5 全属性 | 24 小时 |
| 🧬 Gene | 基因突变 | 孵化时 |

### 4. 能量系统

宠物需要能量才能战斗：

- **EN (Energy)**: 战斗消耗
- **EXP (Experience)**: 升级经验
- **Token 配额**: 每日 API 调用次数

**能量恢复:**
- GitHub 绿墙 (commit) → +10 EN/天
- 零食投喂 → +5~50 EN
- 自然恢复 → 5 EN/小时

---

## GitHub Actions 游戏服务器

### 1. 每小时结算 (hourly-settlement.yml)

```yaml
name: Hourly Settlement
on:
  schedule:
    - cron: '0 * * * *'  # 每小时
  workflow_dispatch:

jobs:
  settlement:
    runs-on: ubuntu-latest
    steps:
      - 扫描所有玩家仓库的 cookie
      - 结算能量恢复
      - 更新 pet.soul
      - 推送排行榜
```

### 2. 每日排行 (daily-rank.yml)

```yaml
name: Daily Rank
on:
  schedule:
    - cron: '0 0 * * *'  # 每天午夜
  workflow_dispatch:

jobs:
  rank:
    runs-on: ubuntu-latest
    steps:
      - 收集所有玩家数据
      - 计算等级/属性排行
      - 更新 leaderboard.json
      - 发布成就徽章
```

### 3. 战斗竞技场 (battle-arena.yml)

```yaml
name: Battle Arena
on:
  repository_dispatch:
    types: [challenge]
  workflow_dispatch:
    inputs:
      opponent:
        description: '对手仓库'
        required: true

jobs:
  battle:
    runs-on: ubuntu-latest
    steps:
      - 下载双方 pet.soul
      - 运行战斗模拟器
      - 生成 battle-report.json
      - 创建 PR/Merge 请求
      - 更新玩家数据
```

---

## 数据流

### 玩家指令提交

```
玩家 → 创建 Issue / 调用 API → GitHub Actions → 处理逻辑 → 回写结果
```

### 战斗流程

```
1. 玩家 A 发起挑战 (Issue/API)
2. Action 下载双方 pet.soul
3. 运行 battle_logic.py
4. 生成 battle-report.json
5. 创建 PR 到输的一方
6. 更新 leaderboard.json
```

---

## 排行榜系统

### 个人排行榜 (每人仓库内)

```json
{
  "player": "your-name",
  "pet_name": "小黄鸭",
  "level": 25,
  "battles": {
    "win": 15,
    "lose": 8
  },
  "rank": {
    "global": 127,
    "weekly": 45
  }
}
```

### 总排行榜 (中央仓库)

```json
{
  "season": "2026-Q2",
  "last_updated": "2026-04-07T12:00:00Z",
  "leaderboard": [
    {
      "rank": 1,
      "player": "top-coder",
      "pet_name": "CodeDragon",
      "level": 99,
      "win_rate": 0.85
    },
    {
      "rank": 2,
      "player": "your-name",
      "pet_name": "小黄鸭",
      "level": 25,
      "win_rate": 0.65
    }
  ]
}
```

---

## 文件结构

```
agent-monster-pet/          # 玩家仓库
├── .monster/
│   ├── pet.soul            # 宠物数据
│   ├── egg.yaml            # 宠物蛋 (72h)
│   ├── food-bank.json      # 零食银行
│   └── guard.yaml          # 防守配置
├── cookies/
│   └── generate.py         # 生成零食工具
├── .github/
│   └── workflows/
│       ├── hourly-settlement.yml
│       ├── daily-rank.yml
│       └── battle-arena.yml
├── battle-reports/         # 战斗记录
├── leaderboard.json        # 个人排行
└── README.md               # 宠物展示页
```

---

## 安装流程 (简化版)

```bash
# 1. Fork 基地仓库
gh repo fork agent-monster/agent-monster-pet

# 2. Clone 到本地
git clone https://github.com/your-name/agent-monster-pet.git
cd agent-monster-pet

# 3. 安装依赖
pip install -r requirements.txt

# 4. 领取宠物
python monster.py init

# 5. 启用 Actions
gh workflow enable hourly-settlement.yml
gh workflow enable daily-rank.yml
gh workflow enable battle-arena.yml
```

---

## 下一步开发计划

1. **Phase 1**: 简化安装流程
2. **Phase 2**: 实现零食系统
3. **Phase 3**: GitHub Actions 游戏服务器
4. **Phase 4**: 排行榜和战斗系统
5. **Phase 5**: MCP/Plugin 集成
