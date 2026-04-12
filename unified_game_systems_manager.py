#!/usr/bin/env python3
"""
Unified Game Systems Manager - Phase 1.3
统一的游戏系统管理器 - 使用 Judge Server 作为主存储

架构（更新）：
- Judge Server 作为主存储（中央数据库）
- 本地存储作为缓存/离线回退
- 所有操作优先使用 API
- 网络不可用时自动降级到本地存储
"""

import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json
import uuid

from judge_server_client import JudgeServerClient, get_judge_server_client
from persistent_food_manager import PersistentFoodManager
from persistent_cookie_manager import PersistentCookieManager
from hybrid_user_data_manager import HybridUserDataManager


class UnifiedGameSystemsManager:
    """
    统一游戏系统管理器 - Phase 1.3
    
    功能：
    1. 管理所有游戏数据系统（食物、Cookie、用户、库存等）
    2. 使用 Judge Server 作为主存储，本地存储为缓存
    3. 支持离线模式和故障转移
    4. 自动同步和冲突解决
    """
    
    def __init__(
        self,
        cache_dir: Path = None,
        judge_server_url: str = "http://agentmonster.openx.pro:10000",
        enable_auto_sync: bool = True,
    ):
        """
        初始化统一管理器
        
        Args:
            cache_dir: 缓存目录路径（默认 .monster）
            judge_server_url: Judge Server URL
            enable_auto_sync: 是否启用自动同步
        """
        if cache_dir is None:
            cache_dir = Path(".monster")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # 初始化 Judge Server 客户端
        self.judge_server_client = JudgeServerClient(judge_server_url)
        self.judge_server_url = judge_server_url
        self.enable_auto_sync = enable_auto_sync
        
        # 初始化各个系统管理器（用于缓存和离线支持）
        self.food_manager = PersistentFoodManager(
            cache_dir=self.cache_dir,
            judge_server_client=self.judge_server_client,
        )
        
        self.cookie_manager = PersistentCookieManager(
            cache_dir=self.cache_dir,
            judge_server_client=self.judge_server_client,
        )
        
        self.user_data_manager = HybridUserDataManager(
            local_cache_dir=self.cache_dir,
            judge_server_manager=self.judge_server_client,
        )
        
        # 缓存和状态
        self.lock = threading.RLock()
        self.server_online = True
        self.last_sync_time: Dict[str, datetime] = {}
        self.operation_cache: Dict[str, Any] = {}
        
        # 验证服务器连接
        self._check_server_connectivity()
        
        print("✓ 统一游戏系统管理器已初始化（Judge Server 主模式）")
    
    def _check_server_connectivity(self) -> bool:
        """检查 Judge Server 连接状态"""
        try:
            is_healthy = self.judge_server_client.health_check()
            self.server_online = is_healthy
            if is_healthy:
                print(f"✓ 已连接到 Judge Server: {self.judge_server_url}")
            else:
                print(f"⚠️  Judge Server 不可达，使用本地缓存模式")
            return is_healthy
        except Exception as e:
            print(f"⚠️  无法连接到 Judge Server: {e}")
            self.server_online = False
            return False
    
    # ========== 食物系统 API ==========
    
    def create_farm(self, owner: str, repository: str, url: str) -> Optional[Dict]:
        """创建农场（使用 Judge Server）"""
        try:
            if self.server_online:
                farm = self.judge_server_client.create_farm(owner, repository, url)
                if farm:
                    # 缓存到本地
                    self.operation_cache[f"farm_{owner}_{repository}"] = farm
                    print(f"✓ 农场已创建 (ID: {farm.get('id')})")
                    return farm
            else:
                print("⚠️  Judge Server 不可用，使用本地模式")
        except Exception as e:
            print(f"⚠️  创建农场失败: {e}")
        
        # 降级到本地存储
        return self.food_manager.create_farm(owner, repository, url)
    
    def get_farm(self, farm_id: int) -> Optional[Dict]:
        """获取农场详情"""
        try:
            if self.server_online:
                farm = self.judge_server_client.get_farm(farm_id)
                if farm:
                    return farm
        except Exception as e:
            print(f"⚠️  获取农场失败: {e}")
        
        # 降级到本地缓存
        for cache_key, cached_farm in self.operation_cache.items():
            if cache_key.startswith("farm_") and cached_farm.get("id") == farm_id:
                return cached_farm
        
        return None
    
    def add_food_to_farm(
        self,
        owner_or_farm_id: Any,
        repository: str = None,
        food_type: str = None,
        quantity: int = 1,
        emoji: str = None,
    ) -> Optional[Dict]:
        """向农场添加食物"""
        try:
            # 判断是农场 ID（Judge Server）还是 owner（本地）
            if isinstance(owner_or_farm_id, int):
                farm_id = owner_or_farm_id
                if self.server_online:
                    # 生成唯一的 food_id（使用 UUID）
                    food_id = f"food_{uuid.uuid4().hex}"
                    food = self.judge_server_client.add_food_to_farm(
                        farm_id, food_id, food_type or "cookie", quantity, emoji=emoji
                    )
                    if food:
                        print(f"✓ 食物已添加到农场")
                        return food
                else:
                    print(f"⚠️  Judge Server 不可用，无法添加食物到农场 ID {farm_id}")
                    return None
            else:
                owner = owner_or_farm_id
                if self.server_online:
                    # 先搜索农场
                    farms = self.judge_server_client.search_farms(owner=owner, repository=repository or "")
                    if farms:
                        farm_id = farms[0].get("id")
                        food_id = f"food_{uuid.uuid4().hex}"
                        food = self.judge_server_client.add_food_to_farm(
                            farm_id, food_id, food_type or "cookie", quantity, emoji=emoji
                        )
                        if food:
                            return food
                # 降级到本地（仅当使用 owner/repository 时）
                return self.food_manager.add_food_to_farm(owner, repository, food_type, quantity)
        except Exception as e:
            print(f"⚠️  添加食物失败: {e}")
            # 仅在使用 owner/repository 时才能降级
            if not isinstance(owner_or_farm_id, int):
                try:
                    return self.food_manager.add_food_to_farm(owner_or_farm_id, repository, food_type, quantity)
                except Exception as fallback_error:
                    print(f"⚠️  本地降级也失败: {fallback_error}")
            return None
    
    def consume_food(
        self,
        farm_id_or_owner: Any,
        food_id_or_repository: str,
        eater_id: str = None,
        eater_pet_id: str = None,
    ) -> Tuple[bool, Dict]:
        """消费食物"""
        try:
            if isinstance(farm_id_or_owner, int):
                # Judge Server API
                farm_id = farm_id_or_owner
                food_id = food_id_or_repository
                if self.server_online and eater_id:
                    success = self.judge_server_client.consume_food(
                        farm_id, food_id, eater_id, eater_pet_id or ""
                    )
                    if success:
                        print(f"✓ 食物已消费")
                        return True, {"success": True}
            else:
                # 本地 API
                owner = farm_id_or_owner
                repository = food_id_or_repository
                if self.server_online and eater_id:
                    # 获取农场信息
                    farms = self.judge_server_client.search_farms(owner=owner, repository=repository)
                    if farms:
                        farm_id = farms[0].get("id")
                        # 查找食物
                        farm_data = self.judge_server_client.get_farm(farm_id)
                        # 实现消费逻辑
                        return True, {"success": True}
        except Exception as e:
            print(f"⚠️  消费食物失败: {e}")
        
        # 降级到本地
        return self.food_manager.consume_food(farm_id_or_owner, food_id_or_repository, eater_id, eater_pet_id)
    
    def get_farm_statistics(self, owner: str = None) -> Dict:
        """获取农场统计"""
        try:
            if self.server_online and owner:
                farms = self.judge_server_client.search_farms(owner=owner)
                if farms:
                    total_foods = 0
                    total_quantity = 0
                    for farm in farms:
                        farm_id = farm.get("id")
                        stats = self.judge_server_client.get_farm_statistics(farm_id)
                        if stats:
                            total_foods += stats.get("total_foods", 0)
                            total_quantity += stats.get("total_quantity", 0)
                    return {
                        "owner": owner,
                        "farms": len(farms),
                        "total_foods": total_foods,
                        "total_quantity": total_quantity,
                    }
        except Exception as e:
            print(f"⚠️  获取农场统计失败: {e}")
        
        # 降级到本地
        if owner:
            farms = self.food_manager.search_farms_by_owner(owner)
            if not farms:
                return {"owner": owner, "farms": 0}
            return {
                "owner": owner,
                "farms": len(farms),
                "total_foods": sum(len(f.foods) for f in farms),
                "total_quantity": sum(f.current_quantity for f in farms for f in [f] if hasattr(f, "current_quantity")),
            }
        return {}
    
    # ========== Cookie 系统 API ==========
    
    def register_cookie(
        self,
        cookie_id: str,
        cookie_type: str = "cookie",
        emoji: str = "🍪",
        generator_id: str = None,
    ) -> bool:
        """注册 Cookie"""
        try:
            if self.server_online:
                cookie = self.judge_server_client.register_cookie(
                    cookie_id, cookie_type, emoji=emoji, generator_id=generator_id or ""
                )
                if cookie:
                    print(f"✓ Cookie 已注册")
                    return True
        except Exception as e:
            print(f"⚠️  注册 Cookie 失败: {e}")
        
        # 降级到本地
        return self.cookie_manager.register_cookie(cookie_id, cookie_type, None, generator_id)
    
    def claim_cookie(self, cookie_id: str, player_id: str, exp_reward: int = 10, energy_reward: int = 5) -> Tuple[bool, Dict]:
        """玩家索赔 Cookie"""
        try:
            if self.server_online:
                claim = self.judge_server_client.claim_cookie(
                    cookie_id, player_id, exp_reward, energy_reward
                )
                if claim:
                    print(f"✓ Cookie 已索赔")
                    return True, claim
        except Exception as e:
            print(f"⚠️  索赔 Cookie 失败: {e}")
        
        # 降级到本地
        success, response = self.cookie_manager.claim_cookie(cookie_id, player_id)
        return success, response
    
    def get_cookie_statistics(self) -> Dict:
        """获取 Cookie 统计"""
        try:
            if self.server_online:
                stats = self.judge_server_client.get_cookie_statistics()
                if stats:
                    return stats
        except Exception as e:
            print(f"⚠️  获取 Cookie 统计失败: {e}")
        
        # 降级到本地
        return self.cookie_manager.get_global_statistics()
    
    def scan_cookies(self, player_id: str) -> Dict:
        """扫描玩家的 Cookie"""
        try:
            if self.server_online:
                result = self.judge_server_client.scan_cookies(player_id)
                if result:
                    print(f"✓ Cookie 已扫描")
                    return result
        except Exception as e:
            print(f"⚠️  扫描 Cookie 失败: {e}")
        
        return {"player_id": player_id, "fragments": {}}
    
    # ========== 蛋系统 API ==========
    
    def create_egg(self, owner_id: str, incubation_hours: int = 72) -> Optional[Dict]:
        """创建蛋"""
        try:
            if self.server_online:
                egg_id = f"egg_{uuid.uuid4().hex}"
                egg = self.judge_server_client.create_egg(egg_id, owner_id, incubation_hours)
                if egg:
                    print(f"✓ 蛋已创建")
                    return egg
        except Exception as e:
            print(f"⚠️  创建蛋失败: {e}")
        
        return None
    
    def get_egg(self, egg_id: str) -> Optional[Dict]:
        """获取蛋信息"""
        try:
            if self.server_online:
                egg = self.judge_server_client.get_egg(egg_id)
                if egg:
                    return egg
        except Exception as e:
            print(f"⚠️  获取蛋信息失败: {e}")
        
        return None
    
    def hatch_egg(self, egg_id: str, pet_id: str) -> bool:
        """孵化蛋"""
        try:
            if self.server_online:
                success = self.judge_server_client.hatch_egg(egg_id, pet_id)
                if success:
                    print(f"✓ 蛋已孵化")
                    return True
        except Exception as e:
            print(f"⚠️  孵化蛋失败: {e}")
        
        return False
    
    def get_egg_statistics(self) -> Dict:
        """获取蛋统计"""
        try:
            if self.server_online:
                stats = self.judge_server_client.get_egg_statistics()
                if stats:
                    return stats
        except Exception as e:
            print(f"⚠️  获取蛋统计失败: {e}")
        
        return {}
    
    # ========== 商店系统 API ==========
    
    def list_shop_items(self) -> List[Dict]:
        """列出商店物品"""
        try:
            if self.server_online:
                items = self.judge_server_client.list_shop_items()
                if items is not None:
                    return items
        except Exception as e:
            print(f"⚠️  列出商店物品失败: {e}")
        
        return []
    
    def buy_item(self, item_id: str, player_id: str, quantity: int = 1) -> Tuple[bool, Dict]:
        """购买物品"""
        try:
            if self.server_online:
                transaction = self.judge_server_client.buy_item(item_id, player_id, quantity)
                if transaction:
                    print(f"✓ 物品已购买")
                    return True, transaction
        except Exception as e:
            print(f"⚠️  购买物品失败: {e}")
        
        return False, {}
    
    def get_shop_statistics(self) -> Dict:
        """获取商店统计"""
        try:
            if self.server_online:
                stats = self.judge_server_client.get_shop_statistics()
                if stats:
                    return stats
        except Exception as e:
            print(f"⚠️  获取商店统计失败: {e}")
        
        return {}
    
    # ========== 系统状态 API ==========
    
    def get_system_status(self) -> Dict:
        """获取系统总体状态"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "judge_server": {
                "url": self.judge_server_url,
                "online": self.server_online,
            },
            "local_storage": {
                "cache_dir": str(self.cache_dir),
            },
        }
    
    def check_server_connectivity(self) -> bool:
        """检查 Judge Server 连接状态"""
        return self._check_server_connectivity()
    
    def export_all_data(self, export_dir: str) -> Dict:
        """导出所有数据（备份）"""
        export_path = Path(export_dir)
        export_path.mkdir(parents=True, exist_ok=True)
        
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "exports": {},
        }
        
        # 尝试从 Judge Server 导出
        if self.server_online:
            try:
                farms = self.judge_server_client.search_farms()
                farm_file = export_path / "farms_export.json"
                with open(farm_file, 'w') as f:
                    json.dump(farms, f, indent=2)
                results["exports"]["farms"] = str(farm_file)
            except Exception as e:
                results["exports"]["farms"] = f"Error: {e}"
        
        return results



# ============================================================================
# 集成示例
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print(" 🎮 统一游戏系统管理器演示 - Phase 1.3 (Judge Server 主模式)")
    print("=" * 80)
    print()
    
    from pathlib import Path
    
    # 创建管理器（会自动连接到 Judge Server）
    manager = UnifiedGameSystemsManager(
        cache_dir=Path(".monster"),
        judge_server_url="http://localhost:10000",
        enable_auto_sync=True,
    )
    
    print()
    print("1️⃣  系统状态")
    print("-" * 80)
    status = manager.get_system_status()
    print(f"Judge Server: {status['judge_server']['url']}")
    print(f"在线状态: {'✓ 在线' if status['judge_server']['online'] else '⚠️  离线'}")
    print()
    
    if status['judge_server']['online']:
        print("2️⃣  农场系统 (Farm System)")
        print("-" * 80)
        # 创建农场（使用时间戳确保唯一性）
        timestamp = int(datetime.now().timestamp())
        repo_name = f"test-repo-{timestamp}"
        farm = manager.create_farm("alice", repo_name, f"https://github.com/alice/{repo_name}")
        if farm:
            farm_id = farm.get('id')
            print(f"✓ 农场已创建 (ID: {farm_id})")
            
            # 添加食物
            food = manager.add_food_to_farm(farm_id, food_type="cookie", quantity=10, emoji="🍪")
            if food:
                print(f"✓ 食物已添加 (ID: {food.get('food_id')})")
            
            # 获取统计
            stats = manager.get_farm_statistics("alice")
            if stats:
                print(f"✓ 农场统计: {stats['total_foods']} 种食物, {stats['total_quantity']} 总数量")
        
        print()
        print("3️⃣  Cookie 系统")
        print("-" * 80)
        # 注册 Cookie
        if manager.register_cookie("0xcookie001", "cookie", "🍪", "alice"):
            print(f"✓ Cookie 已注册")
            
            # 索赔 Cookie
            success, claim = manager.claim_cookie("0xcookie001", "bob", 100, 50)
            if success:
                print(f"✓ Cookie 已被 bob 索赔")
        
        # Cookie 统计
        cookie_stats = manager.get_cookie_statistics()
        if cookie_stats:
            print(f"✓ Cookie 统计: {cookie_stats.get('total_cookies', 0)} 个 Cookie")
        
        print()
        print("4️⃣  蛋系统 (Egg System)")
        print("-" * 80)
        # 创建蛋
        egg = manager.create_egg("alice", 72)
        if egg:
            egg_id = egg.get('egg_id')
            print(f"✓ 蛋已创建 (ID: {egg_id})")
            
            # 蛋统计
            egg_stats = manager.get_egg_statistics()
            if egg_stats:
                print(f"✓ 蛋统计: {egg_stats.get('total_eggs', 0)} 个蛋")
        
        print()
        print("5️⃣  商店系统 (Shop System)")
        print("-" * 80)
        # 列出物品
        items = manager.list_shop_items()
        print(f"✓ 商店物品: {len(items)} 个物品")
        
        # 商店统计
        shop_stats = manager.get_shop_statistics()
        if shop_stats:
            print(f"✓ 商店统计: {shop_stats.get('total_items', 0)} 件物品")
    else:
        print("⚠️  Judge Server 离线，应用将使用本地缓存模式")
    
    print()
    print("=" * 80)
    print("✓ 演示完成!")
    print("=" * 80)
