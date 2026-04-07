package main

import (
	"encoding/json"
	"fmt"
	"io/fs"
	"math"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type StatBlock struct {
	Base int `json:"base"`
	IV   int `json:"iv"`
	EV   int `json:"ev"`
	EXP  int `json:"exp"`
}

type Metadata struct {
	Name           string `json:"name"`
	Species        string `json:"species"`
	BirthTime      string `json:"birth_time"`
	Owner          string `json:"owner"`
	Generation     int    `json:"generation"`
	EvolutionStage int    `json:"evolution_stage"`
	Avatar         string `json:"avatar"`
}

type GeneBlock struct {
	Weight        float64  `json:"weight"`
	SourceCommits []string `json:"source_commits"`
}

type Stats struct {
	HP      StatBlock `json:"hp"`
	Attack  StatBlock `json:"attack"`
	Defense StatBlock `json:"defense"`
	Speed   StatBlock `json:"speed"`
	Armor   StatBlock `json:"armor"`
	Quota   StatBlock `json:"quota"`
}

type Genes struct {
	Logic    GeneBlock `json:"logic"`
	Creative GeneBlock `json:"creative"`
	Speed    GeneBlock `json:"speed"`
}

type Signature struct {
	Algorithm string `json:"algorithm"`
	Value     string `json:"value"`
	KeyID     string `json:"keyid"`
}

type PetSoul struct {
	Metadata      Metadata      `json:"metadata"`
	Stats         Stats         `json:"stats"`
	Genes         Genes         `json:"genes"`
	BattleHistory []interface{} `json:"battle_history"`
	Signature     Signature     `json:"signature"`
}

const (
	ColorReset   = "\033[0m"
	ColorRed     = "\033[31m"
	ColorGreen   = "\033[32m"
	ColorYellow  = "\033[33m"
	ColorBlue    = "\033[34m"
	ColorMagenta = "\033[35m"
	ColorCyan    = "\033[36m"
)

func renderBar(label string, current, max int, color string) string {
	width := 20
	filled := int(float64(current) / float64(max) * float64(width))
	bar := strings.Repeat("█", filled) + strings.Repeat("░", width-filled)
	return fmt.Sprintf("%s%s%s: %s%s/%d%s", color, label, ColorReset, color, bar, max, ColorReset)
}

func renderStat(name string, stat StatBlock) string {
	total := calculateStat(stat)
	color := ColorCyan
	if name == "HP" {
		color = ColorRed
	} else if name == "Attack" {
		color = ColorYellow
	} else if name == "Defense" {
		color = ColorBlue
	} else if name == "Speed" {
		color = ColorGreen
	} else if name == "Armor" {
		color = ColorMagenta
	}
	return renderBar(name, total, 255, color)
}

func calculateStat(stat StatBlock) int {
	return ((2 * stat.Base) + stat.IV + (stat.EV / 4)) + 100
}

func calculateLevel(exp int) int {
	return int(math.Floor(math.Pow(float64(exp), 1.0/3.0))) + 1
}

func renderAvatar(avatar string) string {
	lines := strings.Split(avatar, "\n")
	var result []string
	for _, line := range lines {
		result = append(result, ColorCyan+line+ColorReset)
	}
	return strings.Join(result, "\n")
}

func findSoulFile() string {
	searchPaths := []string{
		".monster/pet.soul",
		"../.monster/pet.soul",
		".monster/pet.json",
	}
	for _, p := range searchPaths {
		if _, err := os.Stat(p); err == nil {
			return p
		}
	}

	dir, _ := os.Getwd()
	filepath.WalkDir(dir, func(path string, d fs.DirEntry, err error) error {
		if strings.HasSuffix(path, "pet.soul") || strings.HasSuffix(path, "pet.json") {
			fmt.Printf("Found soul file: %s\n", path)
		}
		return nil
	})

	return ""
}

func loadSoul(path string) (*PetSoul, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("cannot read soul file: %w", err)
	}

	var soul PetSoul
	if err := json.Unmarshal(data, &soul); err != nil {
		return nil, fmt.Errorf("cannot parse soul file: %w", err)
	}

	return &soul, nil
}

func renderPet(soul *PetSoul) string {
	var sb strings.Builder

	sb.WriteString("\n")
	sb.WriteString(renderAvatar(soul.Metadata.Avatar))
	sb.WriteString("\n\n")

	sb.WriteString(fmt.Sprintf("%s══════════════════════════════════════%s\n", ColorCyan, ColorReset))
	sb.WriteString(fmt.Sprintf("  %s%s%s (Gen %d)\n", ColorYellow, soul.Metadata.Name, ColorReset, soul.Metadata.Generation))
	sb.WriteString(fmt.Sprintf("  Species: %s | Stage: %d\n", soul.Metadata.Species, soul.Metadata.EvolutionStage))
	sb.WriteString(fmt.Sprintf("  Owner: %s\n", soul.Metadata.Owner))
	sb.WriteString(fmt.Sprintf("%s══════════════════════════════════════%s\n", ColorCyan, ColorReset))

	sb.WriteString("\n")
	sb.WriteString(fmt.Sprintf("%s┌─ STATS ─────────────────────────┐%s\n", ColorBlue, ColorReset))
	sb.WriteString(fmt.Sprintf("%s│%s\n", ColorBlue, ColorReset))
	sb.WriteString(fmt.Sprintf("%s│  %s%s%s\n", ColorBlue, ColorReset, renderStat("HP", soul.Stats.HP), ColorReset))
	sb.WriteString(fmt.Sprintf("  │  %s\n", renderStat("Attack", soul.Stats.Attack)))
	sb.WriteString(fmt.Sprintf("  │  %s\n", renderStat("Defense", soul.Stats.Defense)))
	sb.WriteString(fmt.Sprintf("  │  %s\n", renderStat("Speed", soul.Stats.Speed)))
	sb.WriteString(fmt.Sprintf("  │  %s\n", renderStat("Armor", soul.Stats.Armor)))
	sb.WriteString(fmt.Sprintf("  │  %s\n", renderStat("Quota", soul.Stats.Quota)))
	sb.WriteString(fmt.Sprintf("%s└──────────────────────────────────┘%s\n", ColorBlue, ColorReset))

	sb.WriteString("\n")
	sb.WriteString(fmt.Sprintf("%s┌─ GENES ─────────────────────────┐%s\n", ColorMagenta, ColorReset))
	sb.WriteString(fmt.Sprintf("  │  Logic:   %.1f%%\n", soul.Genes.Logic.Weight*100))
	sb.WriteString(fmt.Sprintf("  │  Creative: %.1f%%\n", soul.Genes.Creative.Weight*100))
	sb.WriteString(fmt.Sprintf("  │  Speed:   %.1f%%\n", soul.Genes.Speed.Weight*100))
	sb.WriteString(fmt.Sprintf("%s└──────────────────────────────────┘%s\n", ColorMagenta, ColorReset))

	battles := len(soul.BattleHistory)
	sb.WriteString(fmt.Sprintf("\n  Battles: %d | Last Updated: %s\n", battles, time.Now().Format("2006-01-02 15:04")))

	return sb.String()
}

func main() {
	soulPath := findSoulFile()
	if soulPath == "" {
		soulPath = ".monster/pet.soul"
	}

	soul, err := loadSoul(soulPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		fmt.Println("Run egg_incubator.py first to create your monster!")
		os.Exit(1)
	}

	fmt.Println(renderPet(soul))
}
