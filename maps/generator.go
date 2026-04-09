package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"math/rand"
	"os"
	"path/filepath"
	"strconv"
	"time"
)

// Map 数据结构
type Map struct {
	Version     string               `json:"version"`
	MapID       string               `json:"map_id"`
	OwnerID     int                  `json:"owner_id"`
	OwnerName   string               `json:"owner_username"`
	CreatedAt   time.Time            `json:"created_at"`
	UpdatedAt   time.Time            `json:"updated_at"`
	Width       int                  `json:"width"`
	Height      int                  `json:"height"`
	Terrain     [][]int              `json:"terrain"`
	Elements    []Element            `json:"elements"`
	Connections Connections          `json:"connections"`
	Statistics  Statistics           `json:"statistics"`
}

// Element 地图元素
type Element struct {
	ID   string                 `json:"id"`
	Type string                 `json:"type"` // wild_pokemon, food, obstacle, npc
	X    int                    `json:"x"`
	Y    int                    `json:"y"`
	Data map[string]interface{} `json:"data"`
}

// Connections 连接信息
type Connections struct {
	North *string `json:"north"`
	South *string `json:"south"`
	East  *string `json:"east"`
	West  *string `json:"west"`
}

// Statistics 统计信息
type Statistics struct {
	TotalWildPokemon int        `json:"total_wild_pokemon"`
	TotalFood        int        `json:"total_food"`
	TotalObstacles   int        `json:"total_obstacles"`
	VisitedCount     int        `json:"visited_count"`
	LastVisited      *time.Time `json:"last_visited"`
}

// Pokemon 列表
var pokemonList = []struct {
	id    string
	name  string
	level int
}{
	{"0001", "妙蛙种子", 3},
	{"0004", "小火龙", 4},
	{"0007", "杰尼龟", 5},
	{"0016", "波波", 6},
	{"0019", "小拉达", 4},
	{"0021", "胡地", 7},
	{"0025", "皮卡丘", 5},
	{"0027", "小岩鼠", 5},
	{"0029", "尼多兰", 4},
	{"0032", "尼多兰", 4},
	{"0035", "皮皮", 6},
	{"0041", "小鼠", 3},
	{"0043", "臭臭花", 5},
	{"0046", "绿毛虫", 3},
	{"0052", "小猫", 5},
	{"0054", "可达鸭", 5},
	{"0058", "小火狐", 5},
	{"0061", "小蝌蚪", 3},
	{"0063", "腹斯", 4},
	{"0066", "小拳石", 5},
}

// Food 列表
var foodList = []struct {
	foodType  string
	foodName  string
	restoresHP int
	quantity  int
}{
	{"berry", "树莓", 20, 3},
	{"apple", "苹果", 15, 2},
	{"blueberry", "蓝莓", 25, 5},
	{"orange", "橙子", 18, 3},
	{"banana", "香蕉", 22, 4},
	{"mango", "芒果", 28, 2},
}

// generateTerrain 生成地形
func generateTerrain(width, height int) [][]int {
	terrain := make([][]int, height)
	for i := 0; i < height; i++ {
		terrain[i] = make([]int, width)
		for j := 0; j < width; j++ {
			// 0=草地(70%), 1=森林(15%), 2=水域(10%), 3=山地(5%)
			rand := rand.Intn(100)
			if rand < 70 {
				terrain[i][j] = 0
			} else if rand < 85 {
				terrain[i][j] = 1
			} else if rand < 95 {
				terrain[i][j] = 2
			} else {
				terrain[i][j] = 3
			}
		}
	}
	return terrain
}

// generateWildPokemon 生成野生精灵
func generateWildPokemon(width, height int, count int) []Element {
	elements := make([]Element, 0)
	for i := 0; i < count; i++ {
		pokemon := pokemonList[rand.Intn(len(pokemonList))]
		element := Element{
			ID:   fmt.Sprintf("wild_%03d", i+1),
			Type: "wild_pokemon",
			X:    rand.Intn(width),
			Y:    rand.Intn(height),
			Data: map[string]interface{}{
				"pokemon_id":   pokemon.id,
				"pokemon_name": pokemon.name,
				"level":        pokemon.level + rand.Intn(3),
				"rarity":       []string{"common", "uncommon", "rare"}[rand.Intn(3)],
			},
		}
		elements = append(elements, element)
	}
	return elements
}

// generateFood 生成食物
func generateFood(width, height int, count int) []Element {
	elements := make([]Element, 0)
	for i := 0; i < count; i++ {
		food := foodList[rand.Intn(len(foodList))]
		element := Element{
			ID:   fmt.Sprintf("food_%03d", i+1),
			Type: "food",
			X:    rand.Intn(width),
			Y:    rand.Intn(height),
			Data: map[string]interface{}{
				"food_type":   food.foodType,
				"food_name":   food.foodName,
				"quantity":    food.quantity,
				"restores_hp": food.restoresHP,
			},
		}
		elements = append(elements, element)
	}
	return elements
}

// generateObstacles 生成障碍物
func generateObstacles(width, height int, count int) []Element {
	elements := make([]Element, 0)
	obstacles := []struct {
		obsType string
		name    string
	}{
		{"rock", "岩石"},
		{"tree", "大树"},
		{"bush", "灌木"},
		{"fence", "栅栏"},
	}

	for i := 0; i < count; i++ {
		obs := obstacles[rand.Intn(len(obstacles))]
		element := Element{
			ID:   fmt.Sprintf("obstacle_%03d", i+1),
			Type: "obstacle",
			X:    rand.Intn(width),
			Y:    rand.Intn(height),
			Data: map[string]interface{}{
				"obstacle_type": obs.obsType,
				"obstacle_name": obs.name,
				"passable":      false,
			},
		}
		elements = append(elements, element)
	}
	return elements
}

// generateMap 生成地图
func generateMap(mapID string, ownerID int, ownerName string, width int, height int) *Map {
	now := time.Now()
	
	// 生成地形
	terrain := generateTerrain(width, height)
	
	// 生成元素
	elements := make([]Element, 0)
	elements = append(elements, generateWildPokemon(width, height, rand.Intn(5)+5)...)
	elements = append(elements, generateFood(width, height, rand.Intn(3)+3)...)
	elements = append(elements, generateObstacles(width, height, rand.Intn(2)+2)...)
	
	return &Map{
		Version:   "1.0",
		MapID:     mapID,
		OwnerID:   ownerID,
		OwnerName: ownerName,
		CreatedAt: now,
		UpdatedAt: now,
		Width:     width,
		Height:    height,
		Terrain:   terrain,
		Elements:  elements,
		Connections: Connections{
			North: nil,
			South: nil,
			East:  nil,
			West:  nil,
		},
		Statistics: Statistics{
			TotalWildPokemon: len(generateWildPokemon(width, height, 10)),
			TotalFood:        len(generateFood(width, height, 10)),
			TotalObstacles:   len(generateObstacles(width, height, 10)),
			VisitedCount:     0,
			LastVisited:      nil,
		},
	}
}

// saveMap 保存地图到文件
func saveMap(m *Map, filename string) error {
	data, err := json.MarshalIndent(m, "", "  ")
	if err != nil {
		return err
	}

	return ioutil.WriteFile(filename, data, 0644)
}

// loadMap 加载地图
func loadMap(filename string) (*Map, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	var m Map
	err = json.Unmarshal(data, &m)
	if err != nil {
		return nil, err
	}

	return &m, nil
}

// findMapConnections 查找地图连接
func findMapConnections(mapID string, mapsDir string) Connections {
	connections := Connections{}
	
	// 尝试查找相邻的地图 ID
	mapIDNum, _ := strconv.Atoi(mapID)
	
	// 生成可能的相邻地图 ID
	directions := map[string]int{
		"north": mapIDNum - 100,
		"south": mapIDNum + 100,
		"west":  mapIDNum - 1,
		"east":  mapIDNum + 1,
	}
	
	for dir, adjMapID := range directions {
		if adjMapID > 0 {
			filename := filepath.Join(mapsDir, fmt.Sprintf("%03d.json", adjMapID))
			if _, err := os.Stat(filename); err == nil {
				// 文件存在
				adjMapIDStr := fmt.Sprintf("%03d", adjMapID)
				switch dir {
				case "north":
					connections.North = &adjMapIDStr
				case "south":
					connections.South = &adjMapIDStr
				case "west":
					connections.West = &adjMapIDStr
				case "east":
					connections.East = &adjMapIDStr
				}
			}
		}
	}
	
	return connections
}

// updateMapConnections 更新所有地图的连接
func updateMapConnections(mapsDir string) error {
	files, err := ioutil.ReadDir(mapsDir)
	if err != nil {
		return err
	}

	for _, file := range files {
		if filepath.Ext(file.Name()) == ".json" && file.Name() != "generator.go" {
			mapPath := filepath.Join(mapsDir, file.Name())
			m, err := loadMap(mapPath)
			if err != nil {
				log.Printf("Error loading map %s: %v", file.Name(), err)
				continue
			}

			// 查找连接
			m.Connections = findMapConnections(m.MapID, mapsDir)

			// 保存更新后的地图
			err = saveMap(m, mapPath)
			if err != nil {
				log.Printf("Error saving map %s: %v", file.Name(), err)
			}
		}
	}

	return nil
}

// listMaps 列出所有地图
func listMaps(mapsDir string) error {
	files, err := ioutil.ReadDir(mapsDir)
	if err != nil {
		return err
	}

	fmt.Println("Available Maps:")
	fmt.Println("==============")
	for _, file := range files {
		if filepath.Ext(file.Name()) == ".json" {
			m, err := loadMap(filepath.Join(mapsDir, file.Name()))
			if err != nil {
				continue
			}

			fmt.Printf("Map %s (Owner: %s, Size: %dx%d, Elements: %d)\n",
				m.MapID, m.OwnerName, m.Width, m.Height,
				len(m.Elements))
		}
	}

	return nil
}

// visualizeMap 可视化地图（在终端中显示）
func visualizeMap(m *Map) {
	fmt.Printf("\n=== Map %s ===\n", m.MapID)
	fmt.Printf("Owner: %s | Size: %dx%d\n", m.OwnerName, m.Width, m.Height)
	fmt.Printf("Elements: %d (Wild Pokemon: %d, Food: %d, Obstacles: %d)\n",
		len(m.Elements), m.Statistics.TotalWildPokemon, 
		m.Statistics.TotalFood, m.Statistics.TotalObstacles)
	fmt.Println("\nTerrain Map (0=草, 1=森, 2=水, 3=山):")
	
	// 限制显示大小
	maxHeight := int(math.Min(float64(m.Height), 15))
	maxWidth := int(math.Min(float64(m.Width), 30))
	
	for i := 0; i < maxHeight; i++ {
		for j := 0; j < maxWidth; j++ {
			fmt.Print(m.Terrain[i][j])
		}
		fmt.Println()
	}
	
	if m.Width > maxWidth || m.Height > maxHeight {
		fmt.Println("... (map truncated for display)")
	}
	
	fmt.Println("\nConnections:")
	fmt.Printf("  North: %v\n", m.Connections.North)
	fmt.Printf("  South: %v\n", m.Connections.South)
	fmt.Printf("  East:  %v\n", m.Connections.East)
	fmt.Printf("  West:  %v\n", m.Connections.West)
	fmt.Println()
}

func main() {
	rand.Seed(time.Now().UnixNano())

	// 命令行参数
	generateCmd := flag.NewFlagSet("generate", flag.ExitOnError)
	mapIDFlag := generateCmd.String("id", "", "Map ID (e.g., 001, 002)")
	ownerIDFlag := generateCmd.Int("owner-id", 1, "Owner ID")
	ownerNameFlag := generateCmd.String("owner", "player", "Owner username")
	widthFlag := generateCmd.Int("width", 20, "Map width")
	heightFlag := generateCmd.Int("height", 20, "Map height")

	listCmd := flag.NewFlagSet("list", flag.ExitOnError)
	visualizeCmd := flag.NewFlagSet("visualize", flag.ExitOnError)
	visualizeMapIDFlag := visualizeCmd.String("id", "001", "Map ID to visualize")
	
	updateCmd := flag.NewFlagSet("update-connections", flag.ExitOnError)

	if len(os.Args) < 2 {
		fmt.Println("Map Generator for Agent Monster")
		fmt.Println("\nUsage:")
		fmt.Println("  go run generator.go generate -id <map_id> -owner <owner_name> [-owner-id <owner_id>] [-width <w>] [-height <h>]")
		fmt.Println("  go run generator.go list")
		fmt.Println("  go run generator.go visualize -id <map_id>")
		fmt.Println("  go run generator.go update-connections")
		fmt.Println("\nExample:")
		fmt.Println("  go run generator.go generate -id 001 -owner player1")
		fmt.Println("  go run generator.go generate -id 002 -owner player2 -width 30 -height 30")
		fmt.Println("  go run generator.go list")
		fmt.Println("  go run generator.go visualize -id 001")
		return
	}

	mapsDir := "."

	switch os.Args[1] {
	case "generate":
		generateCmd.Parse(os.Args[2:])
		if *mapIDFlag == "" {
			fmt.Println("Error: -id flag is required")
			generateCmd.PrintDefaults()
			return
		}

		// 检查地图是否已存在
		filename := filepath.Join(mapsDir, fmt.Sprintf("%s.json", *mapIDFlag))
		if _, err := os.Stat(filename); err == nil {
			fmt.Printf("Error: Map %s already exists\n", *mapIDFlag)
			return
		}

		// 生成地图
		m := generateMap(*mapIDFlag, *ownerIDFlag, *ownerNameFlag, *widthFlag, *heightFlag)

		// 查找连接
		m.Connections = findMapConnections(*mapIDFlag, mapsDir)

		// 保存地图
		err := saveMap(m, filename)
		if err != nil {
			log.Fatalf("Error saving map: %v", err)
		}

		fmt.Printf("✅ Map %s created successfully!\n", *mapIDFlag)
		visualizeMap(m)

	case "list":
		listCmd.Parse(os.Args[2:])
		err := listMaps(mapsDir)
		if err != nil {
			log.Fatalf("Error listing maps: %v", err)
		}

	case "visualize":
		visualizeCmd.Parse(os.Args[2:])
		filename := filepath.Join(mapsDir, fmt.Sprintf("%s.json", *visualizeMapIDFlag))
		m, err := loadMap(filename)
		if err != nil {
			log.Fatalf("Error loading map: %v", err)
		}
		visualizeMap(m)

	case "update-connections":
		updateCmd.Parse(os.Args[2:])
		err := updateMapConnections(mapsDir)
		if err != nil {
			log.Fatalf("Error updating connections: %v", err)
		}
		fmt.Println("✅ Map connections updated successfully!")

	default:
		fmt.Printf("Unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}
