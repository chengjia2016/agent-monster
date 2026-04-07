# Judge Server 用户管理系统部署指南

## 架构概述

```
┌─────────────────────────────────────────────────────────────┐
│              MCP Server (Python)                            │
│  提供命令行接口，使用 Judge Server API 管理用户数据        │
├─────────────────────────────────────────────────────────────┤
│              HTTP API 层                                     │
│  judge_server_client.py - Python HTTP 客户端                │
│  mcp_judge_server_commands.py - MCP 命令集                 │
├─────────────────────────────────────────────────────────────┤
│              Judge Server (Go)                              │
│  REST API + 数据库操作层 + 业务逻辑                        │
│  • 用户账户管理                                             │
│  • Pokemon 集合管理                                         │
│  • 物品库存管理                                             │
│  • 交易记录                                                 │
├─────────────────────────────────────────────────────────────┤
│              PostgreSQL Database                            │
│  user_accounts, user_pokemons, user_inventory,             │
│  account_transactions 表                                   │
└─────────────────────────────────────────────────────────────┘
```

## 部署步骤

### Step 1: 在 Judge Server 中添加用户表

在 judge-server 的 PostgreSQL 数据库中执行：

```sql
-- 文件: judge-server/SCHEMA_USERS.sql
-- 执行此文件创建所有用户相关表
```

或通过 Go 代码自动创建（推荐）：
- `database.UpdateSchema()` 在 main.go 中自动执行
- 所有表会在 Judge Server 启动时自动创建

### Step 2: 编译并运行 Judge Server

```bash
cd judge-server
go build -o judge-server ./cmd/main.go
./judge-server
```

Judge Server 将在 `http://0.0.0.0:10000` 启动，并自动：
1. 创建所有用户管理表
2. 注册 10+ 个新的用户 API 端点

### Step 3: 验证 Judge Server 运行

```bash
# 检查健康状态
curl http://localhost:10000/health

# 应返回
# {"status":"healthy","version":"1.0.0","timestamp":"..."}
```

### Step 4: 使用 MCP Server 的新命令

```bash
# 检查Judge Server连接
python3 -c "from mcp_judge_server_commands import cmd_judge_server_status; print(cmd_judge_server_status())"

# 获取用户账户信息
python3 -c "from mcp_judge_server_commands import cmd_account_info; print(cmd_account_info('username'))"

# 增加用户余额
python3 -c "from mcp_judge_server_commands import cmd_add_balance; print(cmd_add_balance('username', 100, 'reward'))"
```

## API 端点列表

### 用户账户 API

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | /api/users/create | 创建用户账户 |
| GET | /api/users/{github_id} | 获取用户信息 |
| GET | /api/user/balance/get | 获取用户余额 |
| POST | /api/user/balance/update | 更新用户余额 |

### Pokemon API

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | /api/user/pokemons/get | 获取用户的 Pokemon 列表 |
| POST | /api/user/pokemons/add | 添加 Pokemon 到收藏 |

### 物品API

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | /api/user/inventory/get | 获取用户的物品列表 |
| POST | /api/user/inventory/add | 添加物品到背包 |

### 交易API

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | /api/user/transactions/get | 获取用户交易历史 |

## 数据迁移（可选）

如果之前有本地用户数据，可以迁移到 Judge Server：

```bash
# 创建用户账户（一次性）
python3 -c "
from judge_server_client import get_judge_server_client
from user_manager import UserManager

client = get_judge_server_client()
um = UserManager()

for user in um.list_users():
    account = um.get_account(user.user_id)
    client.create_user_account(
        github_id=user.github_id,
        github_login=user.github_login,
        email=user.email,
        avatar_url=user.avatar_url,
        balance=account.balance if account else 0
    )
    print(f'✓ Migrated user: {user.github_login}')
"
```

## 测试验证

### 1. 连接测试

```bash
python3 << 'EOF'
from judge_server_client import get_judge_server_client

client = get_judge_server_client()
if client.health_check():
    print("✓ Judge Server 连接正常")
else:
    print("✗ Judge Server 连接失败")
EOF
```

### 2. 用户管理测试

```bash
python3 << 'EOF'
from judge_server_client import get_judge_server_client

client = get_judge_server_client()

# 创建测试用户
success = client.create_user_account(
    github_id=999999,
    github_login="test_user",
    email="test@example.com"
)
print(f"创建用户: {'✓' if success else '✗'}")

# 获取用户
account = client.get_user_account(999999)
print(f"获取用户: {'✓' if account else '✗'}")

# 更新余额
success = client.update_user_balance(999999, 100, "初始余额")
print(f"更新余额: {'✓' if success else '✗'}")

# 获取余额
balance = client.get_user_balance(999999)
print(f"获取余额: {balance}")
EOF
```

### 3. Pokemon 管理测试

```bash
python3 << 'EOF'
from judge_server_client import get_judge_server_client

client = get_judge_server_client()

# 添加 Pokemon
success = client.add_user_pokemon(999999, "poke_1", "Pikachu", level=5, species="Electric")
print(f"添加 Pokemon: {'✓' if success else '✗'}")

# 获取 Pokemon 列表
pokemons = client.get_user_pokemons(999999)
print(f"获取 Pokemon: {len(pokemons)} 个")
for pokemon in pokemons:
    print(f"  - {pokemon['pet_name']} Lv.{pokemon['level']}")
EOF
```

### 4. 物品管理测试

```bash
python3 << 'EOF'
from judge_server_client import get_judge_server_client

client = get_judge_server_client()

# 添加物品
success = client.add_user_item(999999, "ball_1", "Poke Ball", quantity=10)
print(f"添加物品: {'✓' if success else '✗'}")

# 获取物品列表
items = client.get_user_inventory(999999)
print(f"获取物品: {len(items)} 种")
for item in items:
    print(f"  - {item['item_name']} × {item['quantity']}")
EOF
```

## MCP 命令使用

### 获取账户信息

```bash
# 在 MCP 中注册命令
# /judge-account <username>
```

### 增加余额

```bash
# /judge-balance-add <username> <amount> [reason]
```

### 管理 Pokemon

```bash
# /judge-pokemons-list <username>
# /judge-pokemon-add <username> <pet_id> <pet_name> [level] [species]
```

### 管理物品

```bash
# /judge-inventory-list <username>
# /judge-item-add <username> <item_id> <item_name> [quantity]
```

## 故障排查

### Judge Server 无法连接

**症状**: `Failed to connect to Judge Server`

**解决方案**:
1. 检查 Judge Server 是否运行: `curl http://localhost:10000/health`
2. 检查防火墙: `sudo ufw allow 10000`
3. 检查端口: `netstat -tlnp | grep 10000`

### 数据库连接错误

**症状**: `Failed to connect to database`

**解决方案**:
1. 检查 PostgreSQL 运行状态: `sudo systemctl status postgresql`
2. 检查数据库配置: `.config/config.yaml`
3. 检查凭证: 用户名、密码、数据库名

### API 返回 404

**症状**: `Endpoint not found`

**解决方案**:
1. 检查 Judge Server 是否已更新到最新版本
2. 确保运行了 `database.UpdateSchema()` 初始化用户表
3. 重启 Judge Server

## 性能优化

### 数据库索引

已自动创建以下索引：
- `idx_user_accounts_github_id` - 用户账户查询
- `idx_user_pokemons_github_id` - Pokemon 查询
- `idx_user_inventory_github_id` - 物品查询
- `idx_account_transactions_github_id` - 交易查询

### 连接池

Judge Server 使用 PostgreSQL 连接池，确保性能：
- 最大连接数: 100
- 空闲超时: 5 分钟
- 准备语句缓存: 启用

## 安全考虑

### 认证

当前实现使用 GitHub ID 作为用户标识符。生产环境应添加：
- API 密钥认证
- OAuth2 集成
- JWT 令牌

### 授权

确保只有用户本人能访问自己的数据：
```go
if githubID != requestGithubID {
    return unauthorized_error
}
```

### 数据加密

建议对敏感字段加密：
- email (已存储纯文本)
- balance 日志(财务数据)

## 监控和日志

### Judge Server 日志

```bash
# 查看日志
tail -f judge-server.log

# 启用调试模式
DEBUG=true ./judge-server
```

### 数据库查询

```sql
-- 查看用户总数
SELECT COUNT(*) FROM user_accounts;

-- 查看总余额
SELECT SUM(balance) FROM user_accounts;

-- 查看最近交易
SELECT * FROM account_transactions ORDER BY created_at DESC LIMIT 10;
```

## 后续计划

### Phase 2: MCP Server 集成
- [ ] 在 mcp_server.py 中集成这些新命令
- [ ] 替换本地余额管理为 Judge Server
- [ ] 添加缓存层以减少 API 调用

### Phase 3: 前端集成
- [ ] Web 仪表板显示用户余额
- [ ] Pokemon 查看器
- [ ] 交易历史查看

### Phase 4: 高级功能
- [ ] 用户间转账
- [ ] Pokemon 交易市场
- [ ] 排行榜与成就
- [ ] 活动和奖励系统

## 文件清单

| 文件 | 用途 |
|------|------|
| judge_server_client.py | Python HTTP 客户端 |
| mcp_judge_server_commands.py | MCP 命令实现 |
| judge-server/internal/model/user.go | Go 数据模型 |
| judge-server/internal/db/users.go | Go 数据库层 |
| judge-server/internal/handler/users.go | Go API 处理器 |
| judge-server/SCHEMA_USERS.sql | SQL Schema |

## 支持

如有问题，请检查：
1. Judge Server 日志输出
2. PostgreSQL 连接
3. Python 依赖 (requests 库)
4. 网络连接

