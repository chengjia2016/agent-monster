#!/bin/bash
# Agent Monster Quick Install Script

set -e

echo "Agent Monster - Quick Install"
echo "================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required"
    exit 1
fi

echo "Python version: $(python3 --version)"

# Check Git
if ! command -v git &> /dev/null; then
    echo "Git is required"
    exit 1
fi

echo "Git version: $(git --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Claim starter pet
echo ""
echo "Claiming your starter pet..."
python3 claim_pet.py

# Check GitHub CLI
if command -v gh &> /dev/null; then
    echo ""
    echo "Configuring GitHub Actions..."

    # Enable workflows
    gh workflow enable hourly-settlement.yml 2>/dev/null || true
    gh workflow enable daily-rank.yml 2>/dev/null || true
    gh workflow enable battle-arena.yml 2>/dev/null || true

    echo "GitHub Actions enabled"
fi

echo ""
echo "================================"
echo "Installation complete!"
echo ""
echo "Usage:"
echo "   /monster init       - Re-initialize"
echo "   /monster status     - View pet status"
echo "   /monster analyze    - Analyze repository"
echo "   /monster traps      - Scan traps"
echo "   /monster duel       - Start battle"
echo ""
echo "Hide food cookies:"
echo "   Add in code: # agent_monster cookie 0x..."
echo ""
echo "Pet egg incubation:"
echo "   Wait 72 hours for automatic hatching"
echo ""
