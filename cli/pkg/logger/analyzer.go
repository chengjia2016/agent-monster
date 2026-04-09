package logger

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strings"
	"time"
)

// LogEntry represents a single log entry
type LogEntry struct {
	Timestamp  time.Time
	Level      string
	Message    string
	RawLine    string
	LineNumber int
}

// LogAnalysis contains analysis results
type LogAnalysis struct {
	TotalLines      int
	ErrorCount      int
	WarnCount       int
	InfoCount       int
	DebugCount      int
	APICallCount    int
	APIErrorCount   int
	AverageDuration time.Duration
	Errors          []LogEntry
	Warnings        []LogEntry
	APIRequests     []LogEntry
	APIErrors       []LogEntry
	SessionDuration time.Duration
	StartTime       time.Time
	EndTime         time.Time
	StatusSummary   map[string]int
	ErrorPatterns   map[string]int // Common error patterns
}

// AnalyzeLogFile analyzes a log file and returns analysis results
func AnalyzeLogFile(logPath string) (*LogAnalysis, error) {
	file, err := os.Open(logPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	analysis := &LogAnalysis{
		StatusSummary: make(map[string]int),
		ErrorPatterns: make(map[string]int),
	}

	scanner := bufio.NewScanner(file)
	lineNum := 0

	for scanner.Scan() {
		lineNum++
		line := scanner.Text()
		analysis.TotalLines++

		// Parse log entry
		entry := parseLogEntry(line, lineNum)
		if entry == nil {
			continue
		}

		// Count by level
		switch entry.Level {
		case "ERROR":
			analysis.ErrorCount++
			analysis.Errors = append(analysis.Errors, *entry)
			extractErrorPattern(entry.Message, analysis.ErrorPatterns)
		case "WARN":
			analysis.WarnCount++
			analysis.Warnings = append(analysis.Warnings, *entry)
		case "INFO":
			analysis.InfoCount++
		case "DEBUG":
			analysis.DebugCount++
		}

		// Count API calls
		if strings.Contains(entry.Message, "API Request") {
			analysis.APICallCount++
			analysis.APIRequests = append(analysis.APIRequests, *entry)
		}

		// Count API errors
		if strings.Contains(entry.Message, "API Error") {
			analysis.APIErrorCount++
			analysis.APIErrors = append(analysis.APIErrors, *entry)
		}

		// Track time range
		if entry.Timestamp.IsZero() == false {
			if analysis.StartTime.IsZero() {
				analysis.StartTime = entry.Timestamp
			}
			analysis.EndTime = entry.Timestamp
		}
	}

	// Calculate session duration
	if !analysis.StartTime.IsZero() && !analysis.EndTime.IsZero() {
		analysis.SessionDuration = analysis.EndTime.Sub(analysis.StartTime)
	}

	return analysis, scanner.Err()
}

// parseLogEntry parses a single log line
func parseLogEntry(line string, lineNum int) *LogEntry {
	// Pattern: [HH:MM:SS.mmm] [LEVEL] message
	re := regexp.MustCompile(`\[(\d{2}:\d{2}:\d{2}\.\d{3})\] \[([A-Z]+)\] (.*)`)
	matches := re.FindStringSubmatch(line)

	if len(matches) < 4 {
		// Try to handle section headers and other formats
		if strings.Contains(line, "───") || strings.Contains(line, "═══") || strings.Contains(line, "▶") {
			return &LogEntry{
				Level:      "SECTION",
				Message:    line,
				RawLine:    line,
				LineNumber: lineNum,
			}
		}
		return nil
	}

	entry := &LogEntry{
		Level:      matches[2],
		Message:    matches[3],
		RawLine:    line,
		LineNumber: lineNum,
	}

	// Parse timestamp
	timeStr := matches[1]
	parsedTime, err := time.Parse("15:04:05.000", timeStr)
	if err == nil {
		// Use today's date with the parsed time
		now := time.Now()
		entry.Timestamp = time.Date(now.Year(), now.Month(), now.Day(),
			parsedTime.Hour(), parsedTime.Minute(), parsedTime.Second(),
			parsedTime.Nanosecond(), now.Location())
	}

	return entry
}

// extractErrorPattern extracts common error patterns
func extractErrorPattern(message string, patterns map[string]int) {
	// Extract error type (text before colon)
	if idx := strings.Index(message, ":"); idx > 0 {
		errorType := strings.TrimSpace(message[:idx])
		patterns[errorType]++
	}
}

// PrintSummary prints a summary of the analysis
func (a *LogAnalysis) PrintSummary() {
	fmt.Println("\n═══════════════════════════════════════════════════════════")
	fmt.Println("📊 Log Analysis Summary")
	fmt.Println("═══════════════════════════════════════════════════════════")

	fmt.Printf("\n📈 Statistics:\n")
	fmt.Printf("  Total Lines:        %d\n", a.TotalLines)
	fmt.Printf("  Session Duration:   %v\n", a.SessionDuration)
	if !a.StartTime.IsZero() {
		fmt.Printf("  Start Time:         %s\n", a.StartTime.Format("15:04:05"))
	}
	if !a.EndTime.IsZero() {
		fmt.Printf("  End Time:           %s\n", a.EndTime.Format("15:04:05"))
	}

	fmt.Printf("\n📋 Log Levels:\n")
	fmt.Printf("  INFO:               %d\n", a.InfoCount)
	fmt.Printf("  DEBUG:              %d\n", a.DebugCount)
	fmt.Printf("  WARN:               %d\n", a.WarnCount)
	fmt.Printf("  ERROR:              %d ❌\n", a.ErrorCount)

	fmt.Printf("\n🌐 API Statistics:\n")
	fmt.Printf("  Total API Calls:    %d\n", a.APICallCount)
	fmt.Printf("  API Errors:         %d ❌\n", a.APIErrorCount)

	if len(a.Errors) > 0 {
		fmt.Printf("\n❌ Errors (%d):\n", len(a.Errors))
		for i, err := range a.Errors {
			if i >= 5 {
				fmt.Printf("  ... and %d more\n", len(a.Errors)-5)
				break
			}
			fmt.Printf("  [Line %d] %s\n", err.LineNumber, err.Message)
		}
	}

	if len(a.ErrorPatterns) > 0 {
		fmt.Printf("\n🎯 Error Patterns:\n")
		// Sort error patterns by frequency
		type patternCount struct {
			pattern string
			count   int
		}
		var patterns []patternCount
		for pattern, count := range a.ErrorPatterns {
			patterns = append(patterns, patternCount{pattern, count})
		}
		sort.Slice(patterns, func(i, j int) bool {
			return patterns[i].count > patterns[j].count
		})

		for i, pc := range patterns {
			if i >= 5 {
				fmt.Printf("  ... and %d more patterns\n", len(patterns)-5)
				break
			}
			fmt.Printf("  [%d] %s\n", pc.count, pc.pattern)
		}
	}

	if len(a.Warnings) > 0 {
		fmt.Printf("\n⚠️  Warnings (%d):\n", len(a.Warnings))
		for i, warn := range a.Warnings {
			if i >= 3 {
				fmt.Printf("  ... and %d more\n", len(a.Warnings)-3)
				break
			}
			fmt.Printf("  [Line %d] %s\n", warn.LineNumber, warn.Message)
		}
	}

	fmt.Println("\n═══════════════════════════════════════════════════════════")
}

// PrintHealthCheck prints a health check report
func (a *LogAnalysis) PrintHealthCheck() {
	fmt.Println("\n═══════════════════════════════════════════════════════════")
	fmt.Println("🏥 Session Health Check")
	fmt.Println("═══════════════════════════════════════════════════════════")

	health := 100
	issues := []string{}

	// Check for errors
	if a.ErrorCount > 0 {
		health -= (a.ErrorCount * 5)
		issues = append(issues, fmt.Sprintf("Found %d errors", a.ErrorCount))
	}

	// Check for API errors
	if a.APIErrorCount > 0 {
		health -= (a.APIErrorCount * 10)
		issues = append(issues, fmt.Sprintf("Found %d API errors", a.APIErrorCount))
	}

	// Check for warnings
	if a.WarnCount > 0 {
		health -= (a.WarnCount * 2)
		issues = append(issues, fmt.Sprintf("Found %d warnings", a.WarnCount))
	}

	// Check API call success rate
	if a.APICallCount > 0 {
		successRate := float64(a.APICallCount-a.APIErrorCount) / float64(a.APICallCount) * 100
		if successRate < 80 {
			health -= 20
			issues = append(issues, fmt.Sprintf("API success rate low: %.1f%%", successRate))
		}
	}

	// Clamp health to 0-100
	if health < 0 {
		health = 0
	}

	// Print health score
	healthBar := getHealthBar(health)
	fmt.Printf("\n%s Health Score: %d/100\n", healthBar, health)

	if health == 100 {
		fmt.Println("\n✅ Session completed successfully!")
	} else if health >= 80 {
		fmt.Println("\n✅ Session completed with minor issues")
	} else if health >= 50 {
		fmt.Println("\n⚠️  Session completed with some issues")
	} else {
		fmt.Println("\n❌ Session completed with significant issues")
	}

	if len(issues) > 0 {
		fmt.Println("\n🔍 Issues Found:")
		for _, issue := range issues {
			fmt.Printf("  • %s\n", issue)
		}
	}

	fmt.Println("\n═══════════════════════════════════════════════════════════")
}

// getHealthBar returns a visual health bar
func getHealthBar(health int) string {
	bar := "["
	filled := health / 10
	for i := 0; i < 10; i++ {
		if i < filled {
			bar += "█"
		} else {
			bar += "░"
		}
	}
	bar += "]"

	if health >= 80 {
		return "🟢 " + bar
	} else if health >= 50 {
		return "🟡 " + bar
	} else {
		return "🔴 " + bar
	}
}

// PrintDetailedReport prints a detailed report
func (a *LogAnalysis) PrintDetailedReport() {
	a.PrintSummary()
	a.PrintHealthCheck()

	// Print API calls details
	if len(a.APIRequests) > 0 {
		fmt.Println("\n🌐 API Requests Details:")
		for i, req := range a.APIRequests {
			if i >= 10 {
				fmt.Printf("  ... and %d more\n", len(a.APIRequests)-10)
				break
			}
			fmt.Printf("  [%s] %s\n", req.Timestamp.Format("15:04:05"), req.Message)
		}
	}

	// Print API errors details
	if len(a.APIErrors) > 0 {
		fmt.Println("\n❌ API Error Details:")
		for i, apiErr := range a.APIErrors {
			if i >= 10 {
				fmt.Printf("  ... and %d more\n", len(a.APIErrors)-10)
				break
			}
			fmt.Printf("  [%s] %s\n", apiErr.Timestamp.Format("15:04:05"), apiErr.Message)
		}
	}
}

// GetErrorReport returns a formatted error report
func (a *LogAnalysis) GetErrorReport() string {
	if a.ErrorCount == 0 && a.APIErrorCount == 0 {
		return "✅ No errors found"
	}

	report := "Error Report:\n"
	report += fmt.Sprintf("  Errors: %d\n", a.ErrorCount)
	report += fmt.Sprintf("  API Errors: %d\n", a.APIErrorCount)

	if len(a.ErrorPatterns) > 0 {
		report += "\nTop Error Patterns:\n"
		type patternCount struct {
			pattern string
			count   int
		}
		var patterns []patternCount
		for pattern, count := range a.ErrorPatterns {
			patterns = append(patterns, patternCount{pattern, count})
		}
		sort.Slice(patterns, func(i, j int) bool {
			return patterns[i].count > patterns[j].count
		})

		for i, pc := range patterns {
			if i >= 3 {
				break
			}
			report += fmt.Sprintf("    %d. %s (%d)\n", i+1, pc.pattern, pc.count)
		}
	}

	return report
}
