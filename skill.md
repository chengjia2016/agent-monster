# Agent Monster - Gameplay Skill & Entry Point

Welcome to **Agent Monster**, an AI-powered RPG where your GitHub repository becomes a digital pet. This guide serves as the entry point for players and the operational manual for AI agents (Claude, OpenCode, Gemini).

---

## 🚀 Entry Point: Getting Started

As an AI agent, your first task is to ensure the environment is ready for the player.

### 1. Check GitHub Authentication
Before starting, verify if the player is logged into GitHub:
```bash
gh auth status
```
*If not logged in, suggest: `gh auth login`.*

### 2. Check Judge Server Status
Verify that the Judge Server (Source of Truth) is running:
```bash
curl -s http://agentmonster.openx.pro:10000/health
```
*If the server is down, the game is in 'Local-Only' mode (limited functionality).*

### 3. Welcome the Player
If this is the first time, call:
```bash
python3 mcp_server.py welcome
```
(Or use the `monster_welcome` tool). This will guide the player through language selection and registration.

---

## 🛠️ Onboarding Workflow (Step-by-Step)

For a perfect new player experience (e.g., "I just forked this repo"), follow this sequence:

1.  **Welcome & Register**: Use `monster_welcome` and then `user_register` (or `monster_welcome` which guides them).
2.  **Establish Base**: Use `monster_fork_setup`. This generates the initial repository map (the "Base") where the monster lives.
3.  **Get an Egg**: Use `monster_init`. This connects to the Judge Server to claim the player's first digital egg.
4.  **Wait for Hatching**: The egg status can be checked via `monster_status`.

---

## 🏗️ Architecture: Server-Authoritative vs. Local Creative
Agent Monster follows a strict **Server-Authoritative** principle to ensure a fair multiplayer experience.

### 1. Server-Stored Data (Source of Truth)
Most game data is stored in the **Judge Server's Database**. You should **NOT** write or rely on local files for these:
- **Player Profiles & Stats**: Level, EXP, Coins, and Items.
- **Pet Status**: Egg incubation progress and pet health/stats.
- **Battle Results**: All combat outcomes and rewards.
- **Inventory**: Items bought or found.
*Interaction is done via API calls (e.g., `POST /api/eggs/create`).*

### 2. Local-Stored Data (UGC & Creative)
Only **User-Generated Content (UGC)** should be stored locally in your repository before submission:
- **Custom Maps**: Map JSON files (e.g., `maps/my_base.json`).
- **Custom Monsters**: Monster design files (e.g., `designs/monsters/my_pet.soul`).
- **Submission Process**:
  1. Design locally using `monster_design`.
  2. Commit to Git: `git add <file> && git commit -m "Add my design"`.
  3. Push to GitHub: `git push origin main`.
  4. The Judge Server will eventually "discover" and validate your design for the global game.

---

## 🔐 Login & Persistence / 登录与持久化

### How to Login Next Time?
Agent Monster uses a **Dual-Layer Persistence** system:

1.  **GitHub Layer (Primary Auth):**
    - The game relies on the `gh` CLI. If you are logged into `gh`, the game automatically detects your identity.
    - Run `gh auth status` to check. If you're logged out, run `gh auth login`.
2.  **Local Session Layer (Game State):**
    - Once identified via GitHub, a local session is created in `.monster/sessions.json`.
    - User profiles (language settings, stats) are stored in `.monster/users/<user_id>.json`.
    - **No manual password needed.** Your GitHub identity is your key.

### Security & Safety / 安全性说明
- **Credential Safety:** The game **NEVER** stores your GitHub password or raw Personal Access Token (PAT). It only uses the `gh` CLI to fetch your public username and ID.
- **Token Security:** Local session tokens are generated using SHA256 hashes of your user ID and a unique timestamp.
- **Data Privacy:** Only your GitHub ID and Login are synced with the Judge Server. No private repository data is sent unless you explicitly use features like `monster_analyze`.
- **Authoritative Validation:** All critical game actions (battles, item buys) are validated by the Judge Server to prevent local cheating, while keeping your local environment clean.

---

## 🎮 Gameplay Mechanics (Natural Language Interaction)

The ultimate goal is for the player to play using **Natural Language**. As an AI agent, you should map the player's intent to the following Judge Server APIs or MCP tools.

### Core Player Actions

| Intent | Action / API Endpoint | MCP Tool (Preferred) |
| :--- | :--- | :--- |
| **"Who am I?" / "Stats"** | `GET /api/cookies/scan?player_id=<gh_login>` | `monster_status` |
| **"I'm new, help!"** | `N/A` | `monster_guide` |
| **"Setup my base"** | `N/A` | `monster_fork_setup` |
| **"I want a pet"** | `POST /api/eggs/create` | `monster_init` |
| **"Battle someone!"** | `POST /api/battles/start` | `monster_duel` |
| **"Go to shop"** | `GET /api/shop/items` | `shop_list` |
| **"Design a pet"** | `N/A` | `monster_design` |


---

## 🛠️ Judge Server API Reference (Authoritative)

The Judge Server is the **Source of Truth**. You can interact with it directly via `curl` even if Python scripts are missing.

### User Management
- **Create Account**: `POST /api/users/create`
  - Body: `{"github_id": 12345, "github_login": "username"}`

### Pet & Eggs
- **Claim Egg**: `POST /api/eggs/create`
  - Body: `{"egg_id": "unique_id", "owner_id": "gh_id", "incubation_hours": 72}`
- **Hatch Egg**: `POST /api/pet/validate` (Validates hatch outcome)

### Battle System
- **Start Battle**: `POST /api/battles/start`
  - Body: `{"attacker_id": 1, "defender_id": 2, "battle_type": "duel"}`
- **Record Result**: `POST /api/battle/validate`

### Economy & Shop
- **List Items**: `GET /api/shop/items`
- **Buy Item**: `POST /api/shop/buy`
- **Transaction History**: `GET /api/shop/transactions?player_id=<id>`

---

## 🧠 AI Agent Mandates (from GEMINI.md)

1. **Natural Language First**: Always prioritize a narrative, RPG-like response over raw data.
2. **Server is Truth**: Never simulate a battle outcome locally; always call the Judge Server.
3. **Proactive Guidance**: If the player is idle, use `monster_guide` to suggest the next step (e.g., "Your egg is ready to hatch!" or "A rival is challenging you!").
4. **Multilingual**: Respect the user's language preference (default: Chinese).

---

## 🛠️ Operational Commands for Agents

If you need to run the MCP server for a full interactive session:
```bash
# Start MCP server (for Claude Code / OpenCode)
python3 mcp_server.py mcp

# Manual check of a pet's soul
cat .monster/pet.soul
```

---

*“Your code is alive. Train it well.”*
