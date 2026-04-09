package api

import "time"

// Pokemon represents a user's Pokemon
type Pokemon struct {
	ID         string    `json:"id"`
	UserID     string    `json:"user_id"`
	Name       string    `json:"name"`
	Species    string    `json:"species"`
	Level      int       `json:"level"`
	Experience int       `json:"experience"`
	MaxHP      int       `json:"max_hp"`
	CurrentHP  int       `json:"current_hp"`
	Attack     int       `json:"attack"`
	Defense    int       `json:"defense"`
	SpAttack   int       `json:"sp_attack"`
	SpDefense  int       `json:"sp_defense"`
	Speed      int       `json:"speed"`
	Skills     []string  `json:"skills"`
	Ability    string    `json:"ability"`
	Type       string    `json:"type"`
	CapturedAt time.Time `json:"captured_at"`
}

// WildPokemon represents a wild Pokemon available for capture
type WildPokemon struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	Level     int    `json:"level"`
	Rarity    string `json:"rarity"`
	Location  string `json:"location"`
	Type      string `json:"type"`
	SpawnRate int    `json:"spawn_rate"`
}

// Battle represents a battle record
type Battle struct {
	ID             string    `json:"id"`
	AttackerID     string    `json:"attacker_id"`
	DefenderID     string    `json:"defender_id"`
	AttackerTeamID string    `json:"attacker_team_id"`
	DefenderTeamID string    `json:"defender_team_id"`
	Status         string    `json:"status"`
	Winner         string    `json:"winner"`
	BattleType     string    `json:"battle_type"`
	CreatedAt      time.Time `json:"created_at"`
}

// Base represents a defense base
type Base struct {
	ID           string `json:"id"`
	UserID       string `json:"user_id"`
	Name         string `json:"name"`
	Location     string `json:"location"`
	Level        int    `json:"level"`
	Wins         int    `json:"wins"`
	Losses       int    `json:"losses"`
	PokemonCount int    `json:"pokemon_count"`
}
