# CLI Screen Implementation Testing Plan

## Test Environment

- **Judge Server**: http://127.0.0.1:10000
- **CLI Binary**: `/root/pet/agent-monster/cli/agent-monster`
- **Test Date**: 2026-04-08

## Test Scenarios

### 1. GitHub Integration Tests

#### Test 1.1: GitHub Login Check
- **Objective**: Verify GitHub CLI authentication detection
- **Steps**:
  1. Run CLI and navigate to GitHub Integration screen
  2. Check if login status is detected
  3. Verify proper error message if not logged in
- **Expected Result**: ✅ Shows login status or guidance

#### Test 1.2: Repository Listing
- **Objective**: Fetch and display user repositories
- **Steps**:
  1. Navigate to "GitHub Integration" → "查看我的仓库"
  2. Wait for async loading
  3. Verify repositories display with stars/forks
- **Expected Result**: ✅ Shows list of repositories with metadata

#### Test 1.3: Issues Display
- **Objective**: Show GitHub issues from first repository
- **Steps**:
  1. Navigate to "GitHub Integration" → "查看Issues"
  2. Wait for loading
  3. Verify issues display with status
- **Expected Result**: ✅ Shows open/closed issues with proper icons

#### Test 1.4: Pull Requests Display
- **Objective**: Show GitHub PRs from first repository
- **Steps**:
  1. Navigate to "GitHub Integration" → "查看Pull Requests"
  2. Wait for loading
  3. Verify PRs display with status
- **Expected Result**: ✅ Shows open/closed PRs with proper icons

### 2. Pokemon Management Tests

#### Test 2.1: Pokemon List Loading
- **Objective**: Load Pokemon from judge-server API
- **Steps**:
  1. Navigate to "我的宠物"
  2. Check if Pokemon list loads
  3. Verify fallback to mock data if API unavailable
- **Expected Result**: ✅ Shows Pokemon list or mock data

#### Test 2.2: Pokemon Detail Display with Sprite
- **Objective**: Display Pokemon details with colored ASCII sprite
- **Steps**:
  1. Select a Pokemon from list
  2. Verify sprite displays correctly
  3. Check stats are displayed properly
- **Expected Result**: ✅ Shows Pokemon sprite and stats

#### Test 2.3: Wild Pokemon Capture List
- **Objective**: Load wild Pokemon from API
- **Steps**:
  1. Navigate to "捕获精灵"
  2. Verify wild Pokemon load or show mock data
  3. Check rarity color coding
- **Expected Result**: ✅ Shows wild Pokemon with rarity colors

#### Test 2.4: Sprite Rendering
- **Objective**: Verify colored sprites display correctly
- **Steps**:
  1. Check sprite data contains ANSI codes
  2. Verify terminal renders colors properly
  3. Test with different Pokemon names
- **Expected Result**: ✅ Sprites display in colors

### 3. User Profile Tests

#### Test 3.1: Profile Information Display
- **Objective**: Display user profile with GitHub data and game stats
- **Steps**:
  1. Navigate to "个人资料"
  2. Verify GitHub user info displays
  3. Check game stats are shown
- **Expected Result**: ✅ Shows complete profile with all sections

#### Test 3.2: Experience Progress Bar
- **Objective**: Verify progress bar calculation and display
- **Steps**:
  1. View profile screen
  2. Check progress bar renders correctly
  3. Verify percentage matches experience value
- **Expected Result**: ✅ Progress bar displays correctly

### 4. Navigation Tests

#### Test 4.1: Screen Navigation Flow
- **Objective**: Test navigation between screens
- **Steps**:
  1. Navigate from Main Menu → GitHub → Repos → Back → Main Menu
  2. Test other navigation paths
  3. Verify proper state management
- **Expected Result**: ✅ All transitions work smoothly

#### Test 4.2: Keyboard Controls
- **Objective**: Verify keyboard navigation works
- **Steps**:
  1. Test arrow keys (up/down)
  2. Test enter key (select)
  3. Test ESC/H key (back)
  4. Test Ctrl+C (quit)
- **Expected Result**: ✅ All controls respond correctly

### 5. API Integration Tests

#### Test 5.1: Judge-Server API Calls
- **Objective**: Verify API client makes correct requests
- **Steps**:
  1. Check GetPokemon endpoint
  2. Check ListWildPokemon endpoint
  3. Verify error handling
- **Expected Result**: ✅ APIs respond or gracefully handle errors

#### Test 5.2: GitHub API Integration
- **Objective**: Verify GitHub API calls work
- **Steps**:
  1. Verify gh CLI token retrieval
  2. Test repository fetch
  3. Test issues/PRs fetch
- **Expected Result**: ✅ GitHub API calls succeed

### 6. Error Handling Tests

#### Test 6.1: Network Error Handling
- **Objective**: Handle judge-server unavailability
- **Steps**:
  1. Stop judge-server
  2. Navigate to Pokemon screens
  3. Verify fallback to mock data
- **Expected Result**: ✅ Shows mock data, no crash

#### Test 6.2: GitHub Unavailable
- **Objective**: Handle GitHub API errors
- **Steps**:
  1. Disconnect network or use invalid token
  2. Navigate to GitHub screens
  3. Verify error display
- **Expected Result**: ✅ Shows error message gracefully

### 7. UI/UX Tests

#### Test 7.1: Color Display
- **Objective**: Verify colored text displays properly
- **Steps**:
  1. Check title colors
  2. Check selected item highlighting
  3. Check sprite colors in detail screens
- **Expected Result**: ✅ Colors display correctly

#### Test 7.2: Text Truncation
- **Objective**: Verify long text truncates properly
- **Steps**:
  1. Check repository descriptions truncate
  2. Check issue titles truncate
  3. Verify no text overflow
- **Expected Result**: ✅ Text truncates cleanly

#### Test 7.3: Loading Indicators
- **Objective**: Verify loading state display
- **Steps**:
  1. Navigate to GitHub screens
  2. Check loading indicator appears
  3. Verify it disappears when data loads
- **Expected Result**: ✅ Loading indicator works

### 8. Performance Tests

#### Test 8.1: Async Loading Performance
- **Objective**: Verify async data loading doesn't block UI
- **Steps**:
  1. Navigate to GitHub screens
  2. Try to navigate while loading
  3. Check UI remains responsive
- **Expected Result**: ✅ UI responsive during loading

#### Test 8.2: Memory Usage
- **Objective**: Verify reasonable memory footprint
- **Steps**:
  1. Run CLI
  2. Navigate through multiple screens
  3. Check memory doesn't grow excessively
- **Expected Result**: ✅ Reasonable memory usage

## Test Execution Log

### Date: 2026-04-08

#### Pre-test Setup
- [✓] Judge-server running on port 10000
- [✓] CLI binary built successfully (8.4MB)
- [✓] GitHub CLI configured
- [✓] User profile data ready

#### Test Results

| Test ID | Category | Test Name | Status | Notes |
|---------|----------|-----------|--------|-------|
| 1.1 | GitHub | Login Check | PENDING | To be tested |
| 1.2 | GitHub | Repository Listing | PENDING | To be tested |
| 1.3 | GitHub | Issues Display | PENDING | To be tested |
| 1.4 | GitHub | Pull Requests Display | PENDING | To be tested |
| 2.1 | Pokemon | List Loading | PENDING | To be tested |
| 2.2 | Pokemon | Detail with Sprite | PENDING | To be tested |
| 2.3 | Pokemon | Wild Pokemon List | PENDING | To be tested |
| 2.4 | Pokemon | Sprite Rendering | PENDING | To be tested |
| 3.1 | Profile | Profile Display | PENDING | To be tested |
| 3.2 | Profile | Progress Bar | PENDING | To be tested |
| 4.1 | Navigation | Screen Flow | PENDING | To be tested |
| 4.2 | Navigation | Keyboard Controls | PENDING | To be tested |
| 5.1 | API | Judge-Server APIs | PENDING | To be tested |
| 5.2 | API | GitHub APIs | PENDING | To be tested |
| 6.1 | Error Handling | Network Error | PENDING | To be tested |
| 6.2 | Error Handling | GitHub Error | PENDING | To be tested |
| 7.1 | UI/UX | Color Display | PENDING | To be tested |
| 7.2 | UI/UX | Text Truncation | PENDING | To be tested |
| 7.3 | UI/UX | Loading Indicators | PENDING | To be tested |
| 8.1 | Performance | Async Loading | PENDING | To be tested |
| 8.2 | Performance | Memory Usage | PENDING | To be tested |

## Test Summary

- **Total Tests**: 21
- **Passed**: 0
- **Failed**: 0
- **Pending**: 21

## Next Steps

1. Execute all tests manually
2. Document results
3. Fix any issues found
4. Move to battle system integration
5. Implement game mechanics

## Known Issues

- None yet (awaiting testing)

## Recommendations

1. Test in different terminal sizes
2. Test with different Pokemon types
3. Test with large repository counts
4. Add more comprehensive logging
5. Consider adding test fixtures/mock server
