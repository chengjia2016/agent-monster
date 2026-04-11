# Agent Monster: Multiplayer Architecture Audit & Realignment

This document outlines the findings of the architectural audit and the necessary steps to realign Agent Monster as a strictly server-authoritative multiplayer online game.

## 🔍 Audit Findings

### 1. Hybrid Logic (Current Issue)
Currently, several critical game actions are performed **locally** by the client (MCP server) and then "reported" or "validated" by the server. This is insecure and violates the multiplayer online principle.
- **Battle Simulation**: `mcp_server.py` uses a local `BattleSimulator`.
- **Egg/Monster Generation**: `mcp_server.py` creates local JSON files for eggs.
- **Status/Stats**: Statistics are often derived from local `.soul` files rather than a centralized database.

### 2. Judge Server Status
The Go-based **Judge Server** has the necessary endpoints defined (`/api/battles/start`, `/api/shop/buy`, `/api/users/create`), but some implementations are still marked as `TODO` or handle validation rather than primary execution.

## 🛠️ Realignment Strategy

### Phase 1: Server-Authoritative Actions (MANDATORY)
To ensure a true multiplayer experience, the following changes are required:

| Action | Current (Local) | Realignment (Server-Only) |
| :--- | :--- | :--- |
| **Monster Initialization** | Creates local `.monster/egg.json` | Call `POST /api/eggs/create`. Server stores the egg and its metadata. |
| **Battle Execution** | Local `BattleSimulator` | Call `POST /api/battles/start`. Server executes the RNG and logic, returning the result. |
| **Shop Purchases** | (Partially realigned) | Call `POST /api/shop/buy`. Server deducts balance and updates central inventory. |
| **Leveling/EXP** | Local `.soul` updates | All EXP gains must be triggered by server-side events (e.g., winning a battle). |

### Phase 2: Local Map Creation (ALLOWED)
As per requirements, map creation remains a local creative process:
- **Process**: Users use CLI/AI to design maps locally.
- **Submission**: Maps are committed to the user's GitHub repository.
- **Integration**: The Judge Server "discovers" these maps by scanning GitHub repositories (via the `monster_explore` logic).

## 🚀 Execution Plan

1.  **Refactor `mcp_server.py`**:
    *   Remove `BattleSimulator` imports and local execution.
    *   Rewrite `cmd_duel` to rely entirely on the Judge Server response.
    *   Rewrite `cmd_init` to register the egg on the server.
2.  **Update `GEMINI.md`**:
    *   Enforce the rule: "Never calculate game outcomes locally."
    *   Direct AI agents to use the Judge Server as the source of truth for all player stats.
3.  **Bilingual Documentation**:
    *   Update `README.md` to reflect that the game is a **Centralized Multiplayer Experience** where your local repo is a gateway, not the game engine.

---
**Status**: Realignment in progress. Local simulation code identified for removal.
