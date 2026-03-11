# Test Strategy — Codopia Platform

**Generated**: 2026-02-23  
**Repo**: AllienNova/Codopia @ `154343d`

---

## 1. Current State

**No automated tests exist.** The only test-related file is `test_magic_workshop.py`, which is a standalone Flask demo server (not a test suite). The `docs/deployment/TESTING_AND_DEPLOYMENT.md` describes a Jest/Cypress/pytest strategy that was never implemented.

---

## 2. Test Pyramid

```
         ┌─────────┐
         │  E2E    │  Cypress — 5 critical user journeys
         │ (few)   │
         ├─────────┤
         │ Integr. │  pytest (backend API) + RTL (frontend flows) — 15-20 tests
         │ (some)  │
         ├─────────┤
         │  Unit   │  pytest (backend) + Jest (frontend) — 50+ tests
         │ (many)  │
         └─────────┘
```

---

## 3. Test Layers

### 3.1 Unit Tests

**Backend (pytest)**:
- `backend/auth_service.py`: hash_password, verify_password, determine_tier, create_user_account, sign_in_user, create_child_profile
- `backend/supabase_client.py`: All CRUD methods (with mocked Supabase client)
- `backend/gemini_live_sparkle_fixed.py`: _check_safety, _get_age_appropriate_response_style, _get_tier_context, _build_system_prompt, _get_fallback_response
- `main.py`: generate_children_cards helper, tier assignment logic

**Frontend (Jest + React Testing Library)**:
- `lib/security.ts`: sanitizeInput, validateProjectContent, generateCSRFToken, validateCSRFToken, validateSession
- `lib/children.ts`: determineTierFromAge, validateChildData, formatLearningTime, calculateProgressPercentage, getAchievementLevel, getTierInfo
- `lib/auth.ts`: signUpParent, signInUser, signOut, createChildProfile (with mocked Supabase)
- `components/ChildCard.tsx`: Render states, tier display, progress display
- `components/ui/button.tsx`, `card.tsx`: Render and variant tests

### 3.2 Integration Tests

**Backend API (pytest + Flask test client)**:
- `GET /` — Landing page renders
- `POST /signup` — Creates user, sets JWT cookie, redirects to dashboard
- `POST /signin` — Authenticates user, sets JWT cookie
- `GET /dashboard` — Requires auth, renders child cards
- `GET /learning/magic-workshop` — Renders Magic Workshop
- `GET /signout` — Clears cookie, redirects
- `POST /forgot-password` — Returns confirmation page
- Socket.IO: `init_sparkle` event → `sparkle_ready` response
- Socket.IO: `sparkle_message` event → `sparkle_response` response

**Frontend Flows (React Testing Library)**:
- Sign-up multi-step flow: parent form → child form → completion
- Dashboard: load children, add child, display tier info
- Auth context: login state management, session persistence

### 3.3 End-to-End Tests (Cypress)

| E2E Flow | Steps | Priority |
|----------|-------|----------|
| **Parent Registration** | Visit `/signup` → Fill form → Submit → Verify redirect to dashboard → Verify child card displayed | P0 |
| **Parent Sign-in** | Visit `/signin` → Enter credentials → Submit → Verify dashboard loads | P0 |
| **Magic Workshop Access** | Sign in → Click "Start Learning" on Magic Workshop child → Verify learning environment loads → Interact with blocks | P0 |
| **Professor Sparkle Chat** | Access Magic Workshop → Send message to Sparkle → Verify response received → Verify age-appropriate tone | P1 |
| **Add Child** | Sign in → Dashboard → Click "Add Child" → Fill form → Submit → Verify new child card appears | P1 |

---

## 4. Environments

| Environment | Purpose | Database | AI Model | Config |
|-------------|---------|----------|----------|--------|
| **Unit** | Isolated function testing | Mocked | Mocked | In-memory |
| **Integration** | API and flow testing | Mocked Supabase client | Mocked (fallback responses) | Test env vars |
| **E2E** | Full user journey testing | Supabase test project | Gemini (or mocked) | `.env.test` |
| **Staging** | Pre-production validation | Supabase staging project | Gemini | `.env.staging` |

---

## 5. Mocking Strategy

| Dependency | Mock Approach | Library |
|------------|---------------|---------|
| **Supabase (backend)** | Mock `supabase_client.client` with in-memory dict responses | `unittest.mock` / `pytest-mock` |
| **Supabase (frontend)** | Mock `@supabase/supabase-js` createClient | `jest.mock()` |
| **Gemini AI** | Use existing fallback response path (set `GEMINI_AVAILABLE = False`) | Built-in fallback |
| **Socket.IO** | Use `flask-socketio` test client | `socketio.test_client()` |
| **localStorage** | Use `jest-localstorage-mock` | npm package |

---

## 6. Required Gates

### Pre-Merge (PR) Gates
1. All unit tests pass (pytest + Jest)
2. All integration tests pass
3. Lint passes (ESLint + flake8/ruff)
4. Type check passes (TypeScript `tsc --noEmit`)
5. No new security warnings (Supabase key exposure check)

### Pre-Deploy Gates
1. All PR gates pass
2. E2E tests pass against staging
3. Build succeeds (`next build` + `pip install`)
4. Health check endpoint responds

### Post-Deploy Gates
1. Health check endpoint responds on production
2. Smoke test: landing page loads
3. Smoke test: sign-in flow works
4. Professor Sparkle responds to test message

---

## 7. Coverage Targets

| Layer | Target | Current |
|-------|--------|---------|
| Unit (backend) | 80% | 0% |
| Unit (frontend) | 70% | 0% |
| Integration | Key flows covered | 0% |
| E2E | 5 critical paths | 0% |
