# Agent Monster Map System

这是Agent Monster游戏的地图系统。每个玩家都可以生成自己的地图，并与其他玩家的地图连接形成一个无限的游戏世界。

## 目录结构

```
maps/
├── README.md              # 本文件
├── generator.go           # Map生成器程序
├── 001.json              # 地图数据文件 (例如)
├── 002.json
├── 003.json
└── ...
```

## Map JSON 格式

每个地图由一个JSON文件表示，包含以下内容：

### 基本信息
- `version`: 地图版本 (当前 1.0)
- `map_id`: 地图ID (如 "001", "002" 等)
- `owner_id`: 地图创建者的GitHub用户ID
- `owner_username`: 地图创建者的用户名
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 地图数据
- `width`: 地图宽度 (格子数)
- `height`: 地图高度 (格子数)
- `terrain`: 二维地形数组
  - 0 = 草地 (70%)
  - 1 = 森林 (15%)
  - 2 = 水域 (10%)
  - 3 = 山地 (5%)

### 元素
`elements` 是地图上的所有元素列表，包括：

1. **野生精灵** (`wild_pokemon`)
   - `pokemon_id`: 精灵编号
   - `pokemon_name`: 精灵名字
   - `level`: 等级
   - `rarity`: 稀有度 (common/uncommon/rare)

2. **食物** (`food`)
   - `food_type`: 食物类型
   - `food_name`: 食物名字
   - `quantity`: 数量
   - `restores_hp`: 回复血量

3. **障碍物** (`obstacle`)
   - `obstacle_type`: 障碍物类型
   - `obstacle_name`: 障碍物名字
   - `passable`: 是否可通过

### 连接
`connections` 定义了与相邻地图的连接：
- `north`: 北边相邻的地图ID
- `south`: 南边相邻的地图ID
- `east`: 东边相邻的地图ID
- `west`: 西边相邻的地图ID

### 统计
`statistics` 包含地图的统计信息：
- `total_wild_pokemon`: 野生精灵总数
- `total_food`: 食物总数
- `total_obstacles`: 障碍物总数
- `visited_count`: 访问次数
- `last_visited`: 最后访问时间

## 使用Generator

### 前置要求
- Go 1.16 或更高版本

### 生成新地图

```bash
cd maps
go run generator.go generate -id 005 -owner player_name
```

**选项：**
- `-id <map_id>`: 地图ID (必需)
- `-owner <username>`: 所有者用户名 (必需)
- `-owner-id <id>`: 所有者GitHub ID (默认: 1)
- `-width <w>`: 地图宽度 (默认: 20)
- `-height <h>`: 地图高度 (默认: 20)

### 查看所有地图

```bash
go run generator.go list
```

输出示例：
```
Available Maps:
==============
Map 001 (Owner: admin, Size: 20x20, Elements: 10)
Map 002 (Owner: player1, Size: 20x20, Elements: 12)
Map 003 (Owner: player2, Size: 20x20, Elements: 12)
```

### 可视化地图

```bash
go run generator.go visualize -id 001
```

输出示例：
```
=== Map 001 ===
Owner: admin | Size: 20x20
Elements: 10 (Wild Pokemon: 5, Food: 3, Obstacles: 2)

Terrain Map (0=草, 1=森, 2=水, 3=山):
00001110000001100000
00100121000110110000
01100121010010000000
01000020000000000100
00000020000000010010
...

Connections:
  North: <nil>
  South: <nil>
  East: 003
  West: 001
```

### 更新地图连接

当添加新地图时，自动检测相邻地图的连接：

```bash
go run generator.go update-connections
```

## Map ID 命名规则

为了实现自动连接，Map ID 采用特殊的编号规则：

- **相邻规则**:
  - 北/南相邻: ID相差100 (如 001 和 101)
  - 东/西相邻: ID相差1 (如 001 和 002)

- **网格示例**:
  ```
         101  102  103
         |    |    |
    001--002--003--004
         |    |    |
         201  202  203
  ```

- **ID命名约定**:
  - 001-099: 第1行 (北)
  - 101-199: 第2行
  - 201-299: 第3行
  - ...

## Judge Server API 端点

### 获取地图列表

```bash
GET /api/maps
GET /api/maps?owner_id=12345
```

响应:
```json
{
  "success": true,
  "count": 5,
  "data": [...]
}
```

### 获取特定地图

```bash
GET /api/maps/{map_id}
```

### 获取地图元素

```bash
GET /api/maps/{map_id}/elements
GET /api/maps/{map_id}/elements?type=wild_pokemon
GET /api/maps/{map_id}/elements?type=food
```

### 获取地图连接

```bash
GET /api/maps/{map_id}/connections
```

### 穿过边界进入相邻地图

```bash
POST /api/maps/traverse

Request:
{
  "current_map_id": "001",
  "direction": "east"  // north, south, east, west
}

Response:
{
  "success": true,
  "current": "001",
  "next": "002",
  "data": { ... next map data ... }
}
```

### 搜索地图

```bash
GET /api/maps/search?q=player_name
GET /api/maps/search?owner_id=12345
```

### 生成新地图 (待实现)

```bash
POST /api/maps/generate

Request:
{
  "owner_id": 12345,
  "owner_name": "player_name",
  "map_id": "005",
  "width": 20,
  "height": 20
}
```

## Map 系统架构

### 文件流程

```
Generator Program (generator.go)
        ↓
   Generate Map Data
        ↓
   Save to JSON File
        ↓
   Judge Server loads
        ↓
   API provides to CLI
        ↓
   Player explores
```

### 连接系统流程

```
Player at Map 001
    ↓
Moves East/West/North/South
    ↓
Check connections.json
    ↓
Connected Map ID found?
    ↓
POST /api/maps/traverse
    ↓
Load adjacent map
    ↓
Display in CLI
```

## 示例场景

### 场景1: 玩家生成自己的地图

```bash
# 玩家 alice 生成地图 101
go run generator.go generate -id 101 -owner alice -owner-id 99999 -width 30 -height 30

# 自动检测到相邻的地图 001 (来自admin)
# 更新连接信息
go run generator.go update-connections
```

### 场景2: 玩家在地图间探索

```bash
# CLI显示地图 101 的North连接指向地图 001
# 玩家向北走，通过API调用:

curl -X POST http://localhost:10000/api/maps/traverse \
  -H "Content-Type: application/json" \
  -d '{"current_map_id":"101","direction":"north"}'

# 返回地图 001 的数据
# 玩家现在在 admin 的地图中探索
```

### 场景3: 在地图上捕捉精灵

```bash
# 玩家在地图 001 上
# 获取所有野生精灵
GET /api/maps/001/elements?type=wild_pokemon

# 看到有5个野生精灵
# 与服务器进行捕捉交互
POST /api/wild-pokemon/capture
```

## 扩展功能 (未来计划)

- [ ] 动态生成地图 (通过Web界面)
- [ ] 地图编辑器 (自定义地图元素)
- [ ] 地图主题系统 (不同的主题风格)
- [ ] 多人地图 (玩家可在同一地图上互动)
- [ ] 地图排行榜 (最受欢迎的地图)
- [ ] 地图导出/导入
- [ ] 地图分享功能
- [ ] 天气系统 (影响精灵出现)
- [ ] 时间系统 (白天/夜间)
- [ ] 地图事件系统 (随机事件)

## 性能优化建议

1. **地图缓存**: 在内存中缓存常访问的地图
2. **分页**: 列出地图时使用分页
3. **地图压缩**: 压缩terrain数组数据
4. **异步加载**: 预加载相邻地图

## 故障排除

### 问题1: "map not found"
- 检查地图ID是否正确
- 检查maps目录中是否存在对应的JSON文件

### 问题2: 连接为空
- 运行 `update-connections` 更新连接
- 检查ID命名规则是否正确

### 问题3: 生成的地图太小/太大
- 使用 `-width` 和 `-height` 参数调整
- 默认大小为 20x20

## 技术规格

- **格式**: JSON
- **编码**: UTF-8
- **地图尺寸**: 最小10x10, 最大100x100
- **最大元素数**: 1000个
- **版本**: 1.0 (可向前兼容)

## 贡献

欢迎贡献改进！请确保：
- 遵守现有的JSON格式
- 更新此README
- 添加适当的测试

## 许可证

MIT License
