package pokemon

import (
	"strings"
	"unicode/utf8"
)

// GetSprite returns the colored ASCII sprite for a Pokemon by name
func GetSprite(name string) string {
	// Use the existing function from pokemon_data.go
	return GetPokemonSprite(name)
}

// GetSpriteWidth returns the approximate width of a sprite in characters
// This helps with layout calculations
func GetSpriteWidth() int {
	return 32 // Most sprites are around 32 characters wide
}

// GetSpriteHeight returns the approximate height of a sprite in lines
func GetSpriteHeight() int {
	return 8 // Most sprites are around 8 lines tall
}

// SpriteToLines converts a sprite string to individual lines
// This is useful for rendering sprites line by line
func SpriteToLines(sprite string) []string {
	return strings.Split(sprite, "\n")
}

// GetSmallSprite returns a truncated version of the sprite
// Useful for list views where space is limited
func GetSmallSprite(name string) string {
	sprite := GetSprite(name)
	lines := SpriteToLines(sprite)

	// Return only the first 3 lines for compact display
	if len(lines) > 3 {
		lines = lines[:3]
	}

	return strings.Join(lines, "\n")
}

// PokemonExists checks if a Pokemon sprite exists
func PokemonExists(name string) bool {
	normalizedName := strings.ToLower(strings.TrimSpace(name))
	_, exists := PokemonSprites[normalizedName]
	return exists
}

// GetVisualWidth returns the visible character width of a sprite
// This accounts for ANSI escape sequences which don't display
func GetVisualWidth(sprite string) int {
	// Remove ANSI escape sequences to get actual display width
	lines := strings.Split(sprite, "\n")

	if len(lines) == 0 {
		return 0
	}

	// Get the first non-empty line
	for _, line := range lines {
		if len(line) > 0 {
			// Simple approximation: remove ANSI codes and count
			cleanLine := removeANSI(line)
			return utf8.RuneCountInString(cleanLine)
		}
	}

	return 0
}

// removeANSI removes ANSI escape sequences from a string
func removeANSI(s string) string {
	var result strings.Builder
	i := 0

	for i < len(s) {
		if s[i:i+1] == "\x1b" && i+1 < len(s) && s[i+1:i+2] == "[" {
			// Found start of ANSI sequence
			j := i + 2
			for j < len(s) && s[j] < '@' || (s[j] > '~') {
				j++
			}
			if j < len(s) {
				j++ // Include the terminating character
			}
			i = j
		} else if s[i:i+1] == "\x1b" && i+1 < len(s) {
			// Handle other escape sequences
			i += 2
		} else {
			result.WriteByte(s[i])
			i++
		}
	}

	return result.String()
}

// getDefaultSprite returns a simple placeholder sprite
func getDefaultSprite() string {
	return `    [38;2;200;200;200m▄▄▄[0m
    [38;2;200;200;200m█ ?█[0m
    [38;2;200;200;200m▀▀▀[0m`
}
