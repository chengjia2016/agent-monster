package main

import (
	"agent-monster-cli/pkg/github"
	"fmt"
)

func main() {
	fmt.Println("Testing GetAuthAccounts function...")
	fmt.Println()
	
	accounts, err := github.GetAuthAccounts()
	if err != nil {
		fmt.Printf("❌ Error: %v\n", err)
		return
	}
	
	fmt.Printf("✅ Found %d GitHub account(s):\n", len(accounts))
	for i, account := range accounts {
		fmt.Printf("  [%d] %s@%s (Active: %v)\n", i+1, account.Username, account.Hostname, account.Active)
	}
	
	if len(accounts) > 1 {
		fmt.Println()
		fmt.Println("✅ Multiple accounts detected - Account selection screen will be shown!")
	} else if len(accounts) == 1 {
		fmt.Println()
		fmt.Println("ℹ️  Single account detected - Will proceed directly to main menu")
	}
}
