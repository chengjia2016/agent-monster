package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"agent-monster/cli/pkg/logger"
)

func main() {
	// Define commands
	analyzeCmd := flag.NewFlagSet("analyze", flag.ExitOnError)
	healthCmd := flag.NewFlagSet("health", flag.ExitOnError)
	listCmd := flag.NewFlagSet("list", flag.ExitOnError)

	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "analyze":
		analyzeCmd.Parse(os.Args[2:])
		handleAnalyze(analyzeCmd)

	case "health":
		healthCmd.Parse(os.Args[2:])
		handleHealth(healthCmd)

	case "list":
		listCmd.Parse(os.Args[2:])
		handleList()

	case "help":
		printUsage()

	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
		os.Exit(1)
	}
}

func handleAnalyze(fs *flag.FlagSet) {
	file := ""
	if fs.NArg() > 0 {
		file = fs.Arg(0)
	}

	logPath := getLogFile(file)
	if logPath == "" {
		fmt.Println("❌ No log file found")
		os.Exit(1)
	}

	fmt.Printf("📖 Analyzing: %s\n", logPath)

	analysis, err := logger.AnalyzeLogFile(logPath)
	if err != nil {
		fmt.Printf("❌ Error analyzing log: %v\n", err)
		os.Exit(1)
	}

	analysis.PrintDetailedReport()
}

func handleHealth(fs *flag.FlagSet) {
	file := ""
	if fs.NArg() > 0 {
		file = fs.Arg(0)
	}

	logPath := getLogFile(file)
	if logPath == "" {
		fmt.Println("❌ No log file found")
		os.Exit(1)
	}

	fmt.Printf("🏥 Health Check: %s\n", logPath)

	analysis, err := logger.AnalyzeLogFile(logPath)
	if err != nil {
		fmt.Printf("❌ Error analyzing log: %v\n", err)
		os.Exit(1)
	}

	analysis.PrintHealthCheck()
}

func handleList() {
	logDir := filepath.Join(os.Getenv("HOME"), ".agent-monster", "data", "logs")

	entries, err := os.ReadDir(logDir)
	if err != nil {
		fmt.Printf("❌ Error reading log directory: %v\n", err)
		os.Exit(1)
	}

	if len(entries) == 0 {
		fmt.Println("📭 No log files found")
		return
	}

	fmt.Println("📋 Available log files:")
	for _, entry := range entries {
		if !entry.IsDir() && filepath.Ext(entry.Name()) == ".log" {
			info, _ := entry.Info()
			fmt.Printf("  • %s (%s)\n", entry.Name(), formatSize(info.Size()))
		}
	}
}

func getLogFile(file string) string {
	logDir := filepath.Join(os.Getenv("HOME"), ".agent-monster", "data", "logs")

	// If file is specified, check if it exists
	if file != "" {
		filePath := filepath.Join(logDir, file)
		if _, err := os.Stat(filePath); err == nil {
			return filePath
		}
		// Try as-is if it's an absolute path
		if _, err := os.Stat(file); err == nil {
			return file
		}
		return ""
	}

	// Otherwise, get the latest log file
	entries, err := os.ReadDir(logDir)
	if err != nil {
		return ""
	}

	var latest string
	var latestTime int64

	for _, entry := range entries {
		if !entry.IsDir() && filepath.Ext(entry.Name()) == ".log" {
			info, _ := entry.Info()
			if info.ModTime().Unix() > latestTime {
				latestTime = info.ModTime().Unix()
				latest = filepath.Join(logDir, entry.Name())
			}
		}
	}

	return latest
}

func formatSize(bytes int64) string {
	if bytes < 1024 {
		return fmt.Sprintf("%d B", bytes)
	}
	if bytes < 1024*1024 {
		return fmt.Sprintf("%.1f KB", float64(bytes)/1024)
	}
	return fmt.Sprintf("%.1f MB", float64(bytes)/(1024*1024))
}

func printUsage() {
	fmt.Println(`
📊 Agent Monster Log Analyzer

Usage:
  log-analyzer <command> [options]

Commands:
  analyze [file]   Analyze a log file and print detailed report
  health [file]    Print health check report for a log file
  list             List all available log files
  help             Print this help message

Examples:
  log-analyzer analyze                     # Analyze latest log
  log-analyzer analyze agentmonster_20260409_150405.log
  log-analyzer health                      # Health check on latest
  log-analyzer list                        # List all logs

Environment:
  Log files are stored in: ~/.agent-monster/data/logs/
`)
}
