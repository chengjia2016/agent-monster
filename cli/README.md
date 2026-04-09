# Agent Monster CLI - 彩色TUI客户端

这是一个为Agent Monster怪兽对战游戏设计的高级终端用户界面(TUI)客户端。

## 功能特性

✨ **彩色界面**
- 使用Bubble Tea框架构建现代化TUI
- 支持256种颜色
- 动画菜单和平滑过渡

🎮 **完整功能**
- 🐾 **宠物管理** - 查看和管理你的宠物
- ⚔️ **战斗系统** - 发起PvP战斗，查看战斗记录
- 🏰 **防守基地** - 创建和管理你的防守基地
- 🌍 **精灵捕获** - 捕获野生精灵和训练宠物

⚡ **性能优化**
- 响应式设计
- 快速渲染
- 实时状态更新

## 快速开始

### 编译

```bash
cd cli
go mod tidy
go build -o agent-monster cmd/main.go
```

### 运行

```bash
# 连接到本地服务器（默认）
./agent-monster

# 指定自定义服务器地址
./agent-monster -server http://your-server:8080

# 启用调试模式
./agent-monster -debug
```

## 操作指南

### 键盘快捷键

| 快捷键 | 功能 |
|---------|------|
| `↑` / `K` | 上移菜单 |
| `↓` / `J` | 下移菜单 |
| `Enter` | 确认选择 |
| `H` / `Esc` | 返回上级菜单 |
| `Q` / `Ctrl+C` | 退出程序 |

### 主菜单

```
╔═════════════════════════════════════╗
║   Agent Monster - 怪兽对战系统   ║
╚═════════════════════════════════════╝

  ▶ 🐾 我的宠物
    ⚔️  发起战斗
    🏰 防守基地
    🌍 捕获精灵
    ❌ 退出游戏
```

### 宠物管理

- 列出所有宠物及其信息（等级、HP、属性）
- 查看详细属性
- 训练提升等级
- 释放宠物

### 战斗系统

- 选择对手进行战斗
- 查看战斗历史记录
- 查看战斗统计数据

### 防守基地

- 创建个人防守基地
- 查看基地卫士队伍
- 防守战斗历史
- 基地升级

### 精灵捕获

- 浏览可用野生精灵
- 查看精灵稀有度
- 捕获野生精灵
- 捕获历史记录

## 项目结构

```
cli/
├── cmd/
│   └── main.go              # 应用入口
├── pkg/
│   ├── api/
│   │   └── client.go        # HTTP客户端
│   ├── ui/
│   │   ├── app.go           # 主应用模型
│   │   ├── screens.go       # 屏幕渲染
│   │   └── styles.go        # 样式定义
│   └── model/
│       └── types.go         # 数据模型（待实现）
├── go.mod                   # 项目依赖
└── go.sum
```

## 依赖库

- **github.com/charmbracelet/bubbletea** - TUI框架
- **github.com/charmbracelet/lipgloss** - 样式和布局
- **github.com/charmbracelet/bubbles** - UI组件
- **github.com/fatih/color** - 颜色输出

## 配置

### 服务器配置

默认连接到 `http://localhost:8080`

```bash
./agent-monster -server http://your-judge-server:8080
```

### 环境变量

可以通过环境变量配置：

```bash
export AGENT_MONSTER_SERVER=http://your-server:8080
./agent-monster
```

## 开发指南

### 添加新屏幕

1. 在 `pkg/ui/app.go` 中的 `Screen` 枚举中添加新类型
2. 在 `screens.go` 中创建渲染函数
3. 在 `Update()` 中处理导航逻辑

### 自定义样式

编辑 `pkg/ui/styles.go` 中的样式定义：

```go
var StyleCustom = lipgloss.NewStyle().
    Foreground(ColorPrimary).
    Bold(true)
```

### 添加API调用

在 `pkg/api/client.go` 中添加新的API方法：

```go
func (c *Client) NewFeature() error {
    data, err := c.Request("GET", "/api/endpoint", nil)
    // 处理响应
    return err
}
```

## 故障排除

### 终端颜色不显示

- 确保你的终端支持256色
- 试试设置 `TERM=xterm-256color`

### 键盘输入不响应

- 确保在TTY环境中运行（不是在某些IDE中运行）
- 尝试禁用终端的输入法

### 连接服务器失败

- 检查服务器地址是否正确
- 确保judge-server正在运行
- 检查防火墙设置

## 性能优化

CLI客户端设计考虑了性能：

- ✅ 智能缓存减少API调用
- ✅ 异步更新防止UI阻塞
- ✅ 最小化重绘区域
- ✅ 内存高效的数据结构

## 未来计划

- [ ] 声音效果
- [ ] 宠物动画
- [ ] 战斗动画
- [ ] 保存游戏进度本地缓存
- [ ] 配置文件支持
- [ ] 主题定制

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
