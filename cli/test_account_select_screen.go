package main

import (
	"agent-monster-cli/pkg/github"
	"agent-monster-cli/pkg/ui"
	"fmt"
)

func main() {
	fmt.Println("Testing Account Select Screen Rendering...")
	fmt.Println()
	
	// Get real accounts
	accounts, err := github.GetAuthAccounts()
	if err != nil {
		fmt.Printf("❌ Error getting accounts: %v\n", err)
		return
	}
	
	if len(accounts) == 0 {
		fmt.Println("❌ No accounts found")
		return
	}
	
	fmt.Printf("✅ Found %d accounts\n\n", len(accounts))
	
	// Create an app and set up account select state
	app := &ui.App{
		Width:  80,
		Height: 24,
		CurrentScreen: ui.AccountSelectScreen,
		SelectedIndex: 0,
		AccountSelectState: &ui.AccountSelectState{
			Accounts: accounts,
			SelectedIndex: 0,
			Loading: false,
		},
	}
	
	// Render the account select screen
	view := app.View()
	
	fmt.Println("=== Account Selection Screen Output ===")
	fmt.Println(view)
	fmt.Println("=== End of Output ===")
	fmt.Println()
	fmt.Println("✅ Account selection screen rendered successfully!")
	fmt.Println("✅ Use Arrow Keys (↑/↓), J/K, or Page Up/Down to navigate")
	fmt.Println("✅ Press Enter to select account")
	fmt.Println("✅ Press Esc to cancel")
}
