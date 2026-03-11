# SSOT — Single Source of Truth — Codopia Platform

---

## 0. Execution Manifest

| Field | Value |
|-------|-------|
| **Repo** | AllienNova/Codopia |
| **Branch** | `main` |
| **Revision** | `154343d6652f056f8712899e858118a3dadc354a` |
| **Generation Date** | 2026-02-23 |
| **Docs/Plans Analyzed** | 20 files (see `docs/Plan_Index.md` for full inventory) |
| **Source Files Analyzed** | 90+ files across Python, TypeScript/React, SQL, JSON, YAML |
| **Method** | Full repository scan + all documentation ingest + code behavior analysis |

**Key documents analyzed:**
1. `SANDBOX_REVIEW_AND_UPDATED_IMPLEMENTATION_PLAN.md` (Implementation Plan)
2. `STRATEGIC_NEXT_STEPS_ROADMAP.md` (Business Roadmap)
3. `INTERACTIVE_LEARNING_DEPLOYMENT_ROADMAP.md` (Deployment Plan)
4. `PROFESSOR_SPARKLE_DEPLOYMENT_GUIDE.md` (AI Tutor Guide)
5. `FINAL_DELIVERY_REPORT.md` (Delivery Report)
6. `COMPREHENSIVE_QUALITY_ASSURANCE_REPORT.md` (QA Report)
7. `docs/architecture/AUTH_MIGRATION_STRATEGY.md` (Auth Architecture)
8. `docs/architecture/DB_MIGRATION_PLAN.md` (DB Architecture)
9. `docs/deployment/FINAL_DEPLOYMENT_SUMMARY.md` (Deployment Summary)
10. `docs/deployment/TESTING_AND_DEPLOYMENT.md` (Test Plan)
11. `docs/api/GEMINI_LIVE_INTEGRATION_EXPLANATION.md` (API Reference)
12. All 5 SQL migration files
13. All Python source files (main.py, backend/*.py)
14. All TypeScript/React source files (app/, lib/, components/, contexts/)
15. Configuration files (package.json, railway.json, vercel.json, Procfile, tsconfig.json)

---

## 1. Product Definition

### 1.1 Purpose

Codopia is an AI-powered coding education platform for children ages 5-18. It provides age-appropriate learning environments organized into three progressive tiers, each guided by an AI tutor named "Professor Sparkle" powered by Google Gemini.

### 1.2 Value Proposition

- **For parents**: A safe, monitored environment where children learn real programming skills through play, with progress tracking and age-appropriate content.
- **For children**: A magical, engaging coding experience that adapts to their age and skill level, with an AI tutor that provides personalized guidance.
- **Differentiator**: Three-tier progressive curriculum (ages 5-18) with real-time AI tutoring, comprehensive child safety protocols, and parent oversight.

### 1.3 Target Users / Personas

| Persona | Description | Primary Needs |
|---------|-------------|---------------|
| **Parent** | Adult (25-50) with children ages 5-18. May or may not have technical background. | Safe learning environment, progress visibility, value for money, easy onboarding. |
| **Young Learner (5-7)** | Pre-reader or early reader. Short attention span. Learns through play. | Visual/block-based coding, magical themes, immediate feedback, encouragement. |
| **Middle Learner (8-12)** | Can read and follow instructions. Interested in games and apps. | App building, creative projects, increasing complexity, peer recognition. |
| **Teen Learner (13-18)** | Can handle abstract concepts. Career-curious. Wants real skills. | Real programming languages, industry-relevant projects, portfolio building. |

### 1.4 Core Use Cases

| UC-ID | Use Case | Persona | Description |
|-------|----------|---------|-------------|
| UC-01 | Parent registers and enrolls children | Parent | Create account, add 1+ children with name/age, system assigns tier automatically. |
| UC-02 | Parent monitors progress | Parent | View dashboard with child cards showing tier, progress, achievements. |
| UC-03 | Child learns in Magic Workshop | Young Learner | Drag-and-drop block coding with magical theme, guided by Professor Sparkle. |
| UC-04 | Child learns in Innovation Lab | Middle Learner | Build apps with advanced blocks and components, guided by Professor Sparkle. |
| UC-05 | Child learns in Professional Studio | Teen Learner | Write real code (Python, JavaScript), build projects, guided by Professor Sparkle. |
| UC-06 | Child interacts with Professor Sparkle | All Learners | Ask coding questions, get age-appropriate explanations, receive encouragement. |
| UC-07 | Parent manages children | Parent | Add, edit, or delete child profiles. |
| UC-08 | Parent subscribes to plan | Parent | Choose subscription plan (Free, Family, Classroom) and pay. |

### 1.5 Non-Goals

The following are explicitly **not** in scope for the current implementation:

- Native mobile applications (iOS/Android)
- Teacher/classroom management tools
- Multi-language/internationalization
- Real-time collaborative coding between students
- Video/voice calling between students
- Marketplace for user-created content
- Blockchain-based certificates
- AR/VR learning environments

---

## 2. System Architecture Overview

### 2.1 High-Level Components

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENTS                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Next.js SPA │  │ Flask SSR    │  │ Socket.IO    │  │
│  │  (Vercel)    │  │ (Railway)    │  │ Client       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                    BACKEND (Flask)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ HTTP Routes  │  │ Auth Service │  │ Socket.IO    │  │
│  │ (SSR + API)  │  │ (In-Memory)  │  │ Server       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         │                  │          ┌───────▼───────┐  │
│         │                  │          │ Professor     │  │
│         │                  │          │ Sparkle       │  │
│         │                  │          │ (Gemini AI)   │  │
│         │                  │          └───────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                  DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Supabase     │  │ In-Memory    │  │ Google       │  │
│  │ PostgreSQL   │  │ Dict Store   │  │ Gemini API   │  │
│  │ (Next.js)    │  │ (Flask)      │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow Overview

**Registration Flow (Flask)**:
1. Parent submits signup form → Flask validates → SHA-256 hashes password → stores in Python list → generates JWT → sets cookie → redirects to dashboard.

**Registration Flow (Next.js)**:
1. Parent submits signup form → Supabase `auth.signUp()` → Supabase creates user in `auth.users` → trigger creates profile in `public.profiles` → redirect to dashboard → `createChildProfile()` inserts into `public.children`.

**Learning Flow (Flask)**:
1. Authenticated parent navigates to `/learning/magic-workshop` → Flask renders HTML with inline Tailwind CSS → child interacts with drag-and-drop blocks → Socket.IO connects to Professor Sparkle → messages routed through safety check → Gemini API (or fallback) generates response → response sent back via Socket.IO.

### 2.3 Runtime Environments

| Environment | Stack | Host | URL |
|-------------|-------|------|-----|
| **Backend** | Flask 3.x + Flask-SocketIO + Flask-CORS | Railway | `https://<app>.railway.app` |
| **Frontend** | Next.js 15 + React 19 + Tailwind CSS 4 | Vercel | `https://<app>.vercel.app` |
| **Database** | PostgreSQL 15 (Supabase) | Supabase Cloud | `https://ylymepybqcykyomsmxwk.supabase.co` |
| **AI** | Google Gemini Pro | Google Cloud | `generativelanguage.googleapis.com` |

---

## 3. Codebase Index (Pointer Summary)

> Full details in [`docs/Codebase_Index.md`](./Codebase_Index.md)

### 3.1 Key Subsystem Map

| Subsystem | Primary Files | LOC | Status |
|-----------|---------------|-----|--------|
| **Flask Monolith** | `main.py` | 1,327 | Running — serves landing, auth, dashboard, Magic Workshop, Sparkle |
| **Next.js Frontend** | `app/`, `components/`, `contexts/`, `lib/` | ~2,000 | Built — serves landing, auth, dashboard (separate from Flask) |
| **Supabase Client** | `backend/supabase_client.py` | 399 | Built — CRUD methods for all entities, fallback to in-memory |
| **Auth Service** | `backend/auth_service.py` | 201 | Built — in-memory user storage, SHA-256 hashing |
| **Professor Sparkle** | `backend/gemini_live_sparkle_fixed.py` | 517 | Running — Gemini AI tutor with safety protocols and fallback |
| **Database Schema** | `supabase/migrations/001-005` | 700+ | Applied — 20+ tables, RLS, functions, triggers, seed data |
| **Security Lib** | `lib/security.ts` | ~200 | Built — XSS prevention, CSRF, session management, audit logging |
| **Children Lib** | `lib/children.ts` | ~300 | Built — CRUD, tier logic, progress, achievements, validation |

### 3.2 Critical Observation: Dual Architecture

The codebase contains **two independent application stacks** that are not integrated:

1. **Flask monolith** (`main.py`): Server-rendered HTML, in-memory auth, Socket.IO for Sparkle. This is the **running application**.
2. **Next.js app** (`app/`, `frontend/`): React SPA, Supabase auth, component library. This is a **separate build** intended for Vercel.

These serve overlapping features (landing page, auth, dashboard) with different implementations and different data stores. See `CONF-006` in `docs/Gaps_Conflicts_Decisions.md`.

### 3.3 File Duplication Warning

The repository contains extensive file duplication (see `docs/Codebase_Index.md` Section 3.1). Key files exist in 2-4 locations. The canonical locations are:

- **Backend**: `main.py` (root), `backend/supabase_client.py`, `backend/gemini_live_sparkle_fixed.py`
- **Frontend**: `app/` (root-level Next.js pages), `lib/` (root-level libraries), `components/` (root-level components)
- **Database**: `supabase/migrations/` (root-level)


---

## 4. Functional Requirements Catalog (Canonical)

> Full traceability in [`docs/Traceability_Matrix.md`](./Traceability_Matrix.md)

### REQ-0001 — Landing Page with Tier Showcase

| Field | Value |
|-------|-------|
| **Description** | Public landing page displaying platform value proposition, three learning tiers, Professor Sparkle introduction, and call-to-action for signup. |
| **Priority** | P0 |
| **Personas** | Parent |
| **Acceptance Criteria** | Page loads without auth. Displays three tier cards (Magic Workshop, Innovation Lab, Professional Studio). Links to signup. Responsive on mobile. |
| **Edge Cases** | Slow network: page should render progressively. SEO: meta tags present. |
| **CodeRefs** | `main.py:31-319` (Flask SSR), `app/page.tsx` (Next.js), `frontend/components/About.jsx`, `Features.jsx`, `Pricing.jsx`, `Navigation.jsx`, `Footer.jsx` |
| **ScreenIDs** | SCR-001 |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | — |
| **TestIDs** | — |
| **ConfigRefs** | — |

### REQ-0002 — Parent Account Registration

| Field | Value |
|-------|-------|
| **Description** | Parent creates account with email, password, full name. System creates profile and allows adding children. |
| **Priority** | P0 |
| **Personas** | Parent |
| **Acceptance Criteria** | Form validates: email format, password ≥8 chars, name required. On success: user created, JWT issued, redirect to dashboard. On duplicate email: error displayed. |
| **Edge Cases** | Concurrent duplicate signups. Password with special characters. Very long name (>255 chars). |
| **CodeRefs** | `main.py:323-386` (Flask), `app/auth/signup/page.tsx` (Next.js multi-step), `lib/auth.ts:signUpParent`, `backend/auth_service.py:create_user_account` |
| **ScreenIDs** | SCR-002 (Flask), SCR-003 (Next.js multi-step) |
| **FlowIDs** | FLOW-001 |
| **ApiIDs** | API-001 |
| **EntIDs** | ENT-001 (profiles) |
| **TestIDs** | T-004, T-005, T-029, T-039 |
| **ConfigRefs** | `FLASK_SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY` |

### REQ-0003 — Parent Sign-In

| Field | Value |
|-------|-------|
| **Description** | Parent signs in with email and password. System verifies credentials, issues session, redirects to dashboard. |
| **Priority** | P0 |
| **Personas** | Parent |
| **Acceptance Criteria** | Correct credentials: JWT cookie set, redirect to `/dashboard`. Wrong credentials: error message, no redirect. Empty fields: client-side validation prevents submit. |
| **Edge Cases** | Account locked after N failures (not implemented). Case-sensitive email. Session expiry. |
| **CodeRefs** | `main.py:388-481` (Flask), `app/auth/signin/page.tsx` (Next.js), `lib/auth.ts:signInUser`, `backend/auth_service.py:sign_in_user` |
| **ScreenIDs** | SCR-004 |
| **FlowIDs** | FLOW-002 |
| **ApiIDs** | API-002 |
| **EntIDs** | ENT-001 |
| **TestIDs** | T-006, T-007, T-030, T-031, T-040 |
| **ConfigRefs** | `FLASK_SECRET_KEY`, `SUPABASE_URL` |

### REQ-0004 — Sign-Out

| Field | Value |
|-------|-------|
| **Description** | User signs out. Session cleared, cookie removed, redirect to landing or sign-in. |
| **Priority** | P0 |
| **Personas** | Parent |
| **Acceptance Criteria** | Cookie cleared. Subsequent dashboard access redirects to sign-in. |
| **Edge Cases** | Sign-out with expired session (should still clear). |
| **CodeRefs** | `main.py:1235-1239` (Flask), `lib/auth.ts:signOut` (Next.js) |
| **ScreenIDs** | — |
| **FlowIDs** | FLOW-003 |
| **ApiIDs** | API-003 |
| **EntIDs** | — |
| **TestIDs** | T-043 |
| **ConfigRefs** | — |

### REQ-0005 — Password Reset

| Field | Value |
|-------|-------|
| **Description** | Parent requests password reset via email. System sends reset link. |
| **Priority** | P1 |
| **Personas** | Parent |
| **Acceptance Criteria** | Form accepts email. Confirmation page displayed. Reset email sent with secure token. Token expires after 1 hour. |
| **Edge Cases** | Non-existent email (show same confirmation to prevent enumeration). Expired token. |
| **CodeRefs** | `main.py:1241-1321` (Flask — partial, no email sending) |
| **ScreenIDs** | SCR-005 |
| **FlowIDs** | FLOW-004 |
| **ApiIDs** | API-004 |
| **EntIDs** | — |
| **TestIDs** | — |
| **ConfigRefs** | — |
| **GAP** | GAP-002: No email service configured. Shows static confirmation only. |

### REQ-0006 — OAuth Callback

| Field | Value |
|-------|-------|
| **Description** | Handle OAuth provider callback (Google, GitHub) after external authentication. |
| **Priority** | P1 |
| **Personas** | Parent |
| **Acceptance Criteria** | Callback exchanges code for session. Redirects to dashboard on success. |
| **Edge Cases** | Invalid code. Provider error. |
| **CodeRefs** | `app/auth/callback/page.tsx` |
| **ScreenIDs** | SCR-006 |
| **FlowIDs** | FLOW-005 |
| **ApiIDs** | — |
| **EntIDs** | ENT-001 |
| **TestIDs** | — |
| **ConfigRefs** | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |

### REQ-0007 — Age-Based Tier Assignment

| Field | Value |
|-------|-------|
| **Description** | When a child is added, the system automatically assigns a learning tier based on age: ≤7 → Magic Workshop, 8-12 → Innovation Lab, 13+ → Professional Studio. |
| **Priority** | P0 |
| **Personas** | System (triggered by Parent adding child) |
| **Acceptance Criteria** | Age 5 → `magic_workshop`. Age 10 → `innovation_lab`. Age 15 → `professional_studio`. Boundary: age 7 → `magic_workshop`, age 8 → `innovation_lab`, age 13 → `professional_studio`. |
| **Edge Cases** | Age below 3 or above 18 (validation should reject). Age exactly at boundary. |
| **CodeRefs** | `main.py:348-354`, `backend/auth_service.py:31-38`, `lib/children.ts:determineTierFromAge`, `supabase/migrations/003_functions_triggers.sql:assign_tier_by_age`, `supabase/migrations/004_tier_assignment_functions.sql` |
| **ScreenIDs** | — |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | ENT-002 (children) |
| **TestIDs** | T-001, T-016 |
| **ConfigRefs** | — |

### REQ-0008 — Parent Dashboard

| Field | Value |
|-------|-------|
| **Description** | Authenticated parent sees dashboard with all enrolled children displayed as cards showing tier, progress, and actions. |
| **Priority** | P0 |
| **Personas** | Parent |
| **Acceptance Criteria** | Requires authentication (redirect if not signed in). Displays all children. Each card shows: name, age, tier, progress percentage, achievements count. "Add Child" button visible. "Start Learning" button per child. |
| **Edge Cases** | No children (show "Add your first child" prompt). Many children (scrollable list). Loading state while fetching. |
| **CodeRefs** | `main.py:483-589` (Flask), `app/dashboard/DashboardContent.tsx` (Next.js), `components/ChildCard.tsx` |
| **ScreenIDs** | SCR-007, SCR-008 |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | ENT-001, ENT-002 |
| **TestIDs** | T-032, T-033, T-039 |
| **ConfigRefs** | `FLASK_SECRET_KEY` |

### REQ-0009 — Add Child Profile

| Field | Value |
|-------|-------|
| **Description** | Parent adds a child profile with name and age. System assigns tier and creates profile. |
| **Priority** | P0 |
| **Personas** | Parent |
| **Acceptance Criteria** | Name required (1-100 chars). Age required (3-18). On submit: child created, tier assigned, dashboard refreshed with new card. |
| **Edge Cases** | Duplicate child name (allowed). Age at tier boundary. Special characters in name. |
| **CodeRefs** | `main.py:535-544` (Flask — UI only, no POST handler), `app/dashboard/DashboardContent.tsx:handleAddChild` (Next.js), `lib/auth.ts:createChildProfile`, `backend/supabase_client.py:create_child_profile` |
| **ScreenIDs** | SCR-008 |
| **FlowIDs** | FLOW-006 |
| **ApiIDs** | API-005 |
| **EntIDs** | ENT-002 |
| **TestIDs** | T-017, T-023, T-042 |
| **ConfigRefs** | `SUPABASE_URL` |
| **GAP** | Flask has UI form but no POST handler to actually create the child. |

### REQ-0010 — Magic Workshop Learning Environment

| Field | Value |
|-------|-------|
| **Description** | Block-based visual programming environment for ages 5-7 with magical theme. Drag-and-drop spell blocks, live preview, Professor Sparkle chat panel. |
| **Priority** | P0 |
| **Personas** | Young Learner |
| **Acceptance Criteria** | Blocks palette visible (Move Wizard, Repeat, Create Star, Play Sound, Change Color). Blocks draggable to workspace. Live preview shows result. Professor Sparkle chat accessible. Purple/pink gradient theme. |
| **Edge Cases** | Touch devices (drag-and-drop must work). Small screens. Sparkle unavailable (show offline message). |
| **CodeRefs** | `main.py:660-1196` (Flask SSR — complete HTML with inline CSS/JS) |
| **ScreenIDs** | SCR-009 |
| **FlowIDs** | FLOW-007 |
| **ApiIDs** | EVT-001, EVT-002 |
| **EntIDs** | — |
| **TestIDs** | T-034, T-041 |
| **ConfigRefs** | — |
| **Note** | Only Module 1 ("Making the Wizard Move") is implemented. Modules 2-10 have no routes. |

### REQ-0011 — Innovation Lab Learning Environment

| Field | Value |
|-------|-------|
| **Description** | App-building platform for ages 8-12 with component palette, design canvas, and live phone preview. |
| **Priority** | P1 |
| **Personas** | Middle Learner |
| **Acceptance Criteria** | Component palette (buttons, labels, inputs, charts, game canvas). Design canvas for layout. Live preview in phone mockup. 10 progressive modules. |
| **Edge Cases** | — |
| **CodeRefs** | — |
| **ScreenIDs** | — |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | — |
| **TestIDs** | — |
| **ConfigRefs** | — |
| **Status** | **Planned-not-implemented** (GAP-004) |

### REQ-0012 — Professional Studio Learning Environment

| Field | Value |
|-------|-------|
| **Description** | Real programming environment for ages 13-18 with code editor, terminal, and project structure. |
| **Priority** | P1 |
| **Personas** | Teen Learner |
| **Acceptance Criteria** | Code editor with syntax highlighting (Python, JavaScript). Terminal/console output. File tree. 10 progressive modules covering Python, JS, React, Flask, databases, algorithms, DevOps. |
| **Edge Cases** | Code execution sandboxing. Infinite loops. Large output. |
| **CodeRefs** | — |
| **ScreenIDs** | — |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | — |
| **TestIDs** | — |
| **ConfigRefs** | — |
| **Status** | **Planned-not-implemented** (GAP-005) |

### REQ-0013 — Professor Sparkle AI Tutor

| Field | Value |
|-------|-------|
| **Description** | AI-powered coding tutor that provides personalized, age-appropriate guidance via text chat. Uses Google Gemini with fallback to pattern-matched static responses. |
| **Priority** | P0 |
| **Personas** | All Learners |
| **Acceptance Criteria** | Responds to coding questions. Adapts language to child's age. Maintains conversation context within session. Provides encouragement. Falls back gracefully when Gemini unavailable. |
| **Edge Cases** | Gemini API rate limit. Very long messages. Non-English input. Gibberish input. |
| **CodeRefs** | `backend/gemini_live_sparkle_fixed.py` (517 LOC), `main.py:1198-1232` (Socket.IO handlers), `backend/static/js/sparkle_integration.js` (client) |
| **ScreenIDs** | SCR-009 (embedded chat panel) |
| **FlowIDs** | FLOW-008 |
| **ApiIDs** | EVT-001, EVT-002 |
| **EntIDs** | — |
| **TestIDs** | T-012, T-013, T-035, T-036, T-041 |
| **ConfigRefs** | `OPENAI_API_KEY` or `GEMINI_API_KEY` |

### REQ-0014 — Professor Sparkle Safety Protocols

| Field | Value |
|-------|-------|
| **Description** | All messages to Professor Sparkle are checked against forbidden topics and emergency keywords before processing. Unsafe messages receive redirect responses. Emergency messages receive support responses. |
| **Priority** | P0 |
| **Personas** | System |
| **Acceptance Criteria** | Forbidden topics (violence, adult content, personal info requests, self-harm) trigger safety response. Emergency keywords ("help", "scared", "hurt") trigger emergency response with support resources. Safe messages pass through to AI. |
| **Edge Cases** | Obfuscated forbidden content. False positives on innocent messages. |
| **CodeRefs** | `backend/gemini_live_sparkle_fixed.py:61-79` (forbidden topics list), `backend/gemini_live_sparkle_fixed.py:200-216` (safety check method) |
| **ScreenIDs** | — |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | — |
| **TestIDs** | T-008, T-009, T-010, T-037 |
| **ConfigRefs** | — |

### REQ-0015 — Age-Appropriate AI Response Style

| Field | Value |
|-------|-------|
| **Description** | Professor Sparkle adjusts vocabulary, pace, emoji usage, and magical elements based on the child's age bracket. |
| **Priority** | P0 |
| **Personas** | System |
| **Acceptance Criteria** | Ages 3-5: simple words, lots of emojis, very slow pace, maximum magical elements. Ages 6-7: simple sentences, some emojis, slow pace. Ages 8-10: moderate vocabulary, moderate pace. Ages 11-13: fuller vocabulary, faster pace. Ages 14+: professional language, minimal emojis, fast pace. |
| **Edge Cases** | Age not provided (default to middle bracket). |
| **CodeRefs** | `backend/gemini_live_sparkle_fixed.py:218-270` |
| **ScreenIDs** | — |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | — |
| **TestIDs** | T-011 |
| **ConfigRefs** | — |

### REQ-0016 — AI Curriculum Awareness

| Field | Value |
|-------|-------|
| **Description** | Professor Sparkle has knowledge of the curriculum for all three tiers and can guide students through specific lessons. |
| **Priority** | P1 |
| **Personas** | System |
| **Acceptance Criteria** | Sparkle references current lesson context. Provides hints aligned with lesson objectives. Suggests next steps based on curriculum progression. |
| **CodeRefs** | `backend/gemini_live_sparkle_fixed.py:81-198` (hardcoded curriculum: 3 tiers × 5-6 lessons) |
| **ScreenIDs** | — |
| **FlowIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | — |
| **TestIDs** | — |
| **ConfigRefs** | — |

### REQ-0017 — Lesson Progress Tracking

| Field | Value |
|-------|-------|
| **Description** | System tracks each child's progress through lessons: completion status, score, time spent. |
| **Priority** | P1 |
| **Personas** | Parent, System |
| **Acceptance Criteria** | Progress saved per child per lesson. Includes: completed (boolean), score (0-100), time_spent (minutes), progress_data (JSON). Upsert behavior (update if exists). |
| **CodeRefs** | `backend/supabase_client.py:252-310` |
| **ScreenIDs** | — |
| **ApiIDs** | API-006 |
| **EntIDs** | ENT-003 (lesson_progress) |
| **TestIDs** | T-024 |
| **ConfigRefs** | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |
| **GAP** | Client methods exist but are not called from any Flask route. |

### REQ-0018 — Achievement System

| Field | Value |
|-------|-------|
| **Description** | Children earn achievements for milestones (first lesson, completing modules, streaks). Achievements displayed on dashboard. |
| **Priority** | P2 |
| **Personas** | Young/Middle/Teen Learner, Parent |
| **Acceptance Criteria** | Achievements awarded automatically via DB trigger. Achievement data includes: id, name, description, icon, earned_at. Displayed on child card. |
| **CodeRefs** | `backend/supabase_client.py:314-351`, `supabase/migrations/003_functions_triggers.sql:check_and_award_achievements` (DB function), seed data: 5 achievements (First Steps, Quick Learner, Persistent Coder, Creative Builder, Master Wizard) |
| **ScreenIDs** | — |
| **ApiIDs** | API-007 |
| **EntIDs** | ENT-004 (achievements), ENT-005 (user_achievements) |
| **TestIDs** | T-020, T-025 |
| **ConfigRefs** | `SUPABASE_URL` |
| **GAP** | DB schema and client methods exist. No UI display. No trigger wiring from app layer. |

### REQ-0019 — Parent Analytics

| Field | Value |
|-------|-------|
| **Description** | Parent can view analytics for their children: total learning time, lessons completed, achievement count, recent activity. |
| **Priority** | P2 |
| **Personas** | Parent |
| **Acceptance Criteria** | Analytics aggregated per child. Shows: total_time, lessons_completed, achievements_earned, last_active. |
| **CodeRefs** | `backend/supabase_client.py:355-384` |
| **ScreenIDs** | — |
| **ApiIDs** | API-008 |
| **EntIDs** | ENT-001, ENT-002, ENT-003, ENT-004 |
| **TestIDs** | — |
| **ConfigRefs** | `SUPABASE_URL` |
| **GAP** | GAP-012. Client method exists. No UI or route. |

### REQ-0020 — Subscription Plans

| Field | Value |
|-------|-------|
| **Description** | Platform offers tiered subscription plans: Free (1 child, basic), Family ($14.99/mo, 3 children, all tiers), Classroom ($49.99/mo, 30 children, admin tools). |
| **Priority** | P2 |
| **Personas** | Parent |
| **Acceptance Criteria** | Plans displayed on pricing page. User can select and subscribe. Subscription stored with status, billing cycle, payment method. |
| **CodeRefs** | `supabase/migrations/003_functions_triggers.sql` (seed data: 3 plans) |
| **ScreenIDs** | — |
| **ApiIDs** | — |
| **EntIDs** | ENT-006 (subscription_plans), ENT-007 (subscriptions) |
| **TestIDs** | — |
| **ConfigRefs** | — |
| **GAP** | GAP-007. Schema and seed data only. No payment integration (CONF-004). |

### REQ-0021 through REQ-0040

> Remaining requirements (projects/portfolio, messaging, notifications, analytics events, RLS, input sanitization, CSRF, session management, permissions, module progress, exercise submissions, health check, child management, marketing components, voice interaction, PWA, i18n, Stripe, teacher tools, collaborative projects) are fully documented in [`docs/Traceability_Matrix.md`](./Traceability_Matrix.md) with complete trace links.


---

## 5. UI / Screen Catalog

### SCR-001 — Landing Page

| Field | Value |
|-------|-------|
| **Name/Route** | `/` |
| **Purpose** | Marketing landing page showcasing platform value, three tiers, Professor Sparkle, and signup CTA. |
| **Components** | Hero section with animated sparkles, tier showcase cards (3), Professor Sparkle introduction, pricing section, navigation bar, footer. |
| **States** | Loading: N/A (static). Empty: N/A. Error: N/A. |
| **Validation** | None (public page). |
| **Accessibility** | Semantic HTML. Alt text on images. Keyboard-navigable CTA buttons. |
| **Linked ReqIDs** | REQ-0001, REQ-0034 |
| **Linked ApiIDs** | — |
| **Linked EntIDs** | — |
| **CodeRefs** | `main.py:31-319` (Flask), `app/page.tsx` (Next.js), `frontend/components/Navigation.jsx`, `Features.jsx`, `About.jsx`, `Pricing.jsx`, `Footer.jsx` |

### SCR-002 — Sign-Up (Flask)

| Field | Value |
|-------|-------|
| **Name/Route** | `/signup` |
| **Purpose** | Single-page registration form for parent account with child enrollment. |
| **Components** | Form: parent name, email, password, child name, child age. Submit button. Error display. Link to sign-in. |
| **States** | Loading: submit button disabled. Empty: form with placeholders. Error: red error message above form. |
| **Validation** | Client: required fields. Server: email format, password length ≥8, duplicate email check. |
| **Accessibility** | Form labels. Error messages linked to fields. |
| **Linked ReqIDs** | REQ-0002, REQ-0007 |
| **Linked ApiIDs** | API-001 |
| **Linked EntIDs** | ENT-001, ENT-002 |
| **CodeRefs** | `main.py:323-386` |

### SCR-003 — Sign-Up (Next.js Multi-Step)

| Field | Value |
|-------|-------|
| **Name/Route** | `/auth/signup` |
| **Purpose** | Multi-step registration: Step 1 (parent account) → Step 2 (add children) → Step 3 (complete). |
| **Components** | Step indicator. Step 1: email, password, confirm password, full name. Step 2: child name, age, add more children button. Step 3: success confirmation with dashboard link. |
| **States** | Loading: spinner on submit buttons. Empty: forms with placeholders. Error: red error banner. Step transitions animated. |
| **Validation** | Client: passwords match, password ≥8 chars, required fields. Server: Supabase auth validation. |
| **Accessibility** | Step indicator with aria-current. Form labels. Show/hide password toggle. |
| **Linked ReqIDs** | REQ-0002, REQ-0007, REQ-0009 |
| **Linked ApiIDs** | API-001, API-005 |
| **Linked EntIDs** | ENT-001, ENT-002 |
| **CodeRefs** | `app/auth/signup/page.tsx` |

### SCR-004 — Sign-In

| Field | Value |
|-------|-------|
| **Name/Route** | `/signin` (Flask), `/auth/signin` (Next.js) |
| **Purpose** | Email/password sign-in form. |
| **Components** | Email input, password input (with show/hide toggle), submit button, forgot password link, sign-up link. |
| **States** | Loading: submit disabled with spinner. Error: red error message (from query param or state). |
| **Validation** | Client: required fields. Server: credential verification. |
| **Linked ReqIDs** | REQ-0003 |
| **Linked ApiIDs** | API-002 |
| **Linked EntIDs** | ENT-001 |
| **CodeRefs** | `main.py:388-481` (Flask), `app/auth/signin/page.tsx` (Next.js) |

### SCR-005 — Forgot Password

| Field | Value |
|-------|-------|
| **Name/Route** | `/forgot-password` |
| **Purpose** | Password reset request form. |
| **Components** | Email input, submit button, confirmation message. |
| **States** | Default: email form. Submitted: static confirmation ("Check your email"). |
| **Validation** | Client: email required. |
| **Linked ReqIDs** | REQ-0005 |
| **Linked ApiIDs** | API-004 |
| **CodeRefs** | `main.py:1241-1321` |
| **GAP** | No email service. Always shows confirmation regardless of email existence. |

### SCR-006 — OAuth Callback

| Field | Value |
|-------|-------|
| **Name/Route** | `/auth/callback` |
| **Purpose** | Handle OAuth provider redirect, exchange code for session. |
| **Components** | Loading spinner. Error display if callback fails. |
| **States** | Loading: processing callback. Success: redirect to dashboard. Error: error message with retry link. |
| **Linked ReqIDs** | REQ-0006 |
| **CodeRefs** | `app/auth/callback/page.tsx` |

### SCR-007 — Parent Dashboard

| Field | Value |
|-------|-------|
| **Name/Route** | `/dashboard` |
| **Purpose** | Parent's main view showing all enrolled children with progress and actions. |
| **Components** | Header with user info and sign-out. Child cards grid (SCR-008). "Add Child" button/form. Empty state prompt. |
| **States** | Loading: skeleton cards. Empty: "Add your first child" prompt with illustration. Error: error banner with retry. Populated: grid of child cards. |
| **Validation** | Auth required (redirect to sign-in if not authenticated). |
| **Linked ReqIDs** | REQ-0008 |
| **Linked ApiIDs** | — |
| **Linked EntIDs** | ENT-001, ENT-002 |
| **CodeRefs** | `main.py:483-589` (Flask), `app/dashboard/DashboardContent.tsx` (Next.js) |

### SCR-008 — Child Card (Component)

| Field | Value |
|-------|-------|
| **Name/Route** | Component (embedded in SCR-007) |
| **Purpose** | Display individual child's tier, progress, achievements, and action buttons. |
| **Components** | Tier badge (color-coded gradient), child name, age, progress bar, achievement count, star rating, "Start Learning" button, edit/delete buttons. |
| **States** | Loading: progress summary loading. Compact: minimal info. Full: all details. |
| **Linked ReqIDs** | REQ-0008, REQ-0033 |
| **Linked ApiIDs** | API-010, API-011 |
| **Linked EntIDs** | ENT-002 |
| **CodeRefs** | `components/ChildCard.tsx`, `lib/children.ts:getTierInfo, getChildProgressSummary` |

### SCR-009 — Magic Workshop Learning Environment

| Field | Value |
|-------|-------|
| **Name/Route** | `/learning/magic-workshop` |
| **Purpose** | Block-based visual programming environment for Module 1: "Making the Wizard Move". |
| **Components** | Block palette (left): Move Wizard, Repeat, Create Star, Play Sound, Change Color. Workspace (center): drop zone for blocks. Preview (right): visual output. Professor Sparkle chat (bottom-right): message input, chat history. Progress bar. Module title. |
| **States** | Loading: "Preparing your magical workspace" message. Active: blocks interactive, preview responsive. Sparkle offline: "Professor Sparkle is resting" message. |
| **Validation** | Auth required. Child must be in Magic Workshop tier. |
| **Linked ReqIDs** | REQ-0010, REQ-0013 |
| **Linked ApiIDs** | EVT-001, EVT-002 |
| **Linked EntIDs** | — |
| **CodeRefs** | `main.py:660-1196` (complete HTML/CSS/JS inline) |

---

## 6. Workflow Catalog

### FLOW-001 — Parent Registration

| Field | Value |
|-------|-------|
| **Trigger** | Parent clicks "Sign Up" / "Get Started" on landing page. |
| **Steps** | 1. Display signup form. 2. Parent fills email, password, name, child name, child age. 3. Client validates (password ≥8, email format). 4. Submit to server. 5. Server checks duplicate email. 6. Server hashes password (SHA-256 + salt). 7. Server creates user in memory (Flask) or Supabase (Next.js). 8. Server assigns tier based on child age. 9. Server creates child profile. 10. Server generates JWT (Flask) or Supabase session (Next.js). 11. Set auth cookie. 12. Redirect to `/dashboard`. |
| **Error + Recovery** | Step 5 duplicate: show "Email already registered" error, stay on form. Step 3 validation fail: show field-level errors. Step 7 Supabase error: show generic error. |
| **Linked ScreenIDs** | SCR-002, SCR-003 |
| **Linked ApiIDs** | API-001, API-005 |
| **Linked ReqIDs** | REQ-0002, REQ-0007, REQ-0009 |
| **Linked TestIDs** | T-004, T-005, T-029, T-039 |

### FLOW-002 — Parent Sign-In

| Field | Value |
|-------|-------|
| **Trigger** | Parent clicks "Sign In" link. |
| **Steps** | 1. Display sign-in form. 2. Parent enters email and password. 3. Client validates required fields. 4. Submit to server. 5. Server looks up user by email. 6. Server verifies password hash. 7. Server generates JWT / Supabase session. 8. Set auth cookie. 9. Redirect to `/dashboard`. |
| **Error + Recovery** | Step 5 user not found: show "Invalid credentials". Step 6 wrong password: show "Invalid credentials" (same message to prevent enumeration). |
| **Linked ScreenIDs** | SCR-004 |
| **Linked ApiIDs** | API-002 |
| **Linked ReqIDs** | REQ-0003 |
| **Linked TestIDs** | T-006, T-007, T-030, T-031, T-040 |

### FLOW-003 — Sign-Out

| Field | Value |
|-------|-------|
| **Trigger** | Parent clicks "Sign Out" button. |
| **Steps** | 1. Clear auth cookie (Flask) / call Supabase signOut (Next.js). 2. Clear localStorage session data. 3. Redirect to `/` or `/signin`. |
| **Error + Recovery** | Cookie already expired: still redirect. Supabase signOut fails: still clear local state and redirect. |
| **Linked ScreenIDs** | — |
| **Linked ApiIDs** | API-003 |
| **Linked ReqIDs** | REQ-0004 |
| **Linked TestIDs** | T-043 |

### FLOW-004 — Password Reset

| Field | Value |
|-------|-------|
| **Trigger** | Parent clicks "Forgot Password" link. |
| **Steps** | 1. Display email form. 2. Parent enters email. 3. Submit. 4. Server shows confirmation page. |
| **Error + Recovery** | No email service configured. Always shows confirmation. |
| **Linked ScreenIDs** | SCR-005 |
| **Linked ApiIDs** | API-004 |
| **Linked ReqIDs** | REQ-0005 |
| **GAP** | GAP-002: No actual email sent. |

### FLOW-005 — OAuth Callback

| Field | Value |
|-------|-------|
| **Trigger** | OAuth provider redirects back to `/auth/callback`. |
| **Steps** | 1. Extract code from URL params. 2. Exchange code for session via Supabase. 3. On success: redirect to `/dashboard`. 4. On error: display error. |
| **Error + Recovery** | Invalid code: show error with link to sign-in. |
| **Linked ScreenIDs** | SCR-006 |
| **Linked ReqIDs** | REQ-0006 |

### FLOW-006 — Add Child

| Field | Value |
|-------|-------|
| **Trigger** | Parent clicks "Add Child" on dashboard. |
| **Steps** | 1. Show add child form (name, age). 2. Client validates (name 1-100 chars, age 3-18). 3. Submit. 4. Server determines tier from age. 5. Server creates child profile. 6. Refresh dashboard to show new card. |
| **Error + Recovery** | Validation fail: show field errors. Supabase error: show generic error. |
| **Linked ScreenIDs** | SCR-008 |
| **Linked ApiIDs** | API-005 |
| **Linked ReqIDs** | REQ-0009, REQ-0007 |
| **Linked TestIDs** | T-017, T-023, T-042 |

### FLOW-007 — Magic Workshop Session

| Field | Value |
|-------|-------|
| **Trigger** | Parent clicks "Start Learning" on Magic Workshop child card. |
| **Steps** | 1. Navigate to `/learning/magic-workshop`. 2. Verify auth. 3. Render block coding environment. 4. Initialize Socket.IO connection. 5. Child drags blocks to workspace. 6. Preview updates in real-time. 7. Child can chat with Professor Sparkle via chat panel. |
| **Error + Recovery** | Auth expired: redirect to sign-in. Socket.IO connection fails: show "Sparkle is resting" message, blocks still functional. |
| **Linked ScreenIDs** | SCR-009 |
| **Linked ApiIDs** | EVT-001, EVT-002 |
| **Linked ReqIDs** | REQ-0010 |
| **Linked TestIDs** | T-034, T-041 |

### FLOW-008 — Professor Sparkle Conversation

| Field | Value |
|-------|-------|
| **Trigger** | Child sends message in Sparkle chat panel. |
| **Steps** | 1. Client emits `sparkle_message` via Socket.IO with message text and session_id. 2. Server receives message. 3. Safety check: scan for forbidden topics and emergency keywords. 4. If unsafe: return safety response immediately. 5. If safe: build system prompt with age-appropriate style + tier context + curriculum. 6. Send to Gemini API. 7. If Gemini fails: use fallback pattern-matched response. 8. Return response via `sparkle_response` event. 9. Client displays response in chat panel. |
| **Error + Recovery** | Step 3 unsafe: safety response returned (no AI call). Step 6 Gemini error: fallback response. Step 6 timeout: fallback response. Socket disconnected: reconnect with exponential backoff. |
| **Linked ScreenIDs** | SCR-009 |
| **Linked ApiIDs** | EVT-001, EVT-002 |
| **Linked ReqIDs** | REQ-0013, REQ-0014, REQ-0015 |
| **Linked TestIDs** | T-035, T-036, T-037 |

---

## 7. API / Event / Job Catalog

### API-001 — POST /signup

| Field | Value |
|-------|-------|
| **Method** | POST |
| **Path** | `/signup` |
| **Auth** | None (public) |
| **Request Schema** | Form data: `parent_name` (string, required), `email` (string, required), `password` (string, required, ≥8 chars), `child_name` (string, required), `child_age` (integer, required, 3-18) |
| **Response** | 302 redirect to `/dashboard` with `auth_token` cookie set. On error: redirect to `/signup?error=<type>`. |
| **Error Taxonomy** | `email_exists`: duplicate email. `invalid_input`: missing/invalid fields. |
| **Retries/Timeouts** | None. |
| **Linked ReqIDs** | REQ-0002, REQ-0007, REQ-0009 |
| **Linked ScreenIDs** | SCR-002 |
| **Linked EntIDs** | ENT-001, ENT-002 |
| **CodeRefs** | `main.py:323-386` |

### API-002 — POST /signin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **Path** | `/signin` |
| **Auth** | None (public) |
| **Request Schema** | Form data: `email` (string, required), `password` (string, required) |
| **Response** | 302 redirect to `/dashboard` with `auth_token` cookie. On error: redirect to `/signin?error=invalid_credentials`. |
| **Error Taxonomy** | `invalid_credentials`: email not found or password mismatch. |
| **Retries/Timeouts** | None. |
| **Linked ReqIDs** | REQ-0003 |
| **Linked ScreenIDs** | SCR-004 |
| **Linked EntIDs** | ENT-001 |
| **CodeRefs** | `main.py:388-481` |

### API-003 — GET /signout

| Field | Value |
|-------|-------|
| **Method** | GET |
| **Path** | `/signout` |
| **Auth** | Cookie (auth_token) |
| **Request Schema** | None. |
| **Response** | 302 redirect to `/`. Clears `auth_token` cookie. |
| **Linked ReqIDs** | REQ-0004 |
| **CodeRefs** | `main.py:1235-1239` |

### API-004 — POST /forgot-password

| Field | Value |
|-------|-------|
| **Method** | POST |
| **Path** | `/forgot-password` |
| **Auth** | None (public) |
| **Request Schema** | Form data: `email` (string, required) |
| **Response** | 200 HTML page with confirmation message. |
| **Linked ReqIDs** | REQ-0005 |
| **Linked ScreenIDs** | SCR-005 |
| **CodeRefs** | `main.py:1241-1321` |
| **GAP** | No email actually sent. |

### API-005 — Supabase: Insert Child Profile

| Field | Value |
|-------|-------|
| **Method** | Supabase client `table('children').insert()` |
| **Path** | N/A (direct DB call) |
| **Auth** | Service role key (backend), Anon key + RLS (frontend) |
| **Request Schema** | `{ parent_id: UUID, name: string, age: int, tier: enum, magic_points: 0, achievements: [] }` |
| **Response** | Inserted row with generated UUID. |
| **Error Taxonomy** | Foreign key violation (invalid parent_id). RLS denial (wrong parent). |
| **Linked ReqIDs** | REQ-0009 |
| **Linked EntIDs** | ENT-002 |
| **CodeRefs** | `backend/supabase_client.py:create_child_profile`, `lib/auth.ts:createChildProfile` |

### API-006 — Supabase: Upsert Lesson Progress

| Field | Value |
|-------|-------|
| **Method** | Supabase client `table('lesson_progress').upsert()` |
| **Auth** | Service role key |
| **Request Schema** | `{ child_id: UUID, lesson_id: string, progress_data: JSON, completed: bool, score: int, time_spent: int }` |
| **Response** | Upserted row. |
| **Linked ReqIDs** | REQ-0017 |
| **Linked EntIDs** | ENT-003 |
| **CodeRefs** | `backend/supabase_client.py:save_lesson_progress` |
| **GAP** | Not called from any route. |

### API-007 — Supabase: Award Achievement

| Field | Value |
|-------|-------|
| **Method** | Supabase client `table('user_achievements').insert()` |
| **Auth** | Service role key |
| **Request Schema** | `{ child_id: UUID, achievement_id: UUID, achievement_data: JSON }` |
| **Response** | Inserted row. |
| **Linked ReqIDs** | REQ-0018 |
| **Linked EntIDs** | ENT-004, ENT-005 |
| **CodeRefs** | `backend/supabase_client.py:award_achievement` |
| **GAP** | Not called from any route. |

### API-008 — Supabase: Get Parent Analytics

| Field | Value |
|-------|-------|
| **Method** | Supabase client — multiple queries aggregated |
| **Auth** | Service role key |
| **Request Schema** | `parent_id: UUID` |
| **Response** | `{ children: [...], total_time: int, lessons_completed: int, achievements: int }` |
| **Linked ReqIDs** | REQ-0019 |
| **Linked EntIDs** | ENT-001, ENT-002, ENT-003, ENT-004 |
| **CodeRefs** | `backend/supabase_client.py:get_parent_analytics` |
| **GAP** | GAP-012. No route or UI. |

### API-009 — Supabase: Health Check

| Field | Value |
|-------|-------|
| **Method** | Supabase client `table('profiles').select().limit(1)` |
| **Auth** | Service role key |
| **Response** | `True` if reachable, `False` otherwise. |
| **Linked ReqIDs** | REQ-0032 |
| **CodeRefs** | `backend/supabase_client.py:health_check` |

### API-010 — Supabase: Update Child

| Field | Value |
|-------|-------|
| **Method** | Supabase client `table('children').update()` |
| **Auth** | Anon key + RLS |
| **Request Schema** | `child_id: UUID, updates: { name?: string, age?: int }` |
| **Linked ReqIDs** | REQ-0033 |
| **Linked EntIDs** | ENT-002 |
| **CodeRefs** | `lib/children.ts:updateChild` |

### API-011 — Supabase: Delete Child

| Field | Value |
|-------|-------|
| **Method** | Supabase client `table('children').delete()` |
| **Auth** | Anon key + RLS |
| **Request Schema** | `child_id: UUID` |
| **Linked ReqIDs** | REQ-0033 |
| **Linked EntIDs** | ENT-002 |
| **CodeRefs** | `lib/children.ts:deleteChild` |

### EVT-001 — Socket.IO: init_sparkle

| Field | Value |
|-------|-------|
| **Type** | Socket.IO Event (client → server) |
| **Channel** | `init_sparkle` |
| **Payload** | `{ child_name: string, child_age: int, tier: string }` |
| **Response Event** | `sparkle_ready` with `{ session_id: string, welcome_message: string }` |
| **Linked ReqIDs** | REQ-0013 |
| **CodeRefs** | `main.py:1198-1215`, `backend/static/js/sparkle_integration.js` |

### EVT-002 — Socket.IO: sparkle_message

| Field | Value |
|-------|-------|
| **Type** | Socket.IO Event (client → server) |
| **Channel** | `sparkle_message` |
| **Payload** | `{ message: string, session_id: string }` |
| **Response Event** | `sparkle_response` with `{ response: string, session_id: string }` |
| **Error Event** | `sparkle_error` with `{ error: string }` |
| **Linked ReqIDs** | REQ-0013, REQ-0014, REQ-0015 |
| **CodeRefs** | `main.py:1217-1232`, `backend/gemini_live_sparkle_fixed.py` |


---

## 8. Data Model

### 8.1 Entity Relationship Overview

```
profiles (ENT-001)
  │
  ├──< children (ENT-002)
  │       │
  │       ├──< lesson_progress (ENT-003)
  │       ├──< user_achievements (ENT-005)
  │       ├──< exercise_submissions (ENT-014)
  │       ├──< module_progress (ENT-013)
  │       └──< projects (ENT-008)
  │               │
  │               └──< project_collaborators (ENT-009)
  │
  ├──< subscriptions (ENT-007)
  │       │
  │       └──> subscription_plans (ENT-006)
  │
  ├──< messages (ENT-010) [sender]
  ├──< notifications (ENT-011)
  └──< analytics_events (ENT-012)

achievements (ENT-004) ──< user_achievements (ENT-005)

modules ──< lessons ──< exercises
```

### 8.2 Table Definitions

#### ENT-001: profiles

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK, references auth.users(id) ON DELETE CASCADE | Supabase auth user ID |
| email | TEXT | UNIQUE, NOT NULL | |
| full_name | TEXT | NOT NULL | |
| role | user_role ENUM | DEFAULT 'parent' | Values: parent, child, teacher, admin |
| avatar_url | TEXT | | |
| settings | JSONB | DEFAULT '{}' | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Auto-updated via trigger |

#### ENT-002: children

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK, DEFAULT gen_random_uuid() | |
| parent_id | UUID | FK → profiles(id) ON DELETE CASCADE, NOT NULL | |
| name | TEXT | NOT NULL | |
| age | INTEGER | NOT NULL, CHECK (3-18) | |
| tier | learning_tier ENUM | NOT NULL | Values: magic_workshop, innovation_lab, professional_studio |
| avatar_url | TEXT | | |
| magic_points | INTEGER | DEFAULT 0, CHECK (≥0) | |
| current_module_id | UUID | FK → modules(id) | |
| preferences | JSONB | DEFAULT '{}' | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ENT-003: lesson_progress

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| child_id | UUID | FK → children(id) ON DELETE CASCADE | |
| lesson_id | UUID | FK → lessons(id) ON DELETE CASCADE | |
| status | progress_status ENUM | DEFAULT 'not_started' | Values: not_started, in_progress, completed |
| score | INTEGER | DEFAULT 0, CHECK (0-100) | |
| time_spent_minutes | INTEGER | DEFAULT 0, CHECK (≥0) | |
| attempts | INTEGER | DEFAULT 0 | |
| completed_at | TIMESTAMPTZ | | |
| progress_data | JSONB | DEFAULT '{}' | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |
| | | UNIQUE(child_id, lesson_id) | |

#### ENT-004: achievements

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| name | TEXT | NOT NULL, UNIQUE | |
| description | TEXT | | |
| icon | TEXT | | Emoji or URL |
| category | TEXT | | |
| tier | learning_tier ENUM | | NULL = all tiers |
| points | INTEGER | DEFAULT 0 | |
| criteria | JSONB | DEFAULT '{}' | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Seed Data**: First Steps (🌟, 10pts), Quick Learner (⚡, 25pts), Persistent Coder (💪, 50pts), Creative Builder (🎨, 75pts), Master Wizard (🧙, 100pts)

#### ENT-005: user_achievements

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| child_id | UUID | FK → children(id) ON DELETE CASCADE | |
| achievement_id | UUID | FK → achievements(id) ON DELETE CASCADE | |
| earned_at | TIMESTAMPTZ | DEFAULT NOW() | |
| | | UNIQUE(child_id, achievement_id) | |

#### ENT-006: subscription_plans

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| name | TEXT | NOT NULL, UNIQUE | |
| description | TEXT | | |
| price_monthly | DECIMAL(10,2) | NOT NULL | |
| price_yearly | DECIMAL(10,2) | | |
| max_children | INTEGER | NOT NULL | |
| features | JSONB | DEFAULT '[]' | |
| is_active | BOOLEAN | DEFAULT true | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Seed Data**: Free ($0, 1 child), Family ($14.99/mo, 3 children), Classroom ($49.99/mo, 30 children)

#### ENT-007: subscriptions

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → profiles(id) ON DELETE CASCADE | |
| plan_id | UUID | FK → subscription_plans(id) | |
| status | subscription_status ENUM | DEFAULT 'active' | Values: active, cancelled, expired, past_due |
| billing_cycle | TEXT | DEFAULT 'monthly' | |
| current_period_start | TIMESTAMPTZ | | |
| current_period_end | TIMESTAMPTZ | | |
| payment_method | JSONB | | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ENT-008: projects

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| child_id | UUID | FK → children(id) ON DELETE CASCADE | |
| title | TEXT | NOT NULL | |
| description | TEXT | | |
| project_type | TEXT | | |
| content | JSONB | DEFAULT '{}' | |
| is_public | BOOLEAN | DEFAULT false | |
| views | INTEGER | DEFAULT 0 | |
| likes | INTEGER | DEFAULT 0 | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ENT-009: project_collaborators

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| project_id | UUID | FK → projects(id) ON DELETE CASCADE | |
| child_id | UUID | FK → children(id) ON DELETE CASCADE | |
| role | TEXT | DEFAULT 'viewer' | |
| added_at | TIMESTAMPTZ | DEFAULT NOW() | |
| | | UNIQUE(project_id, child_id) | |

#### ENT-010: messages

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| sender_id | UUID | FK → profiles(id) ON DELETE CASCADE | |
| receiver_id | UUID | FK → profiles(id) ON DELETE CASCADE | |
| content | TEXT | NOT NULL | |
| is_read | BOOLEAN | DEFAULT false | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ENT-011: notifications

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → profiles(id) ON DELETE CASCADE | |
| title | TEXT | NOT NULL | |
| message | TEXT | | |
| type | TEXT | | |
| is_read | BOOLEAN | DEFAULT false | |
| data | JSONB | DEFAULT '{}' | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ENT-012: analytics_events

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → profiles(id) | |
| event_type | TEXT | NOT NULL | |
| event_data | JSONB | DEFAULT '{}' | |
| session_id | TEXT | | |
| ip_address | INET | | |
| user_agent | TEXT | | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ENT-013: module_progress

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| child_id | UUID | FK → children(id) ON DELETE CASCADE | |
| module_id | UUID | FK → modules(id) ON DELETE CASCADE | |
| status | progress_status ENUM | DEFAULT 'not_started' | |
| completion_percentage | DECIMAL(5,2) | DEFAULT 0 | |
| started_at | TIMESTAMPTZ | | |
| completed_at | TIMESTAMPTZ | | |
| | | UNIQUE(child_id, module_id) | |

#### ENT-014: exercise_submissions

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| child_id | UUID | FK → children(id) ON DELETE CASCADE | |
| exercise_id | UUID | FK → exercises(id) ON DELETE CASCADE | |
| submission_data | JSONB | NOT NULL | |
| is_correct | BOOLEAN | | |
| score | INTEGER | CHECK (0-100) | |
| feedback | TEXT | | |
| submitted_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### Additional Tables (modules, lessons, exercises)

These curriculum content tables are defined in `001_initial_schema.sql` but have **no seed data** and are not populated by any application code.

- **modules**: id, tier, title, description, order_index, is_published, estimated_duration, prerequisites
- **lessons**: id, module_id, title, description, content (JSONB), order_index, lesson_type, estimated_duration
- **exercises**: id, lesson_id, title, description, exercise_type, content (JSONB), solution (JSONB), hints (JSONB), max_score, order_index

### 8.3 Custom Enums

| Enum | Values |
|------|--------|
| `user_role` | parent, child, teacher, admin |
| `learning_tier` | magic_workshop, innovation_lab, professional_studio |
| `progress_status` | not_started, in_progress, completed |
| `subscription_status` | active, cancelled, expired, past_due |

### 8.4 Database Functions

| Function | Trigger | Purpose |
|----------|---------|---------|
| `update_updated_at()` | ON UPDATE (all tables with updated_at) | Auto-update `updated_at` timestamp |
| `assign_tier_by_age(age)` | Called by `handle_new_child` | Returns learning_tier based on age |
| `handle_new_user()` | AFTER INSERT ON auth.users | Creates profile in public.profiles |
| `handle_new_child()` | BEFORE INSERT ON children | Assigns tier if not provided |
| `update_module_progress_on_lesson_completion()` | AFTER UPDATE ON lesson_progress | Recalculates module completion % |
| `check_and_award_achievements()` | AFTER INSERT ON lesson_progress | Checks if achievement criteria met |
| `send_notification(user_id, title, message, type)` | Called by other functions | Inserts notification record |
| `increment_project_views(project_id)` | Called via RPC | Atomically increments view count |

### 8.5 Migrations Strategy

Migrations are stored in `supabase/migrations/` and numbered sequentially (001-005). They are designed to be applied in order via Supabase CLI (`supabase db push`) or manually. Each migration is idempotent where possible (uses `IF NOT EXISTS`).

### 8.6 Data Retention / Audit

No explicit data retention policy is implemented. The `analytics_events` table captures user actions with timestamps but has no TTL or archival process. The `updated_at` triggers provide basic audit trail for record modifications.

---

## 9. Integrations

### 9.1 Supabase (Database + Auth)

| Field | Value |
|-------|-------|
| **Purpose** | PostgreSQL database hosting, user authentication, Row-Level Security, real-time subscriptions (not used), edge functions (not used). |
| **Auth Mechanism** | Service role key (backend, full access), Anon key (frontend, RLS-restricted). |
| **Config/Env Vars** | `SUPABASE_URL` = `https://ylymepybqcykyomsmxwk.supabase.co`, `SUPABASE_SERVICE_ROLE_KEY` (secret), `SUPABASE_ANON_KEY` (public), `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` |
| **Error Handling** | Backend: try/except with fallback to in-memory dict storage. Frontend: error state in React components. |
| **Data Mapping** | Direct table mapping. JSONB for flexible fields (settings, preferences, progress_data, content). |
| **CodeRefs** | `backend/supabase_client.py` (399 LOC), `lib/supabase.ts`, `lib/auth.ts`, `lib/children.ts` |
| **Tests** | None. Required: T-021 through T-025, T-038. |
| **Gaps** | GAP-015: Service role key hardcoded in source. GAP-006: Flask does not use Supabase for user storage. |

### 9.2 Google Gemini AI

| Field | Value |
|-------|-------|
| **Purpose** | AI-powered tutoring responses for Professor Sparkle. Generates age-appropriate, curriculum-aware coding guidance. |
| **Auth Mechanism** | API key via `google-generativeai` Python SDK. |
| **Config/Env Vars** | `OPENAI_API_KEY` (confusingly named, used for Gemini in `gemini_live_sparkle_fixed.py`) or `GEMINI_API_KEY` (used in `professor_sparkle.py`). |
| **Error Handling** | Try/except around API call. On failure: falls back to pattern-matched static responses based on message keywords (greeting, help, code, debug, etc.). |
| **Data Mapping** | Input: system prompt (personality + age style + tier context + curriculum) + user message. Output: text response. |
| **CodeRefs** | `backend/gemini_live_sparkle_fixed.py` (primary), `backend/professor_sparkle.py` (variant) |
| **Tests** | None. Required: T-008 through T-013. |
| **Gaps** | CONF-007: Plans describe WebRTC voice interaction, not implemented. Variable naming confusion (OPENAI_API_KEY for Gemini). |

---

## 10. Security & Permissions

### 10.1 Auth Flows

**Flask Authentication**:
1. Signup: SHA-256(password + random_salt) → store in Python list → generate JWT (HS256, 30-day expiry) → set `auth_token` cookie (httponly).
2. Signin: lookup by email → verify SHA-256 hash → generate JWT → set cookie.
3. Route protection: decorator reads `auth_token` cookie → decode JWT → lookup user by id → inject into request context.

**Next.js Authentication**:
1. Signup: Supabase `auth.signUp(email, password)` → Supabase handles hashing (bcrypt) → creates `auth.users` row → trigger creates `profiles` row → Supabase session cookie.
2. Signin: Supabase `auth.signInWithPassword()` → Supabase verifies → session.
3. Route protection: `AuthContext` checks Supabase session → redirect if not authenticated.

### 10.2 Roles / Permissions Matrix

| Role | View Own Dashboard | View Own Children | Add Child | Edit Child | Delete Child | Access Learning Env | View Other Users | Admin Panel |
|------|-------------------|-------------------|-----------|------------|--------------|--------------------|--------------------|-------------|
| **parent** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (via child) | ❌ | ❌ |
| **child** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (own tier) | ❌ | ❌ |
| **teacher** | ✅ | ✅ (classroom) | ❌ | ❌ | ❌ | ✅ | ✅ (classroom) | ❌ |
| **admin** | ✅ | ✅ (all) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> Note: Teacher and admin roles are defined in the enum but have no implementation.

### 10.3 Sensitive Data Handling

| Data | Storage | Protection |
|------|---------|------------|
| Passwords (Flask) | In-memory Python list | SHA-256 + random salt (WEAK — GAP-020) |
| Passwords (Supabase) | Supabase auth.users | bcrypt (Supabase default) |
| JWT tokens | Cookie | httponly flag, 30-day expiry |
| Supabase service role key | Source code (!) | **CRITICAL VULNERABILITY** — GAP-015 |
| Child personal data | Supabase children table | RLS policies restrict to parent |
| Chat messages | In-memory (session) | Not persisted. Lost on disconnect. |

### 10.4 Secrets Handling

| Secret | Where Used | Current Storage | Recommended |
|--------|-----------|-----------------|-------------|
| `FLASK_SECRET_KEY` | JWT signing | Env var with hardcoded default | Env var only, no default |
| `SUPABASE_SERVICE_ROLE_KEY` | Backend DB access | **Hardcoded in source code** | Env var only, rotate immediately |
| `SUPABASE_ANON_KEY` | Frontend DB access | Env var (public, OK) | OK as-is |
| `OPENAI_API_KEY` / `GEMINI_API_KEY` | AI tutor | Env var | OK |

### 10.5 Audit Logging

- `lib/security.ts:logSecurityEvent()` logs to Supabase `analytics_events` table with event_type, user_id, session_id, IP, user_agent.
- Flask backend has no audit logging (uses `print()` statements).
- No centralized log aggregation or alerting.

---

## 11. Observability & Operations

### 11.1 Logging Strategy

**Current state**: No structured logging. Flask uses `print()` statements for debug output. Frontend uses `console.error()` for error reporting.

**Recommended**: Implement `structlog` (Python) for structured JSON logging. Configure log levels (DEBUG, INFO, WARN, ERROR). Route to stdout for container-based deployment.

### 11.2 Metrics / Tracing

**Current state**: None. No metrics collection, no request tracing, no performance monitoring.

**Recommended**: Add `/health` endpoint (partially exists via Supabase health check). Add `/metrics` endpoint with request count, latency percentiles, error rate, active Socket.IO connections, Gemini API call count/latency.

### 11.3 Alerts

**Current state**: None.

**Recommended**: Alert on: Supabase connection failure, Gemini API error rate >10%, response latency >5s, Socket.IO connection count >1000.

### 11.4 Runbook Basics

| Scenario | Diagnosis | Resolution |
|----------|-----------|------------|
| **Flask won't start** | Check `PORT` env var, check `requirements.txt` installed | Verify Python deps, check port availability |
| **Supabase unreachable** | Check `SUPABASE_URL` env var, check Supabase dashboard status | App falls back to in-memory storage automatically. Restore Supabase connection when available. |
| **Gemini API errors** | Check `OPENAI_API_KEY`/`GEMINI_API_KEY`, check API quota | App falls back to static responses automatically. Check API dashboard for quota/billing. |
| **Socket.IO disconnects** | Check server memory, check connection limits | Client auto-reconnects. If persistent, restart Flask server. |
| **All user data lost** | Flask restarted (in-memory storage) | This is expected with current architecture. Migrate to Supabase persistence (GAP-006). |
| **JWT decode errors** | Secret key changed between restarts | Ensure `FLASK_SECRET_KEY` is consistent across deployments. |

### 11.5 Operational Failure Modes

| Component | Failure Mode | Impact | Mitigation |
|-----------|-------------|--------|------------|
| Flask server | Crash/restart | All in-memory user data lost | GAP-006: Use Supabase for persistence |
| Supabase | Outage | Next.js auth fails, Flask falls back to in-memory | Supabase has 99.9% SLA. Monitor status page. |
| Gemini API | Rate limit / outage | Professor Sparkle uses fallback responses | Fallback is automatic. Quality degrades but service continues. |
| Socket.IO | Connection limit | New Sparkle sessions rejected | Scale horizontally or use Redis adapter for Socket.IO. |

---

## 12. Build / Deploy / Environments

### 12.1 Local Development Steps

**Backend**:
```bash
cd Codopia
pip install -r requirements.txt
export FLASK_SECRET_KEY="dev-secret-key"
export SUPABASE_URL="https://ylymepybqcykyomsmxwk.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="<your-key>"
export OPENAI_API_KEY="<your-gemini-key>"
python main.py
# Flask runs on http://localhost:5000
```

**Frontend**:
```bash
cd Codopia
npm install
# Create .env.local with:
# NEXT_PUBLIC_SUPABASE_URL=https://ylymepybqcykyomsmxwk.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-anon-key>
# NEXT_PUBLIC_APP_URL=http://localhost:3000
npm run dev
# Next.js runs on http://localhost:3000
```

### 12.2 Build Scripts

| Script | Command | Purpose |
|--------|---------|---------|
| `npm run dev` | `next dev --turbopack` | Start Next.js dev server with Turbopack |
| `npm run build` | `next build --turbopack` | Production build |
| `npm run start` | `next start` | Start production server |
| `npm run lint` | `eslint` | Lint TypeScript/React code |
| `pip install -r requirements.txt` | — | Install Python dependencies |

### 12.3 CI/CD

**Current state**: None. No GitHub Actions, no automated testing, no automated deployment.

**Recommended**: GitHub Actions workflow:
1. On PR: lint → type-check → unit tests → integration tests
2. On merge to main: build → E2E tests → deploy to staging
3. On release tag: deploy to production

### 12.4 Deployment Targets

| Target | Service | Config File | Notes |
|--------|---------|-------------|-------|
| Backend | Railway | `railway.json`, `Procfile` | **BUG**: Procfile references `python src/main.py` but correct path is `python main.py` (CONF-008) |
| Frontend | Vercel | `vercel.json` | Next.js auto-detected. Env vars set in Vercel dashboard. |
| Database | Supabase | `supabase/migrations/` | Apply via `supabase db push` |

### 12.5 Infrastructure Resources

| Resource | Provider | Tier | Notes |
|----------|----------|------|-------|
| PostgreSQL | Supabase | Free (500MB) | Project: `ylymepybqcykyomsmxwk` |
| Backend hosting | Railway | Starter | Auto-sleep on inactivity |
| Frontend hosting | Vercel | Hobby | Serverless functions, 30s timeout |
| AI API | Google | Pay-per-use | Gemini Pro |

### 12.6 Environment Variable Catalog

| Variable | Meaning | Where Used | Required |
|----------|---------|-----------|----------|
| `FLASK_SECRET_KEY` | JWT signing key for Flask auth | `main.py:25`, `backend/auth_service.py:12` | Yes (has insecure default) |
| `FLASK_DEBUG` | Enable Flask debug mode | `main.py:1325` | No (default: false) |
| `PORT` | Flask server port | `main.py:29`, `backend/main.py:29` | No (default: 5000) |
| `SUPABASE_URL` | Supabase project URL | `backend/supabase_client.py:20`, `backend/auth_service.py:9` | Yes (has hardcoded default) |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase admin key (SECRET) | `backend/supabase_client.py:21` | Yes (**hardcoded in source — CRITICAL**) |
| `SUPABASE_ANON_KEY` | Supabase public key | `backend/auth_service.py:10` | Yes |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase URL for frontend | `lib/supabase.ts:3`, `vercel.json:17` | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key for frontend | `lib/supabase.ts:4`, `vercel.json:18` | Yes |
| `NEXT_PUBLIC_APP_URL` | Frontend base URL | `app/layout.tsx:20` | No (default: localhost:3000) |
| `NEXT_PUBLIC_BACKEND_URL` | Backend API URL for frontend | `vercel.json:19` | Yes (for production) |
| `OPENAI_API_KEY` | Used for Gemini AI (confusing name) | `backend/gemini_live_sparkle_fixed.py:43` | Yes (for AI features) |
| `GEMINI_API_KEY` | Google Gemini API key | `backend/professor_sparkle.py:18` | Alternative to OPENAI_API_KEY |
| `SECRET_KEY` | Legacy Flask secret | `legacy/main_new.py:24` | No (legacy) |
| `JWT_SECRET_KEY` | Legacy JWT key | `legacy/main_new.py:25` | No (legacy) |
| `DATABASE_URL` | Legacy SQLite URL | `legacy/main_new.py:26` | No (legacy) |

---

## 13. Testing Strategy + Coverage Report

> Full details in [`docs/Testing/Test_Strategy.md`](./Testing/Test_Strategy.md) and [`docs/Testing/Test_Catalog.md`](./Testing/Test_Catalog.md)

### 13.1 Existing Tests

**None.** The file `test_magic_workshop.py` is a standalone Flask demo server that creates its own app instance with module routes. It is not a test suite and does not use any testing framework.

### 13.2 Missing Tests (Required)

| Category | Count | Priority |
|----------|-------|----------|
| Unit tests (backend) | 15 | P0 |
| Unit tests (frontend) | 13 | P0 |
| Integration tests | 10 | P0 |
| E2E tests | 5 | P1 |
| **Total** | **43** | |

### 13.3 Critical E2E Flows

1. **Parent Registration** (T-039): signup → add child → verify dashboard
2. **Parent Sign-In** (T-040): signin → verify dashboard with children
3. **Magic Workshop** (T-041): access learning env → interact with blocks → chat with Sparkle
4. **Add Child** (T-042): dashboard → add child → verify tier assignment
5. **Sign-Out** (T-043): sign out → verify session cleared

### 13.4 Regression Suite Recommendations

- Run all unit and integration tests on every PR.
- Run E2E tests on merge to main.
- Add visual regression testing (Percy or Chromatic) for UI components.
- Add Professor Sparkle safety regression: maintain list of known-unsafe inputs and verify they are always caught.

---

## 14. Inconsistencies, Gaps, and Decisions

> Full details in [`docs/Gaps_Conflicts_Decisions.md`](./Gaps_Conflicts_Decisions.md)

### 14.1 Critical Issues (Fix Immediately)

| ID | Issue | Impact |
|----|-------|--------|
| GAP-015 | Supabase service role key hardcoded in source code | **SECURITY**: Full database access exposed in public repo |
| CONF-006 | Dual application stacks (Flask + Next.js) serving overlapping features | **ARCHITECTURE**: Maintenance burden, inconsistent UX, data isolation |
| GAP-006 | Flask uses in-memory storage — all data lost on restart | **DATA LOSS**: No persistence for Flask-created users |
| CONF-008 | Procfile references wrong path (`src/main.py` vs `main.py`) | **DEPLOYMENT**: Railway deployment fails |

### 14.2 High Priority (Fix Before Beta)

| ID | Issue | Impact |
|----|-------|--------|
| GAP-001 | Zero automated tests | No quality assurance |
| GAP-020 | Weak password hashing (SHA-256, no key stretching) | Security vulnerability |
| GAP-016 | Massive file duplication (files in 2-4 locations) | Maintenance nightmare |
| CONF-003 | Modules 2-10 not routed despite "95% ready" claims | 90% of learning content inaccessible |
| GAP-002 | Password reset has no email service | Feature non-functional |
| GAP-014 | No .env.example, secrets in code | Onboarding friction, security risk |

### 14.3 Prioritized Fix List

1. **IMMEDIATE**: Rotate Supabase service role key (GAP-015)
2. **Week 1**: Decide primary stack — Flask or Next.js (DEC-001)
3. **Week 1**: Fix Procfile path (CONF-008)
4. **Week 1**: Create .env.example, remove hardcoded secrets (GAP-014)
5. **Week 2**: Consolidate file duplicates (GAP-016, DEC-003)
6. **Week 2**: Connect Flask to Supabase for persistence (GAP-006) OR retire Flask UI
7. **Week 2**: Wire modules 2-10 routes (CONF-003)
8. **Week 3**: Implement password hashing upgrade (GAP-020)
9. **Week 3**: Set up test infrastructure and write P0 tests (GAP-001)
10. **Week 4**: Implement email service for password reset (GAP-002)

---

## 15. Rebuild This App Checklist

A numbered sequence that another coding agent can follow to recreate the Codopia platform from scratch.

### Phase 1: Repository Scaffold (Day 1)

1. Create monorepo with structure:
   ```
   codopia/
   ├── backend/          # Flask API + Socket.IO
   ├── frontend/         # Next.js 15 app
   ├── supabase/         # Migrations and config
   ├── docs/             # Documentation
   └── .github/          # CI/CD workflows
   ```

2. Initialize `backend/`:
   - `requirements.txt`: Flask==3.x, flask-socketio, flask-cors, PyJWT, supabase, google-generativeai
   - `app.py`: Flask app factory with CORS, SocketIO
   - `.env.example`: all env vars from Section 12.6

3. Initialize `frontend/`:
   - `npx create-next-app@latest --typescript --tailwind --app`
   - Install: @supabase/supabase-js, @supabase/auth-helpers-nextjs, @radix-ui/react-*, lucide-react, recharts, zustand, zod, react-hook-form
   - `.env.local.example`: NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, NEXT_PUBLIC_BACKEND_URL

### Phase 2: Contracts First — Database Schema (Day 1-2)

4. Create Supabase project.

5. Write and apply migrations in order:
   - `001_initial_schema.sql`: Create all enums (user_role, learning_tier, progress_status, subscription_status). Create all 17 tables per Section 8.2 with proper constraints, indexes, and foreign keys.
   - `002_rls_policies.sql`: Enable RLS on all tables. Create policies per Section 10.2 (parent sees own children, public project access, admin override).
   - `003_functions_triggers.sql`: Create all 8 functions per Section 8.4. Create triggers. Insert seed data (3 subscription plans, 5 achievements).
   - `004_tier_assignment_functions.sql`: Enhanced tier assignment logic.
   - `005_enhanced_rls_policies.sql`: Additional RLS refinements.

6. Verify schema: run `supabase db push`, confirm all tables created, test RLS with anon key.

### Phase 3: Backend Services (Day 2-3)

7. Build `backend/supabase_client.py`:
   - SupabaseClient class with connection pooling
   - CRUD methods for: profiles, children, lesson_progress, user_achievements, analytics_events
   - Fallback to in-memory dict when Supabase unreachable
   - Health check method
   - All methods per Section 7 (API-005 through API-011)

8. Build `backend/auth_service.py`:
   - Use Supabase auth (NOT in-memory storage)
   - `create_user()`: call Supabase auth.signUp, then create child profile
   - `sign_in()`: call Supabase auth.signInWithPassword
   - `verify_token()`: validate Supabase JWT
   - Password hashing: rely on Supabase (bcrypt)

9. Build `backend/professor_sparkle.py`:
   - ProfessorSparkle class per Section 4 (REQ-0013 through REQ-0016)
   - Safety check with forbidden topics list and emergency keywords (REQ-0014)
   - Age-appropriate response style with 5 brackets (REQ-0015)
   - Curriculum awareness for 3 tiers (REQ-0016)
   - Gemini API integration with fallback to pattern-matched responses
   - System prompt builder: personality + age style + tier context + curriculum

### Phase 4: Backend API Routes (Day 3-4)

10. Build Flask HTTP routes:
    - `POST /api/auth/signup` → API-001
    - `POST /api/auth/signin` → API-002
    - `POST /api/auth/signout` → API-003
    - `POST /api/auth/forgot-password` → API-004
    - `GET /api/health` → API-009
    - `GET /api/children` → list children for authenticated parent
    - `POST /api/children` → API-005
    - `PUT /api/children/:id` → API-010
    - `DELETE /api/children/:id` → API-011
    - `GET /api/progress/:child_id` → API-006 (read)
    - `POST /api/progress/:child_id` → API-006 (write)
    - `GET /api/achievements/:child_id` → API-007 (read)
    - `GET /api/analytics` → API-008

11. Build Socket.IO handlers:
    - `init_sparkle` → EVT-001: create session, return welcome message
    - `sparkle_message` → EVT-002: safety check → AI response → emit response
    - `disconnect` → clean up session

### Phase 5: Frontend — Auth & Layout (Day 4-5)

12. Build `frontend/lib/supabase.ts`: Supabase client initialization.

13. Build `frontend/contexts/AuthContext.tsx`: auth state management, session persistence, auto-refresh.

14. Build `frontend/lib/auth.ts`: signUpParent, signInUser, signOut, createChildProfile per Section 7.

15. Build `frontend/lib/security.ts`: sanitizeInput, validateProjectContent, CSRF tokens, session validation per REQ-0026 through REQ-0029.

16. Build `frontend/lib/children.ts`: CRUD operations, tier logic, progress helpers, validation per REQ-0007, REQ-0033.

17. Build `frontend/components/ui/`: Button, Card (Radix UI + Tailwind + CVA).

### Phase 6: Frontend — Pages (Day 5-7)

18. Build `frontend/app/layout.tsx`: root layout with AuthProvider, metadata, global styles.

19. Build `frontend/app/page.tsx` (SCR-001): landing page with tier showcase, Professor Sparkle intro, pricing, CTA.

20. Build `frontend/app/auth/signup/page.tsx` (SCR-003): multi-step registration (parent form → child form → complete).

21. Build `frontend/app/auth/signin/page.tsx` (SCR-004): email/password sign-in.

22. Build `frontend/app/auth/callback/page.tsx` (SCR-006): OAuth callback handler.

23. Build `frontend/app/dashboard/page.tsx` + `DashboardContent.tsx` (SCR-007): parent dashboard with child cards grid, add child form.

24. Build `frontend/components/ChildCard.tsx` (SCR-008): child card with tier badge, progress, actions.

### Phase 7: Frontend — Learning Environments (Day 7-10)

25. Build Magic Workshop (SCR-009, REQ-0010):
    - Block palette with drag-and-drop (Move Wizard, Repeat, Create Star, Play Sound, Change Color)
    - Workspace drop zone
    - Live preview panel
    - Professor Sparkle chat panel (Socket.IO client)
    - 10 progressive modules with routes
    - Purple/pink magical theme

26. Build Innovation Lab (REQ-0011):
    - Component palette (buttons, labels, inputs, charts, game canvas)
    - Design canvas
    - Live phone preview mockup
    - 10 progressive modules
    - Blue/cyan innovation theme

27. Build Professional Studio (REQ-0012):
    - Code editor with syntax highlighting (Monaco Editor or CodeMirror)
    - Terminal/console output panel
    - File tree
    - 10 progressive modules (Python, JS, React, Flask, DB, algorithms, DevOps)
    - Dark professional theme

### Phase 8: Integration Setup (Day 10-11)

28. Configure Supabase:
    - Set up auth providers (email, Google, GitHub)
    - Configure email templates for verification and password reset
    - Set up storage bucket for avatars (if needed)

29. Configure Gemini AI:
    - Obtain API key
    - Set environment variable
    - Test with sample prompts for each age bracket
    - Verify safety check catches all forbidden topics

30. Configure deployment:
    - Railway: fix Procfile to `web: python backend/app.py`
    - Vercel: set env vars in dashboard
    - Set up custom domain (optional)

### Phase 9: Test Setup (Day 11-12)

31. Backend tests:
    - Install pytest, pytest-mock
    - Write unit tests T-001 through T-013 (auth, safety, age-appropriate responses)
    - Write integration tests T-029 through T-038 (Flask routes, Socket.IO)

32. Frontend tests:
    - Install Jest, @testing-library/react, jest-localstorage-mock
    - Write unit tests T-014 through T-028 (security, children, components)

33. E2E tests:
    - Install Cypress
    - Write E2E tests T-039 through T-043 (registration, sign-in, learning, add child, sign-out)

### Phase 10: Run + Verify (Day 12-13)

34. Local verification:
    - Start backend: `cd backend && python app.py`
    - Start frontend: `cd frontend && npm run dev`
    - Run through all 5 E2E flows manually
    - Verify Professor Sparkle responds correctly for each age bracket
    - Verify safety check blocks forbidden content
    - Verify tier assignment for boundary ages (7, 8, 12, 13)

35. Run all tests:
    - `cd backend && pytest -v`
    - `cd frontend && npm test`
    - `cd frontend && npx cypress run`

36. Deploy to staging:
    - Push to Railway (backend)
    - Push to Vercel (frontend)
    - Run smoke tests against staging URLs
    - Verify health endpoint responds
    - Verify sign-in flow works end-to-end

37. Production deploy:
    - Verify all staging tests pass
    - Deploy backend to production Railway
    - Deploy frontend to production Vercel
    - Run post-deploy smoke tests
    - Monitor logs for 1 hour

---

## 16. Multi-Agent System (CrewAI + Agentic-Framework Hybrid) — IMPLEMENTED 2026-03-10

> This section documents the new multi-agent system that replaces the single-agent Professor Sparkle implementation. It was designed as a hybrid architecture combining CrewAI's orchestration with patterns borrowed from the `agentic-framework` (Supercog), specifically the PauseForInput pattern and rich event streaming.

### 16.1 Architecture Decision

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Primary Framework** | CrewAI 0.108+ | 25,000+ GitHub stars, Python-native, hierarchical agent teams, active maintenance |
| **Patterns Borrowed** | `agentic-framework` PauseForInput, Event Streaming, Tool-as-Agent | Better pedagogy support (agent pauses to ask questions), richer frontend integration |
| **LLM Provider** | OpenAI `gpt-4.1-mini` via LiteLLM | Cost-effective ($1.13/student/month est.), fast responses, multi-model failover ready |
| **Rejected** | Embedding Pi Coding Agent (TypeScript) | Would require Node.js runtime in Python backend; CrewAI custom tools replicate Pi's 4 core tools natively |
| **Rejected** | Full migration to `agentic-framework` | Only 122 GitHub stars, Ray dependency adds 500MB, small community risk |

### 16.2 Agent Inventory

| Agent | Role | LLM | Tools | max_iter | Purpose |
|-------|------|-----|-------|----------|---------|
| **Orchestrator** | Intent Classifier + Router | `gpt-4.1-mini` (FAST) | `safety_filter` | 3 | Classifies student intent (TUTOR/CODING/HARDWARE/GENERAL) and routes to specialist agent |
| **Tutor (Socratic)** | Teaching through questions | `gpt-4.1-mini` | `ask_student`, `generate_question`, `get_curriculum`, `safety_filter` | 5 | Pedagogy-first: asks Socratic questions, never gives direct answers |
| **Coding Agent** | Code execution + debugging | `gpt-4.1-mini` | `run_code`, `ask_student`, `safety_filter` | 5 | Runs student code in sandbox, identifies errors, guides student to fix them |
| **Hardware Agent** | Physical computing guide | `gpt-4.1-mini` | `simulate_circuit`, `run_code`, `ask_student`, `get_curriculum`, `safety_filter` | 5 | Wokwi circuit simulation, MicroPython for Pi Pico, LED/sensor projects |

### 16.3 Tool Library

| Tool | Class | File | Description |
|------|-------|------|-------------|
| `ask_student` | `PauseForInputTool` | `backend/agents/tools/pause_for_input.py` | **Core pedagogy tool.** Pauses agent, asks student a question (open/multiple-choice/fill-blank), waits for response. In demo mode returns simulated response. In live mode blocks until frontend submits answer. |
| `run_code` | `CodeSandboxTool` | `backend/agents/tools/code_sandbox.py` | Executes Python/MicroPython code in isolated subprocess with 10s timeout. Returns output or kid-friendly error messages. Blocks dangerous imports (os, sys, subprocess, etc.). |
| `generate_question` | `SocraticQuestionTool` | `backend/agents/tools/socratic.py` | Generates age-appropriate Socratic questions based on topic and tier. Returns question + follow-up prompts. |
| `get_curriculum` | `CurriculumTool` | `backend/agents/tools/curriculum.py` | Returns curriculum data for a tier (module list, learning objectives, prerequisites). Supports per-module detail queries. |
| `safety_filter` | `SafetyFilterTool` | `backend/agents/tools/safety_filter.py` | Checks content against blocklist patterns. Blocks personal info requests, inappropriate content, off-topic queries. Returns safe/blocked status. |
| `simulate_circuit` | `WokwiSimulatorTool` | `backend/agents/tools/wokwi_simulator.py` | Returns Wokwi simulator templates for hardware projects (LED blink, traffic light, temperature sensor, etc.). Tier-aware: simpler projects for younger kids. |

### 16.4 Event System

| Event Type | Emitted By | Purpose | Frontend Action |
|------------|------------|---------|----------------|
| `agent_thinking` | Orchestrator | Agent is reasoning | Show "thinking" animation |
| `tool_call` | Any agent | Agent is using a tool | Show tool name + spinner |
| `tool_result` | Any agent | Tool returned result | Show result in panel |
| `pause_for_input` | Tutor/Coding/Hardware | Agent asks student a question | Show question UI, enable input |
| `student_response` | Frontend | Student answered | Resume agent processing |
| `chat_output` | Any agent | Final response text | Display in chat bubble |
| `code_output` | Coding Agent | Code execution result | Show in code output panel |
| `simulation_update` | Hardware Agent | Circuit state change | Update Wokwi embed |
| `turn_end` | Orchestrator | Processing complete | Hide spinners, log metrics |
| `error` | Any | Something went wrong | Show kid-friendly error message |

**CodeRef:** `backend/agents/events/__init__.py` (EventBus class, AgentEvent dataclass)

### 16.5 API Endpoints (New)

| Method | Path | Handler | Description |
|--------|------|---------|-------------|
| `POST` | `/api/agents/chat` | `agent_chat()` | Main entry point. Accepts `{message, session_id, tier, student_name}`. Returns `{response, intent, agent, events, execution_time}`. |
| `GET` | `/api/agents/health` | `agent_health()` | Returns agent status, tool status, active session count. |
| `POST` | `/api/agents/respond` | `submit_response()` | Submit student's answer to a PauseForInput question. Accepts `{session_id, response}`. |
| `GET` | `/api/agents/curriculum/<tier>` | `get_curriculum()` | Returns curriculum overview for a tier. |
| `GET` | `/api/agents/curriculum/<tier>/<module_id>` | `get_module()` | Returns specific module details. |
| `GET` | `/api/agents/hardware/<tier>` | `list_hardware()` | Lists available hardware projects for a tier. |
| `GET` | `/api/agents/hardware/<tier>/<template>` | `get_hardware_project()` | Returns specific hardware project template with code + wiring. |

**CodeRef:** `backend/agents/api_routes.py` (Flask Blueprint: `agent_bp`, prefix `/api/agents`)

### 16.6 Voice Integration Bridge

| Component | Technology | Purpose |
|-----------|------------|--------|
| **Speech-to-Text (Frontend)** | Web Speech API (`webkitSpeechRecognition`) | Browser-native, zero cost, works offline |
| **Text-to-Speech (Frontend)** | Web Speech API (`speechSynthesis`) | Tier-aware: slower rate for young kids, normal for teens |
| **Real-time Voice (Advanced)** | Gemini Live API (WebSocket) | Bidirectional streaming for natural conversation |
| **Voice Bridge** | `VoiceBridge` class | Manages voice sessions, tier-aware speech parameters, Gemini Live WebSocket connection |

**CodeRef:** `backend/agents/voice_bridge.py`

**Tier-Specific Voice Settings:**

| Tier | Speech Rate | Pitch | Voice | Primary Mode |
|------|-------------|-------|-------|-------------|
| Magic Workshop (5-7) | 0.8 (slow) | 1.2 (high) | Female, warm | Voice primary |
| Innovation Lab (8-12) | 1.0 (normal) | 1.0 | Neutral | Voice + Text equal |
| Professional Studio (13-18) | 1.1 (fast) | 0.9 (low) | Neutral, professional | Text primary |

### 16.7 Physical Computing Projects

| Tier | Hardware | Projects | Approach |
|------|----------|----------|----------|
| **Magic Workshop** | BBC micro:bit V2 (~$25) | LED Heart, Shake Dice, Musical Buttons, Night Light | MicroBlocks visual blocks, drag-and-drop |
| **Innovation Lab** | Pi Pico W (~$30-60) | LED Blink, Traffic Light, Temperature Monitor, Plant Alarm, Weather Station | MicroPython fill-in-the-blank, Wokwi simulator |
| **Professional Studio** | Pi Pico W / ESP32 (~$30-60) | IoT Dashboard, Motor Control, Sensor Network, BLE Communication, Web Server | Full MicroPython, Web Serial API flashing, real hardware |

**CodeRef:** `backend/agents/configs/physical_computing.py`

### 16.8 Verified Test Results (2026-03-10)

| Test | Agent | Tier | Input | Behavior | Time |
|------|-------|------|-------|----------|------|
| T-AGENT-001 | Tutor | Magic Workshop (5-7) | "What is a loop?" | Used `generate_question` + `ask_student` tools. Asked Emma about "repeat spells" before explaining. Socratic, age-appropriate. | 4.77s |
| T-AGENT-002 | Hardware | Innovation Lab (8-12) | "How do I make an LED blink with the Pico?" | Used `simulate_circuit` to show template. Explained GPIO pins with analogy ("like a door"). Asked about repetition patterns. | 12.44s |
| T-AGENT-003 | Coding | Professional Studio (13-18) | "Debug: for i in range(10) print(i)" | Used `run_code` to execute buggy code. Caught SyntaxError. Asked Jordan "What punctuation is missing?" instead of giving answer. | 2.46s |
| T-AGENT-004 | System | All | Health check | All 4 agents ready, all 6 tools operational, event bus connected. | <0.1s |

### 16.9 File Inventory

```
backend/agents/
├── __init__.py                          # Package init, exports CodopiaAgentSystem
├── crew.py                              # Main orchestrator: CodopiaAgentSystem class
├── api_routes.py                        # Flask Blueprint with 7 API endpoints
├── voice_bridge.py                      # Voice integration (Web Speech + Gemini Live)
├── prompts/
│   └── __init__.py                      # Agent backstories, goals, system prompts per tier
├── tools/
│   ├── __init__.py                      # Tool exports
│   ├── pause_for_input.py               # PauseForInputTool (pedagogy core)
│   ├── code_sandbox.py                  # CodeSandboxTool (safe code execution)
│   ├── socratic.py                      # SocraticQuestionTool
│   ├── curriculum.py                    # CurriculumTool
│   ├── safety_filter.py                 # SafetyFilterTool
│   └── wokwi_simulator.py              # WokwiSimulatorTool
├── events/
│   └── __init__.py                      # EventBus, AgentEvent, EventType
└── configs/
    ├── __init__.py
    └── physical_computing.py            # Hardware project templates per tier
```

### 16.10 Dependencies Added

| Package | Version | Purpose |
|---------|---------|--------|
| `crewai` | 0.108+ | Multi-agent orchestration framework |
| `crewai-tools` | latest | Base tool classes |
| `litellm` | latest | Unified LLM API (OpenAI, Claude, Gemini) |
| `google-genai` | latest | Gemini Live API for real-time voice |

### 16.11 Integration with Existing Codebase

The agent system is designed as a **drop-in addition** to the existing Flask backend:

1. **No existing code modified** — all new files in `backend/agents/`
2. **Blueprint registration** — add `from backend.agents.api_routes import agent_bp; app.register_blueprint(agent_bp)` to `main.py`
3. **Socket.IO integration** — EventBus listeners emit to existing Socket.IO server
4. **Replaces** `gemini_live_sparkle_fixed.py` for AI tutoring (old file kept as fallback)
5. **Environment variables** — uses existing `OPENAI_API_KEY` (pre-configured for multi-model via LiteLLM)

---

**END OF SSOT DOCUMENT**

*This document was generated by analyzing the complete Codopia repository (revision `154343d`) including all source code, database migrations, configuration files, and 20 planning/documentation files. Updated 2026-03-10 with Section 16 documenting the new CrewAI multi-agent system with 4 agents, 6 tools, voice integration, physical computing modules, and verified test results. Every feature, endpoint, entity, and workflow found in code or plans is cataloged with full traceability. Items that are planned but not implemented are explicitly marked. Gaps, conflicts, and pending decisions are documented in `docs/Gaps_Conflicts_Decisions.md`.*
