# Current Status — Habitat AI

## Current Phase: 2
## Current Subphase: 2.1 ✅
## Last Modified File: backend/tests/test_properties.py
## Immediate Next Task: Phase 2.2 — Property management endpoints (create/update/delete and status/featured toggles)

## Completed Files:
- [x] Repository structure created
- [x] Reference documents created
- [x] Backend setup (Phase 0.3) — FastAPI, SQLAlchemy, Alembic, config, utilities, tests
- [x] Mobile setup (Phase 0.4) — Expo, NativeWind, TanStack Query, Zustand, layouts, stores, types
- [x] Docker setup (Phase 0.5) — docker-compose (PostgreSQL + Redis + Backend), Dockerfile
- [x] Authentication foundation (Phase 1.1) — users table, auth endpoints, JWT flow, mobile login/register/logout integration
- [x] Authentication polish (Phase 1.2) — stronger validation rules, loading state UX, improved API error messaging, backend auth tests
- [x] Property catalog foundations (Phase 2.1) — properties model, migration, public list/detail/featured endpoints, filters, and tests

## Decisions Made:
- Project name: Habitat AI
- Stack: React Native (Expo) + FastAPI + PostgreSQL + pgvector + Redis + Cloudinary + OpenAI
- AI implementation deferred to Phase 6 but architecture prepared from Phase 1
- All code and commits in English
- Git branching strategy: `master` (production) ← `development` (integration) ← `feature/phase-X.X-*` (work branches)
- NativeWind v4 with Tailwind CSS v3 for mobile styling
- Zustand v5 for global state (auth + theme only)
- TanStack Query v5 for server state
- Axios with interceptors for API client
- Expo SecureStore for JWT token persistence

## Known Issues:
- `development` branch must be created from `master` to follow the documented branching strategy. All future feature branches should be created from and merged into `development`.

## Notes:
- Column `embedding vector(1536)` will be added to properties table in Phase 2 but left NULL until Phase 6
- AI-related UI elements will show "Coming Soon" placeholders until Phase 6
- Backend health endpoint available at `GET /api/health`
- Docker uses `pgvector/pgvector:pg16` image for PostgreSQL with pgvector extension pre-installed
