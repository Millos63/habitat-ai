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

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| **Node.js** | ≥ 18 | [nodejs.org](https://nodejs.org/) |
| **npm** | ≥ 9 | Comes with Node.js |
| **Python** | ≥ 3.12 | [python.org](https://python.org/) |
| **Docker & Docker Compose** | Latest | [docker.com](https://www.docker.com/) |
| **Expo Go** (mobile) | Latest | App Store / Play Store |

### 1. Clone the repository

```bash
git clone https://github.com/Millos63/habitat-ai.git
cd habitat-ai
```

### 2. Backend setup

#### Option A — With Docker (recommended)

This starts PostgreSQL, Redis, and the backend API all at once:

```bash
# Copy environment variables
cp backend/.env.example backend/.env

# Docker Compose already overrides DATABASE_URL and REDIS_URL
# to use the `db` and `redis` service names inside Docker.

# Start all services
docker compose -f docker/docker-compose.yml up --build
```

The backend API will be available at **http://localhost:8000**.
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

#### Option B — Without Docker (manual)

You need PostgreSQL and Redis running locally first.

```bash
# Install PostgreSQL (with pgvector) and Redis on your machine, then:

cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your local database and Redis URLs

# Run database migrations
alembic upgrade head

# Start the backend server (with hot-reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Mobile setup (Expo)

```bash
cd mobile

# Install dependencies
npm install

# Start the Expo development server
npx expo start
```

This will show a QR code in your terminal.

#### 📱 Running on your phone

1. Install **Expo Go** from the App Store (iOS) or Play Store (Android).
2. Make sure your phone and computer are **on the same Wi-Fi network**.
3. Scan the QR code shown in the terminal:
   - **iOS**: Use the Camera app to scan it → tap the notification.
   - **Android**: Open Expo Go → tap "Scan QR code".

#### 💻 Running on your computer

```bash
# Android emulator (requires Android Studio)
npx expo start --android

# iOS simulator (macOS only, requires Xcode)
npx expo start --ios

# Web browser
npx expo start --web
```

> **Note:** For the mobile app to communicate with the backend API running on your machine, you may need to update the API base URL in `mobile/services/` to use your computer's local IP address (e.g., `http://192.168.x.x:8000`) instead of `localhost`, since `localhost` on the phone refers to the phone itself.

### 4. Running everything together

```bash
# Terminal 1 — Start backend + databases via Docker
docker compose -f docker/docker-compose.yml up --build

# Terminal 2 — Start mobile app
cd mobile && npx expo start
```

### 5. Running tests

```bash
# Backend tests
cd backend
python -m pytest tests/ -v
```

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
