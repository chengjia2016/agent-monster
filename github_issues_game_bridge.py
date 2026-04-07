#!/usr/bin/env python3
"""
GitHub Issues Integration with Unified Game Systems Manager

Bridges GitHub Issues (for player interaction) with the main game system.
Enables:
- Posting and tracking battle challenges
- Posting and tracking food trades
- Auto-matching opponents
- Synchronizing Issue state with game state
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
import threading
import time

from github_issues_integration import (
    GitHubIssuesManager,
    ChallengeIssue,
    FoodTradeIssue,
)

# Try to import game manager, but allow the bridge to work without it
try:
    from unified_game_systems_manager import UnifiedGameSystemsManager
    GAME_MANAGER_AVAILABLE = True
except ImportError:
    GAME_MANAGER_AVAILABLE = False
    UnifiedGameSystemsManager = None


class GitHubIssuesGameBridge:
    """
    Bridges GitHub Issues with the main game system.
    
    Responsibilities:
    1. Post player challenges and trades to GitHub Issues
    2. Fetch and process challenges/trades from GitHub
    3. Auto-match opponents from GitHub Issues
    4. Synchronize issue state with game state
    5. Update issue status when battles complete
    """
    
    def __init__(
        self,
        owner: str,
        repo: str,
        cache_dir: Path = None,
        judge_server_url: str = "http://localhost:10000",
    ):
        """
        Initialize the GitHub Issues Game Bridge.
        
        Args:
            owner: GitHub repository owner
            repo: GitHub repository name
            cache_dir: Cache directory for local storage
            judge_server_url: Judge Server URL
        """
        self.github_manager = GitHubIssuesManager(owner, repo)
        self.game_manager = None
        
        # Only initialize game manager if available
        if GAME_MANAGER_AVAILABLE and UnifiedGameSystemsManager:
            try:
                self.game_manager = UnifiedGameSystemsManager(
                    cache_dir=cache_dir,
                    judge_server_url=judge_server_url,
                )
            except Exception as e:
                print(f"⚠️  Game manager unavailable: {e}")
                print(f"   Bridge will work in GitHub Issues mode only")
        else:
            print(f"⚠️  Game manager not available, using GitHub Issues mode only")
        
        self.owner = owner
        self.repo = repo
        
        # Cache for matching
        self.challenge_cache: Dict[int, Dict] = {}
        self.trade_cache: Dict[int, Dict] = {}
        self.last_sync: Optional[datetime] = None
        self.lock = threading.RLock()
        
        print(f"✓ GitHub Issues Game Bridge initialized for {owner}/{repo}")
    
    # ========== Challenge Management ==========
    
    def post_challenge_from_battle(
        self,
        challenger: str,
        challenger_pet: str,
        challenger_level: int,
        defender_pet: Optional[str] = None,
        challenge_type: str = "duel",
        reward: float = 100.0,
        description: str = "",
    ) -> Optional[Dict]:
        """
        Post a challenge to GitHub Issues from a battle request.
        
        Args:
            challenger: Challenger username
            challenger_pet: Challenger's pet name
            challenger_level: Challenger pet's level
            defender_pet: Defender's pet name (optional for open challenges)
            challenge_type: Type of challenge (duel, tournament, team_battle)
            reward: Reward in coins
            description: Challenge description
            
        Returns:
            Challenge Issue data or None on error
        """
        try:
            # Post to GitHub Issues
            issue = self.github_manager.post_challenge(
                challenger=f"@{challenger}",
                challenger_pet=challenger_pet,
                challenger_level=challenger_level,
                challenge_type=challenge_type,
                defender_pet=defender_pet,
                reward=reward,
                description=description,
            )
            
            if issue:
                print(f"✅ Challenge posted to GitHub Issues (Issue #{issue.get('number')})")
                print(f"   URL: {issue.get('html_url')}")
                
                # Cache the challenge
                with self.lock:
                    self.challenge_cache[issue.get('number')] = {
                        'challenger': challenger,
                        'challenger_pet': challenger_pet,
                        'challenge_type': challenge_type,
                        'issue_id': issue.get('number'),
                        'url': issue.get('html_url'),
                        'status': 'open',
                        'created_at': datetime.now(),
                    }
                
                return issue
            
        except Exception as e:
            print(f"❌ Failed to post challenge: {e}")
        
        return None
    
    def fetch_and_match_challenge(
        self,
        defender: str,
        defender_pet: str,
        defender_level: int,
    ) -> Optional[Dict]:
        """
        Fetch challenges from GitHub and find a suitable match.
        
        Args:
            defender: Defender username
            defender_pet: Defender's pet name
            defender_level: Defender pet's level
            
        Returns:
            Matching challenge or None if no suitable match found
        """
        try:
            # Fetch all open challenges
            challenges = self.github_manager.fetch_challenges()
            
            print(f"🔍 Found {len(challenges)} challenges on GitHub")
            
            best_match = None
            
            for challenge in challenges:
                # Skip already accepted challenges
                if challenge.get('status') != 'open':
                    continue
                
                # Check if it's an open challenge (no specific defender)
                if challenge.get('defender_pet'):
                    # Only consider if defender matches
                    if challenge['defender_pet'].lower() != defender_pet.lower():
                        continue
                
                # Level matching (within 10 levels)
                level_diff = abs(challenge['challenger_level'] - defender_level)
                if level_diff > 10:
                    continue
                
                # This is a good match
                best_match = challenge
                break
            
            if best_match:
                print(f"✅ Found matching challenge from {best_match['challenger']}")
                print(f"   Challenge: {best_match['challenger_pet']} vs {best_match['defender_pet'] or defender_pet}")
                print(f"   Reward: {best_match['reward']} coins")
                return best_match
            else:
                print("❌ No suitable challenge matches found")
        
        except Exception as e:
            print(f"❌ Failed to fetch challenges: {e}")
        
        return None
    
    def accept_challenge(
        self,
        issue_id: int,
        defender: str,
        defender_pet: str,
    ) -> bool:
        """
        Accept a challenge and update its status.
        
        Args:
            issue_id: GitHub Issue ID
            defender: Defender username
            defender_pet: Defender's pet name
            
        Returns:
            True if accepted successfully, False otherwise
        """
        try:
            # Add acceptance comment
            comment = f"Accepted by @{defender} with {defender_pet}!"
            self.github_manager.add_comment_to_issue(issue_id, comment)
            
            # Update issue status to "accepted"
            self.github_manager.update_challenge_status(issue_id, "accepted")
            
            print(f"✅ Challenge #{issue_id} accepted!")
            
            # Update cache
            with self.lock:
                if issue_id in self.challenge_cache:
                    self.challenge_cache[issue_id]['status'] = 'accepted'
                    self.challenge_cache[issue_id]['defender'] = defender
                    self.challenge_cache[issue_id]['defender_pet'] = defender_pet
            
            return True
        
        except Exception as e:
            print(f"❌ Failed to accept challenge: {e}")
        
        return False
    
    def complete_challenge(
        self,
        issue_id: int,
        winner: str,
        winner_pet: str,
        loser: str,
        loser_pet: str,
    ) -> bool:
        """
        Mark a challenge as completed after battle.
        
        Args:
            issue_id: GitHub Issue ID
            winner: Winner username
            winner_pet: Winner's pet name
            loser: Loser username
            loser_pet: Loser's pet name
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            # Add result comment
            result = f"""
🏆 **Battle Result**

**Winner:** @{winner} ({winner_pet})
**Loser:** @{loser} ({loser_pet})

Battle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
            self.github_manager.add_comment_to_issue(issue_id, result)
            
            # Update issue status to "completed"
            self.github_manager.update_challenge_status(issue_id, "completed")
            
            print(f"✅ Challenge #{issue_id} marked as completed!")
            
            # Update cache
            with self.lock:
                if issue_id in self.challenge_cache:
                    self.challenge_cache[issue_id]['status'] = 'completed'
                    self.challenge_cache[issue_id]['winner'] = winner
                    self.challenge_cache[issue_id]['loser'] = loser
            
            return True
        
        except Exception as e:
            print(f"❌ Failed to complete challenge: {e}")
        
        return False
    
    # ========== Food Trade Management ==========
    
    def post_food_trade(
        self,
        seller: str,
        farm_name: str,
        food_type: str,
        quantity: int,
        price: float,
        quality: str = "common",
        description: str = "",
    ) -> Optional[Dict]:
        """
        Post a food trade to GitHub Issues.
        
        Args:
            seller: Seller username
            farm_name: Farm name
            food_type: Type of food (vegetable, meat, fruit, special)
            quantity: Quantity available
            price: Price per unit in coins
            quality: Quality tier (common, rare, epic, legendary)
            description: Product description
            
        Returns:
            Food Trade Issue data or None on error
        """
        try:
            # Post to GitHub Issues
            issue = self.github_manager.post_food_trade(
                seller=f"@{seller}",
                farm_name=farm_name,
                food_type=food_type,
                quantity=quantity,
                price=price,
                quality=quality,
                description=description,
            )
            
            if issue:
                print(f"✅ Food trade posted to GitHub Issues (Issue #{issue.get('number')})")
                print(f"   URL: {issue.get('html_url')}")
                
                # Cache the trade
                with self.lock:
                    self.trade_cache[issue.get('number')] = {
                        'seller': seller,
                        'farm_name': farm_name,
                        'food_type': food_type,
                        'quantity': quantity,
                        'price': price,
                        'quality': quality,
                        'issue_id': issue.get('number'),
                        'url': issue.get('html_url'),
                        'status': 'available',
                        'created_at': datetime.now(),
                    }
                
                return issue
            
        except Exception as e:
            print(f"❌ Failed to post food trade: {e}")
        
        return None
    
    def fetch_available_trades(
        self,
        food_type: Optional[str] = None,
        max_price: Optional[float] = None,
        min_quality: str = "common",
    ) -> List[Dict]:
        """
        Fetch available food trades from GitHub.
        
        Args:
            food_type: Filter by food type (optional)
            max_price: Maximum price per unit (optional)
            min_quality: Minimum quality tier
            
        Returns:
            List of matching food trades
        """
        try:
            # Fetch all available trades
            trades = self.github_manager.fetch_food_trades()
            
            print(f"🔍 Found {len(trades)} food trades on GitHub")
            
            # Filter trades
            quality_levels = {"common": 0, "rare": 1, "epic": 2, "legendary": 3}
            min_quality_level = quality_levels.get(min_quality.lower(), 0)
            
            filtered_trades = []
            
            for trade in trades:
                # Skip unavailable trades
                if trade.get('status') != 'available':
                    continue
                
                # Filter by food type if specified
                if food_type and trade.get('food_type', '').lower() != food_type.lower():
                    continue
                
                # Filter by max price if specified
                if max_price and trade.get('price', 0) > max_price:
                    continue
                
                # Filter by minimum quality
                trade_quality_level = quality_levels.get(
                    trade.get('quality', 'common').lower(), 0
                )
                if trade_quality_level < min_quality_level:
                    continue
                
                filtered_trades.append(trade)
            
            print(f"✅ Found {len(filtered_trades)} matching trades")
            return filtered_trades
        
        except Exception as e:
            print(f"❌ Failed to fetch food trades: {e}")
        
        return []
    
    def offer_on_trade(
        self,
        issue_id: int,
        buyer: str,
        quantity: int,
        offered_price: float,
    ) -> bool:
        """
        Make an offer on a food trade.
        
        Args:
            issue_id: GitHub Issue ID
            buyer: Buyer username
            quantity: Quantity to buy
            offered_price: Offered price per unit
            
        Returns:
            True if offer posted successfully, False otherwise
        """
        try:
            # Add offer comment
            comment = f"""
💰 **Trade Offer**

**Buyer:** @{buyer}
**Quantity:** {quantity} units
**Offered Price:** {offered_price} coins/unit
**Total:** {quantity * offered_price} coins

Offer made at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
            self.github_manager.add_comment_to_issue(issue_id, comment)
            
            print(f"✅ Offer posted to trade Issue #{issue_id}!")
            
            return True
        
        except Exception as e:
            print(f"❌ Failed to post offer: {e}")
        
        return False
    
    def complete_trade(
        self,
        issue_id: int,
        buyer: str,
        seller: str,
        quantity: int,
        final_price: float,
    ) -> bool:
        """
        Mark a food trade as completed.
        
        Args:
            issue_id: GitHub Issue ID
            buyer: Buyer username
            seller: Seller username
            quantity: Quantity sold
            final_price: Final price per unit
            
        Returns:
            True if updated successfully, False otherwise
        """
        try:
            # Add completion comment
            result = f"""
✅ **Trade Completed**

**Buyer:** @{buyer}
**Seller:** @{seller}
**Quantity:** {quantity} units
**Final Price:** {final_price} coins/unit
**Total:** {quantity * final_price} coins

Trade completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
            self.github_manager.add_comment_to_issue(issue_id, result)
            
            # Update issue status to "sold"
            self.github_manager.update_food_trade_status(issue_id, "sold")
            
            print(f"✅ Trade Issue #{issue_id} marked as completed!")
            
            # Update cache
            with self.lock:
                if issue_id in self.trade_cache:
                    self.trade_cache[issue_id]['status'] = 'sold'
                    self.trade_cache[issue_id]['buyer'] = buyer
                    self.trade_cache[issue_id]['final_price'] = final_price
            
            return True
        
        except Exception as e:
            print(f"❌ Failed to complete trade: {e}")
        
        return False
    
    # ========== Statistics ==========
    
    def get_player_challenges(self, player: str) -> List[Dict]:
        """Get all challenges by a player."""
        try:
            challenges = self.github_manager.fetch_challenges()
            return [c for c in challenges if c.get('challenger', '').lower() == player.lower()]
        except Exception as e:
            print(f"❌ Failed to fetch player challenges: {e}")
            return []
    
    def get_player_trades(self, player: str) -> List[Dict]:
        """Get all trades by a player."""
        try:
            trades = self.github_manager.fetch_food_trades()
            return [t for t in trades if t.get('seller', '').lower() == player.lower()]
        except Exception as e:
            print(f"❌ Failed to fetch player trades: {e}")
            return []
    
    def print_statistics(self) -> None:
        """Print game bridge statistics."""
        print("\n" + "=" * 70)
        print("📊 GitHub Issues Game Bridge Statistics")
        print("=" * 70)
        
        try:
            # Fetch challenges and trades
            challenges = self.github_manager.fetch_challenges()
            trades = self.github_manager.fetch_food_trades()
            
            # Challenge stats
            open_challenges = [c for c in challenges if c.get('status') == 'open']
            accepted_challenges = [c for c in challenges if c.get('status') == 'accepted']
            completed_challenges = [c for c in challenges if c.get('status') == 'completed']
            
            print(f"\n🎮 Battle Challenges:")
            print(f"   Total: {len(challenges)}")
            print(f"   Open: {len(open_challenges)}")
            print(f"   Accepted: {len(accepted_challenges)}")
            print(f"   Completed: {len(completed_challenges)}")
            
            if completed_challenges:
                total_rewards = sum(c.get('reward', 0) for c in completed_challenges)
                print(f"   Total Rewards Offered: {total_rewards} coins")
            
            # Trade stats
            available_trades = [t for t in trades if t.get('status') == 'available']
            negotiating_trades = [t for t in trades if t.get('status') == 'negotiating']
            sold_trades = [t for t in trades if t.get('status') == 'sold']
            
            print(f"\n🍖 Food Trades:")
            print(f"   Total: {len(trades)}")
            print(f"   Available: {len(available_trades)}")
            print(f"   Negotiating: {len(negotiating_trades)}")
            print(f"   Sold: {len(sold_trades)}")
            
            if sold_trades:
                total_volume = sum(t.get('quantity', 0) for t in sold_trades)
                total_value = sum(t.get('quantity', 0) * t.get('final_price', 0) 
                                for t in sold_trades if 'final_price' in t)
                print(f"   Total Volume Sold: {total_volume} units")
                if total_value > 0:
                    print(f"   Total Value Traded: {total_value} coins")
            
            print("\n" + "=" * 70)
        
        except Exception as e:
            print(f"❌ Failed to compute statistics: {e}")


# ========== Example Usage ==========

def example_usage():
    """Example usage of GitHub Issues Game Bridge."""
    
    print("\n" + "=" * 70)
    print("🎮 GitHub Issues Game Bridge - Example Usage")
    print("=" * 70 + "\n")
    
    # Initialize bridge
    bridge = GitHubIssuesGameBridge("chengjia2016", "agent-monster")
    
    # Example 1: Post a challenge
    print("\n1️⃣  Posting a Challenge")
    print("-" * 70)
    challenge = bridge.post_challenge_from_battle(
        challenger="alice",
        challenger_pet="Dragonite",
        challenger_level=45,
        defender_pet="Mewtwo",
        challenge_type="duel",
        reward=500.0,
        description="Epic battle time!",
    )
    
    if challenge:
        challenge_id = challenge.get('number')
        print(f"\n✅ Challenge posted successfully (Issue #{challenge_id})")
    
    # Example 2: Fetch challenges and find a match
    print("\n2️⃣  Finding a Challenge Match")
    print("-" * 70)
    match = bridge.fetch_and_match_challenge(
        defender="bob",
        defender_pet="Mewtwo",
        defender_level=47,
    )
    
    # Example 3: Post a food trade
    print("\n3️⃣  Posting a Food Trade")
    print("-" * 70)
    trade = bridge.post_food_trade(
        seller="farmer_charlie",
        farm_name="Sunny Valley Farm",
        food_type="meat",
        quantity=100,
        price=50.0,
        quality="epic",
        description="Premium beef from grass-fed cattle",
    )
    
    if trade:
        trade_id = trade.get('number')
        print(f"\n✅ Food trade posted successfully (Issue #{trade_id})")
    
    # Example 4: Fetch available trades
    print("\n4️⃣  Finding Available Trades")
    print("-" * 70)
    available = bridge.fetch_available_trades(food_type="meat", max_price=60.0)
    
    if available:
        print(f"\nFound {len(available)} available meat trades:")
        for trade in available:
            print(f"  - {trade['farm_name']}: {trade['quantity']} units @ {trade['price']}/unit")
    
    # Example 5: Print statistics
    print("\n5️⃣  Statistics")
    print("-" * 70)
    bridge.print_statistics()


if __name__ == "__main__":
    example_usage()
