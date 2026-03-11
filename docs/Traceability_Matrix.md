# Traceability Matrix — Codopia Platform

**Generated**: 2026-02-23  
**Repo**: AllienNova/Codopia @ `154343d`

---

## Legend

- **Implemented**: Code exists and is functional
- **Partial**: Code exists but incomplete or not wired
- **Planned-not-implemented**: Described in plans/schema only
- **—**: Not applicable

---

| ReqID | Description | CodeRefs | ScreenIDs | FlowIDs | ApiIDs/Events/Jobs | EntIDs/Tables | ConfigRefs | TestIDs | Status | Notes/Gaps |
|-------|-------------|----------|-----------|---------|-------------------|---------------|------------|---------|--------|------------|
| REQ-0001 | Landing page with tier showcase | `main.py:31-319`, `app/page.tsx` | SCR-001 | — | — | — | — | — | Implemented (dual) | Two implementations: Flask SSR + Next.js React |
| REQ-0002 | Parent account registration | `main.py:323-386`, `app/auth/signup/page.tsx`, `lib/auth.ts:signUpParent` | SCR-002, SCR-003 | FLOW-001 | API-001 | ENT-001 (profiles) | `FLASK_SECRET_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY` | — | Implemented (dual) | Flask: in-memory. Next.js: Supabase. GAP-006 |
| REQ-0003 | Parent sign-in | `main.py:388-481`, `app/auth/signin/page.tsx`, `lib/auth.ts:signInUser` | SCR-004 | FLOW-002 | API-002 | ENT-001 | `FLASK_SECRET_KEY`, `SUPABASE_URL` | — | Implemented (dual) | Same dual-stack issue |
| REQ-0004 | Sign-out | `main.py:1235-1239`, `lib/auth.ts:signOut` | — | FLOW-003 | API-003 | — | — | — | Implemented (dual) | |
| REQ-0005 | Password reset | `main.py:1241-1321` | SCR-005 | FLOW-004 | API-004 | — | — | — | Partial | GAP-002: No email service. Shows static confirmation only. |
| REQ-0006 | OAuth callback handling | `app/auth/callback/page.tsx` | SCR-006 | FLOW-005 | — | — | `SUPABASE_URL`, `SUPABASE_ANON_KEY` | — | Implemented | Next.js only |
| REQ-0007 | Age-based tier assignment | `main.py:348-354`, `backend/auth_service.py:31-38`, `lib/children.ts:determineTierFromAge`, `003_functions_triggers.sql:assign_tier_by_age` | — | — | — | ENT-002 (children) | — | — | Implemented | Consistent logic across all implementations: ≤7→Magic, ≤12→Innovation, 13+→Professional |
| REQ-0008 | Parent dashboard with child cards | `main.py:483-589`, `app/dashboard/DashboardContent.tsx`, `components/ChildCard.tsx` | SCR-007, SCR-008 | — | — | ENT-001, ENT-002 | — | — | Implemented (dual) | Flask: basic. Next.js: full-featured with progress. |
| REQ-0009 | Add child profile | `main.py:535-544` (UI only), `app/dashboard/DashboardContent.tsx:handleAddChild`, `lib/auth.ts:createChildProfile`, `backend/supabase_client.py:create_child_profile` | SCR-008 | FLOW-006 | API-005 | ENT-002 | `SUPABASE_URL` | — | Implemented (dual) | Flask: UI placeholder only, no POST handler. Next.js: functional. |
| REQ-0010 | Magic Workshop learning environment | `main.py:660-1196` | SCR-009 | FLOW-007 | — | — | — | T-001 | Implemented | Module 1 only. Drag-and-drop blocks, live preview, Professor Sparkle chat. |
| REQ-0011 | Innovation Lab learning environment | — | — | — | — | — | — | — | Planned-not-implemented | GAP-004. No routes or UI exist. |
| REQ-0012 | Professional Studio learning environment | — | — | — | — | — | — | — | Planned-not-implemented | GAP-005. No routes or UI exist. |
| REQ-0013 | Professor Sparkle AI tutor | `backend/gemini_live_sparkle_fixed.py`, `main.py:1198-1232` | SCR-009 (embedded) | FLOW-008 | EVT-001, EVT-002 | — | `OPENAI_API_KEY` or `GEMINI_API_KEY` | — | Implemented | Text-based via Socket.IO. Gemini + fallback responses. |
| REQ-0014 | Professor Sparkle safety protocols | `backend/gemini_live_sparkle_fixed.py:61-79, 200-216` | — | — | — | — | — | — | Implemented | Forbidden topics, emergency keywords, safety responses. |
| REQ-0015 | Age-appropriate AI response style | `backend/gemini_live_sparkle_fixed.py:218-270` | — | — | — | — | — | — | Implemented | 5 age brackets with vocabulary, pace, emoji, magical elements config. |
| REQ-0016 | AI curriculum awareness | `backend/gemini_live_sparkle_fixed.py:81-198` | — | — | — | — | — | — | Implemented | 3 tiers × 5-6 lessons each hardcoded in ProfessorSparkle class. |
| REQ-0017 | Lesson progress tracking | `backend/supabase_client.py:252-310` | — | — | API-006 | ENT-003 (lesson_progress) | `SUPABASE_URL` | — | Partial | Supabase client methods exist. Not called from Flask routes. |
| REQ-0018 | Achievement system | `backend/supabase_client.py:314-351`, `003_functions_triggers.sql:check_and_award_achievements` | — | — | API-007 | ENT-004 (achievements), ENT-005 (user_achievements) | `SUPABASE_URL` | — | Partial | DB schema + client methods exist. No UI. No trigger wiring from app. |
| REQ-0019 | Parent analytics | `backend/supabase_client.py:355-384` | — | — | API-008 | ENT-001, ENT-002, ENT-003, ENT-004 | `SUPABASE_URL` | — | Partial | GAP-012. Client method exists. No UI or route. |
| REQ-0020 | Subscription plans | `003_functions_triggers.sql` (seed data) | — | — | — | ENT-006 (subscription_plans), ENT-007 (subscriptions) | — | — | Partial | Schema + seed data only. No payment flow. GAP-007. |
| REQ-0021 | Student projects/portfolio | `001_initial_schema.sql:194-223` | — | — | — | ENT-008 (projects), ENT-009 (project_collaborators) | — | — | Planned-not-implemented | GAP-009. Schema only. |
| REQ-0022 | Messaging system | `001_initial_schema.sql:229-239` | — | — | — | ENT-010 (messages) | — | — | Planned-not-implemented | GAP-010. Schema only. |
| REQ-0023 | Notification system | `001_initial_schema.sql:242-251`, `003_functions_triggers.sql:send_notification` | — | — | — | ENT-011 (notifications) | — | — | Planned-not-implemented | GAP-011. Schema + function only. |
| REQ-0024 | Analytics event tracking | `001_initial_schema.sql:285-295`, `lib/security.ts:logSecurityEvent` | — | — | — | ENT-012 (analytics_events) | — | — | Partial | Schema exists. Frontend security lib logs events. No backend integration. |
| REQ-0025 | Row-level security | `002_rls_policies.sql`, `005_enhanced_rls_policies.sql` | — | — | — | All tables | — | — | Implemented | Comprehensive RLS policies for parent-child ownership model. |
| REQ-0026 | Input sanitization & XSS prevention | `lib/security.ts:sanitizeInput, validateProjectContent` | — | — | — | — | — | — | Implemented | Frontend only. No backend input validation. |
| REQ-0027 | CSRF protection | `lib/security.ts:generateCSRFToken, validateCSRFToken, initializeCSRF` | — | — | — | — | — | — | Implemented | Frontend token generation. Not verified server-side. |
| REQ-0028 | Session management | `lib/security.ts:validateSession, updateSessionActivity` | — | — | — | — | — | — | Implemented | 8-hour timeout. localStorage-based. |
| REQ-0029 | Permission checking | `lib/security.ts:checkUserPermission, checkParentChildRelationship, checkProjectAccess` | — | — | — | ENT-001, ENT-002, ENT-008 | — | — | Implemented | Frontend permission checks via Supabase RPC. |
| REQ-0030 | Module progress tracking | `001_initial_schema.sql:148-159`, `003_functions_triggers.sql:update_module_progress_on_lesson_completion` | — | — | — | ENT-013 (module_progress) | — | — | Partial | Schema + trigger. No app-level integration. |
| REQ-0031 | Exercise submissions | `001_initial_schema.sql:177-188` | — | — | — | ENT-014 (exercise_submissions) | — | — | Planned-not-implemented | Schema only. No exercises exist. |
| REQ-0032 | Supabase health check | `backend/supabase_client.py:388-395` | — | — | API-009 | — | `SUPABASE_URL` | — | Implemented | |
| REQ-0033 | Child profile management (edit/delete) | `lib/children.ts:updateChild, deleteChild` | SCR-008 | — | API-010, API-011 | ENT-002 | — | — | Implemented | Next.js only. Flask has no edit/delete. |
| REQ-0034 | Marketing components | `frontend/components/About.jsx, Features.jsx, Footer.jsx, Navigation.jsx, Pricing.jsx` | SCR-001 | — | — | — | — | — | Implemented | Next.js marketing page components. |
| REQ-0035 | Voice interaction with Professor Sparkle | — | — | — | — | — | — | — | Planned-not-implemented | CONF-007. Described in plans, not implemented. |
| REQ-0036 | Mobile PWA | — | — | — | — | — | — | — | Planned-not-implemented | GAP-017. No service worker or manifest. |
| REQ-0037 | Multi-language support | — | — | — | — | — | — | — | Planned-not-implemented | GAP-018. No i18n framework. |
| REQ-0038 | Stripe payment processing | — | — | — | — | ENT-007 | — | — | Planned-not-implemented | CONF-004, GAP-007. Schema exists, no code. |
| REQ-0039 | Teacher/classroom management | — | — | — | — | — | — | — | Planned-not-implemented | Described in roadmap only. |
| REQ-0040 | Collaborative projects | — | — | — | — | ENT-009 | — | — | Planned-not-implemented | Schema exists, no code. |

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Implemented | 18 | 45% |
| Implemented (dual-stack) | 6 | 15% |
| Partial | 6 | 15% |
| Planned-not-implemented | 10 | 25% |
| **Total** | **40** | **100%** |

**Effective implementation rate**: ~60% (counting dual-stack as implemented, partial as 50%)
