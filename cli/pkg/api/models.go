package api

import "time"

// Pokemon represents a user's Pokemon
type Pokemon struct {
	ID         int      `json:"id"`
	GitHubID   int      `json:"github_id"`
	PetID      string   `json:"pet_id"`
	Name       string   `json:"pet_name"` // Changed from "name" to "pet_name" to match API
	Species    string   `json:"species"`
	Level      int      `json:"level"`
	Experience int      `json:"experience"`
	MaxHP      int      `json:"max_hp"`
	CurrentHP  int      `json:"current_hp"`
	Attack     int      `json:"attack"`
	Defense    int      `json:"defense"`
	SpAttack   int      `json:"sp_attack"`
	SpDefense  int      `json:"sp_defense"`
	Speed      int      `json:"speed"`
	Skills     []string `json:"skills"`
	Ability    string   `json:"ability"`
	Type       string   `json:"type"`
	CapturedAt string   `json:"created_at"` // Changed from time.Time with "captured_at" to string with "created_at"
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

// MapElement represents an element on the map (Pokemon, food, obstacle)
type MapElement struct {
	ID   string                 `json:"id"`
	Type string                 `json:"type"` // wild_pokemon, food, obstacle
	X    int                    `json:"x"`
	Y    int                    `json:"y"`
	Data map[string]interface{} `json:"data"`
}

// MapConnections represents connections to adjacent maps
type MapConnections struct {
	North *string `json:"north"`
	South *string `json:"south"`
	East  *string `json:"east"`
	West  *string `json:"west"`
}

// MapStatistics represents map statistics
type MapStatistics struct {
	TotalWildPokemon int    `json:"total_wild_pokemon"`
	TotalFood        int    `json:"total_food"`
	TotalObstacles   int    `json:"total_obstacles"`
	VisitedCount     int    `json:"visited_count"`
	LastVisited      string `json:"last_visited"`
}

// MapData represents a game map
type MapData struct {
	Version     string         `json:"version"`
	MapID       string         `json:"map_id"`
	OwnerID     int            `json:"owner_id"`
	OwnerName   string         `json:"owner_username"`
	CreatedAt   string         `json:"created_at"`
	UpdatedAt   string         `json:"updated_at"`
	Width       int            `json:"width"`
	Height      int            `json:"height"`
	Terrain     [][]int        `json:"terrain"` // 0: grass, 1: forest, 2: water, 3: mountain
	Elements    []MapElement   `json:"elements"`
	Connections MapConnections `json:"connections"`
	Statistics  MapStatistics  `json:"statistics"`
}

// PlayerPosition represents the player's position on a map
type PlayerPosition struct {
	MapID string
	X     int
	Y     int
}
