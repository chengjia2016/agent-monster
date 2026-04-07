# Agent Monster - Data Flow & Migration Architecture

## Current State (As-Is)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Agent Monster System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GITHUB USER                                                    │
│       │                                                         │
│       ├─→ onboarding_manager.py                                │
│           │                                                     │
│           ├─→ user_manager.py ──────→ .monster/users/         │
│           │                          (JSON)                    │
│           │                                                     │
│           ├─→ economy_manager.py ──→ .monster/accounts/       │
│           │       │                  (JSON)                    │
│           │       └─→ shop_manager.py ──→ .monster/inventory/ │
│           │                             (JSON per-user)        │
│           │                                                     │
│           ├─→ egg_incubator.py ──────→ .monster/*_egg.json    │
│           │                           (JSON)                   │
│           │                                                     │
│           └─→ food_system.py ────────→ MEMORY ⚠️ LOST ON      │
│                   │                    RESTART!               │
│                   └─→ FoodManager()                            │
│                       [in-memory dict]                         │
│                                                                 │
│  BATTLE SYSTEM                                                  │
│       │                                                         │
│       └─→ battle_logic.py ────────────→ .monster/battles/     │
│                                        (Local files)           │
│                                                                 │
│  COOKIE SYSTEM                                                  │
│       │                                                         │
│       ├─→ cookie.py (generate) ─────→ Code files (comments)   │
│       ├─→ cookie.py (scan) ──────────→ MEMORY ⚠️ NO          │
│       │                               PERSISTENCE              │
│       └─→ food_explorer.py ──────────→ GitHub API search      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ISSUES:
  ⚠️  Food system: data lost on restart
  ⚠️  Cookie system: no persistent storage
  ❌  No Judge Server integration
  ❌  No offline fallback
```

---

## Target State (To-Be)

```
┌──────────────────────────────────────────────────────────────────┐
│               Agent Monster Distributed System                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  PRIMARY: JUDGE SERVER (Source of Truth)                         │
│  ────────────────────────────────────────────                   │
│  http://agentmonster.openx.pro:10000                            │
│  ┌─────────────────────────────────────────┐                   │
│  │ PostgreSQL Database                     │                   │
│  │ ┌──────────────────────────────────┐   │                   │
│  │ │ user_accounts                    │   │  ✅ Ready         │
│  │ │ pokemons                         │   │  ✅ Ready         │
│  │ │ inventory                        │   │  ✅ Ready         │
│  │ │ transactions                     │   │  ✅ Ready         │
│  │ │ battles                          │   │  ✅ Ready         │
│  │ │ ────────────────────────────     │   │                   │
│  │ │ eggs                    (NEW)    │   │  ❌ NEEDS SCHEMA  │
│  │ │ farms                   (NEW)    │   │  ❌ NEEDS SCHEMA  │
│  │ │ foods                   (NEW)    │   │  ❌ NEEDS SCHEMA  │
│  │ │ cookie_fragments        (NEW)    │   │  ❌ NEEDS SCHEMA  │
│  │ └──────────────────────────────────┘   │                   │
│  │ API Endpoints                          │                   │
│  │ /api/users/*                ✅         │                   │
│  │ /api/user/balance/*         ✅         │                   │
│  │ /api/user/pokemons/*        ✅         │                   │
│  │ /api/user/inventory/*       ✅         │                   │
│  │ /api/user/transactions/*    ✅         │                   │
│  │ /api/farms/*            ❌ NEEDS      │                   │
│  │ /api/foods/*            ❌ NEEDS      │                   │
│  │ /api/eggs/*             ❌ NEEDS      │                   │
│  │ /api/cookies/*          ❌ NEEDS      │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                   │
│  CLIENT SIDE: .monster/ (Local Cache)                            │
│  ────────────────────────────────────────────                   │
│  ┌─────────────────────────────────────────┐                   │
│  │ users/                    (mirrored)     │                   │
│  │ accounts/                 (mirrored)     │                   │
│  │ inventory/                (mirrored)     │                   │
│  │ user_cache/               (hybrid mgr)   │                   │
│  │ battles/                  (mirrored)     │                   │
│  │ eggs/                     (mirrored)     │                   │
│  │ farms/                    (mirrored)     │                   │
│  │ foods/                    (mirrored)     │                   │
│  │ cookies/                  (mirrored)     │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                   │
│  HYBRID SYNC LAYER                                              │
│  ────────────────────────────────────────────                   │
│  ┌─────────────────────────────────────────┐                   │
│  │ User Request                            │                   │
│  │  │                                      │                   │
│  │  ├─→ Try Judge Server (5s timeout)     │                   │
│  │  │   ├─→ Success: Use + Cache          │                   │
│  │  │   └─→ Fail/Timeout: Use Cache       │                   │
│  │  │                                      │                   │
│  │  └─→ Queue sync for later (async)      │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

KEY IMPROVEMENTS:
  ✅  All data persists on Judge Server
  ✅  Local cache for offline access
  ✅  Automatic sync when connection restored
  ✅  No data loss on restart
  ✅  True distributed architecture
```

---

## Data Flow: New User Registration

### Current Flow (Broken)
```
GitHub OAuth
    │
    └─→ onboarding_manager.register_from_github()
        │
        ├─→ user_manager.register_user()
        │   └─→ .monster/users/{user_id}.json ⚠️ Local only
        │
        ├─→ economy_manager.create_account()
        │   └─→ .monster/accounts/{user_id}.json ⚠️ Local only
        │
        ├─→ shop_manager (grant items)
        │   └─→ .monster/inventory/{user_id}.json ⚠️ Local only
        │
        ├─→ egg_incubator (create egg)
        │   └─→ .monster/{user_id}_egg.json ⚠️ Local only
        │
        └─→ food_system (create farm)
            └─→ MEMORY ONLY ⚠️ LOST ON RESTART
```

### Target Flow (Proposed)
```
GitHub OAuth
    │
    └─→ onboarding_manager.register_from_github()
        │
        ├─→ hybrid_user_data_manager.save_user_data()
        │   │
        │   ├─→ 1. Save to .monster/user_cache/ (instant)
        │   │
        │   └─→ 2. Sync to Judge Server (async)
        │       ├─→ POST /api/users/create
        │       ├─→ POST /api/user/balance/update (100 coins)
        │       ├─→ POST /api/user/inventory/add (starter items)
        │       ├─→ POST /api/user/pokemons/add (starter pet)
        │       ├─→ POST /api/eggs/create
        │       └─→ POST /api/farms/create
        │
        └─→ Return to user (cache ready immediately)
```

---

## Data Flow: Food Consumption

### Current (Doesn't Work)
```
User Finds Farm
    │
    ├─→ food_explorer.py (find on GitHub) ✓
    │
    ├─→ food_system.get_farm() 
    │   └─→ MEMORY ✗ NOT FOUND (if different process/restart)
    │
    └─→ FOOD LOST ✗
```

### Target (Proposed)
```
User Finds Farm
    │
    ├─→ food_explorer.py (find on GitHub) ✓
    │
    ├─→ hybrid_user_data_manager.get_farm()
    │   │
    │   ├─→ Try: GET /api/farms/{owner}/{repo}
    │   │   └─→ Success: Use + cache to .monster/farms/
    │   │
    │   └─→ Fail: Use .monster/farms/{owner}_{repo}.json
    │
    ├─→ Consume food: POST /api/foods/consume
    │   ├─→ Success: Update local cache
    │   └─→ Fail: Queue for retry
    │
    └─→ FOOD CONSUMED ✓
```

---

## Data Flow: Cross-Repository Food Discovery

### Current (Partially Working)
```
User's Farm (repo A)
    │
    └─→ food_explorer.py
        │
        ├─→ GitHub Search API
        │   └─→ Find .monster/farm.yaml files
        │
        └─→ Results (No persistence)
            ├─→ Display to user ✓
            └─→ Data lost on restart ✗
```

### Target (Full Implementation)
```
User's Farm (repo A)
    │
    └─→ food_explorer.py
        │
        ├─→ GitHub Search API
        │   └─→ GET /search/repositories?q="filename:.monster/farm.yaml"
        │
        ├─→ For each farm found:
        │   │
        │   ├─→ GET /api/farms/{owner}/{repo} (from Judge Server)
        │   │   ├─→ Cache to .monster/farms/
        │   │   └─→ Store farm metadata
        │   │
        │   ├─→ GET /api/foods/farm/{farm_id}
        │   │   └─→ List all foods in farm
        │   │
        │   └─→ Display food options to user
        │
        └─→ User selects food
            │
            ├─→ POST /api/foods/consume
            │   ├─→ Validate: owner != consumer
            │   ├─→ Check: quantity > 0
            │   ├─→ Record: eating history
            │   └─→ Response: nutrition values
            │
            ├─→ Add to user's pet: exp/energy
            │
            └─→ FOOD CONSUMED ✓
```

---

## Cookie Collection Data Flow

### Current (Incomplete)
```
Developer writes code
    │
    ├─→ cookie.py generate
    │   └─→ Insert comment: # 🍪 agent_monster cookie 0x...
    │
    ├─→ Commit to GitHub ✓
    │
    └─→ cookie.py scan (manual)
        ├─→ Find cookies in code ✓
        └─→ NOWHERE TO PERSIST ✗
```

### Target (Proposed)
```
Developer writes code
    │
    ├─→ cookie.py generate
    │   └─→ Insert comment: # 🍪 agent_monster cookie 0x...
    │
    ├─→ Commit to GitHub ✓
    │
    ├─→ GitHub Webhook (new)
    │   └─→ Judge Server notified of commit
    │
    ├─→ Judge Server scans commit
    │   └─→ POST /api/cookies/discover
    │       └─→ Store in cookie_fragments table
    │
    ├─→ User plays game
    │   │
    │   ├─→ GET /api/cookies/search?repo={repo}
    │   │
    │   ├─→ Display available cookies
    │   │
    │   ├─→ User claims: POST /api/cookies/claim
    │   │   ├─→ Verify: cookie not already claimed
    │   │   ├─→ Verify: timestamp valid (not too old)
    │   │   ├─→ Record: claimed_by_github_id + timestamp
    │   │   └─→ Response: nutrition/rewards
    │   │
    │   └─→ Add to pet or food bank
    │
    └─→ COOKIE CLAIMED ✓
```

---

## Offline Mode Data Flow

### Server Down Scenario
```
User performs action
    │
    ├─→ hybrid_user_data_manager.get_user_data()
    │   │
    │   ├─→ Try: GET http://judge-server/api/users/{github_id}
    │   │   │   (timeout: 5 seconds)
    │   │   │
    │   │   └─→ TIMEOUT or ERROR
    │   │
    │   ├─→ FALLBACK: Read .monster/user_cache/{github_id}.json
    │   │   └─→ Return cached data ✓
    │   │
    │   └─→ Queue action for sync later
    │
    └─→ User can continue playing ✓
        (Data will sync when connection restored)

When Server Comes Back Online
    │
    └─→ hybrid_user_data_manager.sync_all_to_server()
        │
        ├─→ For each queued action:
        │   ├─→ Retry POST/PUT request
        │   └─→ On success: mark complete
        │
        └─→ User data synchronized ✓
```

---

## Migration Execution Flow

### Phase 1: Create Schemas (Week 1)
```
PostgreSQL Judge Server
    │
    ├─→ CREATE TABLE eggs
    ├─→ CREATE TABLE farms
    ├─→ CREATE TABLE foods
    ├─→ CREATE TABLE eating_records
    └─→ CREATE TABLE cookie_fragments
```

### Phase 2: Create API Endpoints (Week 1-2)
```
Go Judge Server
    │
    ├─→ POST   /api/farms/create
    ├─→ GET    /api/farms/{owner}/{repo}
    ├─→ POST   /api/foods/add
    ├─→ GET    /api/foods/farm/{farm_id}
    ├─→ POST   /api/foods/consume
    ├─→ POST   /api/eggs/create
    ├─→ GET    /api/eggs/{github_id}
    ├─→ GET    /api/cookies/search
    └─→ POST   /api/cookies/claim
```

### Phase 3: Update Local Systems (Week 2-3)
```
Python Client
    │
    ├─→ Update food_system.py
    │   └─→ Use FoodManager with Judge Server backend
    │
    ├─→ Update cookie.py
    │   └─→ Add Judge Server persistence
    │
    ├─→ Update egg_incubator.py
    │   └─→ Use Judge Server storage
    │
    └─→ Update onboarding_manager.py
        └─→ Use hybrid_user_data_manager
```

### Phase 4: Data Migration (Week 3-4)
```
Existing Data
    │
    ├─→ migrate_to_judge_server.py
    │   ├─→ Export: .monster/users/ → Judge Server
    │   ├─→ Export: .monster/accounts/ → Judge Server
    │   ├─→ Export: .monster/inventory/ → Judge Server
    │   └─→ Verify: No data loss
    │
    └─→ Validate checksums ✓
```

---

## Summary: Key Transitions

| System | Current | Target | Status |
|--------|---------|--------|--------|
| Users | Local JSON | Judge Server | ✅ Ready |
| Economy | Local JSON | Judge Server | ✅ Ready |
| Inventory | Local JSON | Judge Server | ✅ Ready |
| Battles | Local files | Judge Server | ✅ Ready |
| Food | MEMORY ⚠️ | Judge Server ❌ | CRITICAL |
| Cookies | Scanning | Judge Server ❌ | CRITICAL |
| Eggs | Local JSON | Judge Server ❌ | NEEDED |
| Fallback | None | Local cache ✅ | READY |

---

**Architecture Ready**: 80%  
**Implementation Ready**: 40%  
**Effort Remaining**: 35-40 hours  
**Timeline**: 1 week + testing  

