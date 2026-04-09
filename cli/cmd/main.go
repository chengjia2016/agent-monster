package main

import (
	"agent-monster-cli/pkg/api"
	"agent-monster-cli/pkg/ui"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	tea "github.com/charmbracelet/bubbletea"
)

var (
	serverURL string
	debug     bool
)

func init() {
	flag.StringVar(&serverURL, "server", "http://127.0.0.1:10000", "Judge server URL")
	flag.BoolVar(&debug, "debug", false, "Enable debug mode")
	flag.Parse()
}

func main() {
	// 获取用户数据目录
	userDir, err := getUserDataDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: Failed to get user data directory: %v\n", err)
		os.Exit(1)
	}

	// 创建API客户端
	client := api.NewClient(serverURL)

	// 创建应用
	app := ui.NewApp(client, userDir)

	// 启动TUI
	p := tea.NewProgram(app, tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		log.Fatal(err)
	}
}

// getUserDataDir returns the user data directory
func getUserDataDir() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}

	dataDir := filepath.Join(homeDir, ".agent-monster", "data")
	if err := os.MkdirAll(dataDir, 0755); err != nil {
		return "", err
	}

	return dataDir, nil
}
