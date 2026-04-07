# Agent Monster 快速开始指南

## 1. 安装 (30 秒)

```bash
# Fork 并 Clone 仓库
git clone https://github.com/your-name/agent-monster-pet.git
cd agent-monster-pet

# Windows
install.bat

# Linux/macOS
./install.sh
```

**你将获得:**
- 🐤 小黄鸭 (初始宠物)
- 🥚 宠物蛋 (72 小时后孵化)

---

## 2. 埋零食 (随时)

在任何代码文件中添加零食注释：

```python
# 🍪 agent_monster cookie 0x67678328732673287
def my_function():
    pass
```

零食类型：
- 🍪 Cookie - +10 EXP
- 🍩 Donut - +50 EN
- 🍎 Apple - +5 全属性
- 🧬 Gene - 基因突变

---

## 3. 查看状态

```bash
# Claude Code 中
/monster status

# 或 CLI
python monster.py status
```

---

## 4. 等待孵化 (72 小时)

宠物蛋会根据你的行为基因孵化：

| 行为 | 基因 |
|------|------|
| 写代码 | Logic |
| 写文档 | Creative |
| 写配置 | Speed |
| 埋零食 | Lucky |

---

## 5. 战斗

```bash
# Claude Code 中
/monster duel opponent/repo
```

---

## GitHub Actions 自动化

仓库包含 3 个 Actions：

| Workflow | 频率 | 功能 |
|----------|------|------|
| `hourly-settlement.yml` | 每小时 | 结算零食、恢复能量 |
| `daily-rank.yml` | 每天 | 更新排行榜 |
| `battle-arena.yml` | 手动 | 战斗模拟 |

### 启用 Actions

```bash
gh workflow enable hourly-settlement.yml
gh workflow enable daily-rank.yml
gh workflow enable battle-arena.yml
```

---

## 文件说明

```
.monster/
├── pet.soul           # 宠物数据
├── egg.yaml           # 宠物蛋 (72h)
├── food-bank.json     # 零食银行
└── guard.yaml         # 防守配置

.github/workflows/
├── hourly-settlement.yml
├── daily-rank.yml
└── battle-arena.yml

monster.py             # 主 CLI
cookie.py              # 零食生成/扫描
claim_pet.py           # 领取宠物
```

---

## 常见问题

### Q: 宠物蛋多久孵化？
A: 72 小时，从领取时开始计算。

### Q: 零食可以被别人看到吗？
A: 可以，零食在代码注释中是公开的。

### Q: 如何战斗？
A: 使用 `/monster duel <对手仓库>` 发起挑战。

### Q: 排行榜在哪？
A: 每个仓库的 `leaderboard.json` 和中央汇总仓库。

---

**祝你玩得开心！** 🎮
