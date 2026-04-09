package ui

import "github.com/charmbracelet/lipgloss"

// Color scheme
const (
	ColorPrimary    = lipgloss.Color("205")
	ColorAccent     = lipgloss.Color("39")
	ColorSuccess    = lipgloss.Color("42")
	ColorWarning    = lipgloss.Color("226")
	ColorError      = lipgloss.Color("196")
	ColorText       = lipgloss.Color("250")
	ColorDim        = lipgloss.Color("243")
	ColorBackground = lipgloss.Color("235")
)

// Style definitions
var (
	StyleTitle = lipgloss.NewStyle().
			Foreground(ColorWarning).
			Bold(true).
			MarginBottom(1)

	StyleSubtitle = lipgloss.NewStyle().
			Foreground(ColorPrimary).
			Bold(true).
			MarginBottom(1)

	StyleMenuItem = lipgloss.NewStyle().
			Padding(0, 2).
			BorderLeft(true).
			BorderStyle(lipgloss.RoundedBorder()).
			PaddingLeft(2)

	StyleMenuItemSelected = lipgloss.NewStyle().
				Padding(0, 2).
				Background(ColorAccent).
				Foreground(lipgloss.Color("0")).
				Bold(true).
				BorderLeft(true).
				BorderStyle(lipgloss.RoundedBorder()).
				PaddingLeft(2)

	StyleBox = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			Padding(1).
			MarginBottom(1)

	StyleBold = lipgloss.NewStyle().Bold(true)

	StyleDim = lipgloss.NewStyle().
			Foreground(ColorDim)

	StyleSuccess = lipgloss.NewStyle().
			Foreground(ColorSuccess).
			Bold(true)

	StyleError = lipgloss.NewStyle().
			Foreground(ColorError).
			Bold(true)

	StyleWarning = lipgloss.NewStyle().
			Foreground(ColorWarning).
			Bold(true)
)

// Border styles
var (
	BorderDouble = "║  "
	BorderSingle = "│  "
	BorderDot    = "•  "
)
