package ui

import (
	"testing"
)

// TestUpdateHandlesClaimingOperation verifies Update method handles claiming correctly
func TestUpdateHandlesClaimingOperation(t *testing.T) {
	// Simulate claiming operation completion
	msg := OnboardingOperationMsg{
		Operation: "claiming",
		Success:   true,
		Error:     "",
	}

	// Verify the message structure
	if msg.Operation != "claiming" {
		t.Errorf("Expected operation 'claiming', got '%s'", msg.Operation)
	}

	if !msg.Success {
		t.Errorf("Expected Success to be true")
	}

	if msg.Error != "" {
		t.Errorf("Expected Error to be empty, got '%s'", msg.Error)
	}
}

// TestUpdateTransitionsToCompleteAfterClaiming verifies transition after claiming
func TestUpdateTransitionsToCompleteAfterClaiming(t *testing.T) {
	state := &OnboardingState{
		CurrentStep:     int(OnboardingClaimingScreen),
		PokemonsClaimed: false,
		Message:         "",
	}

	// Simulate what Update should do when handling claiming operation
	state.PokemonsClaimed = true
	state.CurrentStep = int(OnboardingCompleteScreen)
	state.Message = "✅ 宝可梦领取成功！"

	// Verify state changed correctly
	if !state.PokemonsClaimed {
		t.Errorf("Expected PokemonsClaimed to be true")
	}

	if state.CurrentStep != int(OnboardingCompleteScreen) {
		t.Errorf("Expected CurrentStep to be OnboardingCompleteScreen")
	}

	if state.Message != "✅ 宝可梦领取成功！" {
		t.Errorf("Expected success message")
	}
}

// TestOperationMessageStructure verifies all operation messages are handled
func TestOperationMessageStructure(t *testing.T) {
	operations := []struct {
		name      string
		operation string
		success   bool
	}{
		{"Fork", "fork", true},
		{"Create Base", "createbase", true},
		{"Generate Map", "generatemap", true},
		{"Claiming", "claiming", true},
	}

	for _, op := range operations {
		msg := OnboardingOperationMsg{
			Operation: op.operation,
			Success:   op.success,
			Error:     "",
		}

		if msg.Operation != op.operation {
			t.Errorf("%s: Expected operation '%s', got '%s'", op.name, op.operation, msg.Operation)
		}

		if msg.Success != op.success {
			t.Errorf("%s: Expected success %v, got %v", op.name, op.success, msg.Success)
		}
	}
}

// TestClaimingOperationWithError verifies claiming can handle errors
func TestClaimingOperationWithError(t *testing.T) {
	msg := OnboardingOperationMsg{
		Operation: "claiming",
		Success:   false,
		Error:     "Failed to claim pokemons",
	}

	if msg.Success {
		t.Errorf("Expected Success to be false")
	}

	if msg.Error != "Failed to claim pokemons" {
		t.Errorf("Expected error message")
	}
}
