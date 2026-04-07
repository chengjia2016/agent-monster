#!/usr/bin/env python3
"""
Enhanced Onboarding Manager
增强的新用户注册系统，集成统一游戏管理器

特性：
- 完整的新用户初始化流程
- 自动分配初始资源（精灵币、物品、蛋、宠物）
- 支持本地和 Judge Server 存储
- Hybrid 缓存支持
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime

try:
    from unified_game_systems_manager import UnifiedGameSystemsManager
    from persistent_egg_incubator import PersistentEggIncubator
    from user_manager import UserManager, User
    from economy_manager import EconomyManager
except ImportError:
    # 导入失败时使用 None
    UnifiedGameSystemsManager = None
    PersistentEggIncubator = None
    UserManager = None
    EconomyManager = None


class EnhancedOnboardingManager:
    """
    增强的新用户注册管理器
    
    初始化流程：
    1. 创建用户账户（GitHub 集成）
    2. 初始化经济账户（100 精灵币）
    3. 分配初始物品
    4. 创建启动宠物（小黄鸭）
    5. 创建启动蛋
    6. 设置农场（可选）
    """
    
    # 初始资源配置
    INITIAL_RESOURCES = {
        "balance": 100.0,  # 精灵币
        "items": {
            "pokeball": 3,           # 精灵球
            "seed_grass": 2,         # 草种子
            "potion_small": 1,       # 小药剂
        },
        "starter_pet": {
            "species": "Psyduck",    # 小黄鸭
            "name": "Psyduck",
            "level": 1,
        },
        "starter_egg": {
            "incubation_hours": 72,
        },
    }
    
    def __init__(
        self,
        cache_dir: Path = None,
        systems_manager: UnifiedGameSystemsManager = None,
        user_manager: UserManager = None,
        economy_manager: EconomyManager = None,
    ):
        """
        初始化增强 onboarding 管理器
        
        Args:
            cache_dir: 缓存目录
            systems_manager: 统一游戏系统管理器
            user_manager: 用户管理器
            economy_manager: 经济管理器
        """
        if cache_dir is None:
            cache_dir = Path(".monster")
        
        self.cache_dir = Path(cache_dir)
        self.onboarding_dir = self.cache_dir / "onboarding"
        self.onboarding_dir.mkdir(parents=True, exist_ok=True)
        self.onboarding_log = self.onboarding_dir / "onboarding_log.jsonl"
        
        # 初始化管理器
        self.systems_manager = systems_manager or (
            UnifiedGameSystemsManager(cache_dir=cache_dir)
            if UnifiedGameSystemsManager else None
        )
        self.egg_incubator = PersistentEggIncubator(cache_dir=cache_dir) if PersistentEggIncubator else None
        self.user_manager = user_manager or (UserManager(str(cache_dir)) if UserManager else None)
        self.economy_manager = economy_manager or (EconomyManager(str(cache_dir)) if EconomyManager else None)
    
    def _log_onboarding(self, github_id: int, github_login: str, success: bool, details: Dict = None):
        """记录新用户注册事件"""
        try:
            record = {
                "timestamp": datetime.utcnow().isoformat(),
                "github_id": github_id,
                "github_login": github_login,
                "success": success,
                **(details or {}),
            }
            
            with open(self.onboarding_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️  记录 onboarding 日志失败: {e}")
    
    def register_new_user(
        self,
        github_id: int,
        github_login: str,
        email: str = "",
        avatar_url: str = "",
    ) -> Tuple[bool, Dict]:
        """
        完整的新用户注册流程
        
        Args:
            github_id: GitHub 数字 ID
            github_login: GitHub 用户名
            email: 邮箱（可选）
            avatar_url: 头像 URL（可选）
            
        Returns:
            (是否成功, 响应数据)
        """
        
        result = {
            "success": False,
            "user_id": None,
            "resources_granted": {},
            "errors": [],
            "warnings": [],
        }
        
        try:
            # 1. 创建用户账户
            user_data = {
                "github_id": github_id,
                "github_login": github_login,
                "email": email,
                "avatar_url": avatar_url,
                "created_at": datetime.utcnow().isoformat(),
            }
            
            # 使用 GitHub ID 作为用户 ID
            user_id = f"user_{github_id}"
            result["user_id"] = user_id
            
            # 2. 保存用户到本地缓存
            if self.systems_manager:
                self.systems_manager.save_user_data(github_id, user_data, sync_to_server=True)
            else:
                # 回退：使用文件存储
                users_dir = self.cache_dir / "users"
                users_dir.mkdir(parents=True, exist_ok=True)
                with open(users_dir / f"{user_id}.json", 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)
            
            # 3. 初始化经济账户（100 精灵币）
            initial_balance = self.INITIAL_RESOURCES["balance"]
            try:
                if self.economy_manager:
                    self.economy_manager.create_account(user_id, initial_balance)
                else:
                    # 回退：手动创建
                    accounts_dir = self.cache_dir / "accounts"
                    accounts_dir.mkdir(parents=True, exist_ok=True)
                    with open(accounts_dir / f"{user_id}.json", 'w', encoding='utf-8') as f:
                        json.dump({
                            "user_id": user_id,
                            "balance": initial_balance,
                            "created_at": datetime.utcnow().isoformat(),
                        }, f, indent=2, ensure_ascii=False)
                
                result["resources_granted"]["balance"] = initial_balance
            except Exception as e:
                result["warnings"].append(f"创建经济账户失败: {e}")
            
            # 4. 分配初始物品
            initial_items = self.INITIAL_RESOURCES["items"]
            try:
                inventory_dir = self.cache_dir / "inventory"
                inventory_dir.mkdir(parents=True, exist_ok=True)
                with open(inventory_dir / f"{user_id}.json", 'w', encoding='utf-8') as f:
                    json.dump(initial_items, f, indent=2, ensure_ascii=False)
                
                result["resources_granted"]["items"] = initial_items
            except Exception as e:
                result["warnings"].append(f"分配初始物品失败: {e}")
            
            # 5. 创建启动宠物（小黄鸭）
            starter_pet = self.INITIAL_RESOURCES["starter_pet"]
            starter_pet_id = f"{starter_pet['species'].lower()}_{github_login}_{github_id}"
            try:
                pets_dir = self.cache_dir / "pets"
                pets_dir.mkdir(parents=True, exist_ok=True)
                with open(pets_dir / f"{starter_pet_id}.json", 'w', encoding='utf-8') as f:
                    json.dump({
                        "pet_id": starter_pet_id,
                        "owner_id": user_id,
                        "species": starter_pet["species"],
                        "name": starter_pet["name"],
                        "level": starter_pet["level"],
                        "created_at": datetime.utcnow().isoformat(),
                    }, f, indent=2, ensure_ascii=False)
                
                result["resources_granted"]["starter_pet"] = {
                    "pet_id": starter_pet_id,
                    "species": starter_pet["species"],
                }
            except Exception as e:
                result["warnings"].append(f"创建启动宠物失败: {e}")
            
            # 6. 创建启动蛋
            try:
                if self.egg_incubator:
                    egg = self.egg_incubator.create_egg(
                        user_id,
                        incubation_hours=self.INITIAL_RESOURCES["starter_egg"]["incubation_hours"],
                        attributes={"initial": True},
                    )
                    result["resources_granted"]["starter_egg"] = {
                        "egg_id": egg.egg_id,
                        "incubation_hours": egg.incubation_hours,
                    }
                else:
                    result["warnings"].append("蛋孵化器不可用")
            except Exception as e:
                result["warnings"].append(f"创建启动蛋失败: {e}")
            
            # 标记成功
            result["success"] = True
            
            # 记录
            self._log_onboarding(github_id, github_login, True, {
                "resources_granted": result["resources_granted"],
                "warnings": result["warnings"],
            })
            
        except Exception as e:
            result["errors"].append(str(e))
            result["success"] = False
            self._log_onboarding(github_id, github_login, False, {
                "error": str(e),
            })
        
        return result["success"], result
    
    def get_user_onboarding_status(self, user_id: str) -> Dict:
        """获取用户的 onboarding 状态"""
        status = {
            "user_id": user_id,
            "registered": False,
            "resources": {
                "balance": 0,
                "items_count": 0,
                "has_starter_pet": False,
                "has_starter_egg": False,
            },
        }
        
        # 检查用户是否存在
        users_dir = self.cache_dir / "users"
        user_file = users_dir / f"{user_id}.json"
        if user_file.exists():
            status["registered"] = True
        
        # 检查资源
        try:
            # 检查余额
            accounts_dir = self.cache_dir / "accounts"
            account_file = accounts_dir / f"{user_id}.json"
            if account_file.exists():
                with open(account_file, 'r', encoding='utf-8') as f:
                    account = json.load(f)
                status["resources"]["balance"] = account.get("balance", 0)
            
            # 检查物品
            inventory_dir = self.cache_dir / "inventory"
            inventory_file = inventory_dir / f"{user_id}.json"
            if inventory_file.exists():
                with open(inventory_file, 'r', encoding='utf-8') as f:
                    inventory = json.load(f)
                status["resources"]["items_count"] = sum(inventory.values())
            
            # 检查启动宠物
            pets_dir = self.cache_dir / "pets"
            if pets_dir.exists():
                for pet_file in pets_dir.glob("*.json"):
                    with open(pet_file, 'r', encoding='utf-8') as f:
                        pet = json.load(f)
                    if pet.get("owner_id") == user_id and pet.get("level") == 1:
                        status["resources"]["has_starter_pet"] = True
                        break
            
            # 检查启动蛋
            if self.egg_incubator:
                eggs = self.egg_incubator.get_owner_eggs(user_id)
                status["resources"]["has_starter_egg"] = len(eggs) > 0
        
        except Exception as e:
            print(f"⚠️  获取 onboarding 状态失败: {e}")
        
        return status
    
    def get_onboarding_statistics(self) -> Dict:
        """获取 onboarding 统计"""
        stats = {
            "total_users": 0,
            "successful_registrations": 0,
            "failed_registrations": 0,
            "average_resources_granted": {},
        }
        
        try:
            if self.onboarding_log.exists():
                with open(self.onboarding_log, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line)
                            if record.get("success"):
                                stats["successful_registrations"] += 1
                            else:
                                stats["failed_registrations"] += 1
            
            stats["total_users"] = stats["successful_registrations"] + stats["failed_registrations"]
        
        except Exception as e:
            print(f"⚠️  计算 onboarding 统计失败: {e}")
        
        return stats


# ============================================================================
# 示例和测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" 📋 增强 Onboarding 系统演示")
    print("=" * 70)
    print()
    
    from pathlib import Path
    
    # 创建管理器
    manager = EnhancedOnboardingManager(cache_dir=Path(".monster"))
    
    # 演示 1: 注册新用户
    print("1️⃣  注册新用户")
    print("-" * 70)
    success, result = manager.register_new_user(
        github_id=123456,
        github_login="testuser",
        email="test@example.com",
        avatar_url="https://example.com/avatar.jpg",
    )
    print(f"✓ 注册结果: {'成功' if success else '失败'}")
    if success:
        print(f"  用户 ID: {result['user_id']}")
        print(f"  分配资源: {json.dumps(result['resources_granted'], indent=4, ensure_ascii=False)}")
    if result['warnings']:
        for warning in result['warnings']:
            print(f"  ⚠️  警告: {warning}")
    print()
    
    # 演示 2: 查看用户状态
    print("2️⃣  查看用户 Onboarding 状态")
    print("-" * 70)
    status = manager.get_user_onboarding_status("user_123456")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    print()
    
    # 演示 3: 统计信息
    print("3️⃣  Onboarding 统计")
    print("-" * 70)
    stats = manager.get_onboarding_statistics()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print()
    
    print("=" * 70)
    print("✓ 演示完成!")
    print("=" * 70)
