#!/bin/bash

# Quick onboarding test script
# This script tests the complete onboarding flow and displays logs

set -e

echo "🎯 Agent Monster CLI - Onboarding Test"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Configuration
CLI_DIR="/root/pet/agent-monster/cli"
LOG_DIR="$HOME/.agent-monster/data/logs"
TIMEOUT=180  # 3 minutes timeout

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if CLI exists
if [ ! -f "$CLI_DIR/agentmonster" ]; then
    echo -e "${RED}❌ CLI not found at $CLI_DIR/agentmonster${NC}"
    echo "Please run: cd $CLI_DIR && go build -o agentmonster ./cmd"
    exit 1
fi

echo -e "${BLUE}📦 CLI Binary: $CLI_DIR/agentmonster${NC}"
echo -e "${BLUE}📋 Logs will be saved to: $LOG_DIR${NC}"
echo ""

# Kill previous CLI instances
echo -e "${YELLOW}🛑 Stopping any previous CLI instances...${NC}"
pkill -f "agentmonster" 2>/dev/null || true
sleep 1

# Clear previous logs (keep only last 5)
if [ -d "$LOG_DIR" ]; then
    ls -t "$LOG_DIR"/agentmonster_*.log 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
fi

echo -e "${GREEN}✅ Ready to start test${NC}"
echo ""
echo "═════════════════════════════════════════════════════════════"
echo "INSTRUCTIONS:"
echo "═════════════════════════════════════════════════════════════"
echo ""
echo "Follow these steps in the CLI:"
echo ""
echo "1️⃣  Press Enter on Welcome screen"
echo "2️⃣  Fork repository (wait for success)"
echo "3️⃣  Press Enter on Base screen"
echo "4️⃣  Use ↓ or ↑ to select map template, press Enter"
echo "5️⃣  Use ↓ or ↑ to select NPC, press Space to select, press Enter"
echo "6️⃣  Press Enter to generate map (may take a few seconds)"
echo "7️⃣  Wait for claiming screen"
echo "8️⃣  See completion screen"
echo "9️⃣  Press Enter to finish"
echo ""
echo "═════════════════════════════════════════════════════════════"
echo "Starting CLI with DEBUG logging (use --debug for even more details)"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Start CLI
START_TIME=$(date +%s)
"$CLI_DIR/agentmonster" --server="http://127.0.0.1:10000" --debug || true
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "═════════════════════════════════════════════════════════════"
echo "Test completed in ${DURATION} seconds"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Show latest log
echo -e "${BLUE}📋 Log Analysis:${NC}"
echo ""

LATEST_LOG=$(ls -t "$LOG_DIR"/agentmonster_*.log 2>/dev/null | head -1)

if [ -z "$LATEST_LOG" ]; then
    echo -e "${RED}❌ No log files found${NC}"
    exit 1
fi

echo -e "${GREEN}Latest log file: $LATEST_LOG${NC}"
echo ""

# Count log entries
echo -e "${BLUE}📊 Log Summary:${NC}"
echo "Total lines: $(wc -l < "$LATEST_LOG")"
echo ""

# Show error count
ERROR_COUNT=$(grep -c "\[ERROR\]\|❌" "$LATEST_LOG" || echo "0")
WARN_COUNT=$(grep -c "\[WARN\]" "$LATEST_LOG" || echo "0")
INFO_COUNT=$(grep -c "\[INFO\]" "$LATEST_LOG" || echo "0")

echo -e "${GREEN}✅ INFO:  $INFO_COUNT${NC}"
echo -e "${YELLOW}⚠️  WARN:  $WARN_COUNT${NC}"
echo -e "${RED}❌ ERROR: $ERROR_COUNT${NC}"

echo ""
echo "═════════════════════════════════════════════════════════════"
echo "Key Events:"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Extract key events
echo -e "${BLUE}🌐 API Calls:${NC}"
grep "🌐.*Request\|📨.*Response" "$LATEST_LOG" | head -20

echo ""
echo -e "${BLUE}⚠️  Issues:${NC}"
if grep -q "ERROR\|❌" "$LATEST_LOG"; then
    grep "ERROR\|❌" "$LATEST_LOG" | head -10
else
    echo "✅ No errors detected"
fi

echo ""
echo "═════════════════════════════════════════════════════════════"
echo "Full log content:"
echo "═════════════════════════════════════════════════════════════"
echo ""
cat "$LATEST_LOG"

echo ""
echo "═════════════════════════════════════════════════════════════"
if [ "$ERROR_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✅ Test likely successful (no errors)${NC}"
else
    echo -e "${RED}❌ Test had errors (see above)${NC}"
fi
echo "═════════════════════════════════════════════════════════════"
