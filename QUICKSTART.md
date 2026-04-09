# Agent Monster CLI - 快速开始指南

## 🚀 启动应用

```bash
cd /root/pet/agent-monster/cli
./agent-monster
```

## ⌨️ 控制说明

### 登录屏幕
- **Enter** 或 **L** - 登录并进入主菜单

### 主菜单
- **⬆️ 上箭头** 或 **K** - 向上移动
- **⬇️ 下箭头** 或 **J** - 向下移动
- **Enter** 或 **L** - 选择菜单项
- **H** 或 **Esc** - 返回上一层
- **Q** 或 **Ctrl+C** - 退出应用

## 📋 菜单选项

### 1. 🐾 我的宠物
查看和管理你的宠物集合

### 2. ⚔️ 发起战斗
与其他玩家对战

### 3. 🏰 防守基地
设置防守策略

### 4. 🌍 捕获精灵
在野外捕获新的精灵

### 5. 💻 GitHub 集成
- 查看我的仓库
- 查看 Issues
- 查看 Pull Requests

### 6. 👤 个人资料
查看你的个人信息和游戏统计

### 7. ❌ 退出游戏
关闭应用

## 🎮 游戏流程

```
启动
  ↓
登录 GitHub (按 Enter)
  ↓
选择菜单选项
  ↓
浏览功能
  ↓
按 H 返回菜单
  ↓
按 Q 退出
```

## 🔧 故障排除

### 问题: "GitHub token 获取失败"
**解决方案:**
```bash
gh auth login
gh auth status
```

### 问题: "CLI 无法启动"
**解决方案:**
```bash
# 重建二进制文件
cd /root/pet/agent-monster/cli
go build -o agent-monster ./cmd/main.go

# 然后运行
./agent-monster
```

### 问题: "屏幕显示乱码"
**解决方案:**
- 确保终端支持 UTF-8
- 使用更新的终端软件（如 iTerm2, Windows Terminal）
- 设置环境变量: `export LANG=en_US.UTF-8`

## 📊 系统要求

- Go 1.21+
- GitHub CLI 2.0+
- 支持 UTF-8 的终端
- 网络连接

## 📁 文件位置

- **可执行文件**: `/root/pet/agent-monster/cli/agent-monster`
- **用户数据**: `~/.agent-monster/data/`
- **配置文件**: `~/.agent-monster/`

## ✨ 功能特点

✅ GitHub 集成  
✅ 12 个交互式屏幕  
✅ 彩色 Pokemon 精灵  
✅ 用户资料管理  
✅ 对战系统  
✅ 精灵捕获  
✅ 键盘快捷键  
✅ 实时加载状态  

## 🎯 下一步

1. 运行应用并登录
2. 浏览所有菜单选项
3. 查看你的 GitHub 仓库集成
4. 探索个人资料功能
5. 准备参加对战！

## 📞 获取帮助

- **bug 报告**: 检查终端输出的错误信息
- **功能请求**: 查看应用内的消息
- **使用建议**: 参考本指南

---

**祝你游戏愉快！** 🎮✨

希望你喜欢 Agent Monster CLI！
