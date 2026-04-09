package ui

import (
	"agent-monster-cli/pkg/github"
	"agent-monster-cli/pkg/pokemon"
	"fmt"
	"strings"

	"github.com/charmbracelet/lipgloss"
)

// RenderPokemonList 渲染宠物列表 - with mini sprites
func (a *App) RenderPokemonList() string {
	title := StyleTitle.Render("🐾 我的宠物列表")

	// Check if user is authenticated
	if a.CurrentUser == nil || a.CurrentUser.ID == 0 {
		errorMsg := StyleError.Render("❌ 错误：未登录或获取用户信息失败")
		controls := StyleDim.Render("BackSpace/H 返回主菜单")
		return title + "\n\n" + errorMsg + "\n\n" + controls
	}

	// 从judge-server获取宠物数据（使用GitHub ID）
	pokemons, err := a.Client.GetUserPokemons(a.CurrentUser.ID)
	if err != nil {
		errorMsg := StyleError.Render(fmt.Sprintf("❌ 获取宠物失败: %v", err))
		controls := StyleDim.Render("BackSpace/H 返回主菜单")
		return title + "\n\n" + errorMsg + "\n\n" + controls
	}

	// 如果没有宠物，显示空状态
	if len(pokemons) == 0 {
		emptyMsg := StyleMenuItem.Render("  暂无宠物，前往【野生宠物捕捉】捕捉你的第一个宠物！")
		controls := StyleDim.Render("BackSpace/H 返回主菜单")
		return title + "\n\n" + emptyMsg + "\n\n" + controls
	}

	// 渲染宠物列表
	var items strings.Builder
	for i, p := range pokemons {
		var line string
		if i == a.SelectedIndex {
			line = StyleMenuItemSelected.Render(fmt.Sprintf(
				"  %-15s Lv.%-3d HP: %2d/%2d [%s]",
				p.Name,
				p.Level,
				p.CurrentHP,
				p.MaxHP,
				p.Type,
			))
		} else {
			line = StyleMenuItem.Render(fmt.Sprintf(
				"  %-15s Lv.%-3d HP: %2d/%2d [%s]",
				p.Name,
				p.Level,
				p.CurrentHP,
				p.MaxHP,
				p.Type,
			))
		}
		items.WriteString(line + "\n")
	}

	controls := StyleDim.Render("⬆️ ⬇️  选择  Enter 查看详情  H 返回")
	return title + "\n\n" + items.String() + "\n" + controls
}

// RenderBattleScreen 渲染战斗屏幕
func (a *App) RenderBattleScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("208")).Render("⚔️  发起战斗")

	battleOptions := []string{
		"选择对手进行PvP战斗",
		"查看战斗记录",
		"战斗统计",
		"返回主菜单",
	}

	var menu strings.Builder
	for i, option := range battleOptions {
		if i == a.SelectedIndex {
			menu.WriteString(StyleMenuItemSelected.Render(fmt.Sprintf("  ▶ %s", option)) + "\n")
		} else {
			menu.WriteString(StyleMenuItem.Render(fmt.Sprintf("    %s", option)) + "\n")
		}
	}

	return title + "\n\n" + menu.String()
}

// RenderDefenseScreen 渲染防守基地屏幕
func (a *App) RenderDefenseScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("32")).Render("🏰 防守基地")

	// 基地信息卡片
	baseInfo := StyleBox.Render(
		StyleBold.Render("基地信息") + "\n" +
			"  位置: 中国 - 深圳\n" +
			"  等级: 5\n" +
			"  卫士: 3只精灵\n" +
			"  防守记录: 12胜 3负\n",
	)

	defenseOptions := []string{
		"创建基地",
		"查看卫士队伍",
		"防守历史记录",
		"基地升级",
		"返回主菜单",
	}

	var menu strings.Builder
	for i, option := range defenseOptions {
		if i == a.SelectedIndex {
			menu.WriteString(StyleMenuItemSelected.Render(fmt.Sprintf("  ▶ %s", option)) + "\n")
		} else {
			menu.WriteString(StyleMenuItem.Render(fmt.Sprintf("    %s", option)) + "\n")
		}
	}

	return title + "\n\n" + baseInfo + "\n" + menu.String()
}

// RenderWildPokemonScreen 渲染野生精灵屏幕
func (a *App) RenderWildPokemonScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("63")).Render("🌍 捕获野生精灵")

	// 从API获取野生精灵数据
	wildPokemons, err := a.Client.ListWildPokemon()
	if err != nil {
		errorMsg := StyleError.Render(fmt.Sprintf("❌ 获取野生精灵失败: %v", err))
		controls := StyleDim.Render("BackSpace/H 返回主菜单")
		return title + "\n\n" + errorMsg + "\n\n" + controls
	}

	// 如果没有野生精灵，显示空状态
	if len(wildPokemons) == 0 {
		emptyMsg := StyleMenuItem.Render("  暂无可捕获的野生精灵")
		controls := StyleDim.Render("BackSpace/H 返回主菜单")
		return title + "\n\n" + emptyMsg + "\n\n" + controls
	}

	// 渲染野生精灵列表
	var items strings.Builder
	for i, p := range wildPokemons {
		var rarity string
		switch r := p.Rarity; r {
		case "常见":
			rarity = StyleSuccess.Render(r)
		case "普通":
			rarity = StyleWarning.Render(r)
		case "罕见":
			rarity = StyleError.Render(r)
		default:
			rarity = r
		}

		var line string
		if i == a.SelectedIndex {
			line = StyleMenuItemSelected.Render(fmt.Sprintf(
				"  %-15s Lv.%-2d [%-4s] %s",
				p.Name,
				p.Level,
				rarity,
				p.Location,
			))
		} else {
			line = StyleMenuItem.Render(fmt.Sprintf(
				"  %-15s Lv.%-2d [%-4s] %s",
				p.Name,
				p.Level,
				rarity,
				p.Location,
			))
		}
		items.WriteString(line + "\n")
	}

	controls := StyleDim.Render("⬆️ ⬇️  选择  Enter 捕获  H 返回")

	return title + "\n\n" + items.String() + "\n" + controls
}

// RenderDetailScreen 渲染详情屏幕 - with colored sprite
func (a *App) RenderDetailScreen() string {
	title := StyleTitle.Render("📊 宠物详情")

	// Check if we have selected Pokemon data
	if len(a.UserProfile.Pokemons) == 0 || a.SelectedIndex >= len(a.UserProfile.Pokemons) {
		// Show error state
		errorMsg := StyleError.Render("❌ 错误：无法获取宠物详情")
		controls := StyleDim.Render("H 返回列表")
		return title + "\n\n" + errorMsg + "\n\n" + controls
	}

	selectedPokemon := a.UserProfile.Pokemons[a.SelectedIndex]

	// Import pokemon package functions
	spriteDisplay := renderPokemonSprite(selectedPokemon.Name)

	details := StyleBox.Render(
		StyleBold.Render(selectedPokemon.Name) + " [" + selectedPokemon.Species + "]\n\n" +
			spriteDisplay + "\n\n" +
			fmt.Sprintf("等级: %d\n", selectedPokemon.Level) +
			fmt.Sprintf("经验: %d\n", 0) +
			fmt.Sprintf("生命值: %d / %d\n", selectedPokemon.HP, selectedPokemon.MaxHP) +
			fmt.Sprintf("攻击: %d\n", selectedPokemon.Attack) +
			fmt.Sprintf("防守: %d\n", selectedPokemon.Defense) +
			fmt.Sprintf("速度: %d\n", selectedPokemon.Speed) +
			fmt.Sprintf("状态: %s\n", selectedPokemon.Status),
	)

	controls := StyleDim.Render("H 返回列表")

	return title + "\n\n" + details + "\n" + controls
}

// renderPokemonSprite renders a Pokemon sprite with proper formatting
func renderPokemonSprite(pokemonName string) string {
	// Get the sprite from the pokemon package
	if !pokemon.PokemonExists(pokemonName) {
		return StyleDim.Render("[精灵: " + pokemonName + " - 未找到精灵数据]")
	}

	// Get the full sprite
	sprite := pokemon.GetSmallSprite(pokemonName)
	if sprite == "" {
		return StyleDim.Render("[精灵: " + pokemonName + " - 无可用精灵]")
	}

	// Split into lines and join with proper spacing
	lines := strings.Split(sprite, "\n")
	var result strings.Builder
	result.WriteString("\n")
	for _, line := range lines {
		if line != "" {
			result.WriteString(line + "\n")
		}
	}

	return result.String()
}

// RenderStatus 渲染状态栏
func (a *App) RenderStatus() string {
	status := fmt.Sprintf("服务器: %s | 屏幕: %d | 选项: %d", a.Client.BaseURL, a.CurrentScreen, a.SelectedIndex)
	return StyleDim.Render(status)
}

// renderLoginScreen renders the GitHub login screen
func (a *App) renderLoginScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("33")).Render("🔐 GitHub 登录")

	if github.IsGitHubLoggedIn() {
		// User is already logged in
		return title + "\n\n" + StyleBox.Render(
			StyleSuccess.Render("✅ 已登录 GitHub")+"\n\n"+
				"按 Enter 继续...",
		)
	}

	return title + "\n\n" + StyleBox.Render(
		"需要 GitHub CLI 登录\n\n"+
			"请先安装 GitHub CLI: https://cli.github.com\n"+
			"然后运行: gh auth login\n\n"+
			"按 Enter 打开登录...",
	)
}

// renderGitHubScreen renders the GitHub integration screen
func (a *App) renderGitHubScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("33")).Render("💻 GitHub 集成")

	options := []string{
		"查看我的仓库",
		"查看 Issues",
		"查看 Pull Requests",
		"返回主菜单",
	}

	var menu strings.Builder
	for i, option := range options {
		if i == a.SelectedIndex {
			menu.WriteString(StyleMenuItemSelected.Render(fmt.Sprintf("  ▶ %s", option)) + "\n")
		} else {
			menu.WriteString(StyleMenuItem.Render(fmt.Sprintf("    %s", option)) + "\n")
		}
	}

	return title + "\n\n" + menu.String()
}

// renderGitHubReposScreen renders the GitHub repositories screen
func (a *App) renderGitHubReposScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("33")).Render("📦 我的仓库")

	// If no repos loaded, fetch them
	if len(a.GitHubState.Repositories) == 0 {
		return title + "\n\n" + StyleBox.Render("获取仓库列表中...\n\n请等待或按 H 返回")
	}

	var items strings.Builder
	for i, repo := range a.GitHubState.Repositories {
		var line string
		status := ""
		if repo.IsPrivate {
			status = "🔒"
		} else {
			status = "🔓"
		}

		if i == a.SelectedIndex {
			line = StyleMenuItemSelected.Render(fmt.Sprintf(
				"  %s %-25s ⭐ %-3d 🍴 %-2d",
				status,
				truncateString(repo.Name, 25),
				repo.Stars,
				repo.Forks,
			))
		} else {
			line = StyleMenuItem.Render(fmt.Sprintf(
				"  %s %-25s ⭐ %-3d 🍴 %-2d",
				status,
				truncateString(repo.Name, 25),
				repo.Stars,
				repo.Forks,
			))
		}
		items.WriteString(line + "\n")

		// Show description if available
		if repo.Description != "" && i == a.SelectedIndex {
			items.WriteString(StyleDim.Render("    📝 "+truncateString(repo.Description, 60)) + "\n")
		}
	}

	controls := StyleDim.Render("⬆️ ⬇️  选择  H 返回")
	return title + "\n\n" + items.String() + "\n" + controls
}

// renderGitHubIssuesScreen renders the GitHub issues screen
func (a *App) renderGitHubIssuesScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("33")).Render("🐛 Issues")

	if len(a.GitHubState.Issues) == 0 {
		return title + "\n\n" + StyleBox.Render("获取 Issues 中...\n\n请等待或按 H 返回")
	}

	var items strings.Builder
	for i, issue := range a.GitHubState.Issues {
		stateIcon := "🟢"
		if issue.State == "closed" {
			stateIcon = "🔴"
		}

		var line string
		if i == a.SelectedIndex {
			line = StyleMenuItemSelected.Render(fmt.Sprintf(
				"  %s #%-4d %s",
				stateIcon,
				issue.Number,
				truncateString(issue.Title, 60),
			))
		} else {
			line = StyleMenuItem.Render(fmt.Sprintf(
				"  %s #%-4d %s",
				stateIcon,
				issue.Number,
				truncateString(issue.Title, 60),
			))
		}
		items.WriteString(line + "\n")
	}

	controls := StyleDim.Render("⬆️ ⬇️  选择  H 返回")
	return title + "\n\n" + items.String() + "\n" + controls
}

// renderGitHubPullRequestsScreen renders the GitHub pull requests screen
func (a *App) renderGitHubPullRequestsScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("33")).Render("📝 Pull Requests")

	if len(a.GitHubState.PullRequests) == 0 {
		return title + "\n\n" + StyleBox.Render("获取 PRs 中...\n\n请等待或按 H 返回")
	}

	var items strings.Builder
	for i, pr := range a.GitHubState.PullRequests {
		stateIcon := "🟢"
		if pr.State == "closed" {
			stateIcon = "🔴"
		}

		var line string
		if i == a.SelectedIndex {
			line = StyleMenuItemSelected.Render(fmt.Sprintf(
				"  %s #%-4d %s",
				stateIcon,
				pr.Number,
				truncateString(pr.Title, 60),
			))
		} else {
			line = StyleMenuItem.Render(fmt.Sprintf(
				"  %s #%-4d %s",
				stateIcon,
				pr.Number,
				truncateString(pr.Title, 60),
			))
		}
		items.WriteString(line + "\n")
	}

	controls := StyleDim.Render("⬆️ ⬇️  选择  H 返回")
	return title + "\n\n" + items.String() + "\n" + controls
}

// Helper function to truncate strings
func truncateString(s string, maxLen int) string {
	if len(s) > maxLen {
		return s[:maxLen-3] + "..."
	}
	return s
}

// renderProfileScreen renders the user profile screen
func (a *App) renderProfileScreen() string {
	title := StyleTitle.Foreground(lipgloss.Color("213")).Render("👤 个人资料")

	if a.CurrentUser == nil || a.UserProfile == nil {
		return title + "\n\n未加载用户信息"
	}

	// Calculate level progress
	nextLevelExp := a.UserProfile.Level * 1000
	expProgress := (a.UserProfile.Experience % 1000) * 100 / 1000
	if nextLevelExp == 0 {
		nextLevelExp = 1000
	}

	progressBar := generateProgressBar(expProgress, 20)

	info := StyleBox.Render(
		StyleBold.Render("GitHub 账户") + "\n" +
			fmt.Sprintf("  用户名: %s\n", a.CurrentUser.Login) +
			fmt.Sprintf("  名称: %s\n", a.CurrentUser.Name) +
			fmt.Sprintf("  公开仓库: %d\n", a.CurrentUser.PublicRepos) +
			"\n" +
			StyleBold.Render("游戏信息") + "\n" +
			fmt.Sprintf("  等级: %d\n", a.UserProfile.Level) +
			fmt.Sprintf("  经验值: %d / %d\n", a.UserProfile.Experience%1000, 1000) +
			fmt.Sprintf("  进度: %s %d%%\n", progressBar, expProgress) +
			fmt.Sprintf("  余额: ¥%.2f\n", a.UserProfile.Balance) +
			"\n" +
			StyleBold.Render("精灵及队伍") + "\n" +
			fmt.Sprintf("  精灵数: %d\n", len(a.UserProfile.Pokemons)) +
			fmt.Sprintf("  队伍数: %d\n", len(a.UserProfile.Teams)) +
			"\n" +
			StyleBold.Render("账户创建") + "\n" +
			fmt.Sprintf("  创建时间: %s\n", a.UserProfile.CreatedAt.Format("2006-01-02 15:04")),
	)

	controls := StyleDim.Render("BackSpace/H 返回主菜单")

	return title + "\n\n" + info + "\n" + controls
}

// Helper function to generate a progress bar
func generateProgressBar(percent int, width int) string {
	filled := (percent * width) / 100
	bar := strings.Repeat("█", filled) + strings.Repeat("░", width-filled)
	return fmt.Sprintf("[%s]", bar)
}
