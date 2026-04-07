@echo off
REM Agent Monster 快速安装脚本 (Windows)

echo 🐤 Agent Monster - 快速安装
echo ================================

REM 检查 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 需要安装 Python 3
    exit /b 1
)

echo ✅ Python 已安装

REM 检查 Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 需要安装 Git
    exit /b 1
)

echo ✅ Git 已安装

REM 安装依赖
echo.
echo 📦 安装依赖...
pip install -r requirements.txt

REM 初始化宠物
echo.
echo 🥚 领取初始宠物...
python claim_pet.py

echo.
echo ================================
echo ✅ 安装完成!
echo.
echo 📖 使用说明:
echo    /monster init       - 重新初始化
echo    /monster status     - 查看宠物状态
echo    /monster analyze    - 分析仓库
echo    /monster traps      - 扫描陷阱
echo    /monster duel       - 发起对战
echo.
echo 🍪 埋零食:
echo    在代码中添加：# 🍪 agent_monster cookie 0x...
echo.
echo 🥚 宠物蛋孵化:
echo    等待 72 小时后自动孵化
echo.

pause
