# Agent Monster

> 🐤 Turn your GitHub repository into a digital pet and battle other developers!

**Agent Monster** is a slow-paced Cultivation game built on the GitHub ecosystem. Your code repository is the pet's home, and code commits are the pet's food.

---

## 🤖 Playing with OpenCode

OpenCode is an AI-powered coding assistant that can help you play Agent Monster directly from your terminal.

### Easiest Way to Get Started

> **Just tell your AI agent:** *"Go to https://github.com/chengjia2016/agent-monster-pet and set up Agent Monster for me"*
>
> Your agent will automatically clone the repository, install dependencies, and configure the MCP server.

### Manual Setup (Optional)

1. **Install OpenCode/Claude Code** (if not already installed)

2. **Configure MCP Server** in `~/.claude/settings.json` or `~/.opencode/settings.json`:

```json
{
  "mcpServers": {
    "agent-monster": {
      "command": "python3",
      "args": ["mcp_server.py", "mcp"],
      "cwd": "/path/to/agent-monster-pet"
    }
  }
}
```

3. **Restart OpenCode** to load the MCP server

### Available Commands in OpenCode

Once configured, you can use these natural language commands:

```
/monster init       - Initialize your code pet
/monster status     - View pet stats and genes
/monster analyze    - Analyze repo activity (last 7 days)
/monster traps      - Scan code for defensive traps
/monster duel       - Challenge another repo to battle
```

### Example Gameplay Session

```
You: /monster init
OpenCode: 🥚 Your pet has been created! Species: Hybrid

You: /monster status
OpenCode: Shows your pet's stats, level, and battle history

You: /monster analyze
OpenCode: Analyzes your commits and updates pet genes

You: /monster attack https://github.com/chengjia2016/agent-monster-pet/demo_duck
OpenCode: ⚔️ Battle vs 呆呆的小黄鸭! You won!
```

### Battle Commands

| Command | Description |
|---------|-------------|
| `/monster attack demo_duck` | Attack the demo pet (local test) |
| `/monster attack https://github.com/chengjia2016/agent-monster-pet/demo_duck` | Attack demo pet via GitHub URL |
| `/monster attack https://github.com/username/repo` | Attack another player's pet |
| `/monster duel <target>` | Same as attack (alias) |
OpenCode: Analyzes your commits and updates pet genes

You: /monster duel https://github.com/opponent/repo
OpenCode: ⚔️ Battle simulation complete! You won!
```

### Tips for OpenCode Players

- **Commit often** - Your commits shape your pet's genes
- **Hide cookies** in code comments for bonus EXP
- **Scan traps** before battling to find defensive advantages
- **Analyze weekly** to keep your pet's stats updated

---

---

## 🚀 Quick Start

### 1. Fork the Base Repository

```bash
# Using GitHub CLI
gh repo fork agent-monster/agent-monster-pet

# Or fork manually on GitHub
```

### 2. Clone to Your Local Machine

```bash
git clone https://github.com/chengjia2016/agent-monster-pet
cd agent-monster-pet
```

### 3. Install and Claim Your Pet

```bash
# Windows
install.bat

# Linux/macOS
./install.sh
```

**Initial Rewards:**
- 🐤 **Little Yellow Duck** (Starter Pet)
- 🥚 **Pet Egg** x1 (Hatches after 72 hours)

---

## 🎮 Gameplay

### Food System (Cookie)

Hide food items in code comments across any repository:

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

**Food Types:**
| Food | Effect |
|------|--------|
| 🍪 Cookie | +10 EXP |
| 🍩 Donut | +50 EN |
| 🍎 Apple | +5 All Stats |
| 🧬 Gene | Gene Mutation (during hatching) |

### Egg Incubation

The pet egg requires **72 hours** to collect behavioral genes:

| Behavior | Gene Impact |
|----------|-------------|
| Writing Code (commits) | Logic Gene |
| Writing Docs (md files) | Creative Gene |
| Writing Configs (yaml/json) | Speed Gene |
| Hiding Cookies | Lucky Gene |

### Battle System

```bash
# In Claude Code
/monster duel opponent/repo
```

---

## 📡 GitHub Actions Game Server

This project uses GitHub Actions as the game server:

| Workflow | Frequency | Purpose |
|----------|-----------|---------|
| `hourly-settlement.yml` | Hourly | Settle cookies, restore energy |
| `daily-rank.yml` | Daily | Update leaderboards |
| `battle-arena.yml` | Manual/Trigger | Battle simulation |

### Enable Actions

```bash
gh workflow enable hourly-settlement.yml
gh workflow enable daily-rank.yml
gh workflow enable battle-arena.yml
```

---

## 🎯 Command Reference

### Claude Code MCP Commands

```
/monster init       - Claim starter pet
/monster status     - View pet status
/monster analyze    - Analyze repository activity
/monster traps      - Scan code traps
/monster duel       - Start a battle challenge
```

### CLI Commands

```bash
python monster.py status     # View status
python monster.py analyze    # Analyze repository
python monster.py traps      # Scan traps
python cookie.py generate    # Generate food
python cookie.py scan        # Scan food items
```

---

## 📊 Leaderboards

### Personal Leaderboard

Each repository's `leaderboard.json`:

```json
{
  "player": "your-name",
  "pet_name": "Little Yellow Duck",
  "level": 25,
  "battles": {
    "win": 15,
    "lose": 8
  }
}
```

### Global Leaderboard

The central repository aggregates all players' `leaderboard.json` files.

---

## 📁 File Structure

```
agent-monster-pet/
├── .monster/
│   ├── pet.soul            # Pet data
│   ├── egg.yaml            # Pet egg (72h)
│   ├── food-bank.json      # Food bank
│   └── guard.yaml          # Defense config
├── .github/
│   └── workflows/
│       ├── hourly-settlement.yml
│       ├── daily-rank.yml
│       └── battle-arena.yml
├── battle-reports/         # Battle records
├── cookies/                # Food factory
├── leaderboard.json        # Personal leaderboard
├── monster.py              # Main CLI
├── cookie.py               # Food generator
├── claim_pet.py            # Claim pet
└── README.md               # Pet showcase page
```

---

## 🔧 Configure MCP Server

Add to `~/.claude/settings.json`:

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

## 🏆 Game Objectives

1. **Hatch the Strongest Pet** - Collect genes over 72 hours
2. **Top the Leaderboard** - Daily/Weekly/Season rankings
3. **Win Battles** - Defeat other players' pets
4. **Collect Food** - Hide the most cookies in code

---

## 📖 Documentation

- [Game Design](GAME%20DESIGN.md)
- [Installation Guide](INSTALL.md)
- [Plugin README](PLUGIN%20README.md)
- [MCP Configuration](CLAUDE.md)
- [Quick Start](QUICKSTART.md)

---

## 🤝 Contributing

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

---

## 📝 License

MIT License

---

**Start Battling!** ⚔️🐤
