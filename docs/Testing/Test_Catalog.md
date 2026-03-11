# Test Catalog — Codopia Platform

**Generated**: 2026-02-23  
**Repo**: AllienNova/Codopia @ `154343d`

---

## Legend

- **Type**: Unit / Integration / E2E
- **Scope**: Function, module, or flow being tested
- **Status**: Exists / Required (not yet written)

---

| TestID | Type | Scope | Preconditions | Steps | Expected Result | Linked ReqIDs | Linked ApiIDs | Linked ScreenIDs | Status |
|--------|------|-------|---------------|-------|-----------------|---------------|---------------|-------------------|--------|
| T-001 | Unit | `auth_service.determine_tier(age)` | None | Call with ages 3,5,7,8,10,12,13,15,18 | Returns `magic_workshop` for ≤7, `innovation_lab` for 8-12, `professional_studio` for 13+ | REQ-0007 | — | — | Required |
| T-002 | Unit | `auth_service.hash_password(pwd)` | None | Hash a password, verify format includes salt separator `:` | Returns `hash:salt` format string | REQ-0002 | — | — | Required |
| T-003 | Unit | `auth_service.verify_password(pwd, hashed)` | T-002 hash output | Verify correct password returns True, wrong password returns False | True for correct, False for incorrect | REQ-0003 | — | — | Required |
| T-004 | Unit | `auth_service.create_user_account(email, pwd, name)` | Empty users dict | Create user, verify returned dict has id, email, success=True | User object with UUID id | REQ-0002 | API-001 | — | Required |
| T-005 | Unit | `auth_service.create_user_account` (duplicate) | User already exists | Attempt to create duplicate email | Returns success=False, error="User already exists" | REQ-0002 | API-001 | — | Required |
| T-006 | Unit | `auth_service.sign_in_user(email, pwd)` | User created via T-004 | Sign in with correct credentials | Returns success=True, user object, session token | REQ-0003 | API-002 | — | Required |
| T-007 | Unit | `auth_service.sign_in_user` (wrong pwd) | User created via T-004 | Sign in with wrong password | Returns success=False, error="Invalid credentials" | REQ-0003 | API-002 | — | Required |
| T-008 | Unit | `ProfessorSparkle._check_safety(msg)` | Sparkle instance | Send messages containing forbidden topics | Returns (False, safety_response) | REQ-0014 | — | — | Required |
| T-009 | Unit | `ProfessorSparkle._check_safety(msg)` (safe) | Sparkle instance | Send normal coding question | Returns (True, "") | REQ-0014 | — | — | Required |
| T-010 | Unit | `ProfessorSparkle._check_safety(msg)` (emergency) | Sparkle instance | Send message with emergency keywords ("help", "scared") | Returns (False, emergency_response) | REQ-0014 | — | — | Required |
| T-011 | Unit | `ProfessorSparkle._get_age_appropriate_response_style(age)` | Sparkle instance | Call with ages 4,6,9,11,14 | Returns correct vocabulary/pace/emoji config per age bracket | REQ-0015 | — | — | Required |
| T-012 | Unit | `ProfessorSparkle._get_fallback_response(msg, session)` | Session with age=6, tier=Magic Workshop | Send "hello" message | Returns greeting with emojis and magical language | REQ-0013, REQ-0015 | — | — | Required |
| T-013 | Unit | `ProfessorSparkle._get_fallback_response(msg, session)` | Session with age=15, tier=Professional Studio | Send "hello" message | Returns professional greeting without excessive emojis | REQ-0013, REQ-0015 | — | — | Required |
| T-014 | Unit | `security.sanitizeInput(input)` | None | Pass strings with `<script>`, SQL injection, XSS payloads | Returns sanitized string with dangerous content removed | REQ-0026 | — | — | Required |
| T-015 | Unit | `security.validateProjectContent(content)` | None | Pass content with `eval()`, `document.write`, oversized content | Returns isValid=false with appropriate errors | REQ-0026 | — | — | Required |
| T-016 | Unit | `children.determineTierFromAge(age)` | None | Call with ages 5,7,8,12,13,18 | Returns correct tier_type enum values | REQ-0007 | — | — | Required |
| T-017 | Unit | `children.validateChildData(name, age)` | None | Empty name, name >100 chars, age <3, age >18, valid data | Returns error string or null | REQ-0009 | — | — | Required |
| T-018 | Unit | `children.formatLearningTime(minutes)` | None | Call with 30, 60, 90, 150 | Returns "30m", "1h", "1h 30m", "2h 30m" | REQ-0019 | — | — | Required |
| T-019 | Unit | `children.calculateProgressPercentage(completed, total)` | None | Call with (0,10), (5,10), (10,10), (0,0) | Returns 0, 50, 100, 0 | REQ-0019 | — | — | Required |
| T-020 | Unit | `children.getAchievementLevel(count)` | None | Call with 0, 5, 10, 25, 50 | Returns Beginner, Rising Star, Creative Developer, Expert Builder, Master Coder | REQ-0018 | — | — | Required |
| T-021 | Unit | `supabase_client.create_user(email, hash, name)` | Mocked Supabase | Create user, verify Supabase insert called | Returns user dict with id | REQ-0002 | — | ENT-001 | Required |
| T-022 | Unit | `supabase_client.create_user` (fallback) | Mocked Supabase (failing) | Create user when Supabase is down | Falls back to in-memory, returns user dict | REQ-0002 | — | ENT-001 | Required |
| T-023 | Unit | `supabase_client.create_child_profile(parent_id, name, age, tier)` | Mocked Supabase | Create child profile | Returns child dict with correct tier | REQ-0009 | API-005 | ENT-002 | Required |
| T-024 | Unit | `supabase_client.save_lesson_progress(child_id, lesson_id, data)` | Mocked Supabase | Save progress, verify upsert behavior | Returns True on success | REQ-0017 | API-006 | ENT-003 | Required |
| T-025 | Unit | `supabase_client.award_achievement(child_id, ach_id, data)` | Mocked Supabase | Award achievement | Returns True, verify insert called | REQ-0018 | API-007 | ENT-004 | Required |
| T-026 | Unit | `security.generateCSRFToken()` | None | Generate token | Returns 64-char hex string | REQ-0027 | — | — | Required |
| T-027 | Unit | `security.validateSession()` | localStorage with recent lastActivity | Validate session | Returns true | REQ-0028 | — | — | Required |
| T-028 | Unit | `security.validateSession()` (expired) | localStorage with 9-hour-old lastActivity | Validate session | Returns false | REQ-0028 | — | — | Required |
| T-029 | Integration | Flask signup flow | Flask test client | POST `/signup` with valid form data | 302 redirect to `/dashboard`, `auth_token` cookie set | REQ-0002 | API-001 | SCR-002 | Required |
| T-030 | Integration | Flask signin flow | User created via T-029 | POST `/signin` with correct credentials | 302 redirect to `/dashboard`, `auth_token` cookie set | REQ-0003 | API-002 | SCR-004 | Required |
| T-031 | Integration | Flask signin (invalid) | No user exists | POST `/signin` with wrong credentials | Redirect to `/signin?error=invalid_credentials` | REQ-0003 | API-002 | SCR-004 | Required |
| T-032 | Integration | Flask dashboard (auth required) | No auth cookie | GET `/dashboard` | 302 redirect to `/signin` | REQ-0008 | — | SCR-007 | Required |
| T-033 | Integration | Flask dashboard (authenticated) | Valid auth cookie | GET `/dashboard` | 200 with child cards HTML | REQ-0008 | — | SCR-007 | Required |
| T-034 | Integration | Flask Magic Workshop | Authenticated | GET `/learning/magic-workshop` | 200 with block coding interface HTML | REQ-0010 | — | SCR-009 | Required |
| T-035 | Integration | Socket.IO init_sparkle | Socket.IO test client | Emit `init_sparkle` with age=6, tier="Magic Workshop" | Receive `sparkle_ready` with session_id and welcome_message | REQ-0013 | EVT-001 | — | Required |
| T-036 | Integration | Socket.IO sparkle_message | Session initialized via T-035 | Emit `sparkle_message` with "Hello" | Receive `sparkle_response` with age-appropriate greeting | REQ-0013 | EVT-002 | — | Required |
| T-037 | Integration | Socket.IO safety check | Session initialized | Emit `sparkle_message` with forbidden content | Receive `sparkle_response` with safety redirect message | REQ-0014 | EVT-002 | — | Required |
| T-038 | Integration | Supabase health check | Supabase client initialized | Call `health_check()` | Returns True when Supabase is reachable | REQ-0032 | API-009 | — | Required |
| T-039 | E2E | Parent registration journey | Clean browser state | Visit `/signup` → Fill parent form → Submit → Add child (age 6) → Complete → Verify dashboard shows Magic Workshop child | Dashboard displays child card with "Magic Workshop" tier | REQ-0002, REQ-0007, REQ-0008, REQ-0009 | API-001, API-005 | SCR-002, SCR-003, SCR-007, SCR-008 | Required |
| T-040 | E2E | Parent sign-in journey | User registered via T-039 | Visit `/signin` → Enter credentials → Submit → Verify dashboard loads with children | Dashboard loads with previously created child | REQ-0003, REQ-0008 | API-002 | SCR-004, SCR-007 | Required |
| T-041 | E2E | Magic Workshop learning | Signed in with Magic Workshop child | Navigate to Magic Workshop → Verify blocks visible → Drag block → Verify preview updates → Chat with Sparkle | Learning environment functional, Sparkle responds | REQ-0010, REQ-0013 | EVT-001, EVT-002 | SCR-009 | Required |
| T-042 | E2E | Add second child | Signed in parent | Dashboard → Add Child → Enter name, age 14 → Submit → Verify Professional Studio child appears | New child card with "Professional Studio" tier | REQ-0007, REQ-0009 | API-005 | SCR-008 | Required |
| T-043 | E2E | Sign-out flow | Signed in | Click Sign Out → Verify redirect to landing or sign-in → Verify dashboard inaccessible | Signed out, cookie cleared, dashboard requires re-auth | REQ-0004 | API-003 | — | Required |

---

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Unit Tests | 28 | All Required (none exist) |
| Integration Tests | 10 | All Required (none exist) |
| E2E Tests | 5 | All Required (none exist) |
| **Total** | **43** | **0 exist, 43 required** |
