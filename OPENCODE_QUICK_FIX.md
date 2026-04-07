# 🚀 OpenCode MCP 快速修复指南

## 问题和解决方案

### ❌ 问题
```
PaMCP • agent-monster MCP error -32000: Connection closed
```

### ✅ 根本原因
OpenCode 配置文件指向了不存在的路径

### 🔧 解决方案
配置文件已自动修复：
- **位置**: `~/.config/opencode/opencode.json`
- **改动**: 路径从 `agent-monster-pet/` 改为 `agent-monster/`
- **脚本**: 使用改进的 `mcp_server_fix.py`

---

## 快速验证

### 1️⃣ 验证修复

```bash
cd /root/pet/agent-monster
python3 verify_opencode_mcp.py
```

**预期输出**: `4/4 通过` ✅

### 2️⃣ 重启 OpenCode

1. 完全关闭 OpenCode
2. 等待 30 秒
3. 重新启动 OpenCode

### 3️⃣ 测试命令

在 OpenCode 中尝试：
```
/monster status
```

**预期结果**: 显示宠物状态，无错误 ✅

---

## 相关文件

| 文件 | 用途 |
|------|------|
| `OPENCODE_MCP_FIX.md` | 详细的修复文档 |
| `verify_opencode_mcp.py` | 验证脚本 |
| `mcp_server_fix.py` | 改进的 MCP 服务器 |
| `~/.config/opencode/opencode.json` | OpenCode 配置（已修复） |

---

## 如果仍有问题

### 步骤 1: 验证配置

```bash
cat ~/.config/opencode/opencode.json | grep -A3 agent-monster
```

应该看到：
```json
"agent-monster": {
  "type": "local",
  "command": ["python3", "/root/pet/agent-monster/mcp_server_fix.py", "mcp"],
```

### 步骤 2: 清除缓存

```bash
rm -rf ~/.config/opencode/cache
rm -rf ~/.cache/opencode
```

### 步骤 3: 完全重启

关闭并重新启动 OpenCode

### 步骤 4: 查看详细文档

查看 `OPENCODE_MCP_FIX.md` 获取更多帮助

---

## 已验证的功能

✅ MCP 初始化  
✅ 工具列表加载（30+ 工具）  
✅ JSON-RPC 协议兼容性  
✅ 连接稳定性  

---

## 提交信息

```
commit 67cf10c - Add verification script
commit 36f090b - Fix OpenCode MCP configuration path
commit ecb63ee - Improve MCP server connection handling
```

---

**修复状态**: ✅ 完成  
**验证状态**: ✅ 全部通过  
**Ready for**: 🚀 使用 OpenCode

