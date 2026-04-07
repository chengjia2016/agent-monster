# Judge Server - 快速参考指南

## 🚀 立即开始

### 服务状态
```bash
systemctl status judge-server
```

### 快速测试
```bash
# 健康检查
curl http://agentmonster.openx.pro:10000/health

# 创建新用户
curl -X POST http://agentmonster.openx.pro:10000/api/users/create \
  -H "Content-Type: application/json" \
  -d '{
    "github_id": 12345,
    "github_login": "myuser",
    "email": "user@example.com",
    "balance": 1000
  }'

# 获取用户信息
curl http://agentmonster.openx.pro:10000/api/users/12345

# 获取用户余额
curl http://agentmonster.openx.pro:10000/api/user/balance/get?github_id=12345

# 更新余额
curl -X POST http://agentmonster.openx.pro:10000/api/user/balance/update \
  -H "Content-Type: application/json" \
  -d '{
    "github_id": 12345,
    "amount": 500,
    "description": "Bonus"
  }'

# 添加Pokemon
curl -X POST http://agentmonster.openx.pro:10000/api/user/pokemons/add \
  -H "Content-Type: application/json" \
  -d '{
    "github_id": 12345,
    "pet_id": "pet_001",
    "pet_name": "Pikachu",
    "level": 10,
    "species": "Electric"
  }'

# 获取Pokemon列表
curl http://agentmonster.openx.pro:10000/api/user/pokemons/get?github_id=12345

# 添加物品
curl -X POST http://agentmonster.openx.pro:10000/api/user/inventory/add \
  -H "Content-Type: application/json" \
  -d '{
    "github_id": 12345,
    "item_id": "item_001",
    "item_name": "Pokeball",
    "quantity": 50
  }'

# 获取库存
curl http://agentmonster.openx.pro:10000/api/user/inventory/get?github_id=12345

# 获取交易历史
curl http://agentmonster.openx.pro:10000/api/user/transactions/get?github_id=12345
```

## 📊 测试用例 (现有数据)

### 已注册用户
| GitHub ID | Username | Balance | Pokemon | Items |
|-----------|----------|---------|---------|-------|
| 101 | alice | 1500 | Pikachu, Charizard | Pokeball, Potion |
| 102 | bob | 500 | Blastoise | Great Ball |
| 103 | charlie | 2000 | Venusaur | Ultra Ball |

### 快速测试已存在的用户
```bash
# 查询alice
curl http://agentmonster.openx.pro:10000/api/users/101

# 获取alice的Pokemon
curl http://agentmonster.openx.pro:10000/api/user/pokemons/get?github_id=101

# 获取alice的库存
curl http://agentmonster.openx.pro:10000/api/user/inventory/get?github_id=101
```

## 🔧 系统命令

```bash
# 重启服务
sudo systemctl restart judge-server

# 查看实时日志
sudo journalctl -u judge-server -f

# 查看最后100行日志
sudo journalctl -u judge-server -n 100

# 清空数据库
PGPASSWORD=xiaodudu psql -h localhost -U postgres -d agent_monster << SQL
TRUNCATE TABLE account_transactions CASCADE;
TRUNCATE TABLE user_inventory CASCADE;
TRUNCATE TABLE user_pokemons CASCADE;
TRUNCATE TABLE user_accounts CASCADE;
SQL
```

## 📁 重要文件

```
/root/pet/agent-monster-pet/judge-server/
├── judge-server                           # 可执行文件
├── .config/config.yaml                    # 配置文件
├── build.sh                               # 编译脚本
├── internal/
│   ├── handler/users.go                   # API处理函数
│   ├── db/users.go                        # 数据库操作
│   └── model/user.go                      # 数据模型
└── SCHEMA_USERS.sql                       # 数据库schema
```

## 📍 重要信息

- **访问地址**: http://agentmonster.openx.pro:10000
- **服务运行用户**: root
- **工作目录**: /root/pet/agent-monster-pet/judge-server/
- **配置路径**: /root/pet/agent-monster-pet/judge-server/.config/config.yaml
- **数据库**: PostgreSQL (host: localhost, user: postgres, dbname: agent_monster)

## ✅ 验证清单

在使用前检查以下项目：

- [ ] Judge Server 服务运行正常: `systemctl status judge-server`
- [ ] Health 端点响应: `curl http://127.0.0.1:10000/health`
- [ ] 数据库连接: `PGPASSWORD=xiaodudu psql -h localhost -U postgres -d agent_monster -c "SELECT 1"`
- [ ] 外部访问: `curl http://agentmonster.openx.pro:10000/health`

## 🆘 故障排查

### 服务无响应
```bash
# 检查进程
ps aux | grep judge-server

# 重启服务
sudo systemctl restart judge-server

# 查看日志
sudo journalctl -u judge-server -n 50
```

### 数据库连接错误
```bash
# 验证 PostgreSQL 运行
sudo systemctl status postgresql

# 测试连接
PGPASSWORD=xiaodudu psql -h localhost -U postgres -d agent_monster -c "SELECT 1"
```

### API 返回错误
```bash
# 启用详细日志
sudo journalctl -u judge-server -f

# 测试单个端点
curl -v http://127.0.0.1:10000/api/users/101
```

## 📚 相关文档

- `DEPLOYMENT_COMPLETE.md` - 部署完成总结
- `JUDGE_SERVER_STATUS.md` - 详细的API文档
- `TEST_REPORT_JUDGE_SERVER.md` - 完整的测试报告

---

**保持更新**: 有问题请查看完整文档或检查日志文件
