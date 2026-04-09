# Go CLI Map Navigation Feature - 地图行动功能指南

**版本**: 1.0  
**发布日期**: 2026-04-09  
**功能**: 在 Go CLI 中添加了地图导航功能

## 功能概述

在 Go CLI 中添加了全新的地图行动系统，允许玩家：

1. **通过 GitHub 链接访问用户地图** - 粘贴GitHub仓库链接直接进入用户的地图
2. **通过地图ID直接进入** - 输入地图ID快速进入指定地图
3. **在地图上自由行动** - 使用方向键或WASD在地图上移动
4. **自动地图切换** - 走到地图边缘时自动切换到相邻地图
5. **查看地图信息** - 显示地图元素、连接关系和玩家位置

## 如何使用

### 启动地图模式

1. 启动 Go CLI：
```bash
cd /root/pet/agent-monster/cli
./agent-monster
```

2. 登录后进入主菜单

3. 选择 **🗺️ 探索地图** (第5个菜单项)

### 输入地图信息

在地图输入模式中，你可以输入：

#### 方式1: GitHub 仓库链接

粘贴用户的 GitHub 仓库链接，系统将自动查找该用户的地图：

```
输入: https://github.com/tomcooler/agent-monster
或: https://github.com/chengjia2016/agent-monster
```

系统将：
- 提取用户名 (tomcooler 或 chengjia2016)
- 搜索该用户的地图
- 加载找到的第一个地图

#### 方式2: 地图ID

直接输入地图ID：

```
输入: 001
或: tom_001
或: 002
```

### 地图导航控制

一旦进入地图，使用以下控制：

| 按键 | 功能 |
|------|------|
| ⬆️ / W | 向北移动 |
| ⬇️ / S | 向南移动 |
| ⬅️ / A | 向西移动 |
| ➡️ / D | 向东移动 |
| M | 返回主菜单 |
| Ctrl+C | 退出游戏 |

### 地图显示说明

地图使用 ASCII 艺术表示：

```
图例:
  @ - 你的位置（玩家）
  P - 野生宝可梦
  F - 食物物品
  X - 障碍物
  . - 草地
  T - 森林
  ~ - 水体
  ^ - 山脉
```

示例地图显示：

```
┌──────────────────────┐
│.......T.....P.......│
│..@...T.T....F.......│
│.T.T.......X.........│
│....X...T.....T......│
│.P........P.........F│
└──────────────────────┘

地图大小: 20x20 | 宝可梦: 5 | 食物: 3 | 障碍: 2

连接的地图:
  ⬆️  北方: 101
  ➡️  东方: 002
```

## 高级功能

### 跨越地图边界

当玩家走到地图边缘时：

- **走向北边** → 自动加载北方的地图（地图ID相差100）
- **走向南边** → 自动加载南方的地图（地图ID相差100）
- **走向东边** → 自动加载东方的地图（地图ID相差1）
- **走向西边** → 自动加载西方的地图（地图ID相差1）

玩家会自动重新定位到新地图的相反边缘，实现无缝过渡。

### 地图连接规则

- **东西方向**: 相邻地图ID差1 (001 ↔ 002)
- **南北方向**: 相邻地图ID差100 (001 ↔ 101)

示例地图网络：

```
        [前情提要]
           ↓
    [201] ← [101] ← [001]
              ↓
            [102]
```

### 查看地图元素

在地图上行动时，你可以看到：

1. **野生宝可梦 (P)** - 可以尝试捕获的宝可梦
2. **食物物品 (F)** - 可以收集的食物资源
3. **障碍物 (X)** - 环境中的通行障碍

## API 端点整合

新功能使用以下 Judge Server API 端点：

### 获取地图
```
GET /api/maps/{map_id}
```

### 列出地图
```
GET /api/maps?page=1&limit=10
```

### 搜索地图
```
GET /api/maps/search?query={query}&page=1&limit=10
```

### 遍历地图
```
POST /api/maps/traverse
{
  "current_map_id": "001",
  "direction": "east"
}
```

## 示例场景

### 场景1: 访问好友的地图

```
1. 启动 CLI 并进入主菜单
2. 选择 "🗺️ 探索地图"
3. 输入朋友的 GitHub 链接: https://github.com/tomcooler/agent-monster
4. 系统加载 tomcooler 的地图
5. 使用 WASD 键在地图上探索
6. 走到东边界时自动进入 tom_002
```

### 场景2: 直接进入指定地图

```
1. 启动 CLI
2. 选择 "🗺️ 探索地图"  
3. 输入地图ID: 001
4. 进入地图 001，从中心位置开始
5. 向北移动进入地图 101
6. 继续探索其他连接的地图
```

## 技术实现

### 新增 API 数据模型

```go
// MapData represents a game map
type MapData struct {
    Version      string                 // 地图版本
    MapID        string                 // 地图唯一ID
    OwnerID      int                    // 所有者ID
    OwnerName    string                 // 所有者名字
    Width        int                    // 宽度
    Height       int                    // 高度
    Terrain      [][]int                // 地形数据
    Elements     []MapElement           // 地图元素
    Connections  MapConnections         // 相邻地图
    Statistics   MapStatistics          // 统计信息
}

// MapElement represents an element on map
type MapElement struct {
    ID   string                 // 元素ID
    Type string                 // 类型 (wild_pokemon, food, obstacle)
    X    int                    // X坐标
    Y    int                    // Y坐标
    Data map[string]interface{} // 额外数据
}

// MapConnections shows adjacent maps
type MapConnections struct {
    North *string // 北方地图ID
    South *string // 南方地图ID
    East  *string // 东方地图ID
    West  *string // 西方地图ID
}
```

### 新增 UI 屏幕

```go
const (
    MapScreen      // 地图显示屏幕
    MapInputScreen // 地图输入屏幕
)
```

### 新增应用状态

```go
type MapState struct {
    CurrentMap       *api.MapData // 当前地图
    PlayerX          int          // 玩家X坐标
    PlayerY          int          // 玩家Y坐标
    InputBuffer      string       // 用户输入缓冲
    TargetRepoURL    string       // GitHub链接
    SelectedMapIndex int          // 选择的地图索引
    AllMaps          []api.MapData // 搜索结果
}
```

## 故障排除

### 问题: 地图加载失败
**解决**: 确保 Judge Server 正在运行 (http://agentmonster.openx.pro:10000)

### 问题: GitHub 链接无效
**解决**: 确保使用正确的 GitHub URL 格式: `https://github.com/username/repo`

### 问题: 地图ID不存在
**解决**: 使用有效的地图ID，例如: 001, 002, 101, tom_001 等

### 问题: 移动无响应
**解决**: 确保当前在 MapScreen，使用 W/A/S/D 或方向键移动

## 文件修改清单

### 新增文件
- `cli/pkg/ui/map_screens.go` - 地图UI屏幕实现 (270+ 行)

### 修改文件
- `cli/pkg/api/models.go` - 添加地图数据模型
- `cli/pkg/api/client.go` - 添加地图API方法
- `cli/pkg/ui/app.go` - 添加MapScreen和MapInputScreen

### 变更摘要

| 文件 | 变更 | 行数 |
|------|------|------|
| models.go | 添加MapData等模型 | +45 |
| client.go | 添加5个地图API方法 | +95 |
| app.go | 添加MapScreen支持 | +15 |
| map_screens.go | 新地图UI系统 | +270 |
| **合计** | | **~425** |

## 测试方法

### 1. 构建CLI
```bash
cd /root/pet/agent-monster/cli
go build -o agent-monster ./cmd/main.go
```

### 2. 运行CLI
```bash
./agent-monster -server http://agentmonster.openx.pro:10000
```

### 3. 测试地图功能

**测试场景1: 通过地图ID进入**
- 输入: `001`
- 预期: 加载地图001，显示ASCII地图，玩家位置在中心

**测试场景2: 通过GitHub链接进入**
- 输入: `https://github.com/tomcooler/agent-monster`
- 预期: 搜索tom_开头的地图，加载第一个

**测试场景3: 地图导航**
- 按下 D 键移动东方
- 预期: 玩家位置向东移动

**测试场景4: 跨地图边界**
- 重复按 D 直到到达东边界
- 预期: 自动加载东方地图(001→002)，玩家在西边界

## 下一步改进

1. **增强地图互动**
   - 捕获野生宝可梦的集成
   - 收集食物物品
   - 克服障碍物

2. **多人功能**
   - 显示其他玩家位置
   - 实时地图更新
   - PvP遭遇战

3. **视觉改进**
   - 彩色地形显示
   - 平滑的地图过渡动画
   - 更详细的元素图标

4. **地图生成**
   - 在CLI中生成新地图
   - 自定义地图大小
   - 地图主题选择

## 许可证

Agent Monster CLI - Map Navigation Feature
© 2026 OpenCode Agent

---

**有问题?** 查看 CLI 目录下的 README.md 或 USAGE_GUIDE.md

