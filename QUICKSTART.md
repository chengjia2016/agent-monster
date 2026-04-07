# Agent Monster Quick Start Guide

## 1. Installation (30 seconds)

```bash
# Fork and Clone the repository
git clone https://github.com/your-name/agent-monster-pet.git
cd agent-monster-pet

# Windows
install.bat

# Linux/macOS
./install.sh
```

**You Will Get:**
- 🐤 Little Yellow Duck (Starter Pet)
- 🥚 Pet Egg x1 (Hatches after 72 hours)

---

## 2. Hide Food (Anytime)

Add food cookies in code comments:

```python
# 🍪 agent_monster cookie 0x67678328732673287
def my_function():
    pass
```

```javascript
// 🍩 agent_monster cookie 0xabcdef1234567890
const x = 1;
```

**Food Types:**
- 🍪 Cookie - +10 EXP
- 🍩 Donut - +50 EN
- 🍎 Apple - +5 All Stats
- 🧬 Gene - Gene Mutation

---

## 3. View Status

```bash
# In Claude Code
/monster status

# Or CLI
python monster.py status
```

---

## 4. Wait for Incubation (72 hours)

The pet egg hatches based on your behavioral genes:

| Behavior | Gene Type |
|----------|-----------|
| Writing Code | Logic |
| Writing Docs | Creative |
| Writing Configs | Speed |
| Hiding Cookies | Lucky |

---

## 5. Battle

```bash
# In Claude Code
/monster duel opponent/repo
```

---

## GitHub Actions Automation

The repository includes 3 Actions:

| Workflow | Frequency | Purpose |
|----------|-----------|---------|
| `hourly-settlement.yml` | Hourly | Settle cookies, restore energy |
| `daily-rank.yml` | Daily | Update leaderboards |
| `battle-arena.yml` | Manual | Battle simulation |

### Enable Actions

```bash
gh workflow enable hourly-settlement.yml
gh workflow enable daily-rank.yml
gh workflow enable battle-arena.yml
```

---

## File Structure

```
.monster/
├── pet.soul           # Pet data
├── egg.yaml           # Pet egg (72h)
├── food-bank.json     # Food bank
└── guard.yaml         # Defense config

.github/workflows/
├── hourly-settlement.yml
├── daily-rank.yml
└── battle-arena.yml

monster.py             # Main CLI
cookie.py              # Food generator/scanner
claim_pet.py           # Claim pet
```

---

## FAQ

### Q: How long does the egg take to hatch?
A: 72 hours, starting from when you claim it.

### Q: Can others see the cookies I hide?
A: Yes, cookies in code comments are public.

### Q: How do I battle?
A: Use `/monster duel <opponent/repo>` to start a challenge.

### Q: Where is the leaderboard?
A: Each repository has a `leaderboard.json`, and there's a central aggregation repository.

---

**Have fun!** 🎮
