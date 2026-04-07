# Agent Monster 安装指南

## 步骤 1: 安装 Python 依赖

```bash
cd C:/Users/Administrator/agentmonster
pip install -r requirements.txt
```

## 步骤 2: 配置 MCP 服务器

### 方法 A: 使用项目的 .mcp.json（推荐）

项目已包含 `.mcp.json` 文件，Claude Code 会自动检测。

启动 Claude Code 时，会提示是否启用 MCP 服务器，输入 `y` 确认。

### 方法 B: 手动配置 settings.json

在 `~/.claude/settings.json` 中添加：

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

## 步骤 3: 启用 MCP 服务器权限

在 Claude Code 中运行：

```
/mcp
```

然后找到 `agent-monster` 并启用它。

或者直接在设置中授权：

```
/permission mcp__agent-monster__monster_init
/permission mcp__agent-monster__monster_status
/permission mcp__agent-monster__monster_analyze
/permission mcp__agent-monster__monster_traps
/permission mcp__agent-monster__monster_duel
```

## 步骤 4: 测试安装

在 Claude Code 中输入：

```
/monster status
```

如果看到宠物状态信息，说明安装成功！

## 故障排除

### MCP 服务器未加载

检查日志：
```bash
python mcp_server.py mcp < /dev/null 2>&1 | head -20
```

### 缺少依赖

```bash
pip install pyyaml
```

### 权限不足

在 Claude Code 中输入：
```
/permission mcp__agent-monster
```

## 使用方法

安装完成后，使用以下命令玩游戏：

| 命令 | 功能 |
|------|------|
| `/monster init` | 孵化你的代码宠物 |
| `/monster status` | 查看宠物状态 |
| `/monster analyze` | 分析仓库更新属性 |
| `/monster traps` | 扫描代码陷阱 |
| `/monster duel` | 发起对战挑战 |
