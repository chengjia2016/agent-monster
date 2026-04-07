#!/usr/bin/env python3
"""
Test GitHub Issues Integration

测试挑战书和食物交易的发布、读取功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from github_issues_integration import (
    GitHubIssuesManager,
    ChallengeIssue,
    FoodTradeIssue,
)


def test_manager_initialization():
    """测试管理器初始化"""
    print("\n" + "=" * 70)
    print("TEST 1: Manager Initialization")
    print("=" * 70)
    
    manager = GitHubIssuesManager(
        owner="chengjia2016",
        repo="agent-monster"
    )
    
    print("✅ Manager initialized successfully")
    print(f"   Owner: {manager.owner}")
    print(f"   Repo: {manager.repo}")
    print(f"   API Base: {manager.api_base}")
    print(f"   Token: {'Available' if manager.token else 'Not set'}")


def test_challenge_formatting():
    """测试挑战书格式化"""
    print("\n" + "=" * 70)
    print("TEST 2: Challenge Formatting")
    print("=" * 70)
    
    manager = GitHubIssuesManager("test_owner", "test_repo")
    
    body = manager._format_challenge_body(
        challenger="alice",
        challenger_pet="Dragonite",
        challenger_level=45,
        challenge_type="duel",
        defender_pet="Mewtwo",
        reward=500.0,
        description="Epic battle time!"
    )
    
    print("📋 Challenge Body:")
    print(body)
    
    # 验证内容
    assert "alice" in body
    assert "Dragonite" in body
    assert "45" in body
    assert "Mewtwo" in body
    assert "500" in body
    print("\n✅ Challenge formatting verified")


def test_food_trade_formatting():
    """测试食物交易格式化"""
    print("\n" + "=" * 70)
    print("TEST 3: Food Trade Formatting")
    print("=" * 70)
    
    manager = GitHubIssuesManager("test_owner", "test_repo")
    
    body = manager._format_food_trade_body(
        seller="farmer_bob",
        farm_name="Sunny Fields",
        food_type="meat",
        quantity=100,
        price=50.0,
        quality="epic",
        description="Premium beef from grass-fed cattle"
    )
    
    print("📋 Food Trade Body:")
    print(body)
    
    # 验证内容
    assert "farmer_bob" in body
    assert "Sunny Fields" in body
    assert "meat" in body.lower()
    assert "100" in body
    assert "50" in body
    assert "epic" in body.lower()
    print("\n✅ Food trade formatting verified")


def test_challenge_parsing():
    """测试挑战书解析"""
    print("\n" + "=" * 70)
    print("TEST 4: Challenge Issue Parsing")
    print("=" * 70)
    
    manager = GitHubIssuesManager("test_owner", "test_repo")
    
    # 模拟 GitHub API 返回的数据
    mock_issue = {
        "number": 42,
        "title": "🎮 DUEL Challenge: Venusaur vs Blastoise",
        "body": """## 🎮 Battle Challenge

**Challenger:** @player_charlie
**Pet:** Venusaur
**Level:** 50
**Type:** DUEL
**Reward:** 300.0 coins

### Challenge Details

**Defending Pet:** Blastoise

**Description:**
Grass vs Water showdown!

### How to Accept
Reply to this issue to accept the challenge!

---
*Posted on 2026-04-07 10:30:00 UTC*
""",
        "state": "open",
        "created_at": "2026-04-07T10:30:00Z",
        "html_url": "https://github.com/chengjia2016/agent-monster/issues/42",
    }
    
    challenge = manager._parse_challenge_issue(mock_issue, "open")
    
    if challenge:
        print("✅ Challenge parsed successfully:")
        print(f"   Issue ID: {challenge.issue_id}")
        print(f"   Challenger: @{challenge.challenger}")
        print(f"   Pet: {challenge.challenger_pet}")
        print(f"   Level: {challenge.challenger_level}")
        print(f"   Type: {challenge.challenge_type}")
        print(f"   Defending Pet: {challenge.defender_pet}")
        print(f"   Reward: {challenge.reward}")
        print(f"   Status: {challenge.status}")
        
        assert challenge.issue_id == 42
        assert challenge.challenger == "player_charlie"
        assert challenge.challenger_pet == "Venusaur"
        assert challenge.challenger_level == 50
        assert challenge.challenge_type == "duel"
        assert challenge.defender_pet == "Blastoise"
        assert challenge.reward == 300.0
    else:
        print("❌ Failed to parse challenge")


def test_food_trade_parsing():
    """测试食物交易解析"""
    print("\n" + "=" * 70)
    print("TEST 5: Food Trade Issue Parsing")
    print("=" * 70)
    
    manager = GitHubIssuesManager("test_owner", "test_repo")
    
    # 模拟 GitHub API 返回的数据
    mock_issue = {
        "number": 33,
        "title": "🍖 EPIC Meat: Dragon Valley Farm - 200 units @ 25 coins",
        "body": """## 🍖 Food Trade

**Seller:** @organic_farmer
**Farm:** Dragon Valley Farm
**Food Type:** Meat
**Quality:** EPIC
**Quantity:** 200 units
**Price:** 25 coins per unit
**Total:** 5000 coins

### Product Details

Premium quality dragonmeat from heritage animals raised on the farm.

### How to Buy
Reply to this issue to make an offer or negotiate the price!

---
*Posted on 2026-04-07 15:20:00 UTC*
""",
        "state": "open",
        "created_at": "2026-04-07T15:20:00Z",
        "html_url": "https://github.com/chengjia2016/agent-monster/issues/33",
    }
    
    trade = manager._parse_food_trade_issue(mock_issue, "available")
    
    if trade:
        print("✅ Food trade parsed successfully:")
        print(f"   Issue ID: {trade.issue_id}")
        print(f"   Seller: @{trade.seller}")
        print(f"   Farm: {trade.farm_name}")
        print(f"   Food Type: {trade.food_type}")
        print(f"   Quality: {trade.quality}")
        print(f"   Quantity: {trade.quantity}")
        print(f"   Price: {trade.price}/unit")
        print(f"   Status: {trade.status}")
        
        assert trade.issue_id == 33
        assert trade.seller == "organic_farmer"
        assert trade.farm_name == "Dragon Valley Farm"
        assert trade.food_type == "meat"
        assert trade.quality == "epic"
        assert trade.quantity == 200
        assert trade.price == 25.0
    else:
        print("❌ Failed to parse food trade")


def test_data_structures():
    """测试数据类"""
    print("\n" + "=" * 70)
    print("TEST 6: Data Structures")
    print("=" * 70)
    
    # 测试 ChallengeIssue
    challenge = ChallengeIssue(
        issue_id=1,
        title="Test Challenge",
        challenger="user1",
        challenger_pet="Pikachu",
        defender_pet="Charizard",
        challenger_level=25,
        challenge_type="duel",
        reward=150.0,
        status="open",
        created_at="2026-04-07T00:00:00Z",
        body="Test body",
        url="https://github.com/test",
    )
    
    print("✅ ChallengeIssue created:")
    challenge_dict = challenge.to_dict()
    print(f"   {challenge_dict}")
    
    # 测试 FoodTradeIssue
    trade = FoodTradeIssue(
        issue_id=2,
        title="Test Trade",
        seller="farmer1",
        farm_name="Test Farm",
        food_type="vegetable",
        quantity=50,
        price=10.0,
        quality="rare",
        status="available",
        created_at="2026-04-07T00:00:00Z",
        body="Test body",
        url="https://github.com/test",
    )
    
    print("\n✅ FoodTradeIssue created:")
    trade_dict = trade.to_dict()
    print(f"   {trade_dict}")


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Agent Monster - GitHub Issues Integration Tests  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        test_manager_initialization()
        test_challenge_formatting()
        test_food_trade_formatting()
        test_challenge_parsing()
        test_food_trade_parsing()
        test_data_structures()
        
        print("\n" + "=" * 70)
        print("✅ All tests completed successfully!")
        print("=" * 70 + "\n")
        
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
