# 商店购买系统 - 裁判服务器集成修复

## 问题总结

用户提出疑问：**购买交易是否通过裁判服务器而不是本地操作？**

### 发现的问题

1. **原始代码没有调用裁判服务器**
   - `economy_manager.purchase_item()` 只进行本地账户修改
   - MCP 服务器的 `cmd_shop_buy()` 直接使用本地 EconomyManager
   - 菜单系统的购买逻辑也是本地处理

2. **裁判服务器存在但未被利用**
   - 裁判服务器是 Go 语言编写的独立服务
   - 已实现 `/api/shop/buy` 端点用于处理购买交易
   - 其他系统（如食物、战斗）已集成裁判服务器验证

## 实施的修复

### 1. MCP 服务器层 (mcp_server.py)

**修改前**：本地处理，无服务器调用

```python
# 旧逻辑：直接修改本地账户
success = economy_manager.purchase_item(user.user_id, item.name, total_cost, item_id)
```

**修改后**：通过裁判服务器处理

```python
# 新逻辑：调用裁判服务器
purchase_request = {
    "player_id": user.user_id,
    "item_id": item_id,
    "quantity": quantity,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
}

judge_result = call_judge_server("/api/shop/buy", purchase_request)

if judge_result.get("success", False):
    remaining_balance = judge_result.get("remaining_coins", 0)
    return f"✅ Purchase Successful (via Judge Server)!"
```

### 2. 菜单系统层 (menu_system.py)

**修改**：集成裁判服务器 API 调用

```python
# 添加了：
JUDGE_SERVER = "http://agentmonster.openx.pro:10000"

def call_judge_server(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """调用裁判服务器 API"""
    # 向 /api/shop/buy 发送 POST 请求
    # 返回服务器的处理结果

# 更新购买逻辑：
judge_result = call_judge_server("/api/shop/buy", purchase_request)
if judge_result.get("success", False):
    # 处理成功响应
```

## 架构变化

### 原始架构
```
User → Menu/MCP → EconomyManager (local) → JSON File
                   ↓
            Account modification
```

### 新架构
```
User → Menu/MCP → Judge Server → PostgreSQL (remote/centralized)
                   ↓
            API validation & processing
                   ↓
            Server response with new balance
```

## 裁判服务器 API 文档

### POST /api/shop/buy

**请求**：
```json
{
  "player_id": "user_id",
  "item_id": "pokeball",
  "quantity": 1,
  "timestamp": "2026-04-08T15:20:00Z"
}
```

**响应（成功）**：
```json
{
  "success": true,
  "item_name": "Poké Ball",
  "quantity": 1,
  "unit_price": 10.0,
  "total_price": 10.0,
  "remaining_coins": 87.0
}
```

**响应（失败）**：
```json
{
  "success": false,
  "error": "Insufficient balance"
}
```

## 集成完成清单

- ✅ MCP 服务器的 `cmd_shop_buy` 集成裁判服务器
- ✅ 菜单系统的购买逻辑集成裁判服务器  
- ✅ 添加了 Judge Server 配置 URL
- ✅ 添加了错误处理和回退机制
- ✅ 时间戳格式化为 ISO 8601
- ✅ 返回新的账户余额

## 依赖关系

需要以下条件来完全启用此功能：

1. **裁判服务器运行**
   - URL: `http://agentmonster.openx.pro:10000`
   - 或本地: `http://localhost:10000`

2. **PostgreSQL 数据库**
   - 数据库名: `agent_monster`
   - 需要 shop 表和 transactions 表

3. **数据库架构**
   - 必须运行 SCHEMA_EXTENSIONS.sql
   - 创建 shop_items、shop_inventory、shop_transactions 表

## 测试状态

### 单元测试
- ✅ Judge Server API 调用逻辑验证
- ✅ 错误处理路径覆盖
- ✅ 数据格式验证

### 集成测试  
- ⏳ 需要运行裁判服务器和数据库
- ⏳ 端到端购买流程测试

### 生产部署
- 确认裁判服务器地址正确
- 验证数据库连接
- 监控错误日志

## 回退机制

如果裁判服务器不可用，系统会返回错误：

```json
{
  "success": false,
  "error": "Connection refused",
  "judge": "unavailable"
}
```

用户会看到：`❌ Purchase failed: Connection refused`

## 未来改进

1. **本地缓存**：实现离线模式，缓存购买请求直到服务器可用
2. **重试机制**：自动重试失败的购买请求
3. **事务一致性**：确保本地和服务器状态始终同步
4. **审计日志**：记录所有购买交易用于审计

## 提交信息

```
feat: integrate judge server for shop purchase validation

- Add judge server API calls to cmd_shop_buy in mcp_server.py
- Add judge server integration to menu_system.py for shop purchases
- Replace local-only purchase logic with judge server validation
- All purchases now go through /api/shop/buy endpoint on judge server
- Fallback error handling when judge server is unavailable
```

## 相关文件

- `mcp_server.py`: cmd_shop_buy 函数
- `menu_system.py`: 购买处理逻辑和 Judge Server 集成
- `judge-server/`: Go 编写的裁判服务器二进制和源代码
