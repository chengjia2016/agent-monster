# 🎯 Agent Monster 新手引导流程 - 完整测试指南

## 📋 快速开始

### 1. 构建CLI
```bash
cd /root/pet/agent-monster/cli
go build -o agentmonster ./cmd
```

### 2. 运行CLI（带日志输出）
```bash
# 运行，日志会输出到终端和文件
./agentmonster

# 或者使用调试模式获得更详细的日志
./agentmonster --debug
```

### 3. 查看日志
```bash
# 查看最新的日志文件
cd /root/pet/agent-monster
./view_logs.sh

# 或者手动查看日志目录
ls ~/.agent-monster/data/logs/

# 实时查看日志
tail -f ~/.agent-monster/data/logs/agentmonster_*.log

# 过滤特定内容
grep "ERROR" ~/.agent-monster/data/logs/agentmonster_*.log
grep "API" ~/.agent-monster/data/logs/agentmonster_*.log
```

---

## 📊 新手引导流程 - 详细日志跟踪

### 🎬 第1步：欢迎屏幕

**预期日志：**
```
[HH:MM:SS.mmm] [INFO] Onboarding input: step=0, key=enter
[HH:MM:SS.mmm] [DEBUG] Onboarding state transition: WelcomeScreen -> ForkScreen
```

**如果卡住：** 按 `Enter` 键应该立即显示上述日志，表示输入被成功捕获。

---

### 🍴 第2步：Fork仓库

**预期日志：**
```
─────────────────────────────────────────────────────────────
▶ Fork GitHub Repository
─────────────────────────────────────────────────────────────
[HH:MM:SS.mmm] [INFO] Forking repository: anomalyco/agent-monster
[HH:MM:SS.mmm] [DEBUG] GitHub client request: fork
```

**常见问题和日志信号：**
- ✅ 成功：`[INFO] Repository forked successfully` 
- ❌ 失败：`[ERROR] Fork failed: ...`
- 🕐 超时：没有任何日志输出超过10秒

---

### 🏰 第3步：创建防守基地

**预期日志：**
```
─────────────────────────────────────────────────────────────
▶ 创建防守基地
─────────────────────────────────────────────────────────────
[HH:MM:SS.mmm] [INFO] Creating user base
```

---

### 🎨 第4步：选择地图模板

**预期日志：**
```
[HH:MM:SS.mmm] [DEBUG] Onboarding input: step=3, key=down
[HH:MM:SS.mmm] [DEBUG] Template selection updated: 0 -> 1
```

---

### 🤖 第5步：选择NPC

**预期日志：**
```
[HH:MM:SS.mmm] [DEBUG] Onboarding input: step=4, key=space
[HH:MM:SS.mmm] [DEBUG] NPC selection toggled
```

---

### 🗺️  第6步：生成地图（关键步骤）

**按 Enter 生成时的预期日志：**

```
[HH:MM:SS.mmm] [DEBUG] Onboarding input: step=5, key=enter
[HH:MM:SS.mmm] [INFO] 正在处理中，请稍候... (Loading screen shown)

─────────────────────────────────────────────────────────────
▶ 生成新手引导地图
─────────────────────────────────────────────────────────────
[HH:MM:SS.mmm] [INFO] Starting map generation
[HH:MM:SS.mmm] [DEBUG] User: tomcooler, Template: 0
[HH:MM:SS.mmm] [INFO] Generated map ID: tomcooler_starter_1

[HH:MM:SS.mmm] [INFO] Calling API: GenerateMap(owner_id=32, owner_name=tomcooler, map_id=tomcooler_starter_1, width=20, height=20)
[HH:MM:SS.mmm] [INFO] 🌐 API Request: POST /api/maps/generate
[HH:MM:SS.mmm] [DEBUG]   Payload: map[...]

[HH:MM:SS.mmm] [INFO] 📨 API Response: Status 201
[HH:MM:SS.mmm] [DEBUG]   Response: {"success":true,"map_id":"tomcooler_starter_1"...

[HH:MM:SS.mmm] [INFO] Map generated successfully
[HH:MM:SS.mmm] [DEBUG] Map ID: tomcooler_starter_1, Size: 20x20
```

**问题排查：**

1. **如果看到API错误（Status 400, 404等）：**
   ```
   [ERROR] ❌ API Error at /api/maps/generate: request failed with status 400: missing required fields
   ```
   → 检查参数是否正确（应该是 `owner_id` 和 `owner_name`，不是 `user_id`）

2. **如果看到超时：**
   ```
   [ERROR] Map generation timeout (30 seconds)
   ```
   → 检查网络连接，或Judge Server是否在运行

3. **如果没有任何日志输出：**
   → 可能CLI没有正确初始化日志系统
   → 尝试用 `--debug` 标志运行

---

### 🎁 第7步：领取宝可梦（关键步骤）

**预期日志：**

```
─────────────────────────────────────────────────────────────
▶ 领取宝可梦命令执行
─────────────────────────────────────────────────────────────
[HH:MM:SS.mmm] [INFO] Starting claiming pokemons command
[HH:MM:SS.mmm] [INFO] Displaying claiming screen for 2 seconds

─────────────────────────────────────────────────────────────
▶ 领取初始宝可梦
─────────────────────────────────────────────────────────────
[HH:MM:SS.mmm] [INFO] Claiming starter pokemons for user: tomcooler (ID: 32)
[HH:MM:SS.mmm] [INFO] 🌐 API Request: POST /api/user/claim-starter-pokemons
[HH:MM:SS.mmm] [DEBUG]   Payload: map[user_id:32]

[HH:MM:SS.mmm] [INFO] 📨 API Response: Status 200
[HH:MM:SS.mmm] [DEBUG]   Response: {"success":true,"message":"Successfully claimed starter pokemons: 1 Psyduck + 2 Eggs"}

[HH:MM:SS.mmm] [INFO] Successfully claimed starter pokemons
[HH:MM:SS.mmm] [INFO] Claiming complete, transitioning to completion screen
```

**问题排查：**

1. **如果user_id为0：**
   ```
   [ERROR] User not authenticated: CurrentUser=..., ID=0
   ```
   → 用户账户在CLI启动时未正确初始化
   → 检查 GitHub 认证流程

2. **如果API返回 {user_id: 0}：**
   ```
   [ERROR] Failed to claim starter pokemons: user github_id is 0, cannot claim pokemons
   ```
   → 需要先创建用户账户
   → 或者使用 `--debug` 查看更详细的用户信息

---

### 🎉 第8步：完成屏幕

**预期日志：**
```
[HH:MM:SS.mmm] [INFO] Onboarding completed successfully
[HH:MM:SS.mmm] [DEBUG] Final state: OnboardingCompleteScreen
```

---

## 🐛 调试技巧

### 1. 启用调试模式
```bash
./agentmonster --debug
```
这会启用 DEBUG 级别日志，显示所有低级信息。

### 2. 监控日志实时变化
```bash
tail -f ~/.agent-monster/data/logs/agentmonster_*.log
```

### 3. 只查看错误
```bash
grep "ERROR\|❌" ~/.agent-monster/data/logs/agentmonster_*.log
```

### 4. 只查看API调用
```bash
grep "API Request\|API Response\|🌐\|📨" ~/.agent-monster/data/logs/agentmonster_*.log
```

### 5. 生成完整的日志分析报告
```bash
cat ~/.agent-monster/data/logs/agentmonster_*.log | grep -E "\[ERROR\]|\[WARN\]|failed|error"
```

---

## 📈 性能基准

### 正常情况下每一步的时间：

| 步骤 | 耗时 | 日志信号 |
|------|------|--------|
| Fork 仓库 | 2-5秒 | 看到 "Repository forked successfully" |
| 创建基地 | <1秒 | 看到 "Creating user base" |
| 选择模板/NPC | 即时 | 每个按键都有日志 |
| **生成地图** | **2-10秒** | "Map generated successfully" |
| **领取宝可梦** | **2-5秒** | "Successfully claimed starter pokemons" |
| 完成 | 即时 | 屏幕更新 |

如果某步超过15秒，检查日志中是否有超时错误。

---

## ✅ 完整测试清单

- [ ] CLI启动时显示初始化日志
- [ ] 按 Enter 进入Fork屏幕
- [ ] Fork成功，看到日志消息
- [ ] 选择地图模板
- [ ] 选择NPC
- [ ] 按 Enter 生成地图，看到"正在处理中"消息
- [ ] 地图生成完成，日志显示"Map generated successfully"
- [ ] 自动转移到领取屏幕
- [ ] 看到"Successfully claimed starter pokemons"
- [ ] 显示完成屏幕
- [ ] 按 Enter 回到主菜单

---

## 🚀 快速测试脚本

```bash
#!/bin/bash
# run_onboarding_test.sh

cd /root/pet/agent-monster

echo "🚀 Starting onboarding test..."
echo ""

# Kill previous instances
pkill -f "agentmonster"

# Start CLI with debug logging
echo "Starting CLI with debug mode..."
timeout 120 ./cli/agentmonster --debug > /tmp/cli_output.log 2>&1 &
CLI_PID=$!

# Wait a bit for startup
sleep 2

echo "✅ CLI started (PID: $CLI_PID)"
echo ""
echo "📋 Follow the onboarding steps in the terminal"
echo ""
echo "Log file: ~/.agent-monster/data/logs/agentmonster_*.log"
echo "View logs with: tail -f ~/.agent-monster/data/logs/agentmonster_*.log"

wait $CLI_PID

echo ""
echo "✅ Test completed"
echo ""
./view_logs.sh
```

保存为 `run_onboarding_test.sh` 并执行：
```bash
chmod +x run_onboarding_test.sh
./run_onboarding_test.sh
```

---

## 📞 常见问题

**Q: 日志文件在哪里？**
A: `~/.agent-monster/data/logs/agentmonster_YYYYMMDD_HHMMSS.log`

**Q: 如何关闭日志文件写入？**
A: 目前无法关闭，但可以用 INFO 级别（默认）而不是 DEBUG

**Q: 日志是实时输出到终端吗？**
A: 是的，所有日志既写入文件也输出到 stderr

**Q: 我怎么知道流程卡住了？**
A: 如果 15 秒内没有新的日志，说明可能卡住了

---

## 📝 日志格式说明

```
[15:04:05.000] [INFO] Starting map generation
^             ^      ^
时间戳         级别    消息
```

- `[DEBUG]` - 详细调试信息
- `[INFO]` - 正常流程信息  
- `[WARN]` - 警告信息
- `[ERROR]` - 错误信息（❌）

特殊符号：
- 🌐 = API 请求
- 📨 = API 响应
- ❌ = 错误
- ✅ = 成功
- ⏳ = 等待中

