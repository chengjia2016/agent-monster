#!/usr/bin/env python3
"""
Agent Monster - GitHub Issues Interactive CLI

交互式命令行工具，支持：
- 自动模式：自动发布和读取 Issues
- 手动模式：用户逐个确认操作
- 菜单驱动：易用的菜单界面
"""

import sys
import json
from pathlib import Path
from typing import Optional, Dict

try:
    from github_issues_integration import (
        GitHubIssuesManager,
        ChallengeIssue,
        FoodTradeIssue,
    )
except ImportError:
    print("❌ Error: Could not import github_issues_integration")
    sys.exit(1)


class GitHubIssuesCLI:
    """GitHub Issues 交互式 CLI"""
    
    def __init__(self, owner: str, repo: str, auto_mode: bool = False):
        """
        初始化 CLI
        
        参数:
        - owner: GitHub 所有者
        - repo: 仓库名
        - auto_mode: 自动模式 (True) 或手动模式 (False)
        """
        self.manager = GitHubIssuesManager(owner, repo)
        self.auto_mode = auto_mode
        self.owner = owner
        self.repo = repo
    
    def print_header(self, title: str) -> None:
        """打印标题"""
        print(f"\n{'═' * 70}")
        print(f"║ {title.center(66)} ║")
        print(f"{'═' * 70}\n")
    
    def print_menu(self, title: str, options: Dict[str, str]) -> str:
        """打印菜单并获取用户选择"""
        print(f"\n{title}")
        print("-" * 50)
        
        for key, desc in options.items():
            print(f"  {key}: {desc}")
        
        while True:
            choice = input("\n👉 Select option: ").strip().lower()
            if choice in options:
                return choice
            print("❌ Invalid choice, please try again")
    
    def post_challenge_interactive(self) -> None:
        """交互式发布挑战"""
        self.print_header("🎮 Post Battle Challenge")
        
        # 收集信息
        challenger = input("Your GitHub username: ").strip()
        challenger_pet = input("Your pet name: ").strip()
        
        while True:
            try:
                challenger_level = int(input("Your pet level: "))
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        print("\nChallenge type:")
        challenge_type = self.print_menu(
            "Select challenge type:",
            {
                "1": "Duel (1v1)",
                "2": "Tournament (1v1v1+)",
                "3": "Team Battle (Team vs Team)",
            }
        )
        challenge_type_map = {"1": "duel", "2": "tournament", "3": "team_battle"}
        challenge_type = challenge_type_map[challenge_type]
        
        defender_pet = input("Target pet name (press Enter for open challenge): ").strip()
        defender_pet = defender_pet if defender_pet else None
        
        while True:
            try:
                reward = float(input("Reward (coins): "))
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        description = input("Description (optional): ").strip()
        description = description if description else None
        
        # 确认
        print("\n📋 Challenge Preview:")
        print(f"  Challenger: {challenger}")
        print(f"  Pet: {challenger_pet} (Level {challenger_level})")
        print(f"  Type: {challenge_type}")
        print(f"  Defending Pet: {defender_pet or 'Open'}")
        print(f"  Reward: {reward} coins")
        
        if not self.auto_mode:
            confirm = input("\nConfirm? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Challenge cancelled")
                return
        
        # 发布
        issue_id = self.manager.post_challenge(
            challenger=challenger,
            challenger_pet=challenger_pet,
            challenger_level=challenger_level,
            challenge_type=challenge_type,
            defender_pet=defender_pet,
            reward=reward,
            description=description,
        )
        
        if issue_id:
            print(f"\n✅ Challenge posted successfully!")
            print(f"   Issue #: {issue_id}")
    
    def post_food_trade_interactive(self) -> None:
        """交互式发布食物交易"""
        self.print_header("🍖 Post Food Trade")
        
        # 收集信息
        seller = input("Your GitHub username: ").strip()
        farm_name = input("Farm name: ").strip()
        
        print("\nFood type:")
        food_choice = self.print_menu(
            "Select food type:",
            {
                "1": "Vegetable 🥬",
                "2": "Meat 🥩",
                "3": "Fruit 🍎",
                "4": "Special ⭐",
            }
        )
        food_type_map = {"1": "vegetable", "2": "meat", "3": "fruit", "4": "special"}
        food_type = food_type_map[food_choice]
        
        while True:
            try:
                quantity = int(input("Quantity (units): "))
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        while True:
            try:
                price = float(input("Price (coins per unit): "))
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        print("\nQuality:")
        quality_choice = self.print_menu(
            "Select quality:",
            {
                "1": "Common",
                "2": "Rare",
                "3": "Epic",
                "4": "Legendary",
            }
        )
        quality_map = {"1": "common", "2": "rare", "3": "epic", "4": "legendary"}
        quality = quality_map[quality_choice]
        
        description = input("Description (optional): ").strip()
        description = description if description else None
        
        # 确认
        total_price = quantity * price
        print("\n📋 Trade Preview:")
        print(f"  Seller: {seller}")
        print(f"  Farm: {farm_name}")
        print(f"  Food: {food_type.title()} ({quality.upper()})")
        print(f"  Quantity: {quantity} units @ {price} coins/unit")
        print(f"  Total: {total_price} coins")
        
        if not self.auto_mode:
            confirm = input("\nConfirm? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Trade cancelled")
                return
        
        # 发布
        issue_id = self.manager.post_food_trade(
            seller=seller,
            farm_name=farm_name,
            food_type=food_type,
            quantity=quantity,
            price=price,
            quality=quality,
            description=description,
        )
        
        if issue_id:
            print(f"\n✅ Trade posted successfully!")
            print(f"   Issue #: {issue_id}")
    
    def view_challenges(self) -> None:
        """查看挑战列表"""
        self.print_header("🎮 Active Challenges")
        
        print("Fetching challenges...")
        challenges = self.manager.fetch_challenges(status="open")
        
        if not challenges:
            print("❌ No challenges found")
            return
        
        print(f"✅ Found {len(challenges)} challenges:\n")
        
        for i, challenge in enumerate(challenges, 1):
            print(f"{i}. #{challenge.issue_id} - {challenge.title}")
            print(f"   Challenger: @{challenge.challenger} ({challenge.challenger_pet})")
            print(f"   Level: {challenge.challenger_level} | Type: {challenge.challenge_type}")
            print(f"   Reward: {challenge.reward} coins")
            print(f"   URL: {challenge.url}\n")
            
            if i >= 10:  # 显示最多 10 个
                print(f"... and {len(challenges) - 10} more")
                break
    
    def view_food_trades(self) -> None:
        """查看食物交易列表"""
        self.print_header("🍖 Available Food Trades")
        
        print("Fetching food trades...")
        trades = self.manager.fetch_food_trades(status="available")
        
        if not trades:
            print("❌ No food trades found")
            return
        
        print(f"✅ Found {len(trades)} food trades:\n")
        
        for i, trade in enumerate(trades, 1):
            print(f"{i}. #{trade.issue_id} - {trade.title}")
            print(f"   Seller: @{trade.seller} ({trade.farm_name})")
            print(f"   Quality: {trade.quality.upper()} | Food: {trade.food_type.title()}")
            print(f"   Price: {trade.price} coins/unit (Total: {trade.quantity * trade.price})")
            print(f"   URL: {trade.url}\n")
            
            if i >= 10:  # 显示最多 10 个
                print(f"... and {len(trades) - 10} more")
                break
    
    def accept_challenge_interactive(self) -> None:
        """接受挑战"""
        self.print_header("⚔️ Accept Challenge")
        
        issue_id_str = input("Enter challenge issue #: ").strip()
        
        try:
            issue_id = int(issue_id_str)
        except ValueError:
            print("❌ Invalid issue number")
            return
        
        username = input("Your GitHub username: ").strip()
        pet_name = input("Your pet name: ").strip()
        
        comment = f"""
## ⚔️ Challenge Accepted!

**Defender:** @{username}
**Pet:** {pet_name}

Let's battle! 🎮
"""
        
        print("\n📋 Acceptance Preview:")
        print(comment)
        
        if not self.auto_mode:
            confirm = input("\nConfirm? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Cancelled")
                return
        
        if self.manager.add_comment(issue_id, comment):
            print(f"\n✅ Challenge accepted!")
            self.manager.update_issue_status(issue_id, "accepted")
        else:
            print(f"\n❌ Failed to accept challenge")
    
    def offer_food_trade_interactive(self) -> None:
        """对食物交易进行报价"""
        self.print_header("💰 Make an Offer")
        
        issue_id_str = input("Enter food trade issue #: ").strip()
        
        try:
            issue_id = int(issue_id_str)
        except ValueError:
            print("❌ Invalid issue number")
            return
        
        username = input("Your GitHub username: ").strip()
        
        while True:
            try:
                offered_price = float(input("Offered price per unit (coins): "))
                break
            except ValueError:
                print("❌ Please enter a valid number")
        
        quantity = input("Quantity interested (press Enter for all): ").strip()
        
        comment = f"""
## 💰 Offer Made

**Buyer:** @{username}
**Offered Price:** {offered_price} coins/unit
**Quantity:** {quantity or 'All units'}

Let's negotiate! 💬
"""
        
        print("\n📋 Offer Preview:")
        print(comment)
        
        if not self.auto_mode:
            confirm = input("\nConfirm? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Cancelled")
                return
        
        if self.manager.add_comment(issue_id, comment):
            print(f"\n✅ Offer posted!")
        else:
            print(f"\n❌ Failed to post offer")
    
    def main_menu(self) -> None:
        """主菜单"""
        while True:
            mode_str = "[AUTO]" if self.auto_mode else "[MANUAL]"
            self.print_header(f"🎮 Agent Monster - GitHub Issues {mode_str}")
            
            choice = self.print_menu(
                "Main Menu",
                {
                    "1": "Post Battle Challenge",
                    "2": "Post Food Trade",
                    "3": "View Active Challenges",
                    "4": "View Food Trades",
                    "5": "Accept Challenge",
                    "6": "Make Food Offer",
                    "7": "Toggle Auto/Manual Mode",
                    "8": "Exit",
                }
            )
            
            if choice == "1":
                self.post_challenge_interactive()
            elif choice == "2":
                self.post_food_trade_interactive()
            elif choice == "3":
                self.view_challenges()
            elif choice == "4":
                self.view_food_trades()
            elif choice == "5":
                self.accept_challenge_interactive()
            elif choice == "6":
                self.offer_food_trade_interactive()
            elif choice == "7":
                self.auto_mode = not self.auto_mode
                print(f"\n✅ Mode switched to: {'AUTO' if self.auto_mode else 'MANUAL'}")
            elif choice == "8":
                print("\n👋 Goodbye!")
                break
            
            input("\n📌 Press Enter to continue...")


def main():
    """主函数"""
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # 获取仓库信息
    owner = "chengjia2016"
    repo = "agent-monster"
    
    # 默认手动模式
    auto_mode = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        auto_mode = True
    
    cli = GitHubIssuesCLI(owner, repo, auto_mode=auto_mode)
    cli.main_menu()


if __name__ == "__main__":
    main()
