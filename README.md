# 🏠 Habitat AI

> Intelligent real estate platform powered by AI

Habitat AI is a modern real estate mobile application that empowers agents with AI-powered tools and provides clients with an intelligent property search experience.

## ✨ Features

- 🏡 Property catalog with advanced filters and map view
- 🤖 AI-powered chatbot for property recommendations
- 🔍 Semantic search — find properties using natural language
- ✍️ AI-generated property descriptions
- 💰 AI-based price estimation
- 👥 Built-in CRM for client management
- 📅 Appointment scheduling system
- 📊 Analytics dashboard for agents
- 📄 AI-powered CV optimizer
- 🔔 Push notifications and property alerts

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Mobile | React Native + Expo + NativeWind + Expo Router |
| Backend | FastAPI (Python) + SQLAlchemy |
| Database | PostgreSQL + pgvector |
| Cache | Redis |
| Storage | Cloudinary |
| AI | OpenAI GPT-4o + LangChain |
| Auth | JWT |

## 📁 Project Structure

```
habitat-ai/
├── mobile/                 # React Native (Expo) application
│   ├── app/                # Expo Router file-based screens
│   │   ├── (tabs)/         # Bottom tab screens
│   │   ├── (auth)/         # Authentication screens
│   │   ├── (agent)/        # Agent-only screens
│   │   └── property/       # Property detail screens
│   ├── components/         # Reusable UI components
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API client functions
│   ├── stores/             # Zustand global state
│   ├── theme/              # NativeWind theme config
│   ├── types/              # TypeScript type definitions
│   ├── utils/              # Pure utility functions
│   └── assets/             # Images, animations, fonts
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routers/        # FastAPI route handlers
│   │   ├── services/       # Business logic layer
│   │   ├── ai/             # AI integrations
│   │   ├── middleware/     # Custom middleware
│   │   └── utils/          # Shared utilities
│   ├── alembic/            # Database migrations
│   └── tests/              # Pytest test suite
├── docs/                   # Reference documentation
└── docker/                 # Docker configuration files
```

## 🚀 Getting Started

> Setup instructions will be added in Phase 0.3–0.5

## 📋 Development Phases

| Phase | Description | Status |
|-------|------------|--------|
| 0 | Setup & Configuration | ✅ Complete |
| 1 | Authentication & Base Structure | ⏳ Pending |
| 2 | Property Catalog | ⏳ Pending |
| 3 | CRM & Messaging | ⏳ Pending |
| 4 | Scheduling & Map | ⏳ Pending |
| 5 | Notifications & Polish | ⏳ Pending |
| 6 | AI Integration | ⏳ Pending |
| 7 | Production & Launch | ⏳ Pending |

## 📄 License

MIT
