#!/bin/bash

# Agent Monster CLI 启动脚本

set -e

# 检查依赖
check_dependencies() {
    if ! command -v go &> /dev/null; then
        echo "❌ Go 未安装，请先安装Go 1.21或更高版本"
        exit 1
    fi
}

# 编译
build() {
    echo "🔨 编译Agent Monster CLI..."
    cd "$(dirname "${BASH_SOURCE[0]}")"
    go mod tidy
    go build -o agent-monster cmd/main.go
    echo "✅ 编译完成！"
}

# 运行
run() {
    echo "🚀 启动Agent Monster CLI..."
    
    # 获取参数
    SERVER_URL="${1:-http://localhost:8080}"
    DEBUG="${DEBUG:-false}"
    
    # 设置环境变量
    export AGENT_MONSTER_SERVER="$SERVER_URL"
    
    # 运行
    if [ "$DEBUG" = "true" ]; then
        ./agent-monster -server "$SERVER_URL" -debug
    else
        ./agent-monster -server "$SERVER_URL"
    fi
}

# 清理
clean() {
    echo "🧹 清理构建文件..."
    rm -f agent-monster
    go clean
    echo "✅ 清理完成！"
}

# 帮助信息
show_help() {
    cat << EOF
Agent Monster CLI - 彩色TUI客户端

使用方法:
    $0 [命令] [选项]

命令:
    build              编译CLI客户端
    run [服务器URL]    运行CLI客户端
    clean              清理构建文件
    help               显示帮助信息

选项:
    DEBUG=true         启用调试模式

示例:
    # 编译并运行
    $0 build
    $0 run http://localhost:8080
    
    # 运行调试模式
    DEBUG=true $0 run
    
    # 清理构建文件
    $0 clean

EOF
}

# 主函数
main() {
    check_dependencies
    
    case "${1:-run}" in
        build)
            build
            ;;
        run)
            run "$2"
            ;;
        clean)
            clean
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            build
            run "$1"
            ;;
    esac
}

main "$@"
