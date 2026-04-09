package ui

import (
	"agent-monster-cli/pkg/api"
	"fmt"
	tea "github.com/charmbracelet/bubbletea"
	"net/url"
	"strings"
)

// renderMapInputScreen renders the screen for entering GitHub URL or map ID
func (a *App) renderMapInputScreen() string {
	title := StyleTitle.
		Foreground(ColorWarning).
		Render("╔═════════════════════════════════════╗\n║       探索地图 - 输入模式       ║\n╚═════════════════════════════════════╝")

	instructions := StyleDim.Render(`
请输入以下之一:
1. GitHub 用户仓库链接 (如: https://github.com/chengjia2016/agent-monster)
2. 地图ID (如: 001)

示例:
  - https://github.com/tomcooler/agent-monster
  - 001
  - 002
`)

	inputLabel := StyleMenuItem.Render("输入:")
	inputBox := StyleMenuItemSelected.Render(fmt.Sprintf("  %s", a.MapState.InputBuffer))

	footer := StyleDim.Render(`
输入完成后按 Enter 确认
按 Esc 返回菜单
`)

	return title + "\n" + instructions + "\n" + inputLabel + "\n" + inputBox + "\n" + footer
}

// renderMapScreen renders the actual map with player
func (a *App) renderMapScreen() string {
	if a.MapState.CurrentMap == nil {
		return StyleError.Render("地图加载失败")
	}

	mapData := a.MapState.CurrentMap
	title := StyleTitle.
		Foreground(ColorWarning).
		Render(fmt.Sprintf("╔═════════════════════════════════════╗\n║    地图: %s - 所有者: %s      ║\n╚═════════════════════════════════════╝",
			mapData.MapID, mapData.OwnerName))

	// Render the map with ASCII art
	mapDisplay := a.renderMapGrid(mapData)

	// Info section
	info := StyleMenuItem.Render(fmt.Sprintf(
		"\n地图大小: %dx%d | 宠物: %d | 食物: %d | 障碍: %d",
		mapData.Width, mapData.Height,
		mapData.Statistics.TotalWildPokemon,
		mapData.Statistics.TotalFood,
		mapData.Statistics.TotalObstacles,
	))

	// Connections info
	connections := a.renderMapConnections(mapData)

	// Controls
	controls := StyleDim.Render(`
⬆️ ⬇️ ⬅️ ➡️  移动 (W/A/S/D)
Enter  确认位置
M      返回菜单
`)

	return title + "\n" + mapDisplay + info + "\n" + connections + "\n" + controls
}

// renderMapGrid renders the map terrain and elements
func (a *App) renderMapGrid(mapData *api.MapData) string {
	// Create a visual representation of the map
	// Using a simplified ASCII art representation

	var sb strings.Builder

	// Top border
	sb.WriteString("┌")
	for x := 0; x < mapData.Width; x++ {
		sb.WriteString("─")
	}
	sb.WriteString("┐\n")

	// Map content
	for y := 0; y < mapData.Height; y++ {
		sb.WriteString("│")
		for x := 0; x < mapData.Width; x++ {
			// Check if player is at this position
			if a.MapState.PlayerX == x && a.MapState.PlayerY == y {
				sb.WriteString("@") // Player marker
				continue
			}

			// Check if there's an element at this position
			hasElement := false
			for _, elem := range mapData.Elements {
				if elem.X == x && elem.Y == y {
					switch elem.Type {
					case "wild_pokemon":
						sb.WriteString("P") // Pokemon
					case "food":
						sb.WriteString("F") // Food
					case "obstacle":
						sb.WriteString("X") // Obstacle
					}
					hasElement = true
					break
				}
			}

			if !hasElement {
				// Show terrain
				if y < len(mapData.Terrain) && x < len(mapData.Terrain[y]) {
					switch mapData.Terrain[y][x] {
					case 0:
						sb.WriteString(".") // Grass
					case 1:
						sb.WriteString("T") // Forest
					case 2:
						sb.WriteString("~") // Water
					case 3:
						sb.WriteString("^") // Mountain
					default:
						sb.WriteString(".")
					}
				} else {
					sb.WriteString(".")
				}
			}
		}
		sb.WriteString("│\n")
	}

	// Bottom border
	sb.WriteString("└")
	for x := 0; x < mapData.Width; x++ {
		sb.WriteString("─")
	}
	sb.WriteString("┘\n")

	// Legend
	legend := StyleDim.Render(`
图例: @ 玩家  P 宝可梦  F 食物  X 障碍  . 草地  T 森林  ~ 水  ^ 山
`)

	return sb.String() + legend
}

// renderMapConnections renders information about adjacent maps
func (a *App) renderMapConnections(mapData *api.MapData) string {
	var sb strings.Builder

	sb.WriteString("\n连接的地图:\n")

	if mapData.Connections.North != nil {
		sb.WriteString(StyleMenuItem.Render(fmt.Sprintf("  ⬆️  北方: %s", *mapData.Connections.North)))
		sb.WriteString("\n")
	}
	if mapData.Connections.South != nil {
		sb.WriteString(StyleMenuItem.Render(fmt.Sprintf("  ⬇️  南方: %s", *mapData.Connections.South)))
		sb.WriteString("\n")
	}
	if mapData.Connections.East != nil {
		sb.WriteString(StyleMenuItem.Render(fmt.Sprintf("  ➡️  东方: %s", *mapData.Connections.East)))
		sb.WriteString("\n")
	}
	if mapData.Connections.West != nil {
		sb.WriteString(StyleMenuItem.Render(fmt.Sprintf("  ⬅️  西方: %s", *mapData.Connections.West)))
		sb.WriteString("\n")
	}

	return sb.String()
}

// parseGitHubURL extracts username and repo from GitHub URL
func parseGitHubURL(githubURL string) (username, repo string, err error) {
	// Parse URL
	u, err := url.Parse(githubURL)
	if err != nil {
		return "", "", err
	}

	// Extract path components
	parts := strings.TrimPrefix(strings.TrimSuffix(u.Path, ".git"), "/")
	components := strings.Split(parts, "/")

	if len(components) < 2 {
		return "", "", fmt.Errorf("invalid GitHub URL format")
	}

	return components[0], components[1], nil
}

// LoadMapFromGitHub loads a map from a GitHub user's repository
func (a *App) LoadMapFromGitHub(githubURL string) error {
	// Parse GitHub URL
	username, _, err := parseGitHubURL(githubURL)
	if err != nil {
		return fmt.Errorf("invalid GitHub URL: %w", err)
	}

	a.Loading = true
	defer func() { a.Loading = false }()

	// Search for maps owned by this user
	// For simplicity, we'll search by the first map ID pattern
	searchQuery := username
	maps, err := a.Client.SearchMaps(searchQuery, 1, 1)
	if err != nil {
		return fmt.Errorf("failed to search maps: %w", err)
	}

	if len(maps) == 0 {
		return fmt.Errorf("no maps found for user %s", username)
	}

	// Load the first map found
	return a.LoadMap(maps[0].MapID)
}

// LoadMap loads a map by ID
func (a *App) LoadMap(mapID string) error {
	a.Loading = true
	defer func() { a.Loading = false }()

	mapData, err := a.Client.GetMapByID(mapID)
	if err != nil {
		return fmt.Errorf("failed to load map: %w", err)
	}

	a.MapState.CurrentMap = mapData
	a.MapState.PlayerX = mapData.Width / 2
	a.MapState.PlayerY = mapData.Height / 2
	a.CurrentScreen = MapScreen

	return nil
}

// HandleMapInput processes input in map screen
func (a *App) HandleMapInput(msg tea.KeyMsg) tea.Cmd {
	switch msg.String() {
	case "up", "w":
		if a.MapState.PlayerY > 0 {
			a.MapState.PlayerY--
		} else if a.MapState.CurrentMap.Connections.North != nil {
			// Move to north map
			return a.traverseToMap(*a.MapState.CurrentMap.Connections.North, "north")
		}

	case "down", "s":
		if a.MapState.PlayerY < a.MapState.CurrentMap.Height-1 {
			a.MapState.PlayerY++
		} else if a.MapState.CurrentMap.Connections.South != nil {
			// Move to south map
			return a.traverseToMap(*a.MapState.CurrentMap.Connections.South, "south")
		}

	case "left", "a":
		if a.MapState.PlayerX > 0 {
			a.MapState.PlayerX--
		} else if a.MapState.CurrentMap.Connections.West != nil {
			// Move to west map
			return a.traverseToMap(*a.MapState.CurrentMap.Connections.West, "west")
		}

	case "right", "d":
		if a.MapState.PlayerX < a.MapState.CurrentMap.Width-1 {
			a.MapState.PlayerX++
		} else if a.MapState.CurrentMap.Connections.East != nil {
			// Move to east map
			return a.traverseToMap(*a.MapState.CurrentMap.Connections.East, "east")
		}

	case "m":
		a.CurrentScreen = MainMenuScreen
		a.SelectedIndex = 0
	}

	return nil
}

// traverseToMap is a helper to traverse to adjacent map
func (a *App) traverseToMap(nextMapID, direction string) tea.Cmd {
	return func() tea.Msg {
		// Load the adjacent map
		nextMap, err := a.Client.GetMapByID(nextMapID)
		if err != nil {
			a.Error = fmt.Sprintf("failed to traverse: %v", err)
			return nil
		}

		a.MapState.CurrentMap = nextMap

		// Reposition player at the opposite edge
		switch direction {
		case "north":
			a.MapState.PlayerY = nextMap.Height - 1
		case "south":
			a.MapState.PlayerY = 0
		case "west":
			a.MapState.PlayerX = nextMap.Width - 1
		case "east":
			a.MapState.PlayerX = 0
		}

		a.Message = fmt.Sprintf("进入地图: %s", nextMapID)
		return nil
	}
}

// HandleMapInputScreenInput processes input on the map input screen
func (a *App) HandleMapInputScreenInput(msg tea.KeyMsg) (*App, tea.Cmd) {
	switch msg.String() {
	case "enter":
		input := strings.TrimSpace(a.MapState.InputBuffer)
		if input == "" {
			a.Error = "请输入地图ID或GitHub链接"
			return a, nil
		}

		a.Loading = true

		// Check if it's a GitHub URL
		if strings.Contains(input, "github.com") {
			go func() {
				if err := a.LoadMapFromGitHub(input); err != nil {
					a.Error = fmt.Sprintf("加载地图失败: %v", err)
				}
				a.Loading = false
			}()
		} else {
			// Assume it's a map ID
			go func() {
				if err := a.LoadMap(input); err != nil {
					a.Error = fmt.Sprintf("加载地图失败: %v", err)
				}
				a.Loading = false
			}()
		}

		return a, nil

	case "esc":
		a.CurrentScreen = MainMenuScreen
		a.SelectedIndex = 4
		return a, nil

	case "backspace":
		if len(a.MapState.InputBuffer) > 0 {
			a.MapState.InputBuffer = a.MapState.InputBuffer[:len(a.MapState.InputBuffer)-1]
		}

	case "ctrl+u":
		a.MapState.InputBuffer = ""

	default:
		// Append character to input buffer
		if len(msg.String()) == 1 && msg.String() >= " " && msg.String() <= "~" {
			a.MapState.InputBuffer += msg.String()
		}
	}

	return a, nil
}
