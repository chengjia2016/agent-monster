# Agent Monster Codebase Audit Report
**Generated: April 7, 2026**

## Executive Summary

This audit identifies all data models and features in the Agent Monster codebase that require migration to the Judge Server, their current storage locations, and implementation status. The system is designed to transition from local JSON storage to a centralized Judge Server with local caching fallback.

---

## 1. DATA MODELS & FEATURES MIGRATION CHECKLIST

### User Accounts
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: Local JSON files (`.monster/users/`)
- **Data Model**: `User` class in `user_manager.py`
- **Judge Server Schema**: `UserAccount` in `judge_server_schema.py`
- **Fields**:
  - `user_id`: UUID (local-only)
  - `github_login`: GitHub username
  - `github_id`: GitHub numeric ID (primary key for Judge Server)
  - `email`, `avatar_url`
  - `registered_at`, `last_login`
- **Implementation**: User manager handles local storage; hybrid manager handles sync
- **Files**:
  - `/root/pet/agent-monster/user_manager.py` (local storage)
  - `/root/pet/agent-monster/judge_server_user_manager.py` (server interface)
  - `/root/pet/agent-monster/hybrid_user_data_manager.py` (fallback mechanism)

### User Inventory (Items)
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: Local JSON per-user files (`.monster/inventory/`)
- **Data Model**: `ShopItem` class in `shop_manager.py`
- **Judge Server Schema**: `Item` in `judge_server_schema.py`
- **Fields**:
  - `item_id`: Unique item identifier
  - `name`: Display name
  - `quantity`: Amount owned
  - `rarity`: Item rarity level
  - `added_at`: Acquisition timestamp
- **Implementation**: Shop manager handles CRUD; can be synced via hybrid manager
- **Files**:
  - `/root/pet/agent-monster/shop_manager.py` (inventory management)
  - `GET/POST /api/user/inventory/*` endpoints on Judge Server

### Pets/Pokemon
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: Local JSON files (`.monster/*_starter_pet.json`)
- **Data Model**: `Pokemon` class in `judge_server_schema.py`
- **Judge Server Schema**: Implemented in schema
- **Fields**:
  - `id`, `name`, `species`
  - `level`, `exp`
  - `hp`, `max_hp`, `attack`, `defense`, `sp_attack`, `sp_defense`, `speed`
  - `moves` (list of move names)
  - `caught_at`
- **Implementation**: Local files exist; Judge Server endpoints ready
- **Files**:
  - `judge_server_schema.py` (data model)
  - `POST /api/user/pokemons/add` (add pokemon)
  - `GET /api/user/pokemons/get?github_id={id}` (list pokemons)

### Eggs
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: Local JSON files (`.monster/*_egg.json`)
- **Data Model**: Egg data in `egg_incubator.py`
- **Judge Server Schema**: Not explicitly defined, should be created
- **Fields**:
  - `id`, `name`
  - `incubation_time_remaining`
  - `hatch_time`, `created_at`
  - `owner_github_id`
- **Implementation**: Egg files exist locally; migration needed
- **Files**:
  - `/root/pet/agent-monster/egg_incubator.py` (egg creation)
  - `/root/pet/agent-monster/.monster/*_egg.json` (local storage)
  - **TODO**: Create `Egg` model in `judge_server_schema.py`

### Shop Items & Global Inventory
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: Centralized JSON file (`.monster/shop.json`)
- **Data Model**: `ShopItem` in `shop_manager.py`
- **Judge Server Schema**: Not explicitly defined (global, not per-user)
- **Fields**:
  - `item_id`, `name`, `description`
  - `item_type` (enum)
  - `price`, `stock`, `max_stock`
- **Implementation**: Shop manager maintains catalog locally
- **Files**:
  - `/root/pet/agent-monster/shop_manager.py`
  - **TODO**: Create `/api/shop/*` endpoints on Judge Server for global catalog

### Battle History
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: Local files (`.monster/battles/`)
- **Data Model**: `BattleRecord` in `judge_server_schema.py`
- **Judge Server Schema**: Implemented
- **Fields**:
  - `battle_id`, `player1_github_id`, `player2_github_id`
  - `player1_pokemon`, `player2_pokemon` (lists of IDs)
  - `winner_github_id`, `prize_coins`
  - `timestamp`, `duration_seconds`
- **Implementation**: Battle records stored locally; schema ready for server
- **Files**:
  - `/root/pet/agent-monster/battle_logic.py` (battle system)
  - `/root/pet/agent-monster/judge_server_schema.py` (BattleRecord model)
  - **TODO**: Create `/api/battles/*` endpoints on Judge Server

### Food/Farm System
- **Status**: ⚠️ PARTIALLY IMPLEMENTED - NEEDS MIGRATION
- **Current Storage**: In-memory + optional YAML export (`.monster/farm.yaml`)
- **Data Model**: `Farm`, `Food` classes in `food_system.py`
- **Judge Server Schema**: Not defined - NEEDS CREATION
- **Features**:
  - Plant food in repositories (cookies, donuts, apples, genes)
  - Regeneration after consumption
  - Cross-repository food discovery and consumption
- **Fields** (`Food`):
  - `id`, `type` (FoodType enum), `quantity`, `max_quantity`
  - `regeneration_hours`, `last_eaten_at`
  - `eating_history` (list of eating records)
  - `seed` (hash)
- **Fields** (`Farm`):
  - `owner`, `repository`, `url`
  - `foods` (list), `planted_at`
- **Implementation**: FoodManager operates in-memory; data loss on restart
- **Files**:
  - `/root/pet/agent-monster/food_system.py` (core system)
  - `/root/pet/agent-monster/food_explorer.py` (discovery via GitHub)
  - **CRITICAL TODO**: Implement persistent storage on Judge Server
  - **CRITICAL TODO**: Implement cross-farm query endpoints

### Cookies (Fragments Collection)
- **Status**: ⚠️ PARTIALLY IMPLEMENTED - DESIGN INCOMPLETE
- **Current Storage**: Scanned from code files (in-memory, not persisted)
- **Data Model**: Cookie fragments generated in `cookie.py`
- **Judge Server Schema**: Not defined
- **Features**:
  - Generate cookie comments in code files: `🍪 agent_monster cookie 0xABC...`
  - Scan repositories for cookies
  - Track eaten cookies per user
- **Fields**:
  - `cookie_id`: Hash (0xABC...)
  - `type`: Cookie type enum (cookie, donut, apple, gene)
  - `file`: Source file path
  - `claimed`: Whether claimed by user
- **Implementation**: 
  - Generation works: `cookie.py generate`
  - Scanning works: `cookie.py scan`
  - Persistence NOT IMPLEMENTED
- **Files**:
  - `/root/pet/agent-monster/cookie.py`
  - **CRITICAL TODO**: Implement cookie fragment persistence
  - **CRITICAL TODO**: Implement claiming mechanism
  - **CRITICAL TODO**: Link to food bank system

### Farm Management
- **Status**: ⚠️ PARTIALLY IMPLEMENTED - NEEDS CENTRALIZATION
- **Current Storage**: YAML file + in-memory (`.monster/farm.yaml`)
- **Data Model**: `Farm` class in `food_system.py`
- **Judge Server Schema**: Not defined
- **Operations**:
  - Create farm (with owner/repo)
  - Add food to farm
  - Calculate regeneration status
  - Consume food with cross-repo discovery
  - Save/load farm data
- **Implementation**: In-memory `FoodManager` with optional YAML export
- **Files**:
  - `/root/pet/agent-monster/food_system.py`
  - `/root/pet/agent-monster/food_explorer.py` (GitHub discovery)
  - **CRITICAL TODO**: Move to persistent Judge Server storage
  - **CRITICAL TODO**: Implement GitHub event integration for farm updates

### Transactions/History
- **Status**: ✅ READY FOR MIGRATION
- **Current Storage**: 
  - Per-user JSON files (`.monster/accounts/`)
  - Append-only log (`.monster/transactions.jsonl`)
- **Data Model**: `Transaction` in `economy_manager.py` and `judge_server_schema.py`
- **Judge Server Schema**: Implemented in `judge_server_schema.py`
- **Transaction Types**:
  - `INITIAL_GRANT`, `PURCHASE`, `FOOD_SALE`, `FOOD_PURCHASE`
  - `BATTLE_REWARD`, `BATTLE_PENALTY`, `PET_SALE`, `AUCTION_SALE`, `SHOP_COMMISSION`
- **Fields**:
  - `id`, `user_id`, `amount`, `trans_type`
  - `description`, `metadata`, `created_at`
  - `balance_before`, `balance_after`
- **Implementation**: Economy manager tracks all transactions
- **Files**:
  - `/root/pet/agent-monster/economy_manager.py`
  - `/root/pet/agent-monster/judge_server_schema.py`
  - `GET /api/user/transactions/get?github_id={id}` endpoint available

---

## 2. TODO & UNIMPLEMENTED FEATURES SCAN

### Food System TODOs
```
File: food_system.py
- Line 226: calculate_food_status() - Working correctly but logic could be optimized
- Missing: Persistent database for farms (currently in-memory)
- Missing: Auto-sync to Judge Server on food state changes
- Missing: Rate limiting for food consumption across repos
```

### Cookie System TODOs
```
File: cookie.py
- Line 77-109: scan_file_for_cookies() - Works but only scans local filesystem
- Missing: Judge Server persistence for found cookies
- Missing: Cookie claiming mechanism
- Missing: Cookie expiration/validity checking
- Missing: Integration with food bank system

Known Issue: 
- os module imported but scan_directory_for_cookies() references undefined os
- (Line 115-123 will fail without import os statement)
```

### Farm Management TODOs
```
File: food_system.py
- Missing: Real persistence (not in-memory)
- Missing: GitHub integration to read .monster/farm.yaml from repos
- Missing: Cross-repository food discovery (partly done in food_explorer.py)
- Missing: Real-time farm state updates on Judge Server

File: food_explorer.py
- Line 71: GitHub search for farms working
- Missing: Automatic farm discovery scheduled task
- Missing: Farm leaderboard (skeleton exists, needs data)
```

### Transactions
```
File: economy_manager.py
- Status: Complete for local use
- Missing: Judge Server sync (via hybrid manager)
- Missing: Dispute resolution mechanism
```

### Battle System
```
File: battle_logic.py
- Status: Mechanics implemented
- Missing: Judge Server storage for battle records
- Missing: Battle replay storage and retrieval
- Missing: Leaderboard queries on Judge Server
```

---

## 3. LOCAL STORAGE vs JUDGE SERVER INTERACTION MAP

### Files That Interact With Local Storage

| File | Storage Type | Features |
|------|--------------|----------|
| `user_manager.py` | Local JSON | User profiles (`.monster/users/`) |
| `economy_manager.py` | Local JSON | Accounts, transactions (`.monster/accounts/`, `.monster/transactions.jsonl`) |
| `shop_manager.py` | Local JSON | Shop catalog, inventory (`.monster/shop.json`, `.monster/inventory/`) |
| `egg_incubator.py` | Local JSON | Egg data (`.monster/*_egg.json`) |
| `food_system.py` | In-memory + YAML | Farm data (`.monster/farm.yaml`) |
| `cookie.py` | File scanning | Cookie fragments in code files |
| `food_explorer.py` | GitHub API | Discovers farms from GitHub repos |
| `onboarding_manager.py` | Local JSON | Onboarding records (`.monster/onboarding.json`) |
| `battle_logic.py` | Local files | Battle records (`.monster/battles/`) |

### Files That Interact With Judge Server

| File | Integration Type | Endpoints Used |
|------|------------------|-----------------|
| `judge_server_user_manager.py` | API client | `/api/users/*`, `/api/user/balance/*`, `/api/user/pokemons/*`, `/api/user/inventory/*`, `/api/user/transactions/*` |
| `hybrid_user_data_manager.py` | Fallback logic | Wraps judge_server_user_manager with local cache |
| `migrate_to_judge_server.py` | Migration tool | Exports local data for server migration |
| `judge_server_client.py` | HTTP helper | Generic HTTP request wrapper |
| `mcp_judge_server_commands.py` | MCP commands | CLI interface to server operations |

---

## 4. MIGRATION STATUS SUMMARY TABLE

| Feature | Local Storage | Judge Server | Implementation | Priority | Blockers |
|---------|---------------|--------------|-----------------|----------|----------|
| **User Accounts** | JSON files | ✅ Ready | Hybrid manager | HIGH | None |
| **User Inventory** | JSON per-user | ✅ Ready | Shop manager | HIGH | Needs sync |
| **Pets/Pokemon** | JSON files | ✅ Ready | egg_incubator | HIGH | Needs endpoints |
| **Eggs** | JSON files | ❌ NOT DEFINED | Partial | HIGH | Create schema |
| **Shop Catalog** | JSON global | ❌ NOT DEFINED | Complete | MEDIUM | Create endpoints |
| **Battle History** | Local files | ✅ Ready | battle_logic | MEDIUM | Needs endpoints |
| **Food/Farms** | In-memory | ❌ NOT DEFINED | Partial | **CRITICAL** | Design architecture |
| **Cookies** | Code scanning | ❌ NOT DEFINED | Skeleton | **CRITICAL** | Design & implement |
| **Farm Management** | In-memory | ❌ NOT DEFINED | Partial | **CRITICAL** | Persistence layer |
| **Transactions** | JSON + log | ✅ Ready | Economy mgr | HIGH | Needs sync |

---

## 5. CRITICAL GAPS REQUIRING IMMEDIATE ACTION

### 1. **Food/Farm Persistence** (CRITICAL)
**Problem**: Food system only works in-memory. No persistent storage.
```python
# food_system.py line 143-144
class FoodManager:
    def __init__(self):
        self.farms: Dict[str, Farm] = {}  # <- Lost on restart!
```
**Solution Required**:
- Create `Farm`, `Food`, `EatingRecord` tables on Judge Server
- Implement `/api/farms/*` endpoints
- Add auto-save to Judge Server on food changes

### 2. **Cookie System Incomplete** (CRITICAL)
**Problem**: Can generate and scan cookies, but nowhere to persist them.
**Solution Required**:
- Create `CookieFragment` table on Judge Server
- Implement `/api/cookies/*` endpoints
- Add claiming mechanism with timestamp validation
- Link to food bank reward system

### 3. **Missing Judge Server Schemas** (CRITICAL)
**Not Defined**:
- `Egg` model
- `Farm` model  
- `Food` model
- `CookieFragment` model
- Global `Shop` / catalog system

### 4. **Cross-Repo Farm Discovery** (HIGH)
**Problem**: food_explorer.py can search GitHub but doesn't connect to food_system.py
**Solution Required**:
- Integrate farm discovery with persistent storage
- Add scheduled sync of discovered farms
- Implement farm rating/leaderboard

### 5. **Hybrid Manager Not Integrated** (MEDIUM)
**Problem**: Created but not wired into registration/normal operations
**Solution Required**:
- Update `onboarding_manager.py` to use HybridUserDataManager
- Add automatic sync on account changes
- Test fallback when server is down

---

## 6. FILE ORGANIZATION & STRUCTURE

### Current Directory Structure
```
.monster/
├── users/                 # User profiles (local JSON)
├── accounts/              # Balances & transactions (local JSON)
├── inventory/             # User item inventories (local JSON)
├── user_cache/            # Hybrid manager cache (local JSON)
├── battles/               # Battle records (local files)
├── pet.soul               # Pet/monster data
├── *_egg.json             # Egg data per user
├── *_starter_pet.json     # Starter pet data per user
├── shop.json              # Shop catalog (global)
├── farm.yaml              # Farm data (currently unused)
├── transactions.jsonl     # Transaction log (append-only)
├── sessions.json          # Active sessions
├── onboarding.json        # Onboarding records
└── menu_sessions.json     # Menu state
```

### Recommended Judge Server Schema Additions
```sql
-- Missing tables to implement
CREATE TABLE farms (
    id SERIAL PRIMARY KEY,
    owner VARCHAR NOT NULL,
    repository VARCHAR NOT NULL,
    url TEXT NOT NULL,
    planted_at TIMESTAMP,
    UNIQUE(owner, repository)
);

CREATE TABLE foods (
    id VARCHAR PRIMARY KEY,
    farm_id INTEGER NOT NULL REFERENCES farms(id),
    type VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    max_quantity INTEGER NOT NULL,
    regeneration_hours INTEGER NOT NULL,
    last_eaten_at TIMESTAMP,
    seed VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE eating_records (
    id SERIAL PRIMARY KEY,
    food_id VARCHAR NOT NULL REFERENCES foods(id),
    eater_github_id INTEGER NOT NULL,
    eater_pet_id VARCHAR,
    eat_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE eggs (
    id VARCHAR PRIMARY KEY,
    owner_github_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    hatch_time TIMESTAMP,
    species VARCHAR,
    stats JSONB,
    FOREIGN KEY (owner_github_id) REFERENCES user_accounts(github_id)
);

CREATE TABLE cookie_fragments (
    id VARCHAR PRIMARY KEY,
    type VARCHAR NOT NULL,
    file_path VARCHAR NOT NULL,
    repository VARCHAR,
    found_at TIMESTAMP NOT NULL,
    claimed_by_github_id INTEGER,
    claimed_at TIMESTAMP,
    valid_until TIMESTAMP
);
```

---

## 7. MIGRATION ROADMAP

### Phase 1: Schema & Endpoints (Week 1-2)
- [ ] Add Egg, Farm, Food, CookieFragment schemas to Judge Server
- [ ] Implement `/api/farms/*` endpoints
- [ ] Implement `/api/foods/*` endpoints
- [ ] Implement `/api/eggs/*` endpoints
- [ ] Implement `/api/cookies/*` endpoints
- [ ] Add `/api/shop/*` for global catalog

### Phase 2: System Integration (Week 2-3)
- [ ] Update `food_system.py` to use Judge Server endpoints
- [ ] Update `cookie.py` to persist fragments
- [ ] Update `egg_incubator.py` to use Judge Server storage
- [ ] Integrate HybridUserDataManager into onboarding flow
- [ ] Add persistence to `FoodManager`

### Phase 3: Data Migration (Week 3-4)
- [ ] Export existing local food data to Judge Server
- [ ] Migrate existing eggs to server
- [ ] Validate data integrity
- [ ] Implement fallback and sync logic

### Phase 4: Testing & Validation (Week 4+)
- [ ] Test with offline mode
- [ ] Load test with multiple concurrent users
- [ ] Verify cross-repo food discovery works
- [ ] Stress test farm system

---

## 8. RECOMMENDATIONS

### Immediate Actions (This Week)
1. **Define missing schemas** in Judge Server
2. **Create persistent storage** for food system
3. **Implement cookie persistence** mechanism
4. **Fix cookie.py import bug** (missing `import os`)

### Short-term (This Month)
1. Integrate HybridUserDataManager into normal flow
2. Migrate all local-only systems to Judge Server
3. Implement cross-farm discovery and sync
4. Add monitoring and sync status dashboard

### Long-term (Ongoing)
1. Optimize query performance for farms/food discovery
2. Implement food marketplace / trading
3. Add farm leveling/achievements
4. Build cookie collection mechanics

---

## Appendix: File Size Summary

| Component | Status | Files | LOC |
|-----------|--------|-------|-----|
| User Management | ✅ Ready | user_manager.py | 179 |
| Economy System | ✅ Ready | economy_manager.py | 381 |
| Shop System | ✅ Ready | shop_manager.py | 290 |
| Egg System | ⚠️ Partial | egg_incubator.py | 318 |
| Food System | ⚠️ Critical | food_system.py | 482 |
| Cookie System | ⚠️ Critical | cookie.py | 196 |
| Farm Discovery | ⚠️ Partial | food_explorer.py | 316 |
| Judge Server Schema | ✅ Ready | judge_server_schema.py | 219 |
| Judge Server Manager | ✅ Ready | judge_server_user_manager.py | 312+ |
| Hybrid Manager | ✅ Ready | hybrid_user_data_manager.py | 230+ |
| Migration Tool | ✅ Ready | migrate_to_judge_server.py | 254+ |

