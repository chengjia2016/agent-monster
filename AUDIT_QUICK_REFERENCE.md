# Agent Monster Migration Audit - Quick Reference

## Status at a Glance

```
✅ READY (5)          ⚠️ PARTIAL (3)        ❌ CRITICAL (2)
├─ User Accounts     ├─ Food/Farms        ├─ Cookie System
├─ Inventory         ├─ Farm Management   └─ Persistence Layer
├─ Pokemon           └─ Eggs (schema)
├─ Transactions
└─ Battle History
```

---

## 1-PAGE SUMMARY

### What's Ready to Move to Judge Server ✅
| System | Files | Status | Effort |
|--------|-------|--------|--------|
| Users | user_manager.py | Complete | 1h |
| Economy | economy_manager.py | Complete | 1h |
| Inventory | shop_manager.py | Complete | 2h |
| Transactions | economy_manager.py | Complete | 1h |
| Battles | battle_logic.py | Complete | 2h |

### What Needs Work First ⚠️ 
| System | Files | Problem | Fix Time |
|--------|-------|---------|----------|
| Food/Farms | food_system.py | In-memory only | 8h |
| Cookies | cookie.py | No persistence | 6h |
| Eggs | egg_incubator.py | No schema | 3h |

### Critical Blockers 🚫
1. **No Judge Server schemas** for: Eggs, Farms, Foods, Cookies
2. **No API endpoints** for: Farms, Foods, Cookies, Shop
3. **Food system not persistent** - data lost on restart
4. **Hybrid manager not wired** into normal operations

---

## Top 5 Priority Items

### 1. Create Judge Server Schemas (BLOCKING EVERYTHING)
**File**: judge-server/internal/model/

Create these models:
```go
type Egg struct { ... }
type Farm struct { ... }
type Food struct { ... }
type CookieFragment struct { ... }
```

**Effort**: 3 hours  
**Impact**: Unblocks 4 other features  
**Start**: TODAY

---

### 2. Implement Farm Persistence (CRITICAL)
**File**: food_system.py + Judge Server endpoints

Make FoodManager use Judge Server instead of in-memory dict.

**Effort**: 8 hours  
**Impact**: Food system actually works  
**Start**: After schemas done

---

### 3. Fix Cookie Persistence (CRITICAL)
**File**: cookie.py + Judge Server endpoints

Add claiming mechanism and Judge Server storage.

**Effort**: 6 hours  
**Impact**: Cookie collection works  
**Start**: After schemas done

---

### 4. Integrate Hybrid Manager (HIGH)
**File**: onboarding_manager.py

Use HybridUserDataManager for new users.

**Effort**: 2 hours  
**Impact**: Server sync works  
**Start**: Week 2

---

### 5. Test Offline Mode (HIGH)
**File**: All managers

Verify fallback when server down.

**Effort**: 4 hours  
**Impact**: System resilient  
**Start**: Week 3

---

## Known Bugs

### 🐛 cookie.py line 115
```python
def scan_directory_for_cookies(directory: str) -> list:
    for root, dirs, files in os.walk(directory):  # <- os not imported!
```
**Fix**: Add `import os` at top

### 🐛 food_system.py line 143
```python
class FoodManager:
    def __init__(self):
        self.farms: Dict[str, Farm] = {}  # Lost on restart!
```
**Fix**: Use Judge Server storage instead

---

## File Dependencies Map

```
Core Systems:
├─ user_manager.py → judge_server_user_manager.py ✓
├─ economy_manager.py → judge_server_schema.py ✓
├─ shop_manager.py → judge_server_schema.py ✓
├─ battle_logic.py → judge_server_schema.py ✓
├─ egg_incubator.py → ??? NO SCHEMA ✗
├─ food_system.py → ??? NO ENDPOINTS ✗
├─ cookie.py → ??? NO PERSISTENCE ✗
└─ food_explorer.py → GitHub API + ??? 

Integration:
├─ onboarding_manager.py → NOT USING hybrid_user_data_manager.py
├─ hybrid_user_data_manager.py → judge_server_user_manager.py
└─ migrate_to_judge_server.py → all above
```

---

## Quick Migration Checklist

**Week 1:**
- [ ] Create Egg/Farm/Food/Cookie schemas (3h)
- [ ] Create API endpoints stub (2h)
- [ ] Fix cookie.py import bug (15min)
- [ ] Update food_system.py to use server (4h)

**Week 2:**
- [ ] Implement cookie persistence (6h)
- [ ] Integrate hybrid manager (2h)
- [ ] Update egg_incubator.py (3h)
- [ ] Update onboarding flow (2h)

**Week 3:**
- [ ] Data migration testing (3h)
- [ ] Offline mode testing (4h)
- [ ] Load testing (3h)

**Week 4:**
- [ ] Production rollout
- [ ] Monitoring setup
- [ ] Documentation

---

## Storage Locations Reference

### Local JSON Files
```
.monster/
├── users/                          # User profiles
├── accounts/                       # Balances
├── inventory/                      # Items per user
├── *_starter_pet.json             # Pets
├── *_egg.json                     # Eggs
├── shop.json                      # Shop catalog (GLOBAL)
├── transactions.jsonl             # Transaction log
└── farm.yaml                      # Farm data (UNUSED)
```

### Judge Server Endpoints (Existing)
```
POST   /api/users/create
GET    /api/users/{github_id}
GET    /api/user/balance/get?github_id=...
POST   /api/user/balance/update
POST   /api/user/pokemons/add
GET    /api/user/pokemons/get?github_id=...
POST   /api/user/inventory/add
GET    /api/user/inventory/get?github_id=...
GET    /api/user/transactions/get?github_id=...
```

### Judge Server Endpoints (MISSING - MUST CREATE)
```
POST   /api/farms/create
GET    /api/farms/{owner}/{repo}
POST   /api/foods/add
GET    /api/foods/farm/{farm_id}
POST   /api/foods/consume
GET    /api/eggs/{github_id}
POST   /api/eggs/create
GET    /api/cookies/search
POST   /api/cookies/claim
GET    /api/shop/catalog
POST   /api/shop/restock
```

---

## System Architecture

### Current (Broken)
```
User → onboarding_manager → user_manager → .monster/users/ ✓
                         → economy_manager → .monster/accounts/ ✓
                         → food_system → MEMORY ✗
                         → cookie.py → NO STORAGE ✗
```

### Target (Proposed)
```
User → onboarding_manager → hybrid_user_data_manager → judge_server ✓
                         → food_system → judge_server ✓
                         → cookie.py → judge_server ✓
                         → egg_incubator → judge_server ✓
                         → battle_logic → judge_server ✓
                         
      + local cache fallback for offline mode ✓
```

---

## Effort Estimation

| Task | Hours | Difficulty | Start |
|------|-------|-----------|-------|
| Create schemas | 3 | Medium | TODAY |
| Create endpoints | 5 | Medium | +0.5d |
| Fix food persistence | 8 | Hard | +1d |
| Fix cookie system | 6 | Hard | +1d |
| Integrate hybrid | 2 | Easy | +2d |
| Update egg system | 3 | Medium | +2d |
| Testing & fixes | 8 | Medium | +3d |
| **TOTAL** | **35h** | - | **1 week** |

---

## Risk Assessment

🔴 **CRITICAL RISKS**
- Food data lost on restart (NO PERSISTENCE)
- Cookie system incomplete (NO STORAGE)
- No schemas defined for new features

🟡 **HIGH RISKS**
- Hybrid manager not integrated
- Cross-repo discovery not working
- Battle history not persisted

🟢 **LOW RISKS**
- User/account migration ready
- Judge Server infrastructure ready
- Tests and tools exist

---

## Success Criteria

✅ All data persists on Judge Server  
✅ Offline mode works with local cache  
✅ Food system persists across restarts  
✅ Cookies collected and tracked  
✅ Cross-repo discovery works  
✅ Zero data loss during migration  
✅ Sync latency < 5 seconds  

---

**Report Generated**: April 7, 2026  
**Status**: AUDIT COMPLETE - Ready for implementation
