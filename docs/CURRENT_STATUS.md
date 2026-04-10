# Current Status — Habitat AI

## Current Phase: 0
## Current Subphase: 0.5 ✅
## Last Modified File: docker/docker-compose.yml
## Immediate Next Task: Phase 1.1 — Authentication (Backend)

## Completed Files:
- [x] Repository structure created
- [x] Reference documents created
- [x] Backend setup (Phase 0.3) — FastAPI, SQLAlchemy, Alembic, config, utilities, tests
- [x] Mobile setup (Phase 0.4) — Expo, NativeWind, TanStack Query, Zustand, layouts, stores, types
- [x] Docker setup (Phase 0.5) — docker-compose (PostgreSQL + Redis + Backend), Dockerfile

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
- None

## Notes:
- Column `embedding vector(1536)` will be added to properties table in Phase 2 but left NULL until Phase 6
- AI-related UI elements will show "Coming Soon" placeholders until Phase 6
- Backend health endpoint available at `GET /api/health`
- Docker uses `pgvector/pgvector:pg16` image for PostgreSQL with pgvector extension pre-installed
