#!/usr/bin/env python3
"""
Integration test for Judge Server Phase 1.2 APIs
Tests farm, cookie, egg, and shop endpoints
"""

import sys
sys.path.insert(0, '/root/pet/agent-monster-pet')

from judge_server_client import JudgeServerClient, get_judge_server_client

def test_farm_operations():
    """Test farm CRUD operations"""
    print("\n=== Testing Farm Operations ===")
    client = get_judge_server_client()
    
    # Create farm
    farm = client.create_farm("testuser", "test-repo", "https://github.com/testuser/test-repo")
    if farm:
        print(f"✓ Created farm: {farm}")
        farm_id = farm.get("id")
        
        # Get farm
        farm_data = client.get_farm(farm_id)
        print(f"✓ Retrieved farm: {farm_data}")
        
        # Add food
        food = client.add_food_to_farm(farm_id, "food1", "cookie", 10, emoji="🍪")
        print(f"✓ Added food: {food}")
        
        # Get statistics
        stats = client.get_farm_statistics(farm_id)
        print(f"✓ Farm statistics: {stats}")
        
        return True
    else:
        print("✗ Failed to create farm")
        return False

def test_cookie_operations():
    """Test cookie operations"""
    print("\n=== Testing Cookie Operations ===")
    client = get_judge_server_client()
    
    # Register cookie
    cookie = client.register_cookie("0x1234567890abcdef", "cookie", emoji="🍪", generator_id="gen1")
    if cookie:
        print(f"✓ Registered cookie: {cookie}")
        
        # Claim cookie
        claim = client.claim_cookie("0x1234567890abcdef", "player1", exp_reward=10, energy_reward=5)
        print(f"✓ Claimed cookie: {claim}")
        
        # Get statistics
        stats = client.get_cookie_statistics()
        print(f"✓ Cookie statistics: {stats}")
        
        # Scan cookies
        scan = client.scan_cookies("player1")
        print(f"✓ Scanned cookies: {scan}")
        
        return True
    else:
        print("✗ Failed to register cookie")
        return False

def test_egg_operations():
    """Test egg operations"""
    print("\n=== Testing Egg Operations ===")
    client = get_judge_server_client()
    
    # Create egg
    egg = client.create_egg("egg001", "testuser", incubation_hours=72)
    if egg:
        print(f"✓ Created egg: {egg}")
        egg_id = egg.get("egg_id")
        
        # Get egg
        egg_data = client.get_egg(egg_id)
        print(f"✓ Retrieved egg: {egg_data}")
        
        # Get statistics
        stats = client.get_egg_statistics()
        print(f"✓ Egg statistics: {stats}")
        
        return True
    else:
        print("✗ Failed to create egg")
        return False

def test_shop_operations():
    """Test shop operations"""
    print("\n=== Testing Shop Operations ===")
    client = get_judge_server_client()
    
    # List items
    items = client.list_shop_items()
    print(f"✓ Listed shop items: {len(items)} items found")
    
    # Get statistics
    stats = client.get_shop_statistics()
    print(f"✓ Shop statistics: {stats}")
    
    return True

def test_phase_12_endpoints():
    """Test all Phase 1.2 endpoints"""
    print("\n" + "=" * 60)
    print("Phase 1.2 Endpoint Summary")
    print("=" * 60)
    
    client = get_judge_server_client()
    endpoints = {
        "Farm": [
            "POST /api/farms/create - CreateFarm",
            "GET /api/farms/:id - GetFarm",
            "GET /api/farms/search - SearchFarms",
            "POST /api/farms/:id/foods - AddFoodToFarm",
            "POST /api/farms/:id/foods/consume - ConsumeFood",
            "GET /api/farms/:id/statistics - GetFarmStatistics",
            "DELETE /api/farms/:id - DeleteFarm",
        ],
        "Cookie": [
            "POST /api/cookies/register - RegisterCookie",
            "POST /api/cookies/claim - ClaimCookie",
            "GET /api/cookies/statistics - GetCookieStatistics",
            "GET /api/cookies/scan - ScanCookies",
        ],
        "Egg": [
            "POST /api/eggs/create - CreateEgg",
            "GET /api/eggs/:id - GetEgg",
            "POST /api/eggs/:id/hatch - HatchEgg",
            "GET /api/eggs/statistics - GetEggStatistics",
        ],
        "Shop": [
            "GET /api/shop/items - ListShopItems",
            "POST /api/shop/buy - BuyItem",
            "GET /api/shop/statistics - GetShopStatistics",
            "GET /api/shop/transactions - GetTransactionHistory",
        ],
    }
    
    total = 0
    for system, ep_list in endpoints.items():
        print(f"\n{system} ({len(ep_list)} endpoints):")
        for ep in ep_list:
            print(f"  • {ep}")
            total += 1
    
    print(f"\nTotal endpoints: {total}")
    return total

def test_integration():
    """Run all integration tests"""
    print("Starting Judge Server Phase 1.2 Integration Tests")
    print("=" * 60)
    
    # Check health
    client = get_judge_server_client()
    if client.health_check():
        print("✓ Judge Server is healthy")
    else:
        print("⚠ Judge Server health check failed (might be offline)")
    
    # Show endpoints
    test_phase_12_endpoints()
    
    # Run tests
    results = []
    try:
        results.append(("Farm Operations", test_farm_operations()))
    except Exception as e:
        print(f"✗ Farm operations failed: {e}")
        results.append(("Farm Operations", False))
    
    try:
        results.append(("Cookie Operations", test_cookie_operations()))
    except Exception as e:
        print(f"✗ Cookie operations failed: {e}")
        results.append(("Cookie Operations", False))
    
    try:
        results.append(("Egg Operations", test_egg_operations()))
    except Exception as e:
        print(f"✗ Egg operations failed: {e}")
        results.append(("Egg Operations", False))
    
    try:
        results.append(("Shop Operations", test_shop_operations()))
    except Exception as e:
        print(f"✗ Shop operations failed: {e}")
        results.append(("Shop Operations", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    return passed == total

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
