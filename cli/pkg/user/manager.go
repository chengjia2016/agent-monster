package user

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"
)

// UserProfile represents a user's game profile
type UserProfile struct {
	GitHubLogin string    `json:"github_login"`
	GitHubID    int       `json:"github_id"`
	Email       string    `json:"email"`
	Balance     float64   `json:"balance"`
	Level       int       `json:"level"`
	Experience  int       `json:"experience"`
	Pokemons    []Pokemon `json:"pokemons"`
	Teams       []Team    `json:"teams"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// Pokemon represents a user's Pokemon
type Pokemon struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Species string `json:"species"`
	Level   int    `json:"level"`
	HP      int    `json:"hp"`
	MaxHP   int    `json:"max_hp"`
	Attack  int    `json:"attack"`
	Defense int    `json:"defense"`
	Speed   int    `json:"speed"`
	Status  string `json:"status"`
}

// Team represents a Pokemon team
type Team struct {
	ID        string   `json:"id"`
	Name      string   `json:"name"`
	Members   []string `json:"members"` // Pokemon IDs
	IsDefault bool     `json:"is_default"`
}

// Manager handles user profile management
type Manager struct {
	DataDir string
}

// NewManager creates a new user manager
func NewManager(dataDir string) *Manager {
	return &Manager{
		DataDir: dataDir,
	}
}

// GetOrCreateProfile gets or creates a user profile
func (m *Manager) GetOrCreateProfile(githubLogin string, githubID int) (*UserProfile, error) {
	profile, err := m.GetProfile(githubLogin)
	if err == nil {
		return profile, nil
	}

	// Create new profile
	profile = &UserProfile{
		GitHubLogin: githubLogin,
		GitHubID:    githubID,
		Balance:     1000.0,
		Level:       1,
		Experience:  0,
		Pokemons:    []Pokemon{},
		Teams:       []Team{},
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	if err := m.SaveProfile(profile); err != nil {
		return nil, err
	}

	return profile, nil
}

// GetProfile retrieves a user profile
func (m *Manager) GetProfile(githubLogin string) (*UserProfile, error) {
	path := filepath.Join(m.DataDir, fmt.Sprintf("%s.json", githubLogin))

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("profile not found: %w", err)
	}

	var profile UserProfile
	if err := json.Unmarshal(data, &profile); err != nil {
		return nil, fmt.Errorf("failed to parse profile: %w", err)
	}

	return &profile, nil
}

// SaveProfile saves a user profile
func (m *Manager) SaveProfile(profile *UserProfile) error {
	if err := os.MkdirAll(m.DataDir, 0755); err != nil {
		return err
	}

	path := filepath.Join(m.DataDir, fmt.Sprintf("%s.json", profile.GitHubLogin))

	profile.UpdatedAt = time.Now()

	data, err := json.MarshalIndent(profile, "", "  ")
	if err != nil {
		return err
	}

	if err := os.WriteFile(path, data, 0644); err != nil {
		return err
	}

	return nil
}

// AddPokemon adds a Pokemon to the user's profile
func (m *Manager) AddPokemon(githubLogin string, pokemon Pokemon) error {
	profile, err := m.GetProfile(githubLogin)
	if err != nil {
		return err
	}

	profile.Pokemons = append(profile.Pokemons, pokemon)

	return m.SaveProfile(profile)
}

// CreateTeam creates a new team for the user
func (m *Manager) CreateTeam(githubLogin string, team Team) error {
	profile, err := m.GetProfile(githubLogin)
	if err != nil {
		return err
	}

	profile.Teams = append(profile.Teams, team)

	return m.SaveProfile(profile)
}

// UpdateBalance updates the user's balance
func (m *Manager) UpdateBalance(githubLogin string, amount float64) error {
	profile, err := m.GetProfile(githubLogin)
	if err != nil {
		return err
	}

	profile.Balance += amount
	if profile.Balance < 0 {
		profile.Balance = 0
	}

	return m.SaveProfile(profile)
}

// GetStats returns game statistics for the user
func (m *Manager) GetStats(githubLogin string) (map[string]interface{}, error) {
	profile, err := m.GetProfile(githubLogin)
	if err != nil {
		return nil, err
	}

	return map[string]interface{}{
		"username":      profile.GitHubLogin,
		"level":         profile.Level,
		"experience":    profile.Experience,
		"balance":       profile.Balance,
		"pokemon_count": len(profile.Pokemons),
		"team_count":    len(profile.Teams),
		"created_at":    profile.CreatedAt,
		"updated_at":    profile.UpdatedAt,
	}, nil
}
