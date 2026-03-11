# Gaps, Conflicts & Decisions — Codopia Platform

**Generated**: 2026-02-23  
**Repo**: AllienNova/Codopia @ `154343d`

---

## 1. Conflicts (Code vs Plans)

| ID | Source | Description | Impact | Proposed Resolution |
|----|--------|-------------|--------|-------------------|
| CONF-001 | Code vs Plan #17 | **Auth system**: Plans describe Supabase auth migration. Code (`main.py`) uses in-memory dict with SHA-256 password hashing. Next.js frontend uses Supabase client auth. Two incompatible auth systems coexist. | CRITICAL — Users created in Flask are invisible to Next.js and vice versa. No persistent user storage in Flask. | Decide canonical auth: either (a) migrate Flask to use Supabase auth, or (b) retire Flask monolith and use Next.js + API routes. Recommend option (b). |
| CONF-002 | Code vs Plan #6 | **Implementation score**: Plans claim 99.2% complete. Actual codebase has: no automated tests, in-memory storage, extensive file duplication, unimplemented integrations (Stripe, Codewars), no CI/CD pipeline. | HIGH — Misleading status may cause incorrect prioritization. | Re-baseline implementation score using objective criteria. Current realistic estimate: ~45-55% of planned features are production-ready. |
| CONF-003 | Code vs Plan #3 | **Modules 2-10**: Plans say "95% ready". Flask `main.py` only has route for Magic Workshop Module 1. No routes for modules 2-10. `test_magic_workshop.py` creates a separate Flask app with module routes but is not integrated. | HIGH — Users cannot access modules 2-10. | Wire module routes into main Flask app, or implement as Next.js pages. |
| CONF-004 | Code vs Plan #19 | **Stripe integration**: Final Delivery Report claims Hermes agent "COMPLETED" Stripe integration. No Stripe code exists anywhere in the repository. | MEDIUM — Payment system entirely missing. | Implement Stripe integration from scratch when monetization is needed. |
| CONF-005 | Code vs Plan #19 | **Codewars integration**: Final Delivery Report claims Hermes agent "COMPLETED" Codewars API integration. No Codewars code exists in the repository. | LOW — Nice-to-have feature. | Implement when Tier 3 coding challenges are prioritized. |
| CONF-006 | Code vs Code | **Dual application stacks**: Flask monolith (`main.py`, 1327 LOC) and Next.js app (`app/`, `frontend/`) serve overlapping features (landing page, auth, dashboard) with different implementations. | CRITICAL — Maintenance burden, inconsistent UX, duplicated effort. | Choose one stack. Recommend Next.js as primary with Flask as API-only backend. |
| CONF-007 | Code vs Plan #7 | **Voice/WebRTC**: Professor Sparkle deployment guide describes real-time voice interaction via WebRTC. Code only implements text-based Socket.IO chat with fallback responses. | MEDIUM — Advertised feature not available. | Implement voice as a future enhancement. Remove from current feature claims. |
| CONF-008 | Code vs Plan #1 | **Railway deploy path**: `railway.json` and `Procfile` reference `python src/main.py`. Actual entrypoint is `main.py` (root) or `backend/main.py`. No `src/` directory exists. | HIGH — Railway deployment would fail. | Fix `Procfile` and `railway.json` to reference correct path. |

---

## 2. Gaps (Missing Items)

| ID | Category | Description | Recommended Implementation |
|----|----------|-------------|---------------------------|
| GAP-001 | Testing | **Zero automated tests**: No unit tests, integration tests, or E2E tests exist. `test_magic_workshop.py` is a standalone demo server, not a test suite. `docs/deployment/TESTING_AND_DEPLOYMENT.md` describes Jest/Cypress/pytest strategy but nothing is implemented. | Create test infrastructure: Jest for frontend, pytest for backend, Cypress for E2E. Priority: auth flows, child CRUD, Professor Sparkle safety checks. |
| GAP-002 | Auth | **No password reset implementation**: Flask `forgot_password()` route renders a form but only returns a static "check your email" page. No email service configured. | Integrate email service (SendGrid/Resend) or use Supabase auth's built-in password reset. |
| GAP-003 | Auth | **No email verification**: Users can sign up without email verification in both Flask and Next.js flows. | Enable Supabase email verification or implement custom verification flow. |
| GAP-004 | Learning | **Innovation Lab (Tier 2) not implemented**: No learning environment routes exist for Tier 2. Dashboard shows tier info but "Start Learning" links to non-existent routes. | Build Tier 2 learning environment with app-building interface. |
| GAP-005 | Learning | **Professional Studio (Tier 3) not implemented**: Same as GAP-004 for Tier 3. | Build Tier 3 learning environment with real code editor (Monaco/CodeMirror). |
| GAP-006 | Data | **No persistent storage in Flask**: User data stored in Python list (`users = []`). All data lost on server restart. Supabase client exists but is not used by Flask routes. | Connect Flask routes to `supabase_client.py` methods, or migrate to Next.js API routes. |
| GAP-007 | Payments | **No payment/subscription system**: Schema defines `subscription_plans` and `subscriptions` tables. Seed data includes Free/Family/Classroom plans. No payment code exists. | Implement Stripe integration when monetization begins. |
| GAP-008 | Content | **No curriculum content**: Schema defines `modules`, `lessons`, `exercises` tables. No seed data for actual lesson content exists. Professor Sparkle has hardcoded curriculum outlines but no interactive exercises. | Create curriculum content management system and seed initial content. |
| GAP-009 | Features | **No project/portfolio system**: Schema defines `projects` and `project_collaborators` tables. No UI or API for project creation/management exists. | Implement project CRUD and portfolio display. |
| GAP-010 | Features | **No messaging system**: Schema defines `messages` table. No UI or API for messaging exists. | Implement parent-teacher messaging when collaboration features are built. |
| GAP-011 | Features | **No notification system**: Schema defines `notifications` table and `send_notification()` function. No UI or trigger logic exists. | Implement notification service and UI. |
| GAP-012 | Features | **No analytics dashboard**: Schema defines `analytics_events` table. `supabase_client.py` has `get_parent_analytics()`. No UI exists. | Build parent analytics dashboard. |
| GAP-013 | DevOps | **No CI/CD pipeline**: No GitHub Actions, no automated testing, no automated deployment. | Set up GitHub Actions for lint, test, build, deploy. |
| GAP-014 | DevOps | **No environment management**: No `.env.example` file. Secrets hardcoded in `supabase_client.py` (service role key visible in source). | Create `.env.example`, remove hardcoded secrets, add to `.gitignore`. |
| GAP-015 | Security | **Hardcoded Supabase service role key**: `backend/supabase_client.py` line 21 contains the full service role key as a default value. This key is committed to a public repository. | CRITICAL: Rotate the Supabase service role key immediately. Remove from source code. Use environment variables only. |
| GAP-016 | Code Quality | **Massive file duplication**: Frontend code exists in 3 locations. Backend files duplicated at root. Migrations duplicated. | Consolidate to single canonical locations. Delete duplicates. |
| GAP-017 | Features | **No mobile optimization**: Plans describe PWA implementation. No service worker, manifest, or offline capability exists. | Implement PWA features when mobile optimization is prioritized. |
| GAP-018 | Features | **No multi-language support**: Plans describe internationalization. No i18n framework configured. | Implement i18n when international expansion begins. |
| GAP-019 | Observability | **No logging/monitoring infrastructure**: Flask uses basic `print()` statements. No structured logging, no metrics collection, no alerting. | Implement structured logging (e.g., structlog), add health metrics endpoint, configure alerting. |
| GAP-020 | Security | **Weak password hashing**: Flask uses plain SHA-256 (`hashlib.sha256`). Auth service uses SHA-256 with salt but no key stretching. Neither uses bcrypt/argon2. | Migrate to bcrypt or argon2 for password hashing. |

---

## 3. Decisions Pending

| ID | Decision | Options | Recommendation | What's Needed to Finalize |
|----|----------|---------|----------------|--------------------------|
| DEC-001 | **Primary application stack** | (a) Flask monolith with server-rendered HTML, (b) Next.js with Flask API backend, (c) Next.js with Supabase-only (no Flask) | Option (b): Next.js frontend + Flask API backend. Flask serves API endpoints only; Next.js handles all UI rendering. This preserves Professor Sparkle WebSocket integration while using modern React UI. | Architecture decision from project owner. Estimate: 2-3 weeks to refactor. |
| DEC-002 | **Auth system** | (a) Keep Flask in-memory auth, (b) Migrate Flask to Supabase auth, (c) Use Next.js + Supabase auth exclusively | Option (c): Supabase auth via Next.js. Eliminates dual auth problem. Flask API uses Supabase JWT verification for protected endpoints. | Depends on DEC-001. |
| DEC-003 | **File duplication cleanup** | (a) Keep all copies for safety, (b) Consolidate to canonical locations, (c) Full repo restructure | Option (c): Full restructure with clear `frontend/`, `backend/`, `shared/` boundaries. | 1-2 days of careful file consolidation with git history preservation. |
| DEC-004 | **Deployment target** | (a) Railway (backend) + Vercel (frontend), (b) Single platform (Railway or Vercel), (c) Self-hosted | Option (a): Railway for Flask backend + Vercel for Next.js frontend. This matches existing config files. | Fix `Procfile` path (CONF-008). Set up proper environment variables. |
| DEC-005 | **Professor Sparkle AI model** | (a) Google Gemini Pro, (b) OpenAI GPT-4, (c) Multiple models with A/B testing | Option (c): Support multiple models. Current code already has fallback pattern. Add proper model selection config. | API key procurement and cost analysis. |
| DEC-006 | **Curriculum content management** | (a) Hardcoded in Python/React, (b) Database-driven (Supabase), (c) CMS (headless) | Option (b): Store curriculum in Supabase `modules`/`lessons`/`exercises` tables. Build admin UI for content management. | Content creation team or process. |
| DEC-007 | **Secret rotation** | Rotate Supabase service role key (GAP-015) | IMMEDIATE: Rotate key in Supabase dashboard, update environment variables, remove from source code. | Access to Supabase project dashboard. |
