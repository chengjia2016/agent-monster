#!/usr/bin/env python3
"""
Agent Monster - GitHub Issues Integration System

将 GitHub Issues 用作玩家互动平台：
- 🎮 发布挑战书 (Battle Challenges)
- 🍖 发布食物交易 (Farm Food Trades)
- 💬 玩家交流和社区

支持自动发布、自动读取、手动模式
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    import requests
except ImportError:
    requests = None


@dataclass
class ChallengeIssue:
    """挑战书 Issue 数据类"""
    issue_id: int
    title: str
    challenger: str  # GitHub username
    challenger_pet: str
    defender_pet: str  # 可选，对方宠物
    challenger_level: int
    challenge_type: str  # "duel", "tournament", "team_battle"
    reward: float  # 金币奖励
    status: str  # "open", "accepted", "completed", "cancelled"
    created_at: str
    body: str
    url: str
    
    def to_dict(self):
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "challenger": self.challenger,
            "challenger_pet": self.challenger_pet,
            "defender_pet": self.defender_pet,
            "challenger_level": self.challenger_level,
            "challenge_type": self.challenge_type,
            "reward": self.reward,
            "status": self.status,
            "created_at": self.created_at,
            "url": self.url,
        }


@dataclass
class FoodTradeIssue:
    """食物交易 Issue 数据类"""
    issue_id: int
    title: str
    seller: str  # GitHub username
    farm_name: str
    food_type: str  # "vegetable", "meat", "fruit", "special"
    quantity: int
    price: float  # 单价
    quality: str  # "common", "rare", "epic", "legendary"
    status: str  # "available", "negotiating", "sold"
    created_at: str
    body: str
    url: str
    
    def to_dict(self):
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "seller": self.seller,
            "farm_name": self.farm_name,
            "food_type": self.food_type,
            "quantity": self.quantity,
            "price": self.price,
            "quality": self.quality,
            "status": self.status,
            "created_at": self.created_at,
            "url": self.url,
        }


class GitHubIssuesManager:
    """GitHub Issues 管理器"""
    
    # Issue 标签定义
    LABELS = {
        "challenge": "🎮 Battle Challenge",
        "food_trade": "🍖 Food Trade",
        "quest": "📋 Quest",
        "announcement": "📢 Announcement",
    }
    
    # 状态标签
    STATUS_LABELS = {
        "open": "Status: Open",
        "accepted": "Status: Accepted",
        "completed": "Status: Completed",
        "cancelled": "Status: Cancelled",
    }
    
    # 食物类型标签
    FOOD_LABELS = {
        "vegetable": "🥬 Vegetable",
        "meat": "🥩 Meat",
        "fruit": "🍎 Fruit",
        "special": "⭐ Special",
    }
    
    # 品质标签
    QUALITY_LABELS = {
        "common": "Common",
        "rare": "Rare",
        "epic": "Epic",
        "legendary": "Legendary",
    }
    
    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        """
        初始化 GitHub Issues 管理器
        
        参数：
        - owner: GitHub 用户名或组织
        - repo: 仓库名称
        - token: GitHub Personal Access Token
        """
        self.owner = owner
        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_base = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = self._get_headers()
    
    def _get_headers(self) -> Dict[str, str]:
        """获取 HTTP 请求头"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    def post_challenge(
        self,
        challenger: str,
        challenger_pet: str,
        challenger_level: int,
        challenge_type: str = "duel",
        defender_pet: Optional[str] = None,
        reward: float = 100.0,
        description: Optional[str] = None,
    ) -> Optional[int]:
        """
        发布挑战书
        
        参数：
        - challenger: 挑战者用户名
        - challenger_pet: 挑战者宠物名
        - challenger_level: 宠物等级
        - challenge_type: 挑战类型 (duel, tournament, team_battle)
        - defender_pet: 被挑战宠物名 (可选)
        - reward: 奖励金币
        - description: 额外描述
        
        返回: Issue ID 或 None
        """
        if not requests:
            print("❌ requests library not available")
            return None
        
        # 生成标题
        title = f"🎮 {challenge_type.upper()} Challenge: {challenger_pet} vs {defender_pet or 'Any'}"
        
        # 生成内容
        body = self._format_challenge_body(
            challenger,
            challenger_pet,
            challenger_level,
            challenge_type,
            defender_pet,
            reward,
            description
        )
        
        # 创建 Issue
        data = {
            "title": title,
            "body": body,
            "labels": [
                self.LABELS["challenge"],
                self.STATUS_LABELS["open"],
            ]
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/issues",
                json=data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ Challenge posted: #{issue['number']}")
                print(f"   URL: {issue['html_url']}")
                return issue['number']
            else:
                print(f"❌ Failed to post challenge: {response.status_code}")
                print(f"   {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error posting challenge: {e}")
            return None
    
    def post_food_trade(
        self,
        seller: str,
        farm_name: str,
        food_type: str,
        quantity: int,
        price: float,
        quality: str = "common",
        description: Optional[str] = None,
    ) -> Optional[int]:
        """
        发布食物交易
        
        参数：
        - seller: 卖家用户名
        - farm_name: 农场名称
        - food_type: 食物类型 (vegetable, meat, fruit, special)
        - quantity: 数量
        - price: 单价
        - quality: 品质 (common, rare, epic, legendary)
        - description: 额外描述
        
        返回: Issue ID 或 None
        """
        if not requests:
            print("❌ requests library not available")
            return None
        
        # 生成标题
        title = f"🍖 {quality.upper()} {food_type.title()}: {farm_name} - {quantity} units @ {price} coins"
        
        # 生成内容
        body = self._format_food_trade_body(
            seller,
            farm_name,
            food_type,
            quantity,
            price,
            quality,
            description
        )
        
        # 创建 Issue
        data = {
            "title": title,
            "body": body,
            "labels": [
                self.LABELS["food_trade"],
                self.FOOD_LABELS.get(food_type, "Other"),
                self.QUALITY_LABELS.get(quality, "Common"),
                self.STATUS_LABELS["open"],
            ]
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/issues",
                json=data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 201:
                issue = response.json()
                print(f"✅ Food trade posted: #{issue['number']}")
                print(f"   URL: {issue['html_url']}")
                return issue['number']
            else:
                print(f"❌ Failed to post food trade: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error posting food trade: {e}")
            return None
    
    def fetch_challenges(self, status: str = "open") -> List[ChallengeIssue]:
        """
        读取挑战书列表
        
        参数:
        - status: 状态过滤 (open, accepted, completed, cancelled)
        
        返回: ChallengeIssue 列表
        """
        if not requests:
            print("❌ requests library not available")
            return []
        
        try:
            # 构建查询条件
            query_params = {
                "labels": self.LABELS["challenge"],
                "state": "open" if status == "open" else "all",
                "per_page": 100,
            }
            
            response = requests.get(
                f"{self.api_base}/issues",
                params=query_params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch challenges: {response.status_code}")
                return []
            
            challenges = []
            for issue in response.json():
                challenge = self._parse_challenge_issue(issue, status)
                if challenge:
                    challenges.append(challenge)
            
            return challenges
        except Exception as e:
            print(f"❌ Error fetching challenges: {e}")
            return []
    
    def fetch_food_trades(self, status: str = "available") -> List[FoodTradeIssue]:
        """
        读取食物交易列表
        
        参数:
        - status: 状态过滤 (available, negotiating, sold)
        
        返回: FoodTradeIssue 列表
        """
        if not requests:
            print("❌ requests library not available")
            return []
        
        try:
            # 构建查询条件
            query_params = {
                "labels": self.LABELS["food_trade"],
                "state": "open",
                "per_page": 100,
            }
            
            response = requests.get(
                f"{self.api_base}/issues",
                params=query_params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch food trades: {response.status_code}")
                return []
            
            trades = []
            for issue in response.json():
                trade = self._parse_food_trade_issue(issue, status)
                if trade:
                    trades.append(trade)
            
            return trades
        except Exception as e:
            print(f"❌ Error fetching food trades: {e}")
            return []
    
    def _format_challenge_body(
        self,
        challenger: str,
        challenger_pet: str,
        challenger_level: int,
        challenge_type: str,
        defender_pet: Optional[str],
        reward: float,
        description: Optional[str]
    ) -> str:
        """生成挑战书内容"""
        body = f"""## 🎮 Battle Challenge

**Challenger:** @{challenger}
**Pet:** {challenger_pet}
**Level:** {challenger_level}
**Type:** {challenge_type.upper()}
**Reward:** {reward} coins

### Challenge Details
"""
        
        if defender_pet:
            body += f"\n**Defending Pet:** {defender_pet}\n"
        else:
            body += f"\n**Defending Pet:** Any (Open Challenge)\n"
        
        if description:
            body += f"\n**Description:**\n{description}\n"
        
        body += f"""
### How to Accept
Reply to this issue to accept the challenge!

---
*Posted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*
"""
        return body
    
    def _format_food_trade_body(
        self,
        seller: str,
        farm_name: str,
        food_type: str,
        quantity: int,
        price: float,
        quality: str,
        description: Optional[str]
    ) -> str:
        """生成食物交易内容"""
        body = f"""## 🍖 Food Trade

**Seller:** @{seller}
**Farm:** {farm_name}
**Food Type:** {food_type.title()}
**Quality:** {quality.upper()}
**Quantity:** {quantity} units
**Price:** {price} coins per unit
**Total:** {quantity * price} coins

### Product Details
"""
        
        if description:
            body += f"\n{description}\n"
        
        body += f"""
### How to Buy
Reply to this issue to make an offer or negotiate the price!

---
*Posted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*
"""
        return body
    
    def _parse_challenge_issue(self, issue: Dict, expected_status: str) -> Optional[ChallengeIssue]:
        """解析挑战书 Issue"""
        try:
            # 从标题提取信息
            title = issue.get("title", "")
            body = issue.get("body", "")
            
            # 提取挑战者和宠物信息
            lines = body.split("\n")
            challenger = ""
            challenger_pet = ""
            challenger_level = 0
            challenge_type = "duel"
            defender_pet = None
            reward = 0.0
            
            for line in lines:
                if line.startswith("**Challenger:**"):
                    challenger = line.split("@")[-1].strip()
                elif line.startswith("**Pet:**"):
                    challenger_pet = line.split(":**")[-1].strip()
                elif line.startswith("**Level:**"):
                    challenger_level = int(line.split(":**")[-1].strip())
                elif line.startswith("**Type:**"):
                    challenge_type = line.split(":**")[-1].strip().lower()
                elif line.startswith("**Defending Pet:**"):
                    defender_pet = line.split(":**")[-1].strip()
                    if defender_pet == "Any (Open Challenge)":
                        defender_pet = None
                elif line.startswith("**Reward:**"):
                    reward_text = line.split(":**")[-1].strip()
                    reward = float(reward_text.split()[0])
            
            # 确定状态
            status = "open"
            if issue.get("state") == "closed":
                status = "completed"
            
            if status != expected_status and expected_status != "all":
                return None
            
            return ChallengeIssue(
                issue_id=issue["number"],
                title=title,
                challenger=challenger,
                challenger_pet=challenger_pet,
                defender_pet=defender_pet,
                challenger_level=challenger_level,
                challenge_type=challenge_type,
                reward=reward,
                status=status,
                created_at=issue["created_at"],
                body=body,
                url=issue["html_url"],
            )
        except Exception as e:
            print(f"⚠️ Error parsing challenge issue: {e}")
            return None
    
    def _parse_food_trade_issue(self, issue: Dict, expected_status: str) -> Optional[FoodTradeIssue]:
        """解析食物交易 Issue"""
        try:
            title = issue.get("title", "")
            body = issue.get("body", "")
            
            # 从标题提取信息
            lines = body.split("\n")
            seller = ""
            farm_name = ""
            food_type = "vegetable"
            quantity = 0
            price = 0.0
            quality = "common"
            
            for line in lines:
                if line.startswith("**Seller:**"):
                    seller = line.split("@")[-1].strip()
                elif line.startswith("**Farm:**"):
                    farm_name = line.split(":**")[-1].strip()
                elif line.startswith("**Food Type:**"):
                    food_type = line.split(":**")[-1].strip().lower()
                elif line.startswith("**Quality:**"):
                    quality = line.split(":**")[-1].strip().lower()
                elif line.startswith("**Quantity:**"):
                    qty_text = line.split(":**")[-1].strip()
                    quantity = int(qty_text.split()[0])
                elif line.startswith("**Price:**"):
                    price_text = line.split(":**")[-1].strip()
                    price = float(price_text.split()[0])
            
            # 确定状态
            status = "available"
            if issue.get("state") == "closed":
                status = "sold"
            
            if status != expected_status and expected_status != "all":
                return None
            
            return FoodTradeIssue(
                issue_id=issue["number"],
                title=title,
                seller=seller,
                farm_name=farm_name,
                food_type=food_type,
                quantity=quantity,
                price=price,
                quality=quality,
                status=status,
                created_at=issue["created_at"],
                body=body,
                url=issue["html_url"],
            )
        except Exception as e:
            print(f"⚠️ Error parsing food trade issue: {e}")
            return None
    
    def update_issue_status(self, issue_id: int, new_status: str) -> bool:
        """
        更新 Issue 状态
        
        参数:
        - issue_id: Issue 编号
        - new_status: 新状态 (open, accepted, completed, cancelled)
        
        返回: 是否成功
        """
        if not requests:
            return False
        
        try:
            # 映射状态到标签
            state = "open" if new_status != "completed" else "closed"
            
            data = {"state": state}
            
            response = requests.patch(
                f"{self.api_base}/issues/{issue_id}",
                json=data,
                headers=self.headers,
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error updating issue status: {e}")
            return False
    
    def add_comment(self, issue_id: int, comment: str) -> bool:
        """
        添加评论
        
        参数:
        - issue_id: Issue 编号
        - comment: 评论内容
        
        返回: 是否成功
        """
        if not requests:
            return False
        
        try:
            data = {"body": comment}
            
            response = requests.post(
                f"{self.api_base}/issues/{issue_id}/comments",
                json=data,
                headers=self.headers,
                timeout=10
            )
            
            return response.status_code == 201
        except Exception as e:
            print(f"❌ Error adding comment: {e}")
            return False
    
    def update_challenge_status(self, issue_id: int, status: str) -> bool:
        """
        Update challenge status (wrapper for update_issue_status)
        
        Args:
            issue_id: GitHub Issue ID
            status: New status (open, accepted, completed, cancelled)
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_issue_status(issue_id, status)
    
    def update_food_trade_status(self, issue_id: int, status: str) -> bool:
        """
        Update food trade status (wrapper for update_issue_status)
        
        Args:
            issue_id: GitHub Issue ID
            status: New status (available, negotiating, sold)
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_issue_status(issue_id, status)
    
    def add_comment_to_issue(self, issue_id: int, comment: str) -> bool:
        """
        Add a comment to an issue (wrapper for add_comment)
        
        Args:
            issue_id: GitHub Issue ID
            comment: Comment content
            
        Returns:
            True if successful, False otherwise
        """
        return self.add_comment(issue_id, comment)


def demo():
    """演示 GitHub Issues 功能"""
    
    print("\n" + "=" * 70)
    print("Agent Monster - GitHub Issues Integration Demo")
    print("=" * 70)
    
    # 使用示例
    owner = "chengjia2016"
    repo = "agent-monster"
    
    manager = GitHubIssuesManager(owner, repo)
    
    # 演示数据
    print("\n📝 Demo: Posting a Challenge")
    print("-" * 70)
    
    challenge_id = manager.post_challenge(
        challenger="player1",
        challenger_pet="Pikachu",
        challenger_level=15,
        challenge_type="duel",
        defender_pet="Charizard",
        reward=250.0,
        description="A classic 1v1 duel! My Pikachu vs your Charizard. Best of luck!"
    )
    
    print("\n📝 Demo: Posting a Food Trade")
    print("-" * 70)
    
    trade_id = manager.post_food_trade(
        seller="farmer_john",
        farm_name="Golden Valley Farm",
        food_type="vegetable",
        quantity=50,
        price=10.0,
        quality="rare",
        description="Fresh organic vegetables grown with love! Perfect for your monsters."
    )
    
    print("\n📖 Demo: Fetching Challenges")
    print("-" * 70)
    
    challenges = manager.fetch_challenges(status="open")
    print(f"\nFound {len(challenges)} open challenges:")
    for challenge in challenges[:3]:  # Show first 3
        print(f"\n  #{challenge.issue_id}: {challenge.title}")
        print(f"  Challenger: @{challenge.challenger} ({challenge.challenger_pet})")
        print(f"  Reward: {challenge.reward} coins")
        print(f"  URL: {challenge.url}")
    
    print("\n📖 Demo: Fetching Food Trades")
    print("-" * 70)
    
    trades = manager.fetch_food_trades(status="available")
    print(f"\nFound {len(trades)} available food trades:")
    for trade in trades[:3]:  # Show first 3
        print(f"\n  #{trade.issue_id}: {trade.title}")
        print(f"  Seller: @{trade.seller} ({trade.farm_name})")
        print(f"  Price: {trade.price} coins/unit")
        print(f"  URL: {trade.url}")


if __name__ == "__main__":
    demo()
