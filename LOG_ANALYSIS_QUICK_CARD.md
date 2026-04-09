# 📊 Log Analysis Quick Card

## 快速命令

### 基础分析
```bash
# 分析最新日志
./analyze_logs.sh analyze

# 分析特定日志
./analyze_logs.sh analyze agentmonster_20260409_181338.log

# 健康检查（评分）
./analyze_logs.sh health

# 快速统计
./analyze_logs.sh stats

# 列出所有日志
./analyze_logs.sh list

# 查看最新日志
./view_logs.sh
```

### 过滤日志
```bash
./analyze_logs.sh filter ERROR     # 只显示错误
./analyze_logs.sh filter WARN      # 只显示警告
./analyze_logs.sh filter API       # 只显示 API 调用
./analyze_logs.sh filter DEBUG     # 只显示调试信息
./analyze_logs.sh filter INFO      # 只显示信息
./analyze_logs.sh filter "custom"  # 自定义搜索
```

## 日志位置
```
~/.agent-monster/data/logs/
```

## 日志格式
```
[HH:MM:SS.mmm] [LEVEL] message
例如：
[15:04:05.123] [INFO] 🌐 API Request: POST /api/users
[15:04:05.145] [ERROR] ❌ API Error at /api/map: timeout
```

## 健康评分标准

| 评分 | 状态 | 符号 | 解释 |
|------|------|------|------|
| 100 | 完美 | 🟢✅ | 无任何问题 |
| 80-99 | 良好 | 🟢✅ | 轻微问题（可忽略） |
| 50-79 | 一般 | 🟡⚠️ | 存在问题，需要关注 |
| <50 | 差 | 🔴❌ | 严重问题，需修复 |

## 常见问题诊断

### 程序卡住
```bash
# 1. 查看最后的日志
tail -20 ~/.agent-monster/data/logs/agentmonster_*.log

# 2. 查看错误
./analyze_logs.sh filter ERROR

# 3. 查看 API 错误
grep "API Error" ~/.agent-monster/data/logs/agentmonster_*.log
```

### API 失败
```bash
# 查看统计
./analyze_logs.sh stats

# 查看 API 错误详情
grep "API Error" ~/.agent-monster/data/logs/agentmonster_*.log

# 查看响应代码
grep "API Response" ~/.agent-monster/data/logs/agentmonster_*.log
```

### 性能问题
```bash
# 查看所有警告
./analyze_logs.sh filter WARN

# 查看内存相关日志
grep -i memory ~/.agent-monster/data/logs/agentmonster_*.log
```

## 常用 grep 命令

```bash
LOG_FILE=~/.agent-monster/data/logs/agentmonster_*.log

# 查看所有错误
grep "\[ERROR\]" $LOG_FILE

# 查看特定操作
grep "map\|pokemon\|battle" $LOG_FILE

# 统计各日志级别
echo "INFO: $(grep -c '\[INFO\]' $LOG_FILE)"
echo "ERROR: $(grep -c '\[ERROR\]' $LOG_FILE)"
echo "WARN: $(grep -c '\[WARN\]' $LOG_FILE)"

# 查看时间范围内的日志
grep "15:0[0-5]:" $LOG_FILE

# 按严重级别排序
(grep ERROR; grep WARN; grep INFO) < $LOG_FILE | sort
```

## 日志级别说明

| 级别 | 用途 | 何时查看 |
|------|------|---------|
| INFO | 正常操作记录 | 理解程序流程 |
| DEBUG | 调试详情 | 启用 `--debug` 模式 |
| WARN | 可能的问题 | 性能或行为异常 |
| ERROR | 失败操作 | 快速定位故障 |

## 日志分析工作流

```
1. 运行 CLI
   ↓
2. ./analyze_logs.sh health
   ↓
3. 检查评分
   ├─ 100: 完成✅
   ├─ 80+: 轻微问题，可忽略
   └─ <80: 需要深入调查
   ↓
4. ./analyze_logs.sh analyze
   ↓
5. 查看错误、警告、API 统计
   ↓
6. ./analyze_logs.sh filter ERROR
   ↓
7. 针对具体错误进行修复
```

## 实时监控

```bash
# 实时查看日志
tail -f ~/.agent-monster/data/logs/agentmonster_*.log

# 实时查看错误
tail -f ~/.agent-monster/data/logs/agentmonster_*.log | grep ERROR

# 追踪特定操作
tail -f ~/.agent-monster/data/logs/agentmonster_*.log | grep "API\|map\|pokemon"
```

## 日志管理

```bash
# 查看日志大小
du -sh ~/.agent-monster/data/logs/

# 清理 7 天前的日志
find ~/.agent-monster/data/logs -name "*.log" -mtime +7 -delete

# 只保留最近 10 个日志
ls -t ~/.agent-monster/data/logs/*.log | tail -n +11 | xargs rm

# 压缩旧日志
gzip ~/.agent-monster/data/logs/agentmonster_202604*.log
```

## 导出分析报告

```bash
# 生成纯文本报告
./analyze_logs.sh analyze > report.txt

# 生成健康报告
./analyze_logs.sh health > health.txt

# 导出错误列表
./analyze_logs.sh filter ERROR > errors.txt

# 创建完整的诊断包
{
  echo "=== HEALTH CHECK ===" && ./analyze_logs.sh health
  echo "" && echo "=== ANALYSIS ===" && ./analyze_logs.sh analyze
  echo "" && echo "=== ERRORS ===" && ./analyze_logs.sh filter ERROR
} > diagnostic_report.txt
```

## 调试技巧

### 启用 DEBUG 模式
```bash
./cli/agentmonster --debug
```

日志内容会更详细，包括：
- 所有 API 请求/响应
- 详细的调试消息
- 变量值
- 函数调用堆栈

### 使用脚本自动诊断
```bash
#!/bin/bash
LOG=$(ls -t ~/.agent-monster/data/logs/*.log | head -1)
echo "📋 Log: $(basename $LOG)"
echo ""
./analyze_logs.sh health "$LOG"
echo ""
echo "Top errors:"
./analyze_logs.sh filter ERROR "$LOG" | head -3
```

### 比较多个会话
```bash
echo "Session 1:"
./analyze_logs.sh stats session1.log | grep "ERROR\|Total"

echo ""
echo "Session 2:"
./analyze_logs.sh stats session2.log | grep "ERROR\|Total"
```

## 性能优化建议

基于日志分析的优化方向：

1. **减少 API 调用** - 查看是否有重复请求
2. **优化响应时间** - 查看 API 错误和重试
3. **降低内存使用** - 查看警告中的内存相关信息
4. **改进错误处理** - 分析错误模式，添加重试机制

## 文档参考

- **完整指南** - 查看 `LOG_ANALYSIS_GUIDE.md`
- **实现细节** - 查看 `LOG_ANALYSIS_IMPLEMENTATION.md`
- **系统总结** - 查看 `LOGGING_SUMMARY.md`
- **测试指南** - 查看 `TESTING_GUIDE.md`

## 常见错误及解决方案

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| TTY error | 非交互式环境 | 使用 `ssh -t` 或本地运行 |
| No log files | CLI 未运行 | 先运行 `./cli/agentmonster` |
| Permission denied | 无执行权限 | `chmod +x analyze_logs.sh` |
| API errors | 网络/服务问题 | 检查连接，查看错误详情 |

---

**快速帮助：** `./analyze_logs.sh help`
