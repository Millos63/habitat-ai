# Architecture — Habitat AI

## Overview

Habitat AI is a real estate mobile application that connects clients looking for properties with agents managing their portfolio, all enhanced by AI-powered features. The system is designed as a mobile-first experience with a robust API backend and an AI layer that becomes active in Phase 6.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Mobile | React Native + Expo + NativeWind + Expo Router |
| Backend | FastAPI (Python) + SQLAlchemy (async) |
| Database | PostgreSQL + pgvector |
| Cache | Redis |
| Storage | Cloudinary |
| AI | OpenAI GPT-4o + LangChain |
| Auth | JWT (python-jose) |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     React Native App                        │
│           (Expo + NativeWind + Expo Router)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS / REST / SSE
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway                             │
│              (FastAPI — /api/v1/*)                          │
│         Auth Middleware · Rate Limiting · CORS              │
└──────┬────────────┬──────────────┬──────────────┬───────────┘
       │            │              │              │
       ▼            ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│PostgreSQL│  │  Redis   │  │Cloudinary│  │   OpenAI     │
│+pgvector │  │  Cache   │  │ Storage  │  │ GPT-4o +     │
│          │  │          │  │          │  │ Embeddings + │
│          │  │          │  │          │  │ Whisper      │
└──────────┘  └──────────┘  └──────────┘  └──────────────┘
```

---

## Backend Structure (`backend/app/`)

```
backend/
├── app/
│   ├── models/         # SQLAlchemy ORM models (one file per entity)
│   ├── schemas/        # Pydantic schemas for request/response validation
│   ├── routers/        # FastAPI route handlers (one file per resource)
│   ├── services/       # Business logic layer (async functions)
│   ├── ai/             # AI integrations (LangChain, OpenAI, embeddings)
│   ├── middleware/     # Custom middleware (auth, rate limiting, logging)
│   └── utils/          # Shared utilities (hashing, JWT, cloudinary client)
├── alembic/
│   └── versions/       # Database migration files
└── tests/              # Pytest test suite
```

### `models/`
SQLAlchemy ORM models mapped directly to PostgreSQL tables. Each file defines one entity (e.g., `user.py`, `property.py`). All models use UUID primary keys and `created_at` / `updated_at` timestamps.

### `schemas/`
Pydantic v2 models for input validation and response serialization. Typically organized as `Base`, `Create`, `Update`, and `Response` variants per entity (e.g., `PropertyCreate`, `PropertyResponse`).

### `routers/`
FastAPI `APIRouter` instances grouped by resource. Each router is included in the main `app.py` with a prefix (e.g., `/api/auth`, `/api/properties`). Route handlers are thin — they validate input and delegate all logic to the service layer.

### `services/`
Pure async functions that contain business logic. A service function receives validated data (Pydantic models), interacts with the database via SQLAlchemy, and returns domain objects. No FastAPI dependencies here — fully testable in isolation.

### `ai/`
All AI-related logic: LangChain chains, OpenAI client wrappers, embedding generation, RAG pipeline, streaming response handlers, and prompt templates. Organized by feature (e.g., `chat.py`, `embeddings.py`, `cv_tools.py`).

### `middleware/`
Custom Starlette/FastAPI middleware:
- `auth.py` — JWT token extraction and user injection
- `rate_limit.py` — Redis-backed rate limiting per user/endpoint
- `logging.py` — Request/response logging

### `utils/`
Shared helper modules:
- `security.py` — Password hashing (bcrypt), JWT creation/verification
- `cloudinary.py` — Cloudinary upload helpers
- `pagination.py` — Common pagination utilities
- `exceptions.py` — Custom HTTP exception classes

---

## Mobile Structure (`mobile/`)

```
mobile/
├── app/                # Expo Router file-based routing
│   ├── (tabs)/         # Bottom tab navigator screens
│   ├── (auth)/         # Authentication screens (outside tab nav)
│   ├── (agent)/        # Agent-specific screens
│   └── property/       # Property detail screens
├── components/
│   ├── ui/             # Base UI components (Button, Input, Card, etc.)
│   ├── property/       # Property-specific components
│   ├── chat/           # Chat/AI components
│   └── shared/         # Cross-feature shared components
├── hooks/              # Custom React hooks
├── services/           # API client functions (*.service.ts)
├── stores/             # Zustand global stores (auth, theme only)
├── theme/              # NativeWind theme config, colors, typography
├── types/              # TypeScript type definitions (one file per entity)
├── utils/              # Pure utility functions (formatting, validation)
└── assets/
    ├── images/         # Static image assets
    ├── animations/     # Lottie animation files
    └── fonts/          # Custom font files
```

### `app/`
File-based routing powered by Expo Router. Each file exports a React component that becomes a screen. Layout files (`_layout.tsx`) define navigation wrappers (tab navigators, stack navigators, auth guards).

### `components/`
Stateless or lightly stateful UI components. Strictly presentational — no direct API calls or global state reads. Data flows in through props.

### `hooks/`
Custom React hooks that encapsulate reusable logic. Data-fetching hooks use TanStack Query under the hood (`useProperties`, `usePropertyDetail`, `useAuth`). Form hooks manage local state and validation.

### `services/`
Functions that make HTTP requests to the backend API. Each file corresponds to one resource (e.g., `properties.service.ts`, `auth.service.ts`). Returns typed responses. Uses a shared Axios or Fetch instance with interceptors for auth headers.

### `stores/`
Zustand stores for global client-side state. Limited to:
- `authStore.ts` — current user, token, login/logout actions
- `themeStore.ts` — light/dark mode preference

All server state (properties, clients, etc.) lives in TanStack Query cache, not Zustand.

### `theme/`
NativeWind / Tailwind configuration, color palette constants, typography scale, and spacing tokens. Ensures visual consistency across the app.

### `types/`
TypeScript interfaces and types. One file per entity (e.g., `property.types.ts`, `user.types.ts`). Shared between services, hooks, and components.

### `utils/`
Pure functions with no side effects: currency formatting, date formatting, distance calculation, string helpers, input validators.

---

## Design Patterns

### Backend — Repository Pattern

```
Router (HTTP layer)
   └── Service (business logic — async functions)
          └── SQLAlchemy Model (ORM — database access)
                 └── PostgreSQL
```

Services are async functions, not classes. A service receives validated Pydantic input and returns typed domain objects. Routers are responsible for HTTP concerns only (status codes, headers, dependency injection).

### Mobile — Custom Hooks + TanStack Query

```
Screen Component
   └── Custom Hook (e.g., useProperties)
          └── TanStack Query (useQuery / useMutation)
                 └── Service Function (e.g., propertiesService.getAll)
                        └── HTTP Request → FastAPI
```

Custom hooks abstract query keys, caching, and refetch logic. Components only interact with hooks, never with services directly.

### Mobile — Global State (Zustand)

Zustand is used **only** for truly global state that is not server-derived:
- Authentication state (user object + JWT token)
- Theme preference (light/dark)

Everything else is TanStack Query cache or local component state.
