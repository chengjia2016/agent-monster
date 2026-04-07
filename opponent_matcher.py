#!/usr/bin/env python3
"""
Advanced Features: Opponent Suggestions and Auto-Matching

Provides intelligent opponent matching for battles based on:
- Pet level compatibility
- Battle history
- Win/loss ratio
- Pet type synergies
- Player reputation
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json


@dataclass
class OpponentProfile:
    """Opponent profile for matching"""
    username: str
    pet_name: str
    pet_level: int
    pet_type: str
    battles_won: int = 0
    battles_lost: int = 0
    average_reward: float = 0.0
    last_battle: Optional[datetime] = None
    reputation: float = 1.0  # 1.0 = neutral
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate"""
        total = self.battles_won + self.battles_lost
        if total == 0:
            return 0.5  # Neutral if no history
        return self.battles_won / total
    
    @property
    def is_active(self) -> bool:
        """Check if player is active in last 7 days"""
        if not self.last_battle:
            return False
        return (datetime.now() - self.last_battle).days < 7
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'username': self.username,
            'pet_name': self.pet_name,
            'pet_level': self.pet_level,
            'pet_type': self.pet_type,
            'battles_won': self.battles_won,
            'battles_lost': self.battles_lost,
            'win_rate': self.win_rate,
            'average_reward': self.average_reward,
            'reputation': self.reputation,
            'is_active': self.is_active,
        }


@dataclass
class MatchScore:
    """Match quality score"""
    opponent: OpponentProfile
    total_score: float
    level_compatibility: float
    battle_history_factor: float
    reputation_factor: float
    type_synergy: float
    activity_factor: float
    reasoning: str
    
    def __repr__(self) -> str:
        return f"MatchScore({self.opponent.username}: {self.total_score:.2f}/100)"


class OpponentMatcher:
    """Intelligent opponent matching system"""
    
    # Pet type matchups (advantage matrix)
    TYPE_ADVANTAGES = {
        "fire": ["grass", "ice", "bug"],
        "water": ["fire", "ground", "rock"],
        "grass": ["water", "ground", "rock"],
        "electric": ["water", "flying"],
        "ice": ["grass", "flying", "ground", "dragon"],
        "fighting": ["normal", "ice", "rock", "dark"],
        "poison": ["grass", "fairy"],
        "ground": ["fire", "electric", "poison", "rock"],
        "flying": ["grass", "fighting", "bug"],
        "psychic": ["fighting", "poison"],
        "bug": ["grass", "psychic", "dark"],
        "rock": ["fire", "ice", "flying", "bug"],
        "ghost": ["ghost", "psychic"],
        "dragon": ["dragon"],
        "dark": ["ghost", "psychic"],
        "steel": ["ice", "rock", "fairy"],
        "fairy": ["fighting", "dragon", "dark"],
        "normal": [],
    }
    
    def __init__(self, player_profile: OpponentProfile):
        """
        Initialize matcher
        
        Args:
            player_profile: Profile of the player looking for opponents
        """
        self.player = player_profile
        self.opponent_profiles: List[OpponentProfile] = []
    
    def add_opponent(self, opponent: OpponentProfile) -> None:
        """Add potential opponent"""
        self.opponent_profiles.append(opponent)
    
    def add_opponents(self, opponents: List[OpponentProfile]) -> None:
        """Add multiple potential opponents"""
        self.opponent_profiles.extend(opponents)
    
    def calculate_level_compatibility(
        self,
        opponent: OpponentProfile,
        tolerance: int = 5,
    ) -> float:
        """
        Calculate level compatibility score (0-100)
        
        Factors:
        - Smaller level difference = higher score
        - Tolerance defines acceptable range
        """
        level_diff = abs(self.player.pet_level - opponent.pet_level)
        
        if level_diff == 0:
            return 100.0  # Perfect match
        elif level_diff <= tolerance:
            return 100.0 - (level_diff * 5)  # Linear penalty
        elif level_diff <= tolerance * 2:
            return 50.0 - (level_diff - tolerance) * 2.5  # Less favorable
        else:
            return max(0.0, 30.0 - (level_diff - tolerance * 2))  # Poor match
    
    def calculate_type_synergy(self, opponent: OpponentProfile) -> float:
        """
        Calculate type synergy score (0-100)
        
        Considers:
        - Advantage matchup (+bonus)
        - Neutral matchup (baseline)
        - Disadvantage matchup (-penalty)
        """
        player_type = self.player.pet_type.lower()
        opponent_type = opponent.pet_type.lower()
        
        score = 50.0  # Neutral baseline
        
        # Player advantages against opponent
        if player_type in self.TYPE_ADVANTAGES:
            if opponent_type in self.TYPE_ADVANTAGES[player_type]:
                score += 25.0  # Player has advantage
        
        # Opponent advantages against player
        if opponent_type in self.TYPE_ADVANTAGES:
            if player_type in self.TYPE_ADVANTAGES[opponent_type]:
                score -= 15.0  # Opponent has advantage
        
        return max(0.0, min(100.0, score))
    
    def calculate_battle_history_factor(self, opponent: OpponentProfile) -> float:
        """
        Calculate battle history factor (0-100)
        
        Factors:
        - No history = neutral (50)
        - High win rate opponent = interesting challenge (bonus)
        - Low win rate opponent = easy opponent (small bonus)
        """
        if opponent.battles_won + opponent.battles_lost == 0:
            return 50.0  # No history = neutral
        
        # Prefer close matches
        if 0.45 <= opponent.win_rate <= 0.55:
            return 100.0  # Perfect balance
        
        win_rate = opponent.win_rate
        if win_rate > 0.55:
            # Strong opponent, interesting challenge
            return 75.0 + (min(win_rate - 0.55, 0.45) * 55.5)
        else:
            # Weaker opponent, easier win
            return 50.0 + ((0.45 - win_rate) * 55.5)
    
    def calculate_reputation_factor(self, opponent: OpponentProfile) -> float:
        """
        Calculate reputation factor (0-100)
        
        Factors:
        - Good reputation = higher score (more trustworthy)
        - Bad reputation = lower score (less trustworthy)
        """
        if opponent.reputation < 0.5:
            return 30.0  # Low reputation
        elif opponent.reputation < 1.0:
            return 50.0 + (1.0 - opponent.reputation) * 50
        elif opponent.reputation == 1.0:
            return 75.0  # Neutral reputation
        else:
            # High reputation
            return 75.0 + min((opponent.reputation - 1.0) * 25, 25.0)
    
    def calculate_activity_factor(self, opponent: OpponentProfile) -> float:
        """
        Calculate activity factor (0-100)
        
        Active players = more likely to accept challenges
        """
        if not opponent.is_active:
            return 40.0  # Inactive
        
        if not opponent.last_battle:
            return 50.0  # Unknown activity
        
        days_since_battle = (datetime.now() - opponent.last_battle).days
        
        if days_since_battle == 0:
            return 100.0  # Very active
        elif days_since_battle <= 3:
            return 80.0  # Recently active
        elif days_since_battle <= 7:
            return 60.0  # Moderately active
        else:
            return 40.0  # Inactive
    
    def match_single(
        self,
        opponent: OpponentProfile,
        weights: Optional[Dict[str, float]] = None,
    ) -> MatchScore:
        """
        Calculate match score for single opponent
        
        Default weights (can be customized):
        - level: 30% (importance of level matching)
        - synergy: 20% (importance of type synergy)
        - history: 25% (importance of balanced battles)
        - reputation: 15% (importance of reputation)
        - activity: 10% (importance of activity)
        """
        if weights is None:
            weights = {
                'level': 0.30,
                'synergy': 0.20,
                'history': 0.25,
                'reputation': 0.15,
                'activity': 0.10,
            }
        
        # Calculate individual factors
        level_score = self.calculate_level_compatibility(opponent)
        synergy_score = self.calculate_type_synergy(opponent)
        history_score = self.calculate_battle_history_factor(opponent)
        reputation_score = self.calculate_reputation_factor(opponent)
        activity_score = self.calculate_activity_factor(opponent)
        
        # Calculate weighted total
        total_score = (
            level_score * weights['level'] +
            synergy_score * weights['synergy'] +
            history_score * weights['history'] +
            reputation_score * weights['reputation'] +
            activity_score * weights['activity']
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            opponent,
            level_score,
            synergy_score,
            history_score,
            reputation_score,
            activity_score,
        )
        
        return MatchScore(
            opponent=opponent,
            total_score=total_score,
            level_compatibility=level_score,
            battle_history_factor=history_score,
            reputation_factor=reputation_score,
            type_synergy=synergy_score,
            activity_factor=activity_score,
            reasoning=reasoning,
        )
    
    def find_best_matches(
        self,
        top_n: int = 5,
        min_score: float = 50.0,
        weights: Optional[Dict[str, float]] = None,
    ) -> List[MatchScore]:
        """
        Find top N best opponents
        
        Args:
            top_n: Number of top matches to return
            min_score: Minimum score threshold
            weights: Custom weight distribution
            
        Returns:
            List of sorted MatchScore objects
        """
        if not self.opponent_profiles:
            return []
        
        matches = [
            self.match_single(opponent, weights)
            for opponent in self.opponent_profiles
        ]
        
        # Filter by minimum score
        matches = [m for m in matches if m.total_score >= min_score]
        
        # Sort by score descending
        matches.sort(key=lambda m: m.total_score, reverse=True)
        
        return matches[:top_n]
    
    def print_match_report(self, match: MatchScore) -> None:
        """Print detailed match report"""
        print(f"\n{'─' * 70}")
        print(f"🎮 Match Candidate: {match.opponent.username}")
        print(f"{'─' * 70}")
        print(f"Pet: {match.opponent.pet_name} (Type: {match.opponent.pet_type}, Level: {match.opponent.pet_level})")
        print(f"\nMatch Scores:")
        print(f"  Level Compatibility: {match.level_compatibility:6.1f}/100  {'█' * int(match.level_compatibility / 5)}")
        print(f"  Type Synergy:        {match.type_synergy:6.1f}/100  {'█' * int(match.type_synergy / 5)}")
        print(f"  Battle History:      {match.battle_history_factor:6.1f}/100  {'█' * int(match.battle_history_factor / 5)}")
        print(f"  Reputation:          {match.reputation_factor:6.1f}/100  {'█' * int(match.reputation_factor / 5)}")
        print(f"  Activity Level:      {match.activity_factor:6.1f}/100  {'█' * int(match.activity_factor / 5)}")
        print(f"\n  Total Score:         {match.total_score:6.1f}/100  {'█' * int(match.total_score / 5)}")
        print(f"\nReasoning:")
        print(f"  {match.reasoning}")
    
    def _generate_reasoning(
        self,
        opponent: OpponentProfile,
        level_score: float,
        synergy_score: float,
        history_score: float,
        reputation_score: float,
        activity_score: float,
    ) -> str:
        """Generate human-readable reasoning for match quality"""
        reasons = []
        
        # Level analysis
        level_diff = abs(self.player.pet_level - opponent.pet_level)
        if level_diff == 0:
            reasons.append("Perfect level match")
        elif level_diff <= 5:
            reasons.append(f"Close level match (±{level_diff})")
        else:
            reasons.append(f"Level gap of {level_diff}")
        
        # Type synergy
        if synergy_score > 60:
            reasons.append("Good type matchup")
        elif synergy_score < 40:
            reasons.append("Disadvantageous type matchup")
        
        # Battle history
        if opponent.battles_won + opponent.battles_lost == 0:
            reasons.append("No battle history yet")
        elif opponent.win_rate > 0.6:
            reasons.append(f"Strong opponent ({opponent.win_rate:.0%} win rate)")
        elif opponent.win_rate < 0.4:
            reasons.append(f"Weaker opponent ({opponent.win_rate:.0%} win rate)")
        
        # Activity
        if opponent.is_active:
            reasons.append("Currently active")
        else:
            reasons.append("Not recently active")
        
        return " • ".join(reasons)


# ========== Example Usage ==========

def example_opponent_matching():
    """Example of opponent matching in action"""
    
    print("\n" + "=" * 70)
    print("🎯 Opponent Matching System - Example")
    print("=" * 70 + "\n")
    
    # Create player profile
    player = OpponentProfile(
        username="alice",
        pet_name="Dragonite",
        pet_level=45,
        pet_type="dragon",
        battles_won=10,
        battles_lost=3,
        average_reward=450.0,
        reputation=1.2,
        last_battle=datetime.now() - timedelta(days=1),
    )
    
    print(f"Player Profile: {player.username}")
    print(f"  Pet: {player.pet_name} (Level {player.pet_level}, Type: {player.pet_type})")
    print(f"  Record: {player.battles_won}W-{player.battles_lost}L ({player.win_rate:.0%})")
    print(f"  Reputation: {player.reputation:.1f}")
    
    # Create potential opponents
    opponents = [
        OpponentProfile(
            username="bob",
            pet_name="Mewtwo",
            pet_level=48,
            pet_type="psychic",
            battles_won=12,
            battles_lost=2,
            average_reward=500.0,
            reputation=1.3,
            last_battle=datetime.now(),
        ),
        OpponentProfile(
            username="charlie",
            pet_name="Gyarados",
            pet_level=42,
            pet_type="water",
            battles_won=5,
            battles_lost=8,
            average_reward=300.0,
            reputation=0.9,
            last_battle=datetime.now() - timedelta(days=5),
        ),
        OpponentProfile(
            username="diana",
            pet_name="Arcanine",
            pet_level=45,
            pet_type="fire",
            battles_won=8,
            battles_lost=4,
            average_reward=400.0,
            reputation=1.1,
            last_battle=datetime.now() - timedelta(days=2),
        ),
        OpponentProfile(
            username="eve",
            pet_name="Alakazam",
            pet_level=44,
            pet_type="psychic",
            battles_won=15,
            battles_lost=1,
            average_reward=550.0,
            reputation=1.4,
            last_battle=datetime.now() - timedelta(hours=1),
        ),
    ]
    
    # Initialize matcher
    matcher = OpponentMatcher(player)
    matcher.add_opponents(opponents)
    
    # Find best matches
    print(f"\n🔍 Finding best match candidates...\n")
    best_matches = matcher.find_best_matches(top_n=3)
    
    print(f"✅ Found {len(best_matches)} excellent match candidates:\n")
    
    for i, match in enumerate(best_matches, 1):
        print(f"\n{i}. {match}")
        matcher.print_match_report(match)
    
    print("\n" + "=" * 70)
    print("✓ Opponent Matching Complete")
    print("=" * 70)


if __name__ == "__main__":
    example_opponent_matching()
