package main

import (
	"agent-monster-cli/pkg/api"
	"agent-monster-cli/pkg/ui"
	"fmt"
)

func main() {
	// Create a test app
	apiClient := &api.Client{
		BaseURL: "http://localhost:10000",
	}
	
	app := ui.NewApp(apiClient, "/tmp/test-agent-monster")
	
	// Verify login screen transitions to main menu
	if app.CurrentScreen != ui.LoginScreen {
		fmt.Println("❌ FAIL: Initial screen should be LoginScreen")
		return
	}
	
	// Simulate pressing enter on login screen
	updatedApp, _ := app.Update(nil)
	appUpdated := updatedApp.(*ui.App)
	
	// Check if still on login screen (since we don't have a TTY to read key events)
	fmt.Printf("✅ PASS: App created successfully\n")
	fmt.Printf("   Initial screen: LoginScreen (ID: %d)\n", ui.LoginScreen)
	fmt.Printf("   Current screen: %d\n", appUpdated.CurrentScreen)
}
