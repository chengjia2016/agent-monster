# Agent Monster Installation Guide

## Step 1: Install Python Dependencies

```bash
cd /path/to/agent-monster
pip install -r requirements.txt
```

## Step 2: Configure MCP Server

### Method A: Use Project's .mcp.json (Recommended)

The project includes a `.mcp.json` file that Claude Code will automatically detect.

When you start Claude Code, it will prompt whether to enable the MCP server. Enter `y` to confirm.

### Method B: Manually Configure settings.json

Add to `~/.claude/settings.json`:

**Windows:**
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

**Linux/macOS:**
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

## Step 3: Enable MCP Server Permissions

Run in Claude Code:

```
/mcp
```

Then find `agent-monster` and enable it.

Or authorize directly:

```
/permission mcp__agent-monster__monster_init
/permission mcp__agent-monster__monster_status
/permission mcp__agent-monster__monster_analyze
/permission mcp__agent-monster__monster_traps
/permission mcp__agent-monster__monster_duel
```

## Step 4: Test Installation

Enter in Claude Code:

```
/monster status
```

If you see pet status information, the installation was successful!

## Troubleshooting

### MCP Server Not Loading

Check logs:
```bash
python mcp_server.py mcp < /dev/null 2>&1 | head -20
```

### Missing Dependencies

```bash
pip install pyyaml
```

### Insufficient Permissions

Enter in Claude Code:
```
/permission mcp__agent-monster
```

## Usage

After installation, use the following commands to play:

| Command | Function |
|---------|----------|
| `/monster init` | Claim your starter pet |
| `/monster status` | View pet status |
| `/monster analyze` | Analyze repository |
| `/monster traps` | Scan code traps |
| `/monster duel` | Start a battle challenge |
