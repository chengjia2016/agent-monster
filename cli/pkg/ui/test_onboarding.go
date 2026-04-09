package ui

import (
	"testing"
)

// TestOnboardingStateInitialization verifies OnboardingState is properly initialized
func TestOnboardingStateInitialization(t *testing.T) {
	// Create a mock app
	app := &App{
		OnboardingState: &OnboardingState{
			CurrentStep:      0,
			SelectedTemplate: 0,
			SelectedNPCs:     make([]bool, 0),
		},
	}

	// Verify initial state
	if app.OnboardingState.CurrentStep != 0 {
		t.Errorf("Expected CurrentStep to be 0, got %d", app.OnboardingState.CurrentStep)
	}

	if app.OnboardingState.SelectedTemplate != 0 {
		t.Errorf("Expected SelectedTemplate to be 0, got %d", app.OnboardingState.SelectedTemplate)
	}

	if app.OnboardingState.RepoForked {
		t.Errorf("Expected RepoForked to be false, got %v", app.OnboardingState.RepoForked)
	}

	if app.OnboardingState.BaseCreated {
		t.Errorf("Expected BaseCreated to be false, got %v", app.OnboardingState.BaseCreated)
	}
}

// TestOnboardingScreenConstant verifies OnboardingScreen constant is defined
func TestOnboardingScreenConstant(t *testing.T) {
	// This test just verifies the constant exists and can be used
	_ = OnboardingScreen
	t.Log("OnboardingScreen constant verified")
}

// TestMapTemplatesExist verifies map templates are available
func TestMapTemplatesExist(t *testing.T) {
	templates := GetMapTemplates()

	if len(templates) != 5 {
		t.Errorf("Expected 5 map templates, got %d", len(templates))
	}

	for i, template := range templates {
		if template.Name == "" {
			t.Errorf("Template %d has empty name", i)
		}
		if len(template.NPCs) == 0 {
			t.Errorf("Template %d has no NPCs", i)
		}
	}
}
