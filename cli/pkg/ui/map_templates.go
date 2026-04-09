package ui

// MapTemplate defines a map style template for onboarding
type MapTemplate struct {
	ID          string
	Name        string
	Description string
	Emoji       string
	Difficulty  string
	TerrainType map[string]int // percentage distribution
	NPCs        []NPC
	Features    []string
}

// NPC represents an NPC character
type NPC struct {
	ID          string
	Name        string
	Type        string // trainer, shopkeeper, healer, elder
	Description string
	Emoji       string
	Dialogue    string
	Position    string // e.g., "center", "north", "south"
}

// GetMapTemplates returns all available map templates
func GetMapTemplates() []MapTemplate {
	return []MapTemplate{
		{
			ID:          "grassland",
			Name:        "🌾 绿草之地",
			Description: "初心者的起源地 - 和平的草原，适合新手探险",
			Emoji:       "🌾",
			Difficulty:  "简单",
			TerrainType: map[string]int{
				"grass":    70,
				"forest":   15,
				"water":    10,
				"mountain": 5,
			},
			NPCs: []NPC{
				{
					ID:          "mentor_oak",
					Name:        "橡树博士",
					Type:        "elder",
					Description: "友善的老研究员，会给予新手建议",
					Emoji:       "👴",
					Dialogue:    "欢迎来到这片绿草之地！我叫橡树博士，有什么问题可以问我。",
					Position:    "center",
				},
				{
					ID:          "trader_berry",
					Name:        "莓莓商人",
					Type:        "shopkeeper",
					Description: "友好的商人，售卖果实和食物",
					Emoji:       "🍓",
					Dialogue:    "需要什么吗？我这里有最新鲜的浆果！",
					Position:    "east",
				},
				{
					ID:          "healer_lily",
					Name:        "莉莉医生",
					Type:        "healer",
					Description: "温柔的医生，可以治疗宠物",
					Emoji:       "💊",
					Dialogue:    "欢迎来到诊所，让我看看你的宠物吧。",
					Position:    "west",
				},
			},
			Features: []string{"安全区域", "新手教程", "友好NPC"},
		},
		{
			ID:          "forest",
			Name:        "🌲 古老森林",
			Description: "神秘的森林 - 各种野生宝可梦和冒险等待着你",
			Emoji:       "🌲",
			Difficulty:  "中等",
			TerrainType: map[string]int{
				"forest":   50,
				"grass":    30,
				"water":    10,
				"mountain": 10,
			},
			NPCs: []NPC{
				{
					ID:          "ranger_green",
					Name:        "绿色护林员",
					Type:        "trainer",
					Description: "资深的护林员，教会你野外生存",
					Emoji:       "🧑‍🌾",
					Dialogue:    "这片森林是我的家！我会教你如何在这里生存。",
					Position:    "center",
				},
				{
					ID:          "potion_master",
					Name:        "药水大师",
					Type:        "shopkeeper",
					Description: "神秘的药剂师，出售稀有的药水",
					Emoji:       "🧪",
					Dialogue:    "这些是我自己配制的药水，质量最好！",
					Position:    "north",
				},
				{
					ID:          "tracker_wolf",
					Name:        "狼人追踪者",
					Type:        "trainer",
					Description: "追踪大师，可以找到稀有宝可梦",
					Emoji:       "🐺",
					Dialogue:    "想找到罕见的宝可梦吗？我知道它们在哪里。",
					Position:    "south",
				},
			},
			Features: []string{"野生宝可梦丰富", "冒险挑战", "稀有资源"},
		},
		{
			ID:          "ocean",
			Name:        "🌊 蓝色海岸",
			Description: "宁静的海边 - 水类宝可梦的天堂",
			Emoji:       "🌊",
			Difficulty:  "中等",
			TerrainType: map[string]int{
				"water":    60,
				"grass":    20,
				"sand":     15,
				"mountain": 5,
			},
			NPCs: []NPC{
				{
					ID:          "captain_sail",
					Name:        "帆船船长",
					Type:        "trainer",
					Description: "经验丰富的船长，拥有强大的水系宠物",
					Emoji:       "⛵",
					Dialogue:    "大海是自由的！加入我的冒险吧。",
					Position:    "center",
				},
				{
					ID:          "fisher_bob",
					Name:        "鱼夫鲍勃",
					Type:        "shopkeeper",
					Description: "渔民，出售各种鱼类宝可梦",
					Emoji:       "🎣",
					Dialogue:    "今天的鱼获真不错！要看看吗？",
					Position:    "east",
				},
				{
					ID:          "mermaid_coral",
					Name:        "珊瑚美人鱼",
					Type:        "healer",
					Description: "神秘的美人鱼，掌握海洋魔法",
					Emoji:       "🧜‍♀️",
					Dialogue:    "海洋的魔力可以治愈一切伤痛。",
					Position:    "west",
				},
			},
			Features: []string{"水系宝可梦", "航海任务", "宝藏寻找"},
		},
		{
			ID:          "mountain",
			Name:        "⛰️  雪山峰顶",
			Description: "险峻的山脉 - 强大的训练者的挑战地",
			Emoji:       "⛰️",
			Difficulty:  "困难",
			TerrainType: map[string]int{
				"mountain": 60,
				"snow":     25,
				"grass":    10,
				"water":    5,
			},
			NPCs: []NPC{
				{
					ID:          "master_frost",
					Name:        "霜冻大师",
					Type:        "trainer",
					Description: "冰系宝可梦的大师，实力高强",
					Emoji:       "🧊",
					Dialogue:    "只有最强的训练者才能在这里生存。敢来试试吗？",
					Position:    "center",
				},
				{
					ID:          "smith_forge",
					Name:        "锻造大师",
					Type:        "shopkeeper",
					Description: "古老的铁匠，打造特殊的装备",
					Emoji:       "🔨",
					Dialogue:    "我的装备可以承受任何风险！",
					Position:    "north",
				},
				{
					ID:          "sage_snow",
					Name:        "白雪贤者",
					Type:        "elder",
					Description: "在山顶修行多年的贤者",
					Emoji:       "🧙",
					Dialogue:    "山顶的风雪让人思考生命的意义...",
					Position:    "south",
				},
			},
			Features: []string{"高难度挑战", "冰系宝可梦", "传奇装备"},
		},
		{
			ID:          "desert",
			Name:        "🏜️  金色沙漠",
			Description: "广阔的沙漠 - 古老的遗迹和神秘的秘密",
			Emoji:       "🏜️",
			Difficulty:  "中等",
			TerrainType: map[string]int{
				"sand":     70,
				"grass":    15,
				"mountain": 10,
				"water":    5,
			},
			NPCs: []NPC{
				{
					ID:          "explorer_sphinx",
					Name:        "狮身人面怪探险家",
					Type:        "trainer",
					Description: "古老沙漠的探险者，知道所有秘密",
					Emoji:       "🗿",
					Dialogue:    "沙漠中隐藏着许多古老的秘密...你想发现它们吗？",
					Position:    "center",
				},
				{
					ID:          "nomad_desert",
					Name:        "游牧民阿拉",
					Type:        "shopkeeper",
					Description: "在沙漠中游牧的商人",
					Emoji:       "🐪",
					Dialogue:    "在沙漠中，任何东西都值钱！",
					Position:    "east",
				},
				{
					ID:          "archaeologist_dig",
					Name:        "考古学家迪格",
					Type:        "elder",
					Description: "研究古代文明的学者",
					Emoji:       "🔍",
					Dialogue:    "这些遗迹讲述了古代的故事...",
					Position:    "west",
				},
			},
			Features: []string{"古代遗迹", "稀有发现", "沙系宝可梦"},
		},
	}
}

// NPCType defines different NPC roles
const (
	NPCTypeTrainer    = "trainer"    // 可以对战
	NPCTypeShopkeeper = "shopkeeper" // 可以交易
	NPCTypeHealer     = "healer"     // 可以治疗
	NPCTypeElder      = "elder"      // 可以提供建议
)

// Difficulty levels
const (
	DifficultyEasy   = "简单"
	DifficultyMedium = "中等"
	DifficultyHard   = "困难"
)
