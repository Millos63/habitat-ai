# Current Status — Habitat AI

## Current Phase: 0
## Current Subphase: 0.2
## Last Modified File: Initial setup
## Immediate Next Task: Subphase 0.3 — Backend Setup

## Completed Files:
- [x] Repository structure created
- [x] Reference documents created
- [ ] Backend setup (Phase 0.3)
- [ ] Mobile setup (Phase 0.4)
- [ ] Docker setup (Phase 0.5)

## Decisions Made:
- Project name: Habitat AI
- Stack: React Native (Expo) + FastAPI + PostgreSQL + pgvector + Redis + Cloudinary + OpenAI
- AI implementation deferred to Phase 6 but architecture prepared from Phase 1
- All code and commits in English
- Git branching strategy: `master` (production) ← `development` (integration) ← `feature/phase-X.X-*` (work branches)

## Known Issues:
- None

## Notes:
- Column `embedding vector(1536)` will be added to properties table in Phase 2 but left NULL until Phase 6
- AI-related UI elements will show "Coming Soon" placeholders until Phase 6
