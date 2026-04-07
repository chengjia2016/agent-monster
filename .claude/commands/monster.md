# /monster command

Agent Monster 游戏命令 - 通过 MCP 工具调用

## 使用方法

输入 `/monster <command>` 来玩游戏。

## 可用命令

### `/monster init`
初始化你的代码宠物，分析最近 72 小时的 Git 提交历史。

### `/monster status`
查看宠物的当前状态，包括等级、属性、进化阶段。

### `/monster analyze`
分析仓库活动并更新宠物属性。

### `/monster traps`
扫描代码中的逻辑陷阱（@monster-trap 注释）。

### `/monster duel`
向另一个仓库发起对战挑战。

## MCP 工具调用

如果 MCP 服务器已配置，以上命令会自动调用对应的 MCP 工具：
- `monster_init`
- `monster_status`
- `monster_analyze`
- `monster_traps`
- `monster_duel`

## 配置

在项目根目录创建 `.mcp.json` 文件：

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

然后在 Claude Code 中启用 MCP 服务器权限。
