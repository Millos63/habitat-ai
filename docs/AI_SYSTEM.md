# AI System Plan — Habitat AI

## Overview

AI features are the primary competitive differentiator of Habitat AI. The architecture is designed and scaffolded from Phase 1 so that AI can be activated in Phase 6 without requiring structural refactors. Until Phase 6, AI endpoints return placeholder responses and AI-related UI shows "Coming Soon" states.

---

## AI Modules

### 1. Chatbot — RAG + Streaming

**Purpose:** Answer property-related questions, recommend properties, and schedule appointments through conversational interaction.

**Implementation:**
- LangChain `ConversationalRetrievalChain` with GPT-4o
- Property recommendations via function calling
- Appointment booking via function calling
- Chat history persisted in `chat_sessions` and `chat_messages` tables
- Redis caches frequent responses (5-minute TTL)
- Responses streamed via Server-Sent Events (SSE)

**Endpoint:** `POST /api/chat/stream`

---

### 2. Semantic Search — pgvector + OpenAI Embeddings

**Purpose:** Allow users to find properties using natural language queries instead of dropdown filters.

**Implementation:**
- Query embedding generated with `text-embedding-3-small` (1536 dimensions)
- Cosine similarity search against `properties.embedding` using `pgvector` `<=>` operator
- IVFFlat index for performance at scale
- Falls back to keyword search if embedding is unavailable

**Endpoint:** `POST /api/properties/search/semantic`

---

### 3. Description Generator

**Purpose:** Help agents write compelling property descriptions from basic data.

**Implementation:**
- GPT-4o prompt with property attributes as structured input
- Returns a 2–3 paragraph description optimized for engagement
- Rate-limited to 20 requests per hour per agent

**Endpoint:** `POST /api/ai/generate-description`

---

### 4. Price Estimator

**Purpose:** Provide data-informed price estimates with confidence scores and reasoning.

**Implementation:**
- Fetches comparable active properties from the database
- Sends comparables + property attributes to GPT-4o for analysis
- Returns estimated price, range, confidence score, and plain-text reasoning

**Endpoint:** `POST /api/ai/estimate-price`

---

### 5. CV Optimizer

**Purpose:** Help real estate agents optimize their professional CVs and cover letters (bonus feature).

**Sub-features:**
- **Optimize:** Rewrite for clarity and impact
- **Adapt:** Tailor CV to a specific job description
- **Score:** ATS compatibility score with strengths/weaknesses
- **Cover Letter:** Generate a tailored cover letter

All optimization/adapt/cover-letter endpoints stream responses via SSE.

**Endpoints:**
- `POST /api/ai/cv/optimize`
- `POST /api/ai/cv/adapt`
- `POST /api/ai/cv/score`
- `POST /api/ai/cv/cover-letter`

---

### 6. Market Analysis *(Planned — Phase 6)*

**Purpose:** Generate zone-based market reports for agents to share with clients.

**Implementation:**
- Aggregates property data by zone/city
- GPT-4o generates narrative report with trends
- Cached in Redis for 1 hour

---

### 7. Voice Search *(Planned — Phase 6)*

**Purpose:** Allow users to search for properties using voice input.

**Implementation:**
- Audio recorded on device and sent to backend
- Transcribed with OpenAI Whisper API
- Transcription text used as semantic search query

---

## Models & APIs

| Task | Model | Notes |
|------|-------|-------|
| Chat, descriptions, price analysis, CV tools | `gpt-4o` | Primary LLM |
| Property embeddings | `text-embedding-3-small` | 1536 dimensions |
| Voice transcription | `whisper-1` | Audio → text |

---

## RAG Architecture

```
User message
     │
     ▼
Generate embedding (text-embedding-3-small)
     │
     ▼
Search pgvector: SELECT * FROM properties
                 ORDER BY embedding <=> :query_embedding LIMIT 5
     │
     ▼
Build context: top-5 matching properties + conversation history
     │
     ▼
GPT-4o prompt with context + system instructions
     │
     ▼
Stream response via SSE → React Native EventSource
```

---

## Cost Estimation

| Feature | Cost per call | Estimated monthly (1,000 users) |
|---------|-------------|--------------------------------|
| Chat (GPT-4o) | ~$0.01–0.03 | ~$30–90 |
| Embedding per property | ~$0.0001 | ~$5 (50k properties) |
| Whisper transcription | ~$0.006/min | ~$6 |
| Description generation | ~$0.02 | ~$10 |
| Price estimation | ~$0.03 | ~$15 |
| CV tools | ~$0.02–0.05 | ~$10 |
| **Total estimate** | | **~$50–150 USD/month** |

---

## Rate Limiting

All limits are per-user, tracked in Redis with a sliding window.

| Endpoint group | Limit |
|---------------|-------|
| Chat messages | 30 per hour |
| Description generation | 20 per hour (agents only) |
| Price estimation | 10 per hour |
| CV tools (any) | 10 per hour |
| Semantic search | 60 per hour |

---

## Fallback Strategy

1. **OpenAI unavailable:** Return `503 Service Temporarily Unavailable` with a friendly message. Disable AI features gracefully in the UI. Log the failure with timestamp and request metadata.
2. **Partial degradation:** Semantic search falls back to keyword/filter-based search automatically.
3. **Redis cache:** Frequent chatbot Q&A pairs are cached for 5 minutes to reduce API calls.
4. **Queue non-urgent tasks:** Description generation and market analysis are queued asynchronously and results delivered via push notification or polling.

---

## Phased Preparation Strategy

To avoid structural refactors when AI is activated in Phase 6, each phase prepares the groundwork:

| Phase | Preparation |
|-------|------------|
| **2** | Add `embedding VECTOR(1536)` (nullable) to `properties`. Add stub `generate_embedding()` that returns `None`. Add disabled "Generate with AI ✨" button in create-property form. |
| **3** | Add `ai_notes TEXT` to `clients` table. Add `source` field to `messages` (`user`/`agent`/`chatbot`). |
| **4** | Add `source` field to `appointments` (`manual`/`app`/`chatbot`). |
| **5** | Add placeholder for semantic property alerts UI. |
| **6** | Implement all AI features: embeddings pipeline, RAG chat, semantic search, generators, CV tools, voice search, market analysis. |

---

## Security Considerations

- OpenAI API key stored in environment variables only — never committed or logged.
- User-supplied text is sanitized before being included in prompts to mitigate prompt injection.
- Streaming responses are chunked and sent through authenticated SSE connections.
- AI usage per user is logged for abuse detection and billing attribution.
- Rate limits are enforced server-side (Redis), not client-side.
