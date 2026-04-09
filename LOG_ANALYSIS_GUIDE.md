# 📊 Log Analysis Guide

## 概述

Agent Monster CLI 的日志系统提供了全面的分析工具，帮助快速诊断问题、理解程序流程、优化性能。

## 快速开始

### 查看最新日志

```bash
./view_logs.sh
```

### 分析日志

```bash
# 分析最新日志
./analyze_logs.sh analyze

# 分析特定日志文件
./analyze_logs.sh analyze agentmonster_20260409_150405.log

# 查看健康状态
./analyze_logs.sh health

# 查看统计信息
./analyze_logs.sh stats

# 列出所有日志
./analyze_logs.sh list

# 过滤特定类型的日志
./analyze_logs.sh filter ERROR   # 只显示错误
./analyze_logs.sh filter WARN    # 只显示警告
./analyze_logs.sh filter API     # 只显示 API 调用
```

## 日志位置

所有日志文件存储在：
```
~/.agent-monster/data/logs/
```

命名格式：
```
agentmonster_YYYYMMDD_HHMMSS.log
```

例如：
```
agentmonster_20260409_150405.log
```

## 日志级别说明

| 级别 | 符号 | 描述 | 用途 |
|------|------|------|------|
| DEBUG | 🔍 | 调试信息 | 深入诊断，仅在 `--debug` 模式启用 |
| INFO | ℹ️ | 信息消息 | 记录正常操作流程 |
| WARN | ⚠️ | 警告消息 | 记录可能的问题 |
| ERROR | ❌ | 错误消息 | 记录失败的操作 |

## 日志格式

每条日志包含以下信息：

```
[HH:MM:SS.mmm] [LEVEL] message
```

例如：
```
[15:04:05.123] [INFO] 🌐 API Request: POST /api/users
[15:04:05.145] [INFO] 📨 API Response: Status 200
[15:04:05.146] [DEBUG]   Response: {user_id: 123}
[15:04:06.501] [ERROR] ❌ API Error at /api/map: connection timeout
```

## 分析工具详解

### 1. analyze 命令

输出详细的分析报告，包括：
- 总行数和时间戳
- 各日志级别的统计
- API 调用统计
- 错误摘要
- 警告摘要
- API 请求详情

**示例输出：**

```
═══════════════════════════════════════════════════════════
📊 Log Analysis Summary
═══════════════════════════════════════════════════════════

📈 Statistics:
  Total Lines:        1247
  Start Time:         Session Started

📋 Log Levels:
  INFO:               523
  DEBUG:              412
  WARN:               8
  ERROR:              2 ❌

🌐 API Statistics:
  Total API Calls:    45
  API Errors:         1 ❌
  Success Rate:       97%

❌ Errors (2):
  [Line 456] ❌ API Error at /api/map: timeout
  [Line 789] ❌ Connection refused

⚠️  Warnings (8):
  [Line 234] Retry attempt 1
  [Line 567] High memory usage: 512MB
```

### 2. health 命令

生成健康检查报告，评估会话质量：

**健康评分标准：**
- 100: 完美 ✅
- 80-99: 轻微问题
- 50-79: 多个问题 ⚠️
- <50: 严重问题 ❌

**计分规则：**
- 每个错误：-5 分
- 每个 API 错误：-10 分
- 每个警告：-2 分
- API 成功率低于 80%：-20 分

**示例输出：**

```
═══════════════════════════════════════════════════════════
🏥 Session Health Check
═══════════════════════════════════════════════════════════

🟢 [█████████░] Health Score: 95/100

✅ Session completed with minor issues

🔍 Issues Found:
  • 1 warning
```

### 3. filter 命令

按类型过滤日志内容：

```bash
./analyze_logs.sh filter ERROR    # 错误
./analyze_logs.sh filter WARN     # 警告
./analyze_logs.sh filter API      # API 调用
./analyze_logs.sh filter DEBUG    # 调试信息
./analyze_logs.sh filter INFO     # 信息
./analyze_logs.sh filter "custom" # 自定义匹配
```

## 常见问题诊断

### 问题：程序卡住

**诊断步骤：**

1. 分析日志
   ```bash
   ./analyze_logs.sh analyze
   ```

2. 查看最后的日志条目
   ```bash
   tail -20 ~/.agent-monster/data/logs/agentmonster_*.log
   ```

3. 查看 API 错误
   ```bash
   grep "API Error\|❌" ~/.agent-monster/data/logs/agentmonster_*.log
   ```

4. 启用 DEBUG 模式重新运行
   ```bash
   ./cli/agentmonster --debug
   ```

### 问题：API 调用失败

**诊断步骤：**

1. 检查 API 统计
   ```bash
   ./analyze_logs.sh stats
   ```

2. 查看 API 错误详情
   ```bash
   grep "API Error" ~/.agent-monster/data/logs/agentmonster_*.log
   ```

3. 查看 API 响应
   ```bash
   grep "API Response" ~/.agent-monster/data/logs/agentmonster_*.log
   ```

### 问题：高内存使用

**诊断步骤：**

1. 查看所有警告
   ```bash
   ./analyze_logs.sh filter WARN
   ```

2. 查看内存相关的日志
   ```bash
   grep -i "memory\|memory\|heap" ~/.agent-monster/data/logs/agentmonster_*.log
   ```

## 日志分析示例

### 示例 1：完美会话

```
健康评分：100/100 ✅
- 没有错误
- 没有警告
- 所有 API 调用成功
```

**诊断结论：** 程序运行正常

### 示例 2：轻微问题

```
健康评分：85/100
- 1 个警告（可忽略）
- 1 个 API 重试（最终成功）
```

**诊断结论：** 程序基本正常，可能存在网络波动

### 示例 3：严重问题

```
健康评分：35/100
- 5 个错误
- 3 个 API 错误
- API 成功率：60%
```

**诊断结论：** 存在重大问题，需要深入调查

## 高级用法

### 1. 实时监控日志

```bash
# 实时查看最新日志
tail -f ~/.agent-monster/data/logs/agentmonster_*.log

# 实时查看错误
tail -f ~/.agent-monster/data/logs/agentmonster_*.log | grep ERROR

# 追踪特定的操作
tail -f ~/.agent-monster/data/logs/agentmonster_*.log | grep "API\|map\|pokemon"
```

### 2. 导出和分享日志

```bash
# 复制最新日志
cp ~/.agent-monster/data/logs/agentmonster_*.log ./latest_log.txt

# 创建日志摘要
./analyze_logs.sh stats > log_summary.txt

# 创建错误报告
grep ERROR ~/.agent-monster/data/logs/agentmonster_*.log > error_report.txt
```

### 3. 比较多个会话

```bash
# 查看所有日志列表
./analyze_logs.sh list

# 分别分析两个日志
./analyze_logs.sh analyze session1.log
./analyze_logs.sh analyze session2.log

# 比较统计数据
echo "Session 1:" && grep "Total Lines\|ERROR" ~/.agent-monster/data/logs/session1.log
echo "Session 2:" && grep "Total Lines\|ERROR" ~/.agent-monster/data/logs/session2.log
```

### 4. 自动化诊断脚本

创建 `diagnose.sh` 脚本进行自动诊断：

```bash
#!/bin/bash

LOG_FILE=$(ls -t ~/.agent-monster/data/logs/*.log | head -1)

echo "📊 Auto-Diagnosis Report"
echo "════════════════════════"
echo ""

echo "1. Health Check:"
bash ./analyze_logs.sh health "$LOG_FILE" | tail -10
echo ""

echo "2. Recent Errors:"
grep ERROR "$LOG_FILE" | tail -3
echo ""

echo "3. API Status:"
echo "  API Calls: $(grep -c 'API Request' "$LOG_FILE")"
echo "  API Errors: $(grep -c 'API Error' "$LOG_FILE")"
```

## 常用 grep 命令

```bash
# 查看所有错误
grep "\[ERROR\]" ~/.agent-monster/data/logs/agentmonster_*.log

# 查看特定 API 调用
grep "POST /api/map" ~/.agent-monster/data/logs/agentmonster_*.log

# 查看响应时间（如果日志中包含）
grep "Response time" ~/.agent-monster/data/logs/agentmonster_*.log

# 按时间范围查找
grep "15:0[0-5]:" ~/.agent-monster/data/logs/agentmonster_*.log

# 查看特定用户的操作
grep "user_123\|github_user" ~/.agent-monster/data/logs/agentmonster_*.log

# 统计每种日志级别的出现次数
echo "INFO: $(grep -c '\[INFO\]' ~/.agent-monster/data/logs/agentmonster_*.log)"
echo "ERROR: $(grep -c '\[ERROR\]' ~/.agent-monster/data/logs/agentmonster_*.log)"
echo "WARN: $(grep -c '\[WARN\]' ~/.agent-monster/data/logs/agentmonster_*.log)"
```

## 性能优化建议

基于日志分析，改进程序性能的建议：

1. **减少 API 调用**
   - 检查是否有重复的 API 请求
   - 实现本地缓存

2. **优化 API 响应时间**
   - 检查慢查询（API 响应时间 > 1s）
   - 优化数据库查询

3. **减少内存使用**
   - 查看是否有内存泄漏警告
   - 优化数据结构

4. **改进错误处理**
   - 分析常见错误模式
   - 添加重试机制

## 日志系统配置

### 启用 DEBUG 模式

```bash
./cli/agentmonster --debug
```

DEBUG 模式会记录：
- 所有 API 请求和响应
- 函数调用堆栈
- 详细的变量值
- 性能指标

### 更改日志目录

默认日志目录为 `~/.agent-monster/data/logs/`，可以通过环境变量修改：

```bash
export AGENTMONSTER_LOG_DIR="/custom/log/path"
./cli/agentmonster
```

## 日志文件管理

### 清理旧日志

```bash
# 删除 7 天前的日志
find ~/.agent-monster/data/logs -name "*.log" -mtime +7 -delete

# 只保留最近 10 个日志
ls -t ~/.agent-monster/data/logs/*.log | tail -n +11 | xargs rm
```

### 压缩日志

```bash
# 将旧日志压缩为 gzip 格式
gzip ~/.agent-monster/data/logs/agentmonster_202604*.log
```

## 故障排除

### 日志文件为空

**原因：** 程序可能在初始化日志前崩溃

**解决方案：**
1. 检查日志目录权限
   ```bash
   ls -la ~/.agent-monster/data/logs/
   ```
2. 检查磁盘空间
   ```bash
   df -h
   ```
3. 启用 DEBUG 模式查看详细信息
   ```bash
   ./cli/agentmonster --debug 2>&1 | tee debug.log
   ```

### 找不到日志文件

**原因：** CLI 可能还没有运行过

**解决方案：**
```bash
# 首先运行 CLI
./cli/agentmonster

# 然后查看日志
./view_logs.sh
```

### 日志分析命令不可用

**原因：** 脚本没有执行权限

**解决方案：**
```bash
chmod +x ./analyze_logs.sh
chmod +x ./view_logs.sh
```

## 总结

日志分析工具提供了三个关键功能：

1. **`analyze`** - 深入了解程序执行流程
2. **`health`** - 快速评估会话质量
3. **`filter`** - 快速定位特定类型的问题

通过这些工具，可以：
- 快速诊断问题
- 理解程序流程
- 优化性能
- 改进用户体验

更多问题？查看 `TESTING_GUIDE.md` 和 `LOGGING_SUMMARY.md`
