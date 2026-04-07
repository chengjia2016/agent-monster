package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"strings"
)

const (
	VERSION     = "0.1.0"
	DEFAULT_DIR = ".monster"
	CONFIG_FILE = "config.json"
	SOUL_FILE   = "pet.soul"
	VAULT_FILE  = "vault.json"
)

var (
	jsonFlag  bool
	debugFlag bool
)

type CLI struct {
	monsterDir string
	config     *Config
	soul       *PetSoul
}

type Config struct {
	GitHubToken string `json:"github_token"`
	UserEmail   string `json:"user_email"`
	SigningKey  string `json:"signing_key"`
	MCPEnabled  bool   `json:"mcp_enabled"`
	LastUpdated string `json:"last_updated"`
}

type PetSoul struct {
	MonsterID      string    `json:"monster_id"`
	Name           string    `json:"name"`
	Type           []string  `json:"type"`
	Nature         string    `json:"nature"`
	Ability        string    `json:"ability"`
	BaseStats      Stats     `json:"base_stats"`
	IVs            Stats     `json:"ivs"`
	EVs            Stats     `json:"evs"`
	Level          int       `json:"level"`
	EXP            int       `json:"exp"`
	EvolutionStage int       `json:"evolution_stage"`
	Moves          []string  `json:"moves"`
	Avatar         string    `json:"avatar"`
	Metadata       Metadata  `json:"metadata"`
	BattleHistory  []Battle  `json:"battle_history"`
	Signature      Signature `json:"signature"`
}

type Stats struct {
	HP      int `json:"hp"`
	Attack  int `json:"attack"`
	Defense int `json:"defense"`
	SpAtk   int `json:"sp_atk"`
	SpDef   int `json:"sp_def"`
	Speed   int `json:"speed"`
}

type Metadata struct {
	BirthTime  string `json:"birth_time"`
	Owner      string `json:"owner"`
	Generation int    `json:"generation"`
}

type Battle struct {
	Timestamp  string `json:"timestamp"`
	OpponentID string `json:"opponent_id"`
	Result     string `json:"result"`
	ExpGained  int    `json:"exp_gained"`
	CommitHash string `json:"commit_hash"`
}

type Signature struct {
	Algorithm string `json:"algorithm"`
	Value     string `json:"value"`
	KeyID     string `json:"keyid"`
}

func NewCLI() *CLI {
	home, _ := user.Current()
	monsterDir := filepath.Join(home.HomeDir, DEFAULT_DIR)

	return &CLI{
		monsterDir: monsterDir,
		config:     &Config{},
	}
}

func (c *CLI) EnsureDir() error {
	if _, err := os.Stat(c.monsterDir); os.IsNotExist(err) {
		return os.MkdirAll(c.monsterDir, 0755)
	}
	return nil
}

func (c *CLI) LoadConfig() error {
	configPath := filepath.Join(c.monsterDir, CONFIG_FILE)
	data, err := os.ReadFile(configPath)
	if err != nil {
		return err
	}
	return json.Unmarshal(data, c.config)
}

func (c *CLI) SaveConfig() error {
	c.config.LastUpdated = "2024-01-01T00:00:00Z"
	data, err := json.MarshalIndent(c.config, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(filepath.Join(c.monsterDir, CONFIG_FILE), data, 0644)
}

func (c *CLI) LoadSoul() error {
	soulPath := filepath.Join(c.monsterDir, SOUL_FILE)
	data, err := os.ReadFile(soulPath)
	if err != nil {
		return err
	}
	return json.Unmarshal(data, &c.soul)
}

func (c *CLI) SaveSoul() error {
	data, err := json.MarshalIndent(c.soul, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(filepath.Join(c.monsterDir, SOUL_FILE), data, 0644)
}

func (c *CLI) Init() error {
	if err := c.EnsureDir(); err != nil {
		return fmt.Errorf("create monster dir: %w", err)
	}

	email := c.getGitConfig("user.email")
	name := c.getGitConfig("user.name")
	signingKey := c.getGitConfig("user.signingkey")

	if email == "" {
		email = "user@localhost"
	}
	if name == "" {
		name = "Developer"
	}

	c.config = &Config{
		GitHubToken: "",
		UserEmail:   email,
		SigningKey:  signingKey,
		MCPEnabled:  false,
	}

	if err := c.SaveConfig(); err != nil {
		return fmt.Errorf("save config: %w", err)
	}

	c.soul = c.generateInitialSoul(email, name)
	if err := c.SaveSoul(); err != nil {
		return fmt.Errorf("save soul: %w", err)
	}

	fmt.Println("✅ Monster initialized at:", c.monsterDir)
	return nil
}

func (c *CLI) getGitConfig(key string) string {
	cmd := exec.Command("git", "config", "--get", key)
	out, _ := cmd.Output()
	return strings.TrimSpace(string(out))
}

func (c *CLI) generateInitialSoul(email, name string) *PetSoul {
	monsterID := fmt.Sprintf("0x%x", hashString(name+email))

	return &PetSoul{
		MonsterID:      monsterID,
		Name:           name + "-Bot",
		Type:           []string{"Hybrid"},
		Nature:         "Hardy",
		Ability:        "VersionControl",
		BaseStats:      Stats{HP: 80, Attack: 70, Defense: 70, SpAtk: 70, SpDef: 70, Speed: 70},
		IVs:            Stats{HP: 20, Attack: 20, Defense: 20, SpAtk: 20, SpDef: 20, Speed: 20},
		EVs:            Stats{HP: 0, Attack: 0, Defense: 0, SpAtk: 0, SpDef: 0, Speed: 0},
		Level:          1,
		EXP:            0,
		EvolutionStage: 1,
		Moves:          []string{"scan", "hotfix"},
		Avatar:         getAvatar(1),
		Metadata: Metadata{
			BirthTime:  "2024-01-01T00:00:00Z",
			Owner:      email,
			Generation: 1,
		},
		BattleHistory: []Battle{},
		Signature: Signature{
			Algorithm: "RSA-SHA256",
			Value:     "",
			KeyID:     c.config.SigningKey,
		},
	}
}

func hashString(s string) int {
	h := 0
	for i, c := range s {
		h = h*31 + int(c)*i
	}
	return h & 0xFFFFFFFF
}

func getAvatar(stage int) string {
	avatars := map[int]string{
		1: `
     ╭───╮
    │ ◕  │
    ╰───╯
   ╭──────╮
  │  ♪ ♪  │
  ╰──────╯`,
		2: `
  ╭───────────╮
 │   ╭═══╮   │
 │  ◕  ◕  │ 
 │   ╰═══╯   │
 ╰───────────╯
╭─────────────╮
│   ══════════│
╰───────────────╯`,
		3: `
  ╭═══════════════════╮
 │   ╭═══════════╮   │
 │  │ ╭═══════╮ │   │
 │  │ │ ◕  ◕ │ │   │
 │  │ ╰═══════╯ │   │
 │   ╰═══════════╯   │
 ╰═══════════════════╯
╭═════════════════════╮
│ ════════════════════ │
╰═══════════════════════╯`,
	}
	return avatars[stage]
}

func (c *CLI) Status() error {
	if c.soul == nil {
		if err := c.LoadSoul(); err != nil {
			return fmt.Errorf("no monster found, run 'init' first")
		}
	}

	if jsonFlag {
		data, _ := json.Marshal(c.soul)
		fmt.Println(string(data))
		return nil
	}

	return c.RenderASCII()
}

func (c *CLI) RenderASCII() error {
	s := c.soul

	fmt.Println("\n" + s.Avatar)
	fmt.Println("═══════════════════════════════════════")
	fmt.Printf("  %s (Lv.%d)\n", s.Name, s.Level)
	fmt.Printf("  ID: %s\n", s.MonsterID)
	fmt.Printf("  Type: %s | Nature: %s | Ability: %s\n",
		strings.Join(s.Type, "/"), s.Nature, s.Ability)
	fmt.Println("═══════════════════════════════════════")

	fmt.Println("\n┌─ STATS ──────────────────────────────────┐")
	stats := []struct {
		Name string
		Val  int
	}{
		{"HP", s.BaseStats.HP}, {"ATK", s.BaseStats.Attack},
		{"DEF", s.BaseStats.Defense}, {"SPA", s.BaseStats.SpAtk},
		{"SPD", s.BaseStats.SpDef}, {"SPE", s.BaseStats.Speed},
	}

	for _, st := range stats {
		filled := st.Val / 20
		empty := 12 - filled
		bar := strings.Repeat("█", filled) + strings.Repeat("░", empty)
		fmt.Printf("│ %-6s │ %-20s │ %3d │\n", st.Name, bar, st.Val)
	}

	fmt.Println("└───────────────────────────────────────────┘")
	fmt.Printf("\nEXP: %d | Battles: %d\n", s.EXP, len(s.BattleHistory))

	return nil
}

func (c *CLI) Auth() error {
	ghToken, err := c.checkGhCLI()
	if err == nil && ghToken != "" {
		c.config.GitHubToken = ghToken
		c.SaveConfig()
		fmt.Println("✅ GitHub authenticated via gh CLI")
		return nil
	}

	fmt.Println("🔐 GitHub OAuth Device Flow")
	fmt.Println("1. Visit: https://github.com/login/device")
	fmt.Println("2. Enter code: ABCD-EFGH")
	fmt.Println("3. Authorize the app")
	fmt.Println("\n(Paste token here or press Enter to use gh CLI)")

	var token string
	fmt.Scan(&token)

	if token == "" {
		return fmt.Errorf("no token provided, install gh CLI: https://cli.github.com")
	}

	c.config.GitHubToken = token
	c.SaveConfig()
	fmt.Println("✅ GitHub token saved")

	return nil
}

func (c *CLI) checkGhCLI() (string, error) {
	cmd := exec.Command("gh", "auth", "token")
	out, err := cmd.Output()
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(out)), nil
}

func (c *CLI) Duel(target string) error {
	fmt.Printf("⚔️ Initiating duel against: %s\n", target)
	fmt.Println("(Battle simulation requires opponent's pet.soul)")

	result := map[string]interface{}{
		"status":  "pending",
		"target":  target,
		"message": "Battle system ready, awaiting opponent",
	}

	data, _ := json.Marshal(result)
	fmt.Println(string(data))

	return nil
}

func (c *CLI) MCPServer() {
	for {
		fmt.Print("> ")
		var input string
		if _, err := fmt.Scan(&input); err != nil {
			break
		}

		var req map[string]interface{}
		if err := json.Unmarshal([]byte(input), &req); err != nil {
			fmt.Println(`{"error": "invalid request"}`)
			continue
		}

		method, _ := req["method"].(string)
		params, _ := req["params"].(map[string]interface{})

		var resp map[string]interface{}

		switch method {
		case "init":
			resp = map[string]interface{}{"result": "initialized"}
		case "status":
			if c.soul == nil {
				c.LoadSoul()
			}
			resp = map[string]interface{}{"monster": c.soul}
		case "duel":
			target, _ := params["target"].(string)
			resp = map[string]interface{}{"target": target, "status": "ready"}
		default:
			resp = map[string]interface{}{"error": "unknown method"}
		}

		respJSON, _ := json.Marshal(resp)
		fmt.Println(string(respJSON))
	}
}

func main() {
	flag.BoolVar(&jsonFlag, "json", false, "Output JSON")
	flag.BoolVar(&debugFlag, "debug", false, "Debug mode")

	duelCmd := flag.NewFlagSet("duel", flag.ExitOnError)
	mcpCmd := flag.NewFlagSet("mcp", flag.ContinueOnError)
	duelTarget := duelCmd.String("target", "", "Target repository or user")

	if len(os.Args) < 2 {
		fmt.Println("Monster CLI v" + VERSION)
		fmt.Println("Usage: monster <command> [options]")
		fmt.Println("\nCommands:")
		fmt.Println("  init          Initialize your monster")
		fmt.Println("  status        Show monster status")
		fmt.Println("  auth          Authenticate with GitHub")
		fmt.Println("  duel          Start a battle")
		fmt.Println("  mcp           Start MCP server mode")
		fmt.Println("\nOptions:")
		fmt.Println("  --json        Output JSON format")
		fmt.Println("  --debug       Debug mode")
		os.Exit(1)
	}

	cli := NewCLI()

	switch os.Args[1] {
	case "init":
		if err := cli.Init(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "status":
		if err := cli.Status(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "auth":
		if err := cli.Auth(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "duel":
		duelCmd.Parse(os.Args[2:])
		if err := cli.Duel(*duelTarget); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "mcp":
		mcpCmd.Parse(os.Args[2:])
		cli.MCPServer()

	default:
		fmt.Printf("Unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
