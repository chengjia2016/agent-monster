package ugc

import (
	"fmt"
	"sort"
	"time"
)

// MapListing 社区地图列表项
type MapListing struct {
	MapID       string
	Title       string
	Description string
	OwnerName   string
	OwnerURL    string
	Difficulty  string
	Tags        []string
	Rating      float64
	Downloads   int
	CreatedAt   time.Time
	UpdatedAt   time.Time
	SourceURL   string
}

// MapMarketplace 地图市场浏览器
type MapMarketplace struct {
	listings map[string]*MapListing
	logger   Logger
}

func NewMapMarketplace(logger Logger) *MapMarketplace {
	return &MapMarketplace{
		listings: make(map[string]*MapListing),
		logger:   logger,
	}
}

// RegisterMap 注册一个新的地图到市场
func (mm *MapMarketplace) RegisterMap(listing *MapListing) error {
	if listing.MapID == "" {
		return fmt.Errorf("MapID cannot be empty")
	}

	if _, exists := mm.listings[listing.MapID]; exists {
		return fmt.Errorf("Map %s already registered", listing.MapID)
	}

	mm.listings[listing.MapID] = listing
	mm.logger.Info("Map registered: %s (%s)", listing.Title, listing.MapID)
	return nil
}

// UpdateMap 更新地图信息
func (mm *MapMarketplace) UpdateMap(mapID string, listing *MapListing) error {
	if _, exists := mm.listings[mapID]; !exists {
		return fmt.Errorf("Map %s not found", mapID)
	}

	mm.listings[mapID] = listing
	mm.logger.Info("Map updated: %s", mapID)
	return nil
}

// GetMap 获取单个地图
func (mm *MapMarketplace) GetMap(mapID string) (*MapListing, error) {
	listing, exists := mm.listings[mapID]
	if !exists {
		return nil, fmt.Errorf("Map %s not found", mapID)
	}
	return listing, nil
}

// ListAllMaps 列出所有地图
func (mm *MapMarketplace) ListAllMaps() []*MapListing {
	var maps []*MapListing
	for _, listing := range mm.listings {
		maps = append(maps, listing)
	}

	// 按下载数排序
	sort.Slice(maps, func(i, j int) bool {
		return maps[i].Downloads > maps[j].Downloads
	})

	return maps
}

// SearchMaps 搜索地图
func (mm *MapMarketplace) SearchMaps(query string) []*MapListing {
	var results []*MapListing

	for _, listing := range mm.listings {
		// 在标题中搜索
		if matchString(listing.Title, query) {
			results = append(results, listing)
			continue
		}

		// 在描述中搜索
		if matchString(listing.Description, query) {
			results = append(results, listing)
			continue
		}

		// 在所有者名中搜索
		if matchString(listing.OwnerName, query) {
			results = append(results, listing)
			continue
		}

		// 在标签中搜索
		for _, tag := range listing.Tags {
			if matchString(tag, query) {
				results = append(results, listing)
				break
			}
		}
	}

	return results
}

// FilterByDifficulty 按难度过滤
func (mm *MapMarketplace) FilterByDifficulty(difficulty string) []*MapListing {
	var results []*MapListing

	for _, listing := range mm.listings {
		if listing.Difficulty == difficulty {
			results = append(results, listing)
		}
	}

	// 按评分排序
	sort.Slice(results, func(i, j int) bool {
		return results[i].Rating > results[j].Rating
	})

	return results
}

// FilterByTag 按标签过滤
func (mm *MapMarketplace) FilterByTag(tag string) []*MapListing {
	var results []*MapListing

	for _, listing := range mm.listings {
		for _, t := range listing.Tags {
			if t == tag {
				results = append(results, listing)
				break
			}
		}
	}

	return results
}

// GetTopMaps 获取最受欢迎的地图
func (mm *MapMarketplace) GetTopMaps(count int) []*MapListing {
	maps := mm.ListAllMaps()

	if count < 0 || count > len(maps) {
		count = len(maps)
	}

	return maps[:count]
}

// GetNewestMaps 获取最新的地图
func (mm *MapMarketplace) GetNewestMaps(count int) []*MapListing {
	var maps []*MapListing
	for _, listing := range mm.listings {
		maps = append(maps, listing)
	}

	// 按创建时间排序
	sort.Slice(maps, func(i, j int) bool {
		return maps[i].CreatedAt.After(maps[j].CreatedAt)
	})

	if count < 0 || count > len(maps) {
		count = len(maps)
	}

	return maps[:count]
}

// GetHighestRatedMaps 获取评分最高的地图
func (mm *MapMarketplace) GetHighestRatedMaps(count int) []*MapListing {
	var maps []*MapListing
	for _, listing := range mm.listings {
		maps = append(maps, listing)
	}

	// 按评分排序
	sort.Slice(maps, func(i, j int) bool {
		return maps[i].Rating > maps[j].Rating
	})

	if count < 0 || count > len(maps) {
		count = len(maps)
	}

	return maps[:count]
}

// GetStatistics 获取市场统计
func (mm *MapMarketplace) GetStatistics() map[string]interface{} {
	totalDownloads := 0
	totalRating := 0.0
	mapsByDifficulty := make(map[string]int)
	uniqueAuthors := make(map[string]bool)

	for _, listing := range mm.listings {
		totalDownloads += listing.Downloads
		totalRating += listing.Rating
		mapsByDifficulty[listing.Difficulty]++
		uniqueAuthors[listing.OwnerName] = true
	}

	avgRating := 0.0
	if len(mm.listings) > 0 {
		avgRating = totalRating / float64(len(mm.listings))
	}

	return map[string]interface{}{
		"total_maps":         len(mm.listings),
		"total_downloads":    totalDownloads,
		"average_rating":     avgRating,
		"unique_authors":     len(uniqueAuthors),
		"maps_by_difficulty": mapsByDifficulty,
	}
}

// PrintMapInfo 打印地图信息
func (mm *MapMarketplace) PrintMapInfo(listing *MapListing) {
	fmt.Println("\n╔════════════════════════════════════╗")
	fmt.Println("║         Map Information           ║")
	fmt.Println("╚════════════════════════════════════╝")

	fmt.Printf("\nTitle:       %s\n", listing.Title)
	fmt.Printf("Map ID:      %s\n", listing.MapID)
	fmt.Printf("Author:      @%s\n", listing.OwnerName)
	fmt.Printf("Difficulty:  %s\n", listing.Difficulty)
	fmt.Printf("Rating:      %.1f/5.0 ⭐\n", listing.Rating)
	fmt.Printf("Downloads:   %d\n", listing.Downloads)
	fmt.Printf("Created:     %s\n", listing.CreatedAt.Format("2006-01-02 15:04:05"))

	if len(listing.Tags) > 0 {
		fmt.Printf("Tags:        %v\n", listing.Tags)
	}

	fmt.Printf("\nDescription:\n%s\n", listing.Description)
}

// PrintMapList 打印地图列表
func (mm *MapMarketplace) PrintMapList(maps []*MapListing) {
	if len(maps) == 0 {
		fmt.Println("No maps found.")
		return
	}

	fmt.Println("\n╔════════════════════════════════════════════════════════╗")
	fmt.Println("║            Available Community Maps                 ║")
	fmt.Println("╚════════════════════════════════════════════════════════╝")

	for i, listing := range maps {
		difficulty_emoji := "🟢"
		if listing.Difficulty == "medium" {
			difficulty_emoji = "🟡"
		} else if listing.Difficulty == "hard" {
			difficulty_emoji = "🔴"
		}

		fmt.Printf("%d. %s [%s] %s\n",
			i+1,
			listing.Title,
			listing.MapID,
			difficulty_emoji,
		)
		fmt.Printf("   Author: @%s | Rating: %.1f⭐ | Downloads: %d\n",
			listing.OwnerName,
			listing.Rating,
			listing.Downloads,
		)
		fmt.Printf("   Tags: %v\n\n", listing.Tags)
	}
}

// PrintMarketplaceStats 打印市场统计
func (mm *MapMarketplace) PrintMarketplaceStats() {
	stats := mm.GetStatistics()

	fmt.Println("\n╔════════════════════════════════════╗")
	fmt.Println("║      Marketplace Statistics      ║")
	fmt.Println("╚════════════════════════════════════╝")

	fmt.Printf("\nTotal Maps:         %d\n", stats["total_maps"])
	fmt.Printf("Total Downloads:    %d\n", stats["total_downloads"])
	fmt.Printf("Average Rating:     %.2f/5.0\n", stats["average_rating"])
	fmt.Printf("Unique Authors:     %d\n", stats["unique_authors"])

	difficultyCount := stats["maps_by_difficulty"].(map[string]int)
	if len(difficultyCount) > 0 {
		fmt.Println("\nMaps by Difficulty:")
		for difficulty, count := range difficultyCount {
			fmt.Printf("  %s: %d maps\n", difficulty, count)
		}
	}
}

// matchString 简单字符串匹配 (大小写不敏感)
func matchString(text, query string) bool {
	// Simple contains check
	if len(query) == 0 {
		return true
	}

	// This is a simple implementation
	// In production, consider using full-text search
	for i := 0; i <= len(text)-len(query); i++ {
		match := true
		for j := 0; j < len(query); j++ {
			if i+j >= len(text) || text[i+j] != query[j] {
				match = false
				break
			}
		}
		if match {
			return true
		}
	}
	return false
}
