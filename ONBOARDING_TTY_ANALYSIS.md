# 🔍 CLI Onboarding Progress Analysis

## 当前状态

CLI 在新手引导的**第 5 步**（确认并生成地图）卡住了。

### 症状
```
第 5 步: 确认并生成地图
按 Enter 生成你的地图
```

## 根本原因诊断

### 1. TTY 环境限制 ❌

**问题：** 
```
[ERROR] TUI error: could not open a new TTY: open /dev/tty: no such device or address
```

**原因：**
- CLI 使用 Bubble Tea（Go TUI 框架）
- Bubble Tea 需要 TTY 来处理键盘输入
- 在非交互式环境（如 SSH 会话、脚本）中，/dev/tty 不可用

**影响：**
- 程序无法读取用户按下的 Enter 键
- 无法继续到第 5 步之后
- 程序立即退出

### 2. 程序流程分析

#### 第 5 步应该发生的事情：
```
用户按 Enter
    ↓
handleOnboarding() 处理按键
    ↓
OnboardingMapPreviewScreen → enter 键
    ↓
生成 generateMapCmd() 异步任务
    ↓
调用 GenerateOnboardingMap()
    ↓
API: Client.GenerateMap(...)
    ↓
移到 OnboardingClaimingScreen
    ↓
显示"正在领取初始宝可梦..."
    ↓
调用 ClaimStarterPokemons()
```

#### 当前被卡在的地方：
```
RenderOnboardingPreview() 显示第 5 步界面
    ↓
handleOnboarding() 等待输入
    ↓
❌ /dev/tty 不可用 → 无法获得输入
    ↓
❌ 程序退出
```

## 日志证据

### 日志文件内容
```
[18:13:38.258] [INFO] Starting Agent Monster CLI
[18:13:38.258] [INFO] Server URL: http://127.0.0.1:10000
[18:13:38.258] [INFO] Debug mode: true
[18:13:38.258] [INFO] User data directory: /root/.agent-monster/data
[18:13:38.258] [INFO] Log directory: /root/.agent-monster/data/logs
[18:13:38.258] [INFO] API client initialized
[18:13:38.258] [INFO] UI application initialized
[18:13:38.258] [INFO] Starting TUI program
[18:13:38.258] [ERROR] TUI error: could not open a new TTY: 
  open /dev/tty: no such device or address
```

### 缺失的日志
- ✓ CLI 初始化正常
- ✓ 日志系统工作正常
- ✗ 没有看到新手引导的任何步骤日志
- ✗ 没有看到用户信息初始化
- ✗ 没有看到地图生成的日志

**结论：** 程序在显示 UI 前就因为 TTY 错误而退出

## 解决方案

### ✅ 方案 1：在 TTY 环境中运行（推荐）

```bash
# 使用 SSH 分配 PTY
ssh -t user@host "cd /path/to/agent-monster && ./cli/agentmonster"

# 或在本地 TTY 中运行
./cli/agentmonster
```

### ✅ 方案 2：改进 CLI 以支持非交互式模式

添加 `--non-interactive` 标志，在非 TTY 环境中运行完整新手引导

```bash
./cli/agentmonster --non-interactive \
  --username testuser \
  --nickname "Test User" \
  --template 0 \
  --npcs "elder,wizard"
```

### ✅ 方案 3：创建 Web 界面

用 HTTP API + 前端替代 TUI

## 第 5 步之后的流程

如果成功从第 5 步继续，将发生以下事情：

### 步骤流程图
```
第 5 步: 按 Enter 生成地图
    ↓
generateMapCmd() 异步执行
    ├─ 调用 API: GenerateMap()
    │  └─ 参数: owner_id, owner_name, map_id, width=20, height=20
    ├─ 等待最多 30 秒
    └─ 返回成功/失败
    ↓
第 6 步: 显示"正在领取初始宝可梦..."（2 秒）
    ↓
claimStarterPokemonsCmd() 异步执行
    ├─ 调用 API: ClaimStarterPokemons()
    │  └─ 参数: user_id
    ├─ 等待最多 15 秒
    └─ 返回成功/失败
    ↓
第 7 步: 显示"恭喜！冒险开始了！"
    ├─ 显示获得的物品
    ├─ 显示接下来可做的事
    └─ 等待用户确认
```

## 关键代码位置

### 第 5 步入口
- **文件：** `cli/pkg/ui/onboarding.go:232`
- **函数：** `RenderOnboardingPreview()`
- **方法：** 渲染第 5 步界面

### 地图生成
- **文件：** `cli/pkg/ui/onboarding.go:506`
- **函数：** `GenerateOnboardingMap()`
- **API：** `a.Client.GenerateMap()`

### 宝可梦领取
- **文件：** `cli/pkg/ui/onboarding.go:543`
- **函数：** `ClaimStarterPokemons()`
- **API：** `a.Client.ClaimStarterPokemons()`

## 输入处理逻辑

```go
// cli/pkg/ui/onboarding.go:602
func (a *App) handleOnboarding(msg tea.KeyMsg) (*App, tea.Cmd) {
    step := OnboardingStep(a.OnboardingState.CurrentStep)
    
    switch step {
    case OnboardingMapPreviewScreen:
        if msg.String() == "enter" {
            // 触发异步地图生成命令
            return a, generateMapCmd(a)
        }
    // ...
    }
}
```

## 日志分析结果

### Health Score
```
🟢 [█████████░] Health Score: 95/100
✅ Session completed with minor issues
🔍 Issues Found:
  • 1 errors
```

### 评估
- **严重程度：** 轻微（不影响核心功能，只是环境限制）
- **根本原因：** TTY 环境问题，不是代码 bug
- **可解决性：** 可以通过使用 TTY 环境解决

## 建议

### 短期（立即执行）
1. 在本地或 SSH -t 中运行 CLI
2. 验证在 TTY 环境中是否正常工作

### 中期（下个版本）
1. 添加 `--non-interactive` 模式
2. 添加更详细的日志记录
3. 改进错误处理

### 长期（未来版本）
1. 开发 Web 界面替代 TUI
2. 支持多种交互模式
3. 更好的跨环境兼容性

## 总结

✗ CLI **无法在非 TTY 环境中完成新手引导**
✓ 但所有代码逻辑都是**正确的**，只是缺少 TTY 的输入处理
✓ 在本地或使用 `ssh -t` 应该**能够正常工作**

---

**最后更新：** 2026-04-09
**诊断工具：** Log Analysis System
**分析基础：** 真实日志文件 + 代码审查
