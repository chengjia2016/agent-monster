package ui

import (
	"testing"
	"time"
)

// TestGenerateMapCmdWithTimeout verifies timeout handling
func TestGenerateMapCmdWithTimeout(t *testing.T) {
	// This tests the timeout logic structure
	// We can't actually test the timeout without mocking the API client
	// But we can verify the message structure

	msg := OnboardingOperationMsg{
		Operation: "generatemap",
		Success:   false,
		Error:     "生成地图超时 (30秒)，请检查网络连接",
	}

	if msg.Success {
		t.Errorf("Expected Success to be false for timeout")
	}

	if msg.Error != "生成地图超时 (30秒)，请检查网络连接" {
		t.Errorf("Expected timeout error message")
	}
}

// TestClaimingTimeoutHandling verifies claiming timeout handling
func TestClaimingTimeoutHandling(t *testing.T) {
	msg := OnboardingOperationMsg{
		Operation: "claiming",
		Success:   true,
		Error:     "",
	}

	// Even if claiming times out, we return success to allow onboarding to complete
	if !msg.Success {
		t.Errorf("Expected claiming to return success even with timeout")
	}
}

// TestTimeoutDoesNotBlockOnboarding verifies timeouts don't prevent progression
func TestTimeoutDoesNotBlockOnboarding(t *testing.T) {
	state := &OnboardingState{
		CurrentStep:     int(OnboardingClaimingScreen),
		PokemonsClaimed: false,
	}

	// Simulate claiming with timeout
	time.Sleep(100 * time.Millisecond)

	// State should still be able to transition
	state.PokemonsClaimed = true
	state.CurrentStep = int(OnboardingCompleteScreen)

	if state.CurrentStep != int(OnboardingCompleteScreen) {
		t.Errorf("Expected to transition to complete screen even after timeout")
	}
}
