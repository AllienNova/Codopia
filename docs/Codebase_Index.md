# Codebase Index — Codopia Platform

**Generated**: 2026-02-23  
**Repo**: AllienNova/Codopia  
**Revision**: `154343d` (main)

---

## 1. Repository Tree (High-Level)

```
Codopia/
├── main.py                          # PRIMARY Flask entrypoint (monolith, 1327 LOC)
├── Procfile                         # Railway: web: python src/main.py
├── railway.json                     # Railway deploy config
├── vercel.json                      # Vercel deploy config (frontend)
├── package.json                     # Next.js 15 frontend deps
├── tsconfig.json                    # TypeScript config
├── next.config.ts                   # Next.js config (empty)
├── requirements.txt                 # Python deps (Flask, Supabase, PyJWT, etc.)
│
├── app/                             # Next.js App Router pages (root-level copy)
│   ├── page.tsx                     # Landing page
│   ├── layout.tsx                   # Root layout + metadata
│   ├── globals.css                  # Global styles
│   ├── auth/
│   │   ├── signin/page.tsx          # Sign-in page
│   │   ├── signup/page.tsx          # Sign-up page (multi-step)
│   │   └── callback/page.tsx        # OAuth callback handler
│   └── dashboard/
│       ├── page.tsx                 # Dashboard wrapper (dynamic import)
│       └── DashboardContent.tsx     # Dashboard logic + UI
│
├── frontend/                        # DUPLICATE of app/ + additional components
│   ├── app/                         # Same structure as root app/
│   ├── pages/app/                   # THIRD copy of pages (legacy)
│   ├── components/
│   │   ├── About.jsx
│   │   ├── Features.jsx
│   │   ├── Footer.jsx
│   │   ├── Navigation.jsx
│   │   ├── Pricing.jsx
│   │   ├── ChildCard.tsx
│   │   ├── providers.tsx
│   │   └── ui/ (button.tsx, card.tsx)
│   ├── contexts/AuthContext.tsx
│   └── lib/ (auth.ts, children.ts, database.types.ts, security.ts, supabase.ts, utils.ts)
│
├── components/                      # Root-level component copies
│   ├── ChildCard.tsx
│   ├── providers.tsx
│   └── ui/ (button.tsx, card.tsx)
│
├── contexts/AuthContext.tsx          # Root-level context copy
├── lib/                             # Root-level lib copies
│   ├── auth.ts
│   ├── children.ts
│   ├── database.types.ts
│   ├── security.ts
│   ├── supabase.ts
│   └── utils.ts
│
├── backend/
│   ├── main.py                      # DUPLICATE of root main.py (Flask app)
│   ├── supabase_client.py           # Supabase DB client (399 LOC)
│   ├── auth_service.py              # Auth service (in-memory, 201 LOC)
│   ├── gemini_live_sparkle.py       # Professor Sparkle (original)
│   ├── gemini_live_sparkle_fixed.py # Professor Sparkle (fixed, 517 LOC)
│   ├── professor_sparkle.py         # Professor Sparkle (variant)
│   ├── ai/professor_sparkle.py      # Professor Sparkle (another variant)
│   ├── auth/auth_service.py         # Auth service (another copy)
│   ├── database/
│   │   ├── database.types.ts
│   │   └── supabase/migrations/     # DUPLICATE of root supabase/migrations/
│   └── static/js/
│       └── sparkle_integration.js   # Client-side Sparkle WebSocket
│
├── supabase/migrations/             # CANONICAL SQL migrations
│   ├── 001_initial_schema.sql       # 335 LOC — 20+ tables
│   ├── 002_rls_policies.sql         # RLS policies for all tables
│   ├── 003_functions_triggers.sql   # DB functions, triggers, seed data
│   ├── 004_tier_assignment_functions.sql
│   └── 005_enhanced_rls_policies.sql
│
├── legacy/
│   ├── App_enhanced.jsx             # Legacy React app
│   └── main_new.py                  # Legacy Flask app (SQLAlchemy)
│
├── scripts/
│   └── create_simple_tables.py      # Quick table creation script
│
├── auth_service.py                  # Root-level copy of backend/auth_service.py
├── gemini_live_sparkle.py           # Root-level copy
├── gemini_live_sparkle_fixed.py     # Root-level copy
├── professor_sparkle.py             # Root-level copy
├── supabase_client.py               # Root-level copy
├── create_simple_tables.py          # Root-level copy
├── magic_workshop_demo.py           # Standalone demo server
├── test_magic_workshop.py           # Test script for Magic Workshop
├── fix_eslint.js                    # ESLint config fix
│
└── docs/                            # Documentation
    ├── api/GEMINI_LIVE_INTEGRATION_EXPLANATION.md
    ├── architecture/AUTH_MIGRATION_STRATEGY.md
    ├── architecture/DB_MIGRATION_PLAN.md
    ├── deployment/FINAL_DEPLOYMENT_SUMMARY.md
    └── deployment/TESTING_AND_DEPLOYMENT.md
```

---

## 2. Module Inventory

### 2.1 Backend — Flask Monolith

| Module | File | LOC | Purpose | Dependencies | Env Vars |
|--------|------|-----|---------|--------------|----------|
| **Flask App (Primary)** | `main.py` | 1327 | Monolithic Flask app: landing page, auth, dashboard, Magic Workshop, Professor Sparkle WebSocket | Flask, flask-socketio, flask-cors, PyJWT, hashlib | `FLASK_SECRET_KEY`, `PORT`, `FLASK_DEBUG` |
| **Supabase Client** | `backend/supabase_client.py` | 399 | Database CRUD: users, children, progress, achievements, analytics | supabase-py | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |
| **Auth Service** | `backend/auth_service.py` | 201 | In-memory auth: signup, signin, password hashing, session tokens, child profiles | hashlib, secrets | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `FLASK_SECRET_KEY` |
| **Professor Sparkle (Fixed)** | `backend/gemini_live_sparkle_fixed.py` | 517 | AI tutor: Gemini integration, safety protocols, age-appropriate responses, curriculum, fallback responses | google-generativeai, websockets | `OPENAI_API_KEY` (used for Gemini config) |
| **Professor Sparkle (Original)** | `backend/professor_sparkle.py` | ~500 | Earlier variant with Gemini Live WebSocket integration | google-generativeai, websockets | `GEMINI_API_KEY` |
| **Sparkle Client JS** | `backend/static/js/sparkle_integration.js` | ~80 | Browser-side WebSocket client for Professor Sparkle | Socket.IO client | — |

**Failure Modes (Backend)**:
- Supabase connection failure → falls back to in-memory dict storage
- Gemini API unavailable → falls back to pattern-matched static responses
- JWT decode failure → redirects to `/signin`
- In-memory user storage → data lost on restart

### 2.2 Frontend — Next.js 15 (App Router)

| Module | Key Files | Purpose | Dependencies |
|--------|-----------|---------|--------------|
| **Landing Page** | `app/page.tsx` | Marketing page with tier showcase, floating sparkles animation | React, Supabase auth |
| **Auth — Sign In** | `app/auth/signin/page.tsx` | Email/password sign-in with Supabase | Supabase auth |
| **Auth — Sign Up** | `app/auth/signup/page.tsx` | Multi-step: parent account → add children → complete | Supabase auth |
| **Auth — Callback** | `app/auth/callback/page.tsx` | OAuth callback handler | Supabase auth |
| **Dashboard** | `app/dashboard/DashboardContent.tsx` | Parent dashboard: child cards, add child, tier info | Supabase, children lib |
| **ChildCard** | `components/ChildCard.tsx` | Reusable child profile card with progress | children lib |
| **Providers** | `components/providers.tsx` | Auth context provider wrapper | AuthContext |
| **Auth Context** | `contexts/AuthContext.tsx` | Global auth state management | Supabase |
| **Auth Lib** | `lib/auth.ts` | signUpParent, signInUser, signOut, createChildProfile | Supabase |
| **Children Lib** | `lib/children.ts` | CRUD children, tier info, progress, achievements, validation | Supabase |
| **Security Lib** | `lib/security.ts` | Input sanitization, XSS prevention, CSRF, session validation, audit logging, permission checks | Supabase |
| **Supabase Client** | `lib/supabase.ts` | Supabase browser client initialization | @supabase/supabase-js |
| **UI Components** | `components/ui/button.tsx`, `card.tsx` | Radix UI + Tailwind styled components | Radix UI, CVA |

**Failure Modes (Frontend)**:
- Supabase env vars missing → client creation fails silently
- Auth session expired → redirect to sign-in
- CSRF token mismatch → request blocked

### 2.3 Database — Supabase PostgreSQL

| Migration | File | Tables Created | Key Features |
|-----------|------|----------------|--------------|
| 001 | `001_initial_schema.sql` | profiles, children, subscription_plans, subscriptions, modules, lessons, exercises, module_progress, lesson_progress, exercise_submissions, projects, project_collaborators, messages, notifications, achievements, user_achievements, analytics_events | UUID PKs, custom enums, check constraints, 20+ indexes |
| 002 | `002_rls_policies.sql` | — | RLS on all tables; parent-child ownership, public project access, admin overrides |
| 003 | `003_functions_triggers.sql` | — | Functions: update_updated_at, assign_tier_by_age, handle_new_user, update_module_progress, check_and_award_achievements, send_notification, increment_project_views. Triggers: 8 triggers. Seed data: 3 subscription plans, 5 achievements |
| 004 | `004_tier_assignment_functions.sql` | — | Enhanced tier assignment logic |
| 005 | `005_enhanced_rls_policies.sql` | — | Additional RLS refinements |

### 2.4 Integrations

| Integration | Where | Auth | Config | Error Handling |
|-------------|-------|------|--------|----------------|
| **Supabase (DB + Auth)** | `backend/supabase_client.py`, `lib/supabase.ts` | Service role key (backend), Anon key (frontend) | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Fallback to in-memory storage |
| **Google Gemini AI** | `backend/gemini_live_sparkle_fixed.py` | API key | `OPENAI_API_KEY` or `GEMINI_API_KEY` | Fallback to static pattern-matched responses |
| **Stripe (Planned)** | Referenced in docs, not in code | — | — | Not implemented |
| **Codewars (Planned)** | Referenced in docs, not in code | — | — | Not implemented |

### 2.5 Jobs / Cron / Background Workers

None implemented. All operations are synchronous request-response.

### 2.6 Build / Deploy

| Target | Config File | Build | Start |
|--------|-------------|-------|-------|
| **Railway (Backend)** | `railway.json`, `Procfile` | `pip install -r requirements.txt` | `python src/main.py` |
| **Vercel (Frontend)** | `vercel.json` | `next build` | `next start` |
| **Local Dev** | — | `pip install -r requirements.txt` + `npm install` | `python main.py` + `npm run dev` |

### 2.7 Tests

| File | Type | Scope |
|------|------|-------|
| `test_magic_workshop.py` | Integration | Magic Workshop module routes (standalone Flask test server) |
| No other test files exist | — | — |

---

## 3. Critical Observations

### 3.1 File Duplication Problem

The repository contains **extensive file duplication**:
- `auth_service.py` exists in 3 locations (root, `backend/`, `backend/auth/`)
- `professor_sparkle.py` exists in 4 locations (root, `backend/`, `backend/ai/`, `gemini_live_sparkle_fixed.py`)
- `supabase_client.py` exists in 2 locations (root, `backend/`)
- Frontend pages exist in 3 locations (`app/`, `frontend/app/`, `frontend/pages/app/`)
- `lib/` files exist in 3 locations (root, `frontend/lib/`)
- `components/` exist in 2 locations (root, `frontend/components/`)
- SQL migrations exist in 2 locations (`supabase/migrations/`, `backend/database/supabase/migrations/`)

### 3.2 Dual Architecture

The project has **two independent application stacks**:
1. **Flask monolith** (`main.py`): Server-rendered HTML with inline Tailwind CSS, in-memory user storage, Socket.IO for Professor Sparkle
2. **Next.js 15 app** (`app/`, `frontend/`): React SPA with Supabase client-side auth, component library, proper state management

These two stacks are **not integrated** — they serve different UIs for the same features.

### 3.3 Canonical Entrypoints

- **Backend**: `main.py` (root) — the running Flask application
- **Frontend**: `app/page.tsx` — the Next.js landing page
- **Database**: `supabase/migrations/001_initial_schema.sql` — canonical schema
