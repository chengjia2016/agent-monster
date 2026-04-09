# CLI 从 Judge-Server 读取数据集成方案

**目标:** 将 Agent Monster CLI 改造为完全从 judge-server 读取数据，CLI 只作为展示层

**现状分析:**
- ✅ Judge-server 已有用户管理 API
- ✅ Judge-server 已有宠物管理接口定义
- ✅ Judge-server 已有库存、物品、战斗 API
- ❌ CLI 目前使用模拟数据和本地用户资料
- ❌ CLI GetPokemon() 没有正确调用 API

---

## 📋 改造清单

### 第1步: 修复 CLI API 客户端

**文件:** `cli/pkg/api/client.go`

需要改造的方法:

```go
// 当前问题: 不传递任何参数，导致 judge-server 返回 HTTP 400
func (c *Client) GetPokemon() ([]Pokemon, error) {
    data, err := c.Request("GET", "/api/pokemon", nil)  // ❌ 缺少 github_id 参数
}

// 改造为:
func (c *Client) GetUserPokemons(githubID int) ([]Pokemon, error) {
    // 需要传递 github_id 参数到 judge-server
    path := fmt.Sprintf("/api/user/pokemons/get?github_id=%d", githubID)
    data, err := c.Request("GET", path, nil)  // ✅ 传递正确的参数
}
```

### 第2步: 扩展 Judge-server 用户管理 API

**Judge-server 现有 API:**
- ✅ `GET /api/users/{github_id}` - 获取用户账户
- ✅ `POST /api/users/create` - 创建用户
- ✅ `GET /api/user/balance/get?github_id=X` - 获取用户余额
- ✅ `GET /api/user/pokemons/get?github_id=X` - 获取用户宠物列表
- ✅ `GET /api/user/inventory/get?github_id=X` - 获取用户物品

**需要添加的 API:**
- `GET /api/user/wild-pokemon` - 获取野生宠物列表
- `POST /api/user/pokemons/add` - 捕获宠物
- `POST /api/user/pokemons/release` - 释放宠物
- `POST /api/battles/start` - 开始战斗
- `GET /api/battles/list` - 获取战斗历表
- `GET /api/user/defense/base` - 获取防守基地信息

### 第3步: 修改 CLI 屏幕渲染逻辑

**文件:** `cli/pkg/ui/screens.go`

#### RenderPokemonList 改造

```go
// 当前: 尝试从 API 获取，失败则显示模拟数据
func (a *App) RenderPokemonList() string {
    pokemons, err := a.Client.GetPokemon()
    if err != nil {
        // 显示模拟数据
        return mockList
    }
    return realList
}

// 改造为: 必须从 server 读取，否则显示错误或空列表
func (a *App) RenderPokemonList() string {
    if a.CurrentUser == nil {
        return "❌ 未登录"
    }
    
    // 使用 GitHub ID 获取宠物
    pokemons, err := a.Client.GetUserPokemons(a.CurrentUser.GitHubID)
    if err != nil {
        return fmt.Sprintf("❌ 获取宠物失败: %v", err)
    }
    
    if len(pokemons) == 0 {
        return "📭 你还没有任何宠物\n\n提示: 在'捕获精灵'菜单中捕获你的第一只宠物！"
    }
    
    return renderPokemonList(pokemons)
}
```

#### RenderWildPokemonScreen 改造

```go
// 改造为: 从 judge-server 获取野生宠物
func (a *App) RenderWildPokemonScreen() string {
    if a.CurrentUser == nil {
        return "❌ 未登录"
    }
    
    // 从 server 获取野生宠物列表
    wildPokemons, err := a.Client.GetWildPokemons()
    if err != nil {
        return fmt.Sprintf("❌ 获取野生精灵失败: %v", err)
    }
    
    return renderWildPokemonList(wildPokemons)
}
```

### 第4步: 统一用户认证

**文件:** `cli/pkg/ui/app.go`

改造登录流程:

```go
// LoginScreen 处理逻辑
case LoginScreen:
    // 1. 从 GitHub 获取用户信息
    githubUser, err := a.GitHub.GetCurrentUser()
    if err != nil {
        a.Error = "GitHub 认证失败"
        return a, nil
    }
    
    // 2. 创建/获取 judge-server 中的用户账户
    serverUser, err := a.Client.CreateOrGetUserAccount(&CreateUserRequest{
        GithubID:    githubUser.ID,  // 需要添加
        GithubLogin: githubUser.Login,
        Email:       githubUser.Email,
        AvatarURL:   githubUser.AvatarURL,
    })
    if err != nil {
        a.Error = fmt.Sprintf("服务器认证失败: %v", err)
        return a, nil
    }
    
    // 3. 保存到应用
    a.CurrentUser = serverUser
    a.CurrentScreen = MainMenuScreen
```

### 第5步: 所有操作通过 Server

**需要改造的操作:**

#### 宠物相关
- ✅ 显示我的宠物 → `GET /api/user/pokemons/get`
- ❌ 捕获宠物 → `POST /api/user/pokemons/add` (需实现)
- ❌ 释放宠物 → `DELETE /api/user/pokemons/{pet_id}` (需实现)
- ❌ 查看宠物详情 → `GET /api/user/pokemons/{pet_id}`

#### 战斗相关
- ❌ 发起战斗 → `POST /api/battles/start` (需实现)
- ❌ 查看战斗记录 → `GET /api/battles/list` (需实现)
- ❌ 获取战斗统计 → `GET /api/battles/stats` (需实现)

#### 防守相关
- ❌ 查看防守基地 → `GET /api/user/defense/base` (需实现)
- ❌ 更新防守队伍 → `PUT /api/user/defense/team` (需实现)

#### 物品相关
- ✅ 获取物品列表 → `GET /api/user/inventory/get`
- ❌ 使用物品 → `POST /api/user/inventory/use` (需实现)

---

## 🔧 实现顺序 (优先级)

### Phase 1 (立即) - 核心数据流
1. ✅ 修复 CLI 宠物 API 调用
2. ✅ 正确传递 github_id 参数
3. ✅ 移除硬编码模拟数据
4. ✅ 测试宠物列表读取

### Phase 2 (短期) - 用户管理集成
1. 改造登录流程集成 judge-server
2. 创建用户账户在 server
3. 缓存 github_id 在 CLI
4. 同步本地和 server 用户数据

### Phase 3 (中期) - 功能操作
1. 实现捕获宠物 API
2. 实现释放宠物 API
3. 实现宠物详情 API
4. 实现宠物升级、训练等

### Phase 4 (长期) - 高级功能
1. 完整的战斗系统
2. 防守基地管理
3. 经济系统集成
4. 物品系统集成

---

## 📝 API 端点映射表

| CLI 功能 | 现有 API | 状态 | 优先级 |
|---------|---------|------|--------|
| 我的宠物列表 | GET /api/user/pokemons/get | ✅ | P1 |
| 野生宠物列表 | GET /api/wild-pokemon/ | ❌ | P1 |
| 宠物详情 | GET /api/user/pokemons/{id} | ⚠️ | P2 |
| 捕获宠物 | POST /api/user/pokemons/add | ❌ | P2 |
| 用户信息 | GET /api/users/{id} | ✅ | P1 |
| 用户余额 | GET /api/user/balance/get | ✅ | P2 |
| 用户物品 | GET /api/user/inventory/get | ✅ | P2 |
| 发起战斗 | POST /api/battles/start | ❌ | P3 |
| 战斗记录 | GET /api/battles/list | ❌ | P3 |
| 防守基地 | GET /api/user/defense/base | ❌ | P3 |

---

## 💻 代码改造示例

### 示例1: 修改 API 客户端

**文件:** `cli/pkg/api/client.go`

```go
// 添加新方法
func (c *Client) GetUserPokemons(githubID int) ([]Pokemon, error) {
    path := fmt.Sprintf("/api/user/pokemons/get?github_id=%d", githubID)
    data, err := c.Request("GET", path, nil)
    if err != nil {
        return nil, err
    }
    
    var response map[string]interface{}
    json.Unmarshal(data, &response)
    
    var pokemons []Pokemon
    if dataRaw, ok := response["data"]; ok {
        jsonData, _ := json.Marshal(dataRaw)
        json.Unmarshal(jsonData, &pokemons)
    }
    
    return pokemons, nil
}

func (c *Client) GetWildPokemons() ([]WildPokemon, error) {
    data, err := c.Request("GET", "/api/wild-pokemon/", nil)
    if err != nil {
        return nil, err
    }
    
    var response map[string]interface{}
    json.Unmarshal(data, &response)
    
    var pokemons []WildPokemon
    if dataRaw, ok := response["data"]; ok {
        jsonData, _ := json.Marshal(dataRaw)
        json.Unmarshal(jsonData, &pokemons)
    }
    
    return pokemons, nil
}

func (c *Client) CaptureWildPokemon(githubID int, wildPokemonID int) (bool, error) {
    req := map[string]interface{}{
        "github_id": githubID,
        "wild_pokemon_id": wildPokemonID,
    }
    
    reqData, _ := json.Marshal(req)
    data, err := c.Request("POST", "/api/user/pokemons/add", reqData)
    if err != nil {
        return false, err
    }
    
    var response map[string]interface{}
    json.Unmarshal(data, &response)
    
    success, _ := response["success"].(bool)
    return success, nil
}
```

### 示例2: 修改屏幕渲染

**文件:** `cli/pkg/ui/screens.go`

```go
func (a *App) RenderPokemonList() string {
    title := StyleTitle.Render("🐾 我的宠物列表")
    
    // 确保已登录
    if a.CurrentUser == nil {
        return title + "\n\n❌ 请先登录"
    }
    
    // 从 server 获取宠物
    pokemons, err := a.Client.GetUserPokemons(a.CurrentUser.GitHubID)
    if err != nil {
        return title + fmt.Sprintf("\n\n❌ 获取宠物失败: %v", err)
    }
    
    // 显示列表或空提示
    if len(pokemons) == 0 {
        return title + "\n\n📭 你还没有任何宠物\n\n提示: 在'捕获精灵'菜单中捕获你的第一只宠物！"
    }
    
    var items strings.Builder
    for i, p := range pokemons {
        var line string
        if i == a.SelectedIndex {
            line = StyleMenuItemSelected.Render(fmt.Sprintf(
                "  %-15s Lv.%-3d HP: %2d/%2d [%s]",
                p.Name,
                p.Level,
                p.CurrentHP,
                p.MaxHP,
                p.Type,
            ))
        } else {
            line = StyleMenuItem.Render(fmt.Sprintf(
                "  %-15s Lv.%-3d HP: %2d/%2d [%s]",
                p.Name,
                p.Level,
                p.CurrentHP,
                p.MaxHP,
                p.Type,
            ))
        }
        items.WriteString(line + "\n")
    }
    
    controls := StyleDim.Render("⬆️ ⬇️  选择  Enter 查看详情  H 返回")
    return title + "\n\n" + items.String() + "\n" + controls
}
```

---

## 🚀 实现步骤

### Step 1: 准备工作 (1 小时)
```bash
# 1. 确认 judge-server 运行中
curl http://127.0.0.1:10000/health

# 2. 测试现有 API
curl -X POST http://127.0.0.1:10000/api/users/create \
  -H "Content-Type: application/json" \
  -d '{
    "github_id": 24448747,
    "github_login": "chengjia2016",
    "email": "test@example.com",
    "avatar_url": "https://...",
    "balance": 1000
  }'

# 3. 测试 GetUserPokemons (需要先创建用户)
curl "http://127.0.0.1:10000/api/user/pokemons/get?github_id=24448747"
```

### Step 2: 修改 CLI API 客户端 (2 小时)
- [ ] 添加 `GetUserPokemons(githubID)`
- [ ] 添加 `GetWildPokemons()`
- [ ] 添加 `CaptureWildPokemon()`
- [ ] 添加 `CreateOrGetUserAccount()`
- [ ] 添加错误处理和日志

### Step 3: 修改屏幕渲染 (2 小时)
- [ ] 更新 LoginScreen 处理
- [ ] 更新 RenderPokemonList
- [ ] 更新 RenderWildPokemonScreen
- [ ] 添加加载状态显示
- [ ] 添加错误提示

### Step 4: 测试和调试 (2 小时)
- [ ] 编译新版本
- [ ] 测试登录流程
- [ ] 测试宠物列表显示
- [ ] 测试野生宠物列表
- [ ] 测试捕获流程

---

## ⚠️ 注意事项

1. **认证方式**: 
   - 当前 CLI 通过 GitHub CLI 认证
   - 需要获取 GitHub ID 传递给 judge-server
   - 可能需要修改 GitHub 客户端添加 ID 字段

2. **错误处理**:
   - judge-server 离线时的处理
   - API 返回错误的处理
   - 网络超时的处理

3. **缓存策略**:
   - 是否缓存宠物列表?
   - 缓存过期时间?
   - 如何处理并发更新?

4. **性能考虑**:
   - 列表分页处理
   - 减少 API 调用次数
   - 异步加载数据

---

## 📊 预期改造影响

| 文件 | 行数变化 | 类型 | 难度 |
|------|--------|------|------|
| `pkg/api/client.go` | +50 | 修改 | 低 |
| `pkg/ui/screens.go` | +100 | 修改 | 中 |
| `pkg/ui/app.go` | +30 | 修改 | 中 |
| `pkg/github/client.go` | +5 | 修改 | 低 |

---

**总体工作量:** 约 8-10 小时开发 + 2-3 小时测试

