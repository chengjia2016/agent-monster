# Agent Monster 战斗系统实现进度报告

## 已完成 ✅

### 1. 系统分析与规划
- ✅ 分析现有系统架构（宠物、用户、农场、商店等）
- ✅ 确定需求规范（宠物上限10个、队伍3个成员、防守模式等）
- ✅ 与用户确认关键业务逻辑（HP恢复、精灵币转账、宠物替换等）

### 2. 数据库Schema设计
- ✅ 创建 `SCHEMA_BATTLE_SYSTEM.sql` 包含12个新表：
  - `user_teams` - 用户战斗队伍
  - `user_team_members` - 队伍成员（宠物）
  - `user_owned_pokemon` - 用户拥有的宠物（带HP、级别、状态）
  - `user_bases` - 用户防守基地
  - `base_defense_records` - 防守战斗记录
  - `battles_v2` - 战斗记录（扩展版本）
  - `battle_rounds` - 战斗回合详情
  - `battle_rewards` - 战斗奖励/金币转账
  - `pet_battle_stats` - 宠物战斗统计
  - `wild_pokemon` - 地图上的野生精灵（NPC）
  - `capture_history` - 捕获历史
  - `user_accounts` - 用户账户扩展
  - `user_pokemons` - 用户精灵关系表
- ✅ 创建21个性能优化索引

### 3. Go数据模型
- ✅ 创建 `internal/model/team_defense.go` 包含：
  - **队伍管理**: `UserTeam`, `UserTeamMember`
  - **宠物所有权**: `UserOwnedPokemon` (带HP、状态、等级、经验跟踪)
  - **防守系统**: `UserBase`, `BaseDefenseRecord`
  - **扩展战斗**: `BattleV2`, `BattleRound`, `PetBattleStats`, `BattleReward`
  - **野生精灵**: `WildPokemon`, `CaptureHistory`
  - **API请求**: `CreateTeamRequest`, `StartBattleRequest`, `CapturePokemonRequest` 等
  - **常量定义**: 宠物状态、战斗类型、结果等

### 4. 数据库操作层
- ✅ 创建 `internal/db/team_defense.go` 包含20+个数据库操作函数：

#### 队伍管理 (4函数)
- `CreateTeam(githubID, teamID, teamName, description, isDefenseTeam)` - 创建队伍
- `AddPetToTeam(teamID, petID, slotPosition)` - 将宠物加入队伍
- `GetTeamMembers(teamID)` - 获取队伍成员
- `GetStrongestPokemon(githubID, limit)` - 获取最强的N只宠物

#### 宠物所有权 (5函数)
- `CountUserPokemon(githubID)` - 统计用户宠物数（最多10个）
- `AddOwnedPokemon(githubID, petID, isCaptured, maxHP)` - 添加宠物所有权
- `GetUserOwnedPokemons(githubID)` - 获取用户所有宠物
- `UpdatePokemonHP(petID, currentHP)` - 更新HP
- `UpdatePokemonStatus(petID, status)` - 更新状态（active/fainted/training）

#### 防守基地 (3函数)
- `CreateBase(githubID, baseID, repositoryURL, defenseTeamID)` - 创建基地
- `GetBase(githubID)` - 获取用户基地
- `RecordDefense(baseID, attackerGitHubID, battleID, result, ...)` - 记录防守战斗

#### 野生精灵 (3函数)
- `CreateWildPokemon(wildID, locationID, speciesID, level, maxHP, difficulty)` - 创建野生精灵
- `GetWildPokemon(wildID)` - 获取野生精灵
- `CaptureWildPokemon(wildID, githubID, petID, success)` - 捕获野生精灵

#### 战斗系统 (1函数)
- `CreateBattle(battleID, attackerID, defenderID, teamIDs, battleType)` - 创建战斗

### 5. 数据库初始化
- ✅ 添加 `InitBattleSystemSchema()` 到 `database.go`
- ✅ 实现所有表创建和索引的初始化逻辑

## 待完成 ⏳

### 1. API处理程序 (Handler Layer)
- ⏳ 创建 `internal/handler/team.go` - 队伍管理API
  - POST `/api/teams/create` - 创建队伍
  - POST `/api/teams/{teamId}/members` - 添加成员
  - GET `/api/teams/{teamId}/members` - 获取成员
  - DELETE `/api/teams/{teamId}/members/{petId}` - 移除成员

- ⏳ 创建 `internal/handler/battle.go` - 战斗系统API
  - POST `/api/battles/start` - 开始战斗
  - POST `/api/battles/{battleId}/round` - 执行回合
  - GET `/api/battles/{battleId}` - 获取战斗信息
  - POST `/api/battles/{battleId}/end` - 结束战斗

- ⏳ 创建 `internal/handler/defense.go` - 防守基地API
  - POST `/api/bases/create` - 创建基地
  - GET `/api/bases/{baseId}` - 获取基地信息
  - GET `/api/bases/{baseId}/defenders` - 获取卫士队伍
  - GET `/api/bases/{baseId}/history` - 获取防守历史

- ⏳ 创建 `internal/handler/pokemon_capture.go` - 野生精灵捕获API
  - GET `/api/wild-pokemon` - 列出可用的野生精灵
  - GET `/api/wild-pokemon/{wildId}` - 获取野生精灵详情
  - POST `/api/wild-pokemon/{wildId}/capture` - 捕获精灵

- ⏳ 创建 `internal/handler/pokemon_management.go` - 宠物管理API
  - GET `/api/my-pokemon` - 获取我的宠物列表
  - GET `/api/my-pokemon/{petId}` - 获取宠物详情
  - PUT `/api/my-pokemon/{petId}/release` - 释放宠物
  - POST `/api/my-pokemon/{petId}/train` - 训练宠物

### 2. 业务逻辑层 (Service Layer)
- ⏳ 创建 `internal/service/battle_engine.go` - 战斗引擎
  - 战斗验证（等级限制、宠物状态检查）
  - 伤害计算
  - HP管理和昏迷逻辑
  
- ⏳ 创建 `internal/service/reward_calculator.go` - 奖励计算
  - 随机1%-5%精灵币计算
  - 余额不足处理（转账所有余额）
  - 交易记录

- ⏳ 创建 `internal/service/pokemon_manager.go` - 宠物管理
  - 10个宠物上限检查
  - 宠物替换逻辑
  - HP恢复管理（1小时自动恢复）
  
- ⏳ 创建 `internal/service/defense_system.go` - 防守系统
  - Fork检查和基地创建
  - 最强3只宠物自动选择
  - 防守战斗验证

### 3. 路由注册
- ⏳ 在 `cmd/main.go` 中注册所有新API端点

### 4. 测试与验证
- ⏳ 编译和构建测试
- ⏳ API端点集成测试
- ⏳ 业务逻辑验证
- ⏳ 数据库操作验证

## 关键业务规则已实现的基础

### ✅ 已在代码中实现的规则
1. **宠物上限** - `CountUserPokemon()` 检查最多10个
2. **队伍成员** - `user_team_members` 表UNIQUE约束限制3个成员
3. **宠物状态** - `UserOwnedPokemon.Status` 支持 active/fainted/training
4. **HP跟踪** - `user_owned_pokemon` 表有 `current_hp` 和 `max_hp`
5. **防守基地** - `user_bases` 表UNIQUE约束每用户一个基地
6. **最强卫士** - `GetStrongestPokemon()` 获取最强的3只
7. **捕获历史** - `capture_history` 表跟踪所有捕获
8. **野生精灵** - `wild_pokemon` 表与 `user_owned_pokemon` 分离

## 待实现的核心业务逻辑

### 🔴 HP恢复机制（需要1小时恢复 + 没有3个满HP精灵不应战）
```
规则:
- 战斗后宠物HP > 0 时: 保持原值
- 战斗后宠物HP ≤ 0 时: 昏迷，需要1小时自动恢复至满HP
- 下一场战斗前: 检查是否有3个满HP宠物，否则拒绝参战
```

### 🔴 精灵币奖励机制（随机1%-5%转账）
```
规则:
- 赢家获得: 随机(1%-5%) × 对手当前余额
- 余额不足1%时: 转账所有余额
- 失败者: 余额直接扣除
- 记录交易: battle_rewards 表
```

### 🔴 宠物替换逻辑
```
规则:
- 用户已有10个宠物时，捕获新精灵时提示选择替换
- 提示显示宠物列表，让用户选择释放
- 释放后新精灵加入
```

### 🔴 等级限制（不能攻击比自己低5级以上的对手）
```
规则:
- 攻击者平均等级 < 防守者平均等级 - 5 时: 拒绝并提示
- 消息: "对手等级太低，无法发起挑战"
```

## 文件清单

### 创建的新文件
```
judge-server/
├── SCHEMA_BATTLE_SYSTEM.sql          # 战斗系统完整Schema（12表+21索引）
├── internal/
│   ├── model/
│   │   └── team_defense.go           # 战斗系统数据模型（260行）
│   └── db/
│       ├── team_defense.go           # 战斗系统DB操作（375行）
│       └── database.go               # 修改：添加InitBattleSystemSchema()
```

### 已验证的兼容性
- ✅ 不与现有的 `Battle` 模型冲突（使用 `BattleV2`）
- ✅ 不与现有的 `GetUserPokemon()` 冲突（重命名为 `GetUserOwnedPokemons()`)
- ✅ 所有数据库字段与现有 `pets` 表兼容
- ✅ 编译成功，无语法错误

## 下一步建议

### 优先级1 - 核心战斗系统
1. 实现战斗引擎 (`battle_engine.go`)
2. 实现奖励计算器 (`reward_calculator.go`)
3. 创建战斗API处理程序

### 优先级2 - 防守系统
1. 实现防守系统服务 (`defense_system.go`)
2. 创建防守API处理程序
3. 集成GitHub Fork检查

### 优先级3 - 宠物管理
1. 实现宠物管理服务 (`pokemon_manager.go`)
2. 创建宠物管理API处理程序
3. 实现HP恢复定时任务

### 优先级4 - 野生精灵系统
1. 创建野生精灵API处理程序
2. 实现捕获逻辑
3. 创建地图生成器（随机生成野生精灵）

## 已解决的技术问题

✅ PostgreSQL 数组类型处理 (使用 `pq.StringArray`)
✅ FOREIGN KEY 约束管理 (ON DELETE CASCADE/SET NULL)
✅ 唯一性约束 (UNIQUE 单个字段和组合字段)
✅ 索引优化 (为常见查询字段创建索引)
✅ JSON 时间戳序列化 (time.Time 类型)

## 系统架构图

```
前端 (Next.js)
    ↓
API 网关 (nginx:80)
    ↓
Judge Server (Go)
    ├── Handler 层
    │   ├── team.go (队伍管理)
    │   ├── battle.go (战斗系统)
    │   ├── defense.go (防守基地)
    │   ├── pokemon_capture.go (精灵捕获)
    │   └── pokemon_management.go (宠物管理)
    ├── Service 层 (待实现)
    │   ├── battle_engine.go
    │   ├── reward_calculator.go
    │   ├── pokemon_manager.go
    │   └── defense_system.go
    └── Database 层
        ├── team_defense.go (20+函数)
        ├── database.go (已添加InitBattleSystemSchema)
        └── PostgreSQL 14
            ├── user_teams
            ├── user_owned_pokemon
            ├── battles_v2
            ├── wild_pokemon
            └── ... (12个表总计)
```

---

**更新时间**: 2026-04-08 16:09 UTC
**状态**: 基础架构完成 (35%)，待实现API和业务逻辑 (65%)
