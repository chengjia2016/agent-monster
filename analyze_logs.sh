#!/bin/bash

# Agent Monster Log Analyzer - 改进版本
# 提供全面的日志分析，无依赖

set -e

LOG_DIR="${HOME}/.agent-monster/data/logs"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${BLUE}▶ $1${NC}"
    echo ""
}

analyze_log() {
    local log_file="$1"
    
    if [ ! -f "$log_file" ]; then
        echo -e "${RED}❌ Log file not found: $log_file${NC}"
        exit 1
    fi

    print_header "📊 Log Analysis Summary"
    
    # Count log levels - 安全的方式
    local total_lines
    local info_count
    local debug_count
    local warn_count
    local error_count
    local api_count
    local api_error_count
    
    total_lines=$(wc -l < "$log_file")
    info_count=$(grep -c "\[INFO\]" "$log_file" 2>/dev/null || true)
    debug_count=$(grep -c "\[DEBUG\]" "$log_file" 2>/dev/null || true)
    warn_count=$(grep -c "\[WARN\]" "$log_file" 2>/dev/null || true)
    error_count=$(grep -c "\[ERROR\]" "$log_file" 2>/dev/null || true)
    api_count=$(grep -c "API Request\|🌐" "$log_file" 2>/dev/null || true)
    api_error_count=$(grep -c "API Error\|❌ API" "$log_file" 2>/dev/null || true)

    echo -e "${BLUE}📈 Statistics:${NC}"
    echo "  Total Lines:        ${total_lines}"
    
    echo ""
    echo -e "${BLUE}📋 Log Levels:${NC}"
    echo -e "  INFO:               ${GREEN}${info_count}${NC}"
    echo -e "  DEBUG:              ${CYAN}${debug_count}${NC}"
    echo -e "  WARN:               ${YELLOW}${warn_count}${NC}"
    echo -e "  ERROR:              ${RED}${error_count} ❌${NC}"

    echo ""
    echo -e "${BLUE}🌐 API Statistics:${NC}"
    echo "  Total API Calls:    ${api_count}"
    echo -e "  API Errors:         ${RED}${api_error_count} ❌${NC}"
    
    # Calculate API success rate
    if [ "$api_count" -gt 0 ]; then
        local api_success=$((api_count - api_error_count))
        local success_rate=$((api_success * 100 / api_count))
        if [ "$success_rate" -ge 80 ]; then
            echo -e "  Success Rate:       ${GREEN}${success_rate}%${NC}"
        elif [ "$success_rate" -ge 50 ]; then
            echo -e "  Success Rate:       ${YELLOW}${success_rate}%${NC}"
        else
            echo -e "  Success Rate:       ${RED}${success_rate}%${NC}"
        fi
    fi

    # Print errors if any
    if [ "$error_count" -gt 0 ]; then
        print_section "❌ Errors (${error_count})"
        grep "\[ERROR\]" "$log_file" | head -5
        if [ "$error_count" -gt 5 ]; then
            local remaining=$((error_count - 5))
            echo -e "${YELLOW}... and ${remaining} more errors${NC}"
        fi
    fi

    # Print warnings if any
    if [ "$warn_count" -gt 0 ]; then
        print_section "⚠️  Warnings (${warn_count})"
        grep "\[WARN\]" "$log_file" | head -3
        if [ "$warn_count" -gt 3 ]; then
            local remaining=$((warn_count - 3))
            echo -e "${YELLOW}... and ${remaining} more warnings${NC}"
        fi
    fi

    # Print API calls summary
    if [ "$api_count" -gt 0 ]; then
        print_section "🌐 API Requests (${api_count})"
        grep "API Request" "$log_file" 2>/dev/null | head -5 | sed 's/^/  /'
        if [ "$api_count" -gt 5 ]; then
            local remaining=$((api_count - 5))
            echo -e "  ${YELLOW}... and ${remaining} more API calls${NC}"
        fi
    fi
}

print_health_check() {
    local log_file="$1"
    
    if [ ! -f "$log_file" ]; then
        echo -e "${RED}❌ Log file not found: $log_file${NC}"
        exit 1
    fi

    print_header "🏥 Session Health Check"

    # Count issues - 安全的方式
    local error_count
    local warn_count
    local api_count
    local api_error_count
    
    error_count=$(grep -c "\[ERROR\]" "$log_file" 2>/dev/null || true)
    warn_count=$(grep -c "\[WARN\]" "$log_file" 2>/dev/null || true)
    api_count=$(grep -c "API Request\|🌐" "$log_file" 2>/dev/null || true)
    api_error_count=$(grep -c "API Error\|❌ API" "$log_file" 2>/dev/null || true)
    
    # Calculate health score
    local health=100
    health=$((health - error_count * 5))
    health=$((health - api_error_count * 10))
    health=$((health - warn_count * 2))
    
    if [ "$health" -lt 0 ]; then
        health=0
    fi

    # Print health bar
    local bar=""
    local filled=$((health / 10))
    for ((i=0; i<10; i++)); do
        if [ $i -lt "$filled" ]; then
            bar="${bar}█"
        else
            bar="${bar}░"
        fi
    done

    if [ "$health" -ge 80 ]; then
        echo -e "${GREEN}🟢 [${bar}] Health Score: ${health}/100${NC}"
    elif [ "$health" -ge 50 ]; then
        echo -e "${YELLOW}🟡 [${bar}] Health Score: ${health}/100${NC}"
    else
        echo -e "${RED}🔴 [${bar}] Health Score: ${health}/100${NC}"
    fi

    echo ""
    
    # Print assessment
    if [ "$health" -eq 100 ]; then
        echo -e "${GREEN}✅ Session completed successfully!${NC}"
    elif [ "$health" -ge 80 ]; then
        echo -e "${GREEN}✅ Session completed with minor issues${NC}"
    elif [ "$health" -ge 50 ]; then
        echo -e "${YELLOW}⚠️  Session completed with some issues${NC}"
    else
        echo -e "${RED}❌ Session completed with significant issues${NC}"
    fi

    # Print issues found
    echo ""
    echo -e "${BLUE}🔍 Issues Found:${NC}"
    [ "$error_count" -gt 0 ] && echo -e "  ${RED}• ${error_count} errors${NC}"
    [ "$warn_count" -gt 0 ] && echo -e "  ${YELLOW}• ${warn_count} warnings${NC}"
    [ "$api_error_count" -gt 0 ] && echo -e "  ${RED}• ${api_error_count} API errors${NC}"
    
    if [ "$error_count" -eq 0 ] && [ "$warn_count" -eq 0 ] && [ "$api_error_count" -eq 0 ]; then
        echo -e "  ${GREEN}• No issues found!${NC}"
    fi
    
    echo ""
}

list_logs() {
    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${RED}❌ Log directory not found: $LOG_DIR${NC}"
        return 1
    fi

    print_header "📋 Available Log Files"

    local count=0
    for file in $(ls -t "$LOG_DIR"/*.log 2>/dev/null); do
        [ -f "$file" ] || continue
        count=$((count + 1))
        local size=$(du -h "$file" | cut -f1)
        local name=$(basename "$file")
        echo "  $count. $name ($size)"
    done

    if [ "$count" -eq 0 ]; then
        echo -e "${YELLOW}No log files found${NC}"
    fi
}

print_usage() {
    cat << 'EOF'

📊 Agent Monster Log Analyzer

Usage:
  ./analyze_logs.sh <command> [options]

Commands:
  analyze [file]   Analyze a log file and print detailed report
  health [file]    Print health check report for a log file
  list             List all available log files
  filter [type]    Filter logs by type (ERROR, WARN, API, etc.)
  stats [file]     Show quick statistics
  help             Print this help message

Examples:
  ./analyze_logs.sh analyze                     # Analyze latest log
  ./analyze_logs.sh analyze agentmonster_20260409_150405.log
  ./analyze_logs.sh health                      # Health check on latest
  ./analyze_logs.sh list                        # List all logs
  ./analyze_logs.sh filter ERROR                # Show only errors
  ./analyze_logs.sh stats                       # Quick stats

Environment:
  Log files are stored in: ~/.agent-monster/data/logs/

EOF
}

get_latest_log() {
    ls -t "$LOG_DIR"/*.log 2>/dev/null | head -1
}

filter_logs() {
    local filter_type="$1"
    local log_file=$(get_latest_log)

    if [ -z "$log_file" ]; then
        echo -e "${RED}❌ No log files found${NC}"
        exit 1
    fi

    print_header "🔍 Filtered Logs: $filter_type"
    
    case "$filter_type" in
        ERROR)
            grep "\[ERROR\]" "$log_file" 2>/dev/null || echo "No errors found"
            ;;
        WARN)
            grep "\[WARN\]" "$log_file" 2>/dev/null || echo "No warnings found"
            ;;
        API)
            grep "API" "$log_file" 2>/dev/null || echo "No API calls found"
            ;;
        DEBUG)
            grep "\[DEBUG\]" "$log_file" 2>/dev/null || echo "No debug messages found"
            ;;
        INFO)
            grep "\[INFO\]" "$log_file" 2>/dev/null || echo "No info messages found"
            ;;
        *)
            grep "$filter_type" "$log_file" 2>/dev/null || echo "No matches found for: $filter_type"
            ;;
    esac
}

# Main logic
case "${1:-}" in
    analyze)
        log_file="${2:-$(get_latest_log)}"
        [ -z "$log_file" ] && { echo -e "${RED}❌ No log files found${NC}"; exit 1; }
        analyze_log "$log_file"
        ;;
    health)
        log_file="${2:-$(get_latest_log)}"
        [ -z "$log_file" ] && { echo -e "${RED}❌ No log files found${NC}"; exit 1; }
        print_health_check "$log_file"
        ;;
    list)
        list_logs
        ;;
    filter)
        [ -z "${2:-}" ] && { echo "Please specify filter type (ERROR, WARN, API, etc.)"; exit 1; }
        filter_logs "$2"
        ;;
    stats)
        log_file="${2:-$(get_latest_log)}"
        [ -z "$log_file" ] && { echo -e "${RED}❌ No log files found${NC}"; exit 1; }
        analyze_log "$log_file" | head -30
        ;;
    help|"")
        print_usage
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        print_usage
        exit 1
        ;;
esac
