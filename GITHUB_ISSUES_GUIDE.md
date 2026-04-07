# 🎮 GitHub Issues Integration Guide

## Overview

The GitHub Issues Integration system transforms GitHub Issues into a dynamic player interaction platform for Agent Monster, enabling:

- **Battle Challenges** - Players can issue PvP battle challenges
- **Food Trades** - Farmers can trade food items
- **Auto & Manual Modes** - Flexible operation modes for different use cases

## Quick Start

### Setup

1. **Set GitHub Token** (required for API access):
```bash
export GITHUB_TOKEN="your_github_token_here"
```

2. **Run CLI**:
```bash
# Manual mode (confirm each action)
python3 github_issues_cli.py

# Auto mode (automatic posting/reading)
python3 github_issues_cli.py --auto
```

### Basic Usage

#### Post a Battle Challenge

```python
from github_issues_cli import GitHubIssuesCLI

cli = GitHubIssuesCLI("chengjia2016", "agent-monster", auto_mode=False)
cli.post_challenge_interactive()
```

#### Post a Food Trade

```python
cli = GitHubIssuesCLI("chengjia2016", "agent-monster", auto_mode=False)
cli.post_food_trade_interactive()
```

#### View Battle Challenges

```python
challenges = cli.manager.fetch_challenges()
for challenge in challenges:
    print(f"Challenge by {challenge['challenger']} - {challenge['challenge_type']} battle")
```

#### View Food Trades

```python
trades = cli.manager.fetch_food_trades()
for trade in trades:
    print(f"Food trade from {trade['seller']} - {trade['food_type']}")
```

## Features

### 1. Battle Challenges 🎮

**Issue Labels:** `🎮 Battle Challenge`, `Status: Open/Accepted/Completed`

**Challenge Types:**
- **Duel (1v1)** - One-on-one battle
- **Tournament (1v1v1+)** - Multi-player tournament
- **Team Battle** - Team vs Team battle

**Challenge Information Captured:**
- Challenger username and pet name
- Pet level
- Challenge type and target opponent
- Reward amount (in coins)
- Status (open, accepted, completed, cancelled)

**Example Challenge Issue:**
```
## 🎮 Battle Challenge

**Challenger:** @alice
**Pet:** Dragonite
**Level:** 45
**Type:** DUEL
**Reward:** 500.0 coins

### Challenge Details
**Defending Pet:** Mewtwo

**Description:**
Epic battle time!

### How to Accept
Reply to this issue to accept the challenge!
```

### 2. Food Trades 🍖

**Issue Labels:** `🍖 Food Trade`, `🥬 Vegetable/🥩 Meat/🍎 Fruit/⭐ Special`

**Food Types:**
- Vegetables 🥬
- Meat 🥩
- Fruits 🍎
- Special Items ⭐

**Quality Tiers:**
- Common (white)
- Rare (blue)
- Epic (purple)
- Legendary (gold)

**Trade Information Captured:**
- Seller username and farm name
- Food type and quality
- Quantity and unit price
- Total trade value
- Status (available, negotiating, sold)

**Example Trade Issue:**
```
## 🍖 Food Trade

**Seller:** @farmer_bob
**Farm:** Sunny Fields
**Food Type:** Meat
**Quality:** EPIC
**Quantity:** 100 units
**Price:** 50.0 coins per unit
**Total:** 5000.0 coins

### Product Details
Premium beef from grass-fed cattle

### How to Buy
Reply to this issue to make an offer or negotiate the price!
```

## Operation Modes

### Manual Mode (Default)

Users confirm each action before it's posted to GitHub Issues.

```bash
python3 github_issues_cli.py
```

**Workflow:**
1. Select action from menu
2. Enter information interactively
3. Review details before posting
4. Confirm to post to GitHub
5. Receive confirmation with Issue URL

**Advantages:**
- Full control over every action
- Can review before posting
- Prevents accidental posts

### Auto Mode

Automatically posts and reads Issues without user confirmation.

```bash
python3 github_issues_cli.py --auto
```

**Workflow:**
1. Provide information via API/CLI arguments
2. System automatically posts to GitHub
3. System automatically fetches and parses Issues

**Advantages:**
- Faster operation
- Suitable for automated systems
- Can be integrated with game servers

## API Reference

### GitHubIssuesManager Class

Core API for GitHub Issues operations.

#### Initialization

```python
from github_issues_integration import GitHubIssuesManager

manager = GitHubIssuesManager("chengjia2016", "agent-monster")
```

#### Post Challenge

```python
issue = manager.post_challenge(
    challenger="@alice",
    challenger_pet="Dragonite",
    challenger_level=45,
    challenge_type="duel",  # "duel", "tournament", "team_battle"
    defender_pet="Mewtwo",
    reward=500.0,
    description="Epic battle time!"
)
```

#### Post Food Trade

```python
issue = manager.post_food_trade(
    seller="@farmer_bob",
    farm_name="Sunny Fields",
    food_type="meat",  # "vegetable", "meat", "fruit", "special"
    quantity=100,
    price=50.0,
    quality="epic",  # "common", "rare", "epic", "legendary"
    description="Premium beef from grass-fed cattle"
)
```

#### Fetch Challenges

```python
challenges = manager.fetch_challenges()
for challenge in challenges:
    print(challenge)
    # Output: {
    #   'issue_id': 42,
    #   'title': 'Challenge by @alice',
    #   'challenger': '@alice',
    #   'challenger_pet': 'Dragonite',
    #   'challenger_level': 45,
    #   'challenge_type': 'duel',
    #   'defender_pet': 'Mewtwo',
    #   'reward': 500.0,
    #   'status': 'open',
    #   'url': 'https://github.com/...',
    #   'created_at': '2026-04-07T...'
    # }
```

#### Fetch Food Trades

```python
trades = manager.fetch_food_trades()
for trade in trades:
    print(trade)
    # Output: {
    #   'issue_id': 33,
    #   'title': 'Food Trade by @farmer_bob',
    #   'seller': '@farmer_bob',
    #   'farm_name': 'Sunny Fields',
    #   'food_type': 'meat',
    #   'quantity': 100,
    #   'price': 50.0,
    #   'quality': 'epic',
    #   'status': 'available',
    #   'url': 'https://github.com/...',
    #   'created_at': '2026-04-07T...'
    # }
```

#### Update Challenge Status

```python
manager.update_challenge_status(issue_id=42, status="accepted")
```

#### Add Comment to Issue

```python
manager.add_comment_to_issue(
    issue_id=42,
    comment="I accept this challenge! @bob"
)
```

### GitHubIssuesCLI Class

Interactive CLI wrapper around GitHubIssuesManager.

```python
from github_issues_cli import GitHubIssuesCLI

cli = GitHubIssuesCLI("chengjia2016", "agent-monster", auto_mode=False)

# Interactive challenge posting
cli.post_challenge_interactive()

# Interactive food trade posting
cli.post_food_trade_interactive()

# View challenges
cli.view_challenges()

# View food trades
cli.view_food_trades()

# Accept challenge
cli.accept_challenge_interactive()

# Make food trade offer
cli.offer_food_trade_interactive()
```

## Data Structures

### ChallengeIssue

```python
from github_issues_integration import ChallengeIssue

challenge = ChallengeIssue(
    issue_id=42,
    title="Challenge by @alice",
    challenger="@alice",
    challenger_pet="Dragonite",
    defender_pet="Mewtwo",
    challenger_level=45,
    challenge_type="duel",
    reward=500.0,
    status="open",
    created_at="2026-04-07T00:00:00Z",
    url="https://github.com/..."
)
```

### FoodTradeIssue

```python
from github_issues_integration import FoodTradeIssue

trade = FoodTradeIssue(
    issue_id=33,
    title="Food Trade by @farmer_bob",
    seller="@farmer_bob",
    farm_name="Sunny Fields",
    food_type="meat",
    quantity=100,
    price=50.0,
    quality="epic",
    status="available",
    created_at="2026-04-07T00:00:00Z",
    url="https://github.com/..."
)
```

## GitHub Labels System

The system automatically creates and applies labels to Issues:

### Functional Labels
- 🎮 Battle Challenge
- 🍖 Food Trade
- 📋 Quest
- 📢 Announcement

### Status Labels
- Status: Open
- Status: Accepted
- Status: Completed
- Status: Cancelled

### Food Type Labels
- 🥬 Vegetable
- 🥩 Meat
- 🍎 Fruit
- ⭐ Special

### Quality Labels
- Common
- Rare
- Epic
- Legendary

## Testing

Run the test suite to verify all functionality:

```bash
python3 test_github_issues_integration.py
```

**Test Coverage:**
- ✅ Manager initialization
- ✅ Challenge formatting and parsing
- ✅ Food trade formatting and parsing
- ✅ Issue body generation
- ✅ Data structure validation

## Common Use Cases

### Use Case 1: Player Posts Battle Challenge

```python
from github_issues_cli import GitHubIssuesCLI

cli = GitHubIssuesCLI("chengjia2016", "agent-monster")
cli.post_challenge_interactive()

# Output:
# 🎮 Post Battle Challenge
# Your GitHub username: alice
# Your pet name: Dragonite
# Your pet level: 45
# Select challenge type: 1 (Duel)
# Target pet name: Mewtwo
# Reward (coins): 500
# Description: Epic battle time!
# 
# ✅ Challenge posted successfully!
# 🔗 https://github.com/chengjia2016/agent-monster/issues/42
```

### Use Case 2: Fetch and Display All Challenges

```python
from github_issues_integration import GitHubIssuesManager

manager = GitHubIssuesManager("chengjia2016", "agent-monster")

# Fetch all open challenges
challenges = manager.fetch_challenges()

print(f"Found {len(challenges)} challenges:\n")
for challenge in challenges:
    if challenge['status'] == 'open':
        print(f"🎮 {challenge['challenger_pet']} (Level {challenge['challenger_level']})")
        print(f"   Challenger: {challenge['challenger']}")
        print(f"   Type: {challenge['challenge_type']}")
        print(f"   Reward: {challenge['reward']} coins")
        print(f"   URL: {challenge['url']}\n")
```

### Use Case 3: Farmer Lists Food for Sale

```python
from github_issues_cli import GitHubIssuesCLI

cli = GitHubIssuesCLI("chengjia2016", "agent-monster")
cli.post_food_trade_interactive()

# Output:
# 🍖 Post Food Trade
# Your GitHub username: farmer_bob
# Farm name: Sunny Fields
# Food type: 2 (Meat)
# Quality level: 3 (Epic)
# Quantity: 100
# Price per unit (coins): 50
# Description: Premium beef from grass-fed cattle
# 
# ✅ Food trade posted successfully!
# 🔗 https://github.com/chengjia2016/agent-monster/issues/33
```

### Use Case 4: Auto-Fetch and Process Challenges

```python
from github_issues_integration import GitHubIssuesManager
import time

manager = GitHubIssuesManager("chengjia2016", "agent-monster")

# Continuously fetch new challenges
while True:
    challenges = manager.fetch_challenges()
    
    for challenge in challenges:
        if challenge['status'] == 'open':
            # Process challenge (e.g., auto-match opponent)
            print(f"Found new challenge: {challenge['challenger_pet']} vs {challenge['defender_pet']}")
            
            # Could trigger auto-battle system
            # start_battle(challenge)
    
    time.sleep(60)  # Check every minute
```

## Troubleshooting

### Issue: "GitHub Token not set"

**Solution:** Set the GitHub token environment variable:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### Issue: "Failed to fetch Issues"

**Solution:** Verify:
1. GitHub token is valid
2. Repository exists and is accessible
3. GitHub API is not rate-limited

Check rate limit:
```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

### Issue: "Issue parsing failed"

**Solution:** Ensure:
1. Issue follows the correct format
2. All required fields are present in Issue body
3. Issue has correct labels applied

## Integration with Main Game

The GitHub Issues system can be integrated with the main Agent Monster game:

```python
from unified_game_systems_manager import UnifiedGameSystemsManager
from github_issues_integration import GitHubIssuesManager

# Initialize unified manager
game = UnifiedGameSystemsManager()

# Initialize GitHub Issues
github = GitHubIssuesManager("chengjia2016", "agent-monster")

# Fetch challenges and automatically match players
challenges = github.fetch_challenges()
for challenge in challenges:
    # Find matching opponent
    opponent = game.find_opponent(challenge['defender_pet'])
    if opponent:
        # Initiate battle
        battle = game.start_battle(
            player1=challenge['challenger'],
            pet1=challenge['challenger_pet'],
            player2=opponent['username'],
            pet2=opponent['pet'],
            wager=challenge['reward']
        )
```

## Performance Considerations

- **Rate Limiting:** GitHub API has 5000 requests/hour per token
- **Caching:** Consider caching fetch results to reduce API calls
- **Batch Operations:** Fetch multiple issues in single call when possible
- **Update Frequency:** Balance between real-time updates and API efficiency

## Security Notes

- Never commit GitHub tokens to version control
- Use environment variables for sensitive data
- Validate user input before posting to GitHub
- Monitor for malicious Issue content
- Implement rate limiting on client side

## Future Enhancements

- [ ] Auto-matching algorithm for finding opponents
- [ ] Reputation scoring system based on challenge history
- [ ] Food quality grading system with images
- [ ] Blockchain integration for trade history
- [ ] Discord webhook notifications for new challenges
- [ ] Leaderboard based on challenge success rate
- [ ] Trading market with dynamic pricing

## Support

For issues, questions, or feature requests:
- Report on GitHub: https://github.com/chengjia2016/agent-monster/issues
- Check existing documentation: GITHUB_ISSUES_GUIDE.md

---

**Last Updated:** April 7, 2026
**Version:** 1.0
**Status:** ✅ Production Ready
