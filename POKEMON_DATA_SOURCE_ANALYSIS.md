# Pokemon 数据来源分析报告

**日期:** 2026-04-08  
**用户:** chengjia2016  

---

## 🔍 发现

### 当前显示的宠物数据来自: **模拟数据 ⚠️**

你在 CLI 中看到的宠物数据 (`皮卡丘`, `妙蛙种子`, `小火龙`) **不是** 来自 judge-server，而是来自应用内的**模拟数据**。

---

## 📊 数据流向分析

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLI 应用启动流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 用户登录 GitHub                                             │
│     └─> 保存用户资料到 ~/.agent-monster/data/chengjia2016.json │
│                                                                 │
│  2. 进入"我的宠物"菜单                                           │
│     └─> 调用 GetPokemon() API                                   │
│         └─> 查询 http://127.0.0.1:10000/api/pokemon/           │
│             └─> HTTP 400 (缺少 pet_id 参数)                     │
│                                                                 │
│  3. API 调用失败                                                │
│     └─> 返回 nil 或 empty list                                 │
│         └─> CLI 显示**模拟数据**作为备选方案                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔴 Judge-server API 现状

### 可用端点

| 端点 | 状态 | 参数 | 返回值 |
|------|------|------|--------|
| `/api/pokemon/` | HTTP 400 | 需要 `pet_id` | 错误信息 |
| `/api/pokemon/?pet_id=1` | HTTP 200 | `pet_id` | `{"data": null}` |
| `/api/battles/` | HTTP 400 | 需要 `battle_id` | 错误信息 |
| `/api/wild-pokemon/` | HTTP 404 | - | 404 Not Found |

### 问题分析

1. **`/api/pokemon/` 端点**
   - 需要 `pet_id` 参数才能查询
   - 但 CLI 调用时没有传递此参数
   - 导致 HTTP 400 错误

2. **数据库中没有初始化的宠物**
   - 查询 `pet_id=1` 返回 `null`
   - 说明 judge-server 中没有宠物数据

3. **缺少用户级别的宠物列表 API**
   - 没有 `/api/pokemon/user/<user_id>/` 这样的端点
   - 只能按单个 `pet_id` 查询

---

## 💾 本地用户数据

**文件:** `~/.agent-monster/data/chengjia2016.json`

```json
{
  "github_login": "chengjia2016",
  "github_id": 0,
  "email": "",
  "balance": 1000.0,
  "level": 1,
  "experience": 0,
  "pokemons": [],        // 空列表！
  "teams": [],           // 空列表
  "created_at": "2026-04-08T...",
  "updated_at": "2026-04-08T..."
}
```

**分析:**
- ✅ 用户资料已创建
- ❌ 本地没有存储任何宠物
- ❌ 本地没有捕获任何宠物

---

## 🎯 当前代码的数据流

### RenderPokemonList() 的流程

```go
// 文件: pkg/ui/screens.go:13-83

func (a *App) RenderPokemonList() string {
    // 第1步: 尝试从 judge-server 获取宠物
    pokemons, err := a.Client.GetPokemon()
    
    if err != nil || len(pokemons) == 0 {
        // 第2步: 如果失败，使用模拟数据
        mockPokemons := []map[string]interface{}{
            {"name": "皮卡丘", "level": 25, ...},
            {"name": "妙蛙种子", "level": 20, ...},
            {"name": "小火龙", "level": 18, ...},
        }
        // 显示模拟数据
        return renderMockList(mockPokemons)
    }
    
    // 第3步: 如果成功，显示真实数据
    return renderRealList(pokemons)
}
```

---

## 📝 GetPokemon() 的实现

**文件:** `pkg/api/client.go`

```go
func (c *Client) GetPokemon() ([]Pokemon, error) {
    // 调用端点: /api/pokemon
    data, err := c.Request("GET", "/api/pokemon", nil)
    if err != nil {
        return nil, err
    }
    
    // 解析响应
    var response map[string]interface{}
    json.Unmarshal(data, &response)
    
    var pokemons []Pokemon
    if dataRaw, ok := response["data"]; ok {
        jsonData, _ := json.Marshal(dataRaw)
        json.Unmarshal(jsonData, &pokemons)
    }
    
    return pokemons, nil
}
```

**问题:**
- 调用 `/api/pokemon` 没有参数
- Judge-server 期望 `pet_id` 参数
- 导致返回错误

---

## 🔧 可能的解决方案

### 方案 1: 修改 CLI 以使用本地用户资料

**优点:**
- 不依赖 judge-server
- 离线可用
- 更快

**实现:**
```go
func (a *App) RenderPokemonList() string {
    // 直接从本地用户资料读取
    if a.UserProfile != nil && len(a.UserProfile.Pokemons) > 0 {
        return renderLocalPokemons(a.UserProfile.Pokemons)
    }
    
    // 没有本地数据，显示提示
    return "你还没有任何宠物。在'捕获精灵'菜单中捕获你的第一只宠物！"
}
```

### 方案 2: 实现完整的 judge-server 集成

**优点:**
- 使用服务器数据
- 支持多设备同步
- 支持在线对战

**需要:**
1. Judge-server 提供用户级别的宠物列表 API
2. CLI 需要发送用户认证信息
3. 实现宠物创建/初始化逻辑

### 方案 3: 混合方案

**建议使用:**
- 本地存储用户拥有的宠物列表
- 定期与 judge-server 同步
- 离线可用，在线时同步

---

## 📋 建议的改进步骤

### 立即可做 (v1.1)
1. ✅ 显示本地用户资料中的宠物
2. ✅ 当本地没有宠物时，显示友好提示
3. ✅ 添加"捕获宠物"功能，在本地创建宠物

### 中期改进 (v2.0)
1. 与 judge-server 创建宠物同步
2. 实现用户级别的宠物列表 API
3. 添加宠物持久化到 judge-server

### 长期规划 (v3.0)
1. 完整的云同步系统
2. 多设备支持
3. 在线对战数据管理

---

## 📊 数据来源总结表

| 数据类型 | 当前来源 | 建议来源 | 状态 |
|---------|---------|---------|------|
| 用户资料 | GitHub + 本地 | 本地/服务器 | ✅ 实现 |
| 宠物列表 | 模拟数据 | 本地/服务器 | ⚠️ 待改进 |
| 战斗记录 | 模拟数据 | 服务器 | ❌ 未实现 |
| 防守基地 | 模拟数据 | 服务器 | ❌ 未实现 |
| 野生宠物 | 模拟数据 | 服务器 | ❌ 未实现 |

---

## 🎯 结论

**现状:**
- ✅ GitHub 认证: 正常
- ✅ 本地用户资料: 已创建
- ⚠️ Judge-server 连接: 已连接，但数据缺失
- ❌ 宠物数据: 目前使用模拟数据

**下一步:**
需要决定是：
1. 完全依赖本地用户资料存储
2. 完全依赖 judge-server 存储
3. 使用混合方案（推荐）

---

**建议:** 建议先实现本地宠物捕获功能，然后逐步添加服务器同步功能。

