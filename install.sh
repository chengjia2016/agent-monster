#!/bin/bash
# Agent Monster 快速安装脚本

set -e

echo "🐤 Agent Monster - 快速安装"
echo "================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python 3"
    exit 1
fi

echo "✅ Python 版本：$(python3 --version)"

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 需要安装 Git"
    exit 1
fi

echo "✅ Git 版本：$(git --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 初始化宠物
echo ""
echo "🥚 领取初始宠物..."
python3 claim_pet.py

# 检查 GitHub CLI
if command -v gh &> /dev/null; then
    echo ""
    echo "🔧 配置 GitHub Actions..."

    # 启用工作流
    gh workflow enable hourly-settlement.yml 2>/dev/null || true
    gh workflow enable daily-rank.yml 2>/dev/null || true
    gh workflow enable battle-arena.yml 2>/dev/null || true

    echo "✅ GitHub Actions 已启用"
fi

echo ""
echo "================================"
echo "✅ 安装完成!"
echo ""
echo "📖 使用说明:"
echo "   /monster init       - 重新初始化"
echo "   /monster status     - 查看宠物状态"
echo "   /monster analyze    - 分析仓库"
echo "   /monster traps      - 扫描陷阱"
echo "   /monster duel       - 发起对战"
echo ""
echo "🍪 埋零食:"
echo "   在代码中添加：# 🍪 agent_monster cookie 0x..."
echo ""
echo "🥚 宠物蛋孵化:"
echo "   等待 72 小时后自动孵化"
echo ""
