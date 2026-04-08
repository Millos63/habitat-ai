# Database Plan — Habitat AI

## Engine

- **PostgreSQL 15+** with the **pgvector** extension for vector similarity search.
- **SQLAlchemy 2.x** (async) as ORM layer.
- **Alembic** for schema migrations.

---

## Table Status Tracker

| Table | Phase | Status |
|-------|-------|--------|
| users | 1 | ⏳ Pending |
| properties | 2 | ⏳ Pending |
| favorites | 2 | ⏳ Pending |
| clients | 3 | ⏳ Pending |
| messages | 3 | ⏳ Pending |
| appointments | 4 | ⏳ Pending |
| property_alerts | 5 | ⏳ Pending |
| chat_sessions | 6 | ⏳ Pending |
| chat_messages | 6 | ⏳ Pending |

---

## Table Definitions

### `users`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| full_name | VARCHAR(255) | NOT NULL |
| phone | VARCHAR(20) | NULLABLE |
| avatar_url | TEXT | NULLABLE |
| role | ENUM('client','agent','admin') | NOT NULL, DEFAULT 'client' |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `properties`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| agent_id | UUID | FK → users(id), ON DELETE SET NULL |
| title | VARCHAR(500) | NOT NULL |
| description | TEXT | NULLABLE |
| price | DECIMAL(15,2) | NOT NULL |
| currency | VARCHAR(3) | NOT NULL, DEFAULT 'MXN' |
| type | ENUM('house','apartment','land','commercial','office') | NULLABLE |
| status | ENUM('active','paused','sold','rented') | NOT NULL, DEFAULT 'active' |
| operation | ENUM('sale','rent') | NULLABLE |
| address | TEXT | NOT NULL |
| city | VARCHAR(255) | NULLABLE |
| state | VARCHAR(255) | NULLABLE |
| zip_code | VARCHAR(10) | NULLABLE |
| latitude | DECIMAL(10,8) | NULLABLE |
| longitude | DECIMAL(11,8) | NULLABLE |
| bedrooms | INTEGER | NOT NULL, DEFAULT 0 |
| bathrooms | INTEGER | NOT NULL, DEFAULT 0 |
| area_m2 | DECIMAL(10,2) | NULLABLE |
| parking_spots | INTEGER | NOT NULL, DEFAULT 0 |
| year_built | INTEGER | NULLABLE |
| amenities | TEXT[] | NULLABLE |
| images | TEXT[] | NULLABLE |
| virtual_tour_url | TEXT | NULLABLE |
| embedding | VECTOR(1536) | NULLABLE — populated in Phase 6 |
| is_featured | BOOLEAN | NOT NULL, DEFAULT FALSE |
| views_count | INTEGER | NOT NULL, DEFAULT 0 |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `favorites`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| user_id | UUID | FK → users(id), ON DELETE CASCADE |
| property_id | UUID | FK → properties(id), ON DELETE CASCADE |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

**Unique constraint:** `UNIQUE(user_id, property_id)`

---

### `clients`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| agent_id | UUID | FK → users(id), ON DELETE CASCADE |
| full_name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | NULLABLE |
| phone | VARCHAR(20) | NULLABLE |
| status | ENUM('new','contacted','interested','negotiating','closed','lost') | NOT NULL, DEFAULT 'new' |
| source | VARCHAR(100) | NULLABLE |
| interests | TEXT | NULLABLE |
| budget_min | DECIMAL(15,2) | NULLABLE |
| budget_max | DECIMAL(15,2) | NULLABLE |
| preferred_zones | TEXT[] | NULLABLE |
| notes | TEXT | NULLABLE |
| ai_notes | TEXT | NULLABLE — populated by AI in Phase 6 |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `messages`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| sender_id | UUID | FK → users(id), ON DELETE CASCADE |
| receiver_id | UUID | FK → users(id), ON DELETE CASCADE |
| property_id | UUID | FK → properties(id), ON DELETE SET NULL, NULLABLE |
| content | TEXT | NOT NULL |
| source | VARCHAR(20) | NOT NULL, DEFAULT 'user' — values: user/agent/chatbot |
| is_read | BOOLEAN | NOT NULL, DEFAULT FALSE |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `appointments`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| property_id | UUID | FK → properties(id), ON DELETE CASCADE |
| client_id | UUID | FK → clients(id), ON DELETE CASCADE |
| agent_id | UUID | FK → users(id), ON DELETE CASCADE |
| scheduled_date | DATE | NOT NULL |
| scheduled_time | TIME | NOT NULL |
| status | ENUM('pending','confirmed','completed','cancelled') | NOT NULL, DEFAULT 'pending' |
| source | VARCHAR(20) | NOT NULL, DEFAULT 'manual' — values: manual/app/chatbot |
| notes | TEXT | NULLABLE |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `property_alerts`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| user_id | UUID | FK → users(id), ON DELETE CASCADE |
| operation | VARCHAR(50) | NULLABLE |
| type | VARCHAR(50) | NULLABLE |
| city | VARCHAR(255) | NULLABLE |
| min_price | DECIMAL(15,2) | NULLABLE |
| max_price | DECIMAL(15,2) | NULLABLE |
| min_bedrooms | INTEGER | NULLABLE |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `chat_sessions`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| user_id | UUID | FK → users(id), ON DELETE CASCADE |
| title | VARCHAR(255) | NOT NULL, DEFAULT 'New conversation' |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

### `chat_messages`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| session_id | UUID | FK → chat_sessions(id), ON DELETE CASCADE |
| role | VARCHAR(20) | NOT NULL — values: user/assistant/system |
| content | TEXT | NOT NULL |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() |

---

## Planned Indexes

```sql
-- users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- properties
CREATE INDEX idx_properties_agent_id ON properties(agent_id);
CREATE INDEX idx_properties_status ON properties(status);
CREATE INDEX idx_properties_city ON properties(city);
CREATE INDEX idx_properties_operation ON properties(operation);
CREATE INDEX idx_properties_type ON properties(type);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_is_featured ON properties(is_featured);
-- Vector similarity index (Phase 6)
CREATE INDEX idx_properties_embedding ON properties USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- favorites
CREATE UNIQUE INDEX idx_favorites_user_property ON favorites(user_id, property_id);
CREATE INDEX idx_favorites_user_id ON favorites(user_id);

-- clients
CREATE INDEX idx_clients_agent_id ON clients(agent_id);
CREATE INDEX idx_clients_status ON clients(status);

-- messages
CREATE INDEX idx_messages_sender_id ON messages(sender_id);
CREATE INDEX idx_messages_receiver_id ON messages(receiver_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- appointments
CREATE INDEX idx_appointments_agent_id ON appointments(agent_id);
CREATE INDEX idx_appointments_scheduled_date ON appointments(scheduled_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- chat_sessions
CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);

-- chat_messages
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);
```

---

## pgvector Extension

The `pgvector` extension must be enabled before creating the `properties` table in Phase 2:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

This will be handled in the first Alembic migration. The `embedding vector(1536)` column will be added to `properties` in Phase 2 but left `NULL` until Phase 6, when the AI pipeline generates embeddings from property descriptions using OpenAI `text-embedding-3-small`.

### Vector Search Query Pattern (Phase 6)

```sql
SELECT *, 1 - (embedding <=> :query_embedding) AS similarity
FROM properties
WHERE status = 'active'
ORDER BY embedding <=> :query_embedding
LIMIT 10;
```

---

## Naming Conventions

- Table names: **plural snake_case** (`users`, `chat_messages`)
- Column names: **snake_case** (`created_at`, `agent_id`)
- Enum type names: **snake_case with `_type` suffix** (e.g., `user_role_type`)
- Index names: `idx_{table}_{column(s)}`
- Foreign key names: `fk_{table}_{referenced_table}`
