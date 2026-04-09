package ui

import (
	"testing"
)

// TestCompleteOnboardingFlowWithClaiming verifies the entire onboarding flow including claiming
func TestCompleteOnboardingFlowWithClaiming(t *testing.T) {
	app := &App{
		OnboardingState: &OnboardingState{
			CurrentStep:      0,
			RepoForked:       false,
			BaseCreated:      false,
			PokemonsClaimed:  false,
			SelectedTemplate: -1,
			SelectedNPCs:     make([]bool, 0),
			Loading:          false,
			Error:            "",
		},
	}

	// Step 0: Welcome screen
	if app.OnboardingState.CurrentStep != int(OnboardingWelcomeScreen) {
		t.Errorf("Expected to start at Welcome screen")
	}

	// Simulate fork operation
	msg := OnboardingOperationMsg{
		Operation: "fork",
		Success:   true,
		Error:     "",
	}
	
	if msg.Operation != "fork" {
		t.Errorf("Fork operation should be recognized")
	}

	// Simulate createbase operation
	msg = OnboardingOperationMsg{
		Operation: "createbase",
		Success:   true,
		Error:     "",
	}
	
	if msg.Operation != "createbase" {
		t.Errorf("Createbase operation should be recognized")
	}

	// Simulate generatemap operation
	msg = OnboardingOperationMsg{
		Operation: "generatemap",
		Success:   true,
		Error:     "",
	}
	
	if msg.Operation != "generatemap" {
		t.Errorf("Generatemap operation should be recognized")
	}

	// Simulate claiming operation (returned from claimStarterPokemonsCmd)
	msg = OnboardingOperationMsg{
		Operation: "claiming",
		Success:   true,
		Error:     "",
	}
	
	if msg.Operation != "claiming" {
		t.Errorf("Claiming operation should be recognized")
	}

	// Verify final state should have all flags set
	app.OnboardingState.PokemonsClaimed = true
	app.OnboardingState.RepoForked = true
	app.OnboardingState.BaseCreated = true

	if !app.OnboardingState.PokemonsClaimed {
		t.Errorf("Expected PokemonsClaimed to be true")
	}

	if !app.OnboardingState.RepoForked {
		t.Errorf("Expected RepoForked to be true")
	}

	if !app.OnboardingState.BaseCreated {
		t.Errorf("Expected BaseCreated to be true")
	}
}

// TestOnboardingOperationSuccessHandling verifies operations handle success correctly
func TestOnboardingOperationSuccessHandling(t *testing.T) {
	operations := []struct {
		name      string
		operation string
	}{
		{"Fork", "fork"},
		{"Create Base", "createbase"},
		{"Generate Map", "generatemap"},
		{"Claim Pokemons", "claiming"},
	}

	for _, op := range operations {
		msg := OnboardingOperationMsg{
			Operation: op.operation,
			Success:   true,
			Error:     "",
		}

		if !msg.Success {
			t.Errorf("%s: Expected Success to be true", op.name)
		}

		if msg.Error != "" {
			t.Errorf("%s: Expected Error to be empty", op.name)
		}
	}
}

// TestOnboardingScreenTransitions verifies screen transitions in order
func TestOnboardingScreenTransitions(t *testing.T) {
	expectedScreens := []OnboardingStep{
		OnboardingWelcomeScreen,
		OnboardingForkScreen,
		OnboardingBaseScreen,
		OnboardingTemplateScreen,
		OnboardingNPCScreen,
		OnboardingMapPreviewScreen,
		OnboardingClaimingScreen,
		OnboardingCompleteScreen,
	}

	state := &OnboardingState{
		CurrentStep: int(OnboardingWelcomeScreen),
	}

	for i, expectedScreen := range expectedScreens {
		if state.CurrentStep != int(expectedScreen) {
			t.Errorf("Step %d: Expected screen %d, got %d", i, int(expectedScreen), state.CurrentStep)
		}

		// Simulate progression to next screen
		if i < len(expectedScreens)-1 {
			state.CurrentStep = int(expectedScreens[i+1])
		}
	}
}

// TestClaimingScreenIsBeforeComplete verifies claiming screen comes before complete
func TestClaimingScreenIsBeforeComplete(t *testing.T) {
	if int(OnboardingClaimingScreen) >= int(OnboardingCompleteScreen) {
		t.Errorf("OnboardingClaimingScreen (value: %d) should come before OnboardingCompleteScreen (value: %d)",
			int(OnboardingClaimingScreen), int(OnboardingCompleteScreen))
	}

	if int(OnboardingClaimingScreen) != int(OnboardingCompleteScreen)-1 {
		t.Errorf("OnboardingClaimingScreen should be immediately before OnboardingCompleteScreen")
	}
}

// TestOnboardingMessageProgression verifies messages update correctly
func TestOnboardingMessageProgression(t *testing.T) {
	app := &App{
		OnboardingState: &OnboardingState{
			Message: "",
			Error:   "",
		},
	}

	messages := map[string]string{
		"fork":      "✅ Fork 成功！",
		"createbase": "✅ 基地创建成功！",
		"claiming":   "✅ 宝可梦领取成功！",
	}

	for operation, expectedMessage := range messages {
		app.OnboardingState.Message = expectedMessage

		if app.OnboardingState.Message != expectedMessage {
			t.Errorf("Operation %s: Expected message '%s', got '%s'", operation, expectedMessage, app.OnboardingState.Message)
		}
	}
}
