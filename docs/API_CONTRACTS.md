# API Contracts — Habitat AI

All endpoints are prefixed with `/api`. Authentication uses Bearer JWT tokens in the `Authorization` header.

---

## Phase 1 — Authentication & Users

### POST `/api/auth/register`

Register a new user account.

- **Auth required:** No
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe",
    "phone": "+521234567890",
    "role": "client"
  }
  ```
- **Response `201`:**
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "user_id": "uuid"
  }
  ```

---

### POST `/api/auth/login`

Authenticate and receive a JWT token.

- **Auth required:** No
- **Body:**
  ```json
  { "email": "user@example.com", "password": "securepassword" }
  ```
- **Response `200`:**
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "user_id": "uuid"
  }
  ```

---

### GET `/api/auth/me`

Get the current authenticated user's profile.

- **Auth required:** Yes
- **Response `200`:** User object

---

### PUT `/api/auth/profile`

Update the current user's profile.

- **Auth required:** Yes
- **Body:**
  ```json
  { "full_name": "Jane Doe", "phone": "+521234567890", "avatar_url": "https://..." }
  ```
- **Response `200`:** Updated User object

---

### POST `/api/uploads/avatar`

Upload a profile avatar image.

- **Auth required:** Yes
- **Body:** `multipart/form-data` with `file` field
- **Response `200`:**
  ```json
  { "url": "https://res.cloudinary.com/..." }
  ```

---

## Phase 2 — Properties

### GET `/api/properties`

List properties with optional filters.

- **Auth required:** No
- **Query params:** `operation`, `type`, `city`, `min_price`, `max_price`, `min_bedrooms`, `min_bathrooms`, `min_area`, `page` (default 1), `limit` (default 20)
- **Response `200`:** `Property[]`
- **Headers:** `X-Total-Count: 42`

---

### GET `/api/properties/featured`

Get featured properties.

- **Auth required:** No
- **Response `200`:** `Property[]`

---

### GET `/api/properties/:id`

Get a single property by ID.

- **Auth required:** No
- **Response `200`:** `Property`
- **Response `404`:** `{ "detail": "Property not found" }`

---

### POST `/api/properties`

Create a new property listing.

- **Auth required:** Yes (agent role)
- **Body:** `PropertyCreate`
- **Response `201`:** `Property`

---

### PUT `/api/properties/:id`

Replace an entire property listing.

- **Auth required:** Yes (property owner)
- **Body:** `PropertyCreate`
- **Response `200`:** `Property`

---

### DELETE `/api/properties/:id`

Delete a property listing.

- **Auth required:** Yes (property owner)
- **Response `200`:**
  ```json
  { "message": "Property deleted successfully" }
  ```

---

### PATCH `/api/properties/:id/status`

Update a property's status.

- **Auth required:** Yes (property owner)
- **Body:** `{ "status": "paused" }`
- **Response `200`:** `Property`

---

### PATCH `/api/properties/:id/featured`

Toggle a property's featured flag.

- **Auth required:** Yes (property owner)
- **Body:** `{ "is_featured": true }`
- **Response `200`:** `Property`

---

### POST `/api/uploads/image`

Upload a single property image.

- **Auth required:** Yes
- **Body:** `multipart/form-data` with `file` field
- **Response `200`:** `{ "url": "https://..." }`

---

### POST `/api/uploads/images`

Upload multiple property images.

- **Auth required:** Yes
- **Body:** `multipart/form-data` with multiple `files` fields
- **Response `200`:** `{ "urls": ["https://...", "https://..."] }`

---

### POST `/api/favorites/:propertyId`

Add a property to favorites.

- **Auth required:** Yes
- **Response `201`:** `{ "message": "Added to favorites" }`

---

### DELETE `/api/favorites/:propertyId`

Remove a property from favorites.

- **Auth required:** Yes
- **Response `200`:** `{ "message": "Removed from favorites" }`

---

### GET `/api/favorites`

Get the current user's favorite properties.

- **Auth required:** Yes
- **Response `200`:** `Property[]`

---

## Phase 3 — Clients (CRM)

### POST `/api/clients`

Create a new client record.

- **Auth required:** Yes (agent)
- **Body:** `ClientCreate`
- **Response `201`:** `Client`

---

### GET `/api/clients`

List the agent's clients with optional filters.

- **Auth required:** Yes (agent)
- **Query params:** `status`, `search`, `page`, `limit`
- **Response `200`:** `Client[]`
- **Headers:** `X-Total-Count: 15`

---

### GET `/api/clients/:id`

Get a single client by ID.

- **Auth required:** Yes (agent, own clients only)
- **Response `200`:** `Client`

---

### PUT `/api/clients/:id`

Update a client record.

- **Auth required:** Yes (agent, own clients only)
- **Body:** `ClientUpdate`
- **Response `200`:** `Client`

---

### PATCH `/api/clients/:id/status`

Update a client's CRM status.

- **Auth required:** Yes (agent)
- **Body:** `{ "status": "interested" }`
- **Response `200`:** `Client`

---

### GET `/api/clients/stats`

Get counts per CRM status for the agent's client portfolio.

- **Auth required:** Yes (agent)
- **Response `200`:**
  ```json
  {
    "new": 5, "contacted": 3, "interested": 8,
    "negotiating": 2, "closed": 12, "lost": 4
  }
  ```

---

## Phase 3 — Messages

### POST `/api/messages`

Send a message.

- **Auth required:** Yes
- **Body:**
  ```json
  { "receiver_id": "uuid", "content": "Hello!", "property_id": "uuid" }
  ```
- **Response `201`:** `Message`

---

### GET `/api/messages/conversations`

List all conversations for the current user.

- **Auth required:** Yes
- **Response `200`:** `Conversation[]` (each with latest message and unread count)

---

### GET `/api/messages/:userId`

Get messages exchanged with a specific user.

- **Auth required:** Yes
- **Query params:** `page`, `limit`
- **Response `200`:** `Message[]`
- **Headers:** `X-Total-Count: 30`

---

### PUT `/api/messages/:id/read`

Mark a message as read.

- **Auth required:** Yes
- **Response `200`:** `{ "message": "Marked as read" }`

---

### GET `/api/messages/unread-count`

Get the total unread message count for the current user.

- **Auth required:** Yes
- **Response `200`:** `{ "count": 7 }`

---

## Phase 4 — Appointments

### POST `/api/appointments`

Schedule a property appointment.

- **Auth required:** Yes
- **Body:**
  ```json
  {
    "property_id": "uuid",
    "scheduled_date": "2024-06-15",
    "scheduled_time": "10:00",
    "notes": "Client prefers morning visits"
  }
  ```
- **Response `201`:** `Appointment`

---

### GET `/api/appointments`

List appointments for the current user.

- **Auth required:** Yes
- **Query params:** `status`, `date`, `page`, `limit`
- **Response `200`:** `Appointment[]`

---

### GET `/api/appointments/today`

Get today's appointments for the authenticated agent.

- **Auth required:** Yes (agent)
- **Response `200`:** `Appointment[]`

---

### GET `/api/appointments/upcoming`

Get upcoming appointments for the current user.

- **Auth required:** Yes
- **Response `200`:** `Appointment[]`

---

### PUT `/api/appointments/:id`

Update an appointment.

- **Auth required:** Yes (owner or agent)
- **Response `200`:** `Appointment`

---

### PATCH `/api/appointments/:id/status`

Update an appointment's status.

- **Auth required:** Yes
- **Body:** `{ "status": "confirmed" }`
- **Response `200`:** `Appointment`

---

### GET `/api/appointments/availability`

Get available time slots for an agent on a specific date.

- **Auth required:** No
- **Query params:** `agent_id`, `date`
- **Response `200`:** `TimeSlot[]`

---

## Phase 5 — Analytics

### GET `/api/analytics/overview`

Get a high-level dashboard summary for the agent.

- **Auth required:** Yes (agent)
- **Response `200`:**
  ```json
  {
    "total_properties": 24,
    "total_clients": 37,
    "total_appointments": 12,
    "views_this_month": 1580
  }
  ```

---

### GET `/api/analytics/properties`

Get property performance analytics.

- **Auth required:** Yes (agent)
- **Response `200`:**
  ```json
  {
    "most_viewed": [{ "id": "uuid", "title": "...", "views": 120 }],
    "favorites_count": [{ "id": "uuid", "title": "...", "count": 45 }],
    "views_by_month": [{ "month": "2024-05", "views": 320 }]
  }
  ```

---

### GET `/api/analytics/clients`

Get CRM analytics for the agent.

- **Auth required:** Yes (agent)
- **Response `200`:**
  ```json
  {
    "by_source": [{ "source": "WhatsApp", "count": 12 }],
    "by_status": [{ "status": "interested", "count": 8 }],
    "conversion_rate": 0.32
  }
  ```

---

### GET `/api/analytics/appointments`

Get appointment analytics for the agent.

- **Auth required:** Yes (agent)
- **Response `200`:**
  ```json
  {
    "by_month": [{ "month": "2024-05", "count": 8 }],
    "by_status": [{ "status": "completed", "count": 15 }],
    "completion_rate": 0.78
  }
  ```

---

## Phase 5 — Property Alerts

### POST `/api/alerts`

Create a new property alert.

- **Auth required:** Yes
- **Body:** `AlertCreate`
- **Response `201`:** `Alert`

---

### GET `/api/alerts`

List the current user's property alerts.

- **Auth required:** Yes
- **Response `200`:** `Alert[]`

---

### PUT `/api/alerts/:id`

Update a property alert.

- **Auth required:** Yes (owner)
- **Response `200`:** `Alert`

---

### DELETE `/api/alerts/:id`

Delete a property alert.

- **Auth required:** Yes (owner)
- **Response `200`:** `{ "message": "Alert deleted" }`

---

### PATCH `/api/alerts/:id/toggle`

Enable or disable a property alert.

- **Auth required:** Yes (owner)
- **Response `200`:** `Alert`

---

## Phase 6 — AI Features

### POST `/api/chat/stream`

Start or continue an AI chat session (Server-Sent Events).

- **Auth required:** Yes
- **Body:**
  ```json
  {
    "message": "Show me 3-bedroom houses under $3M in Polanco",
    "history": [{ "role": "user", "content": "..." }, { "role": "assistant", "content": "..." }]
  }
  ```
- **Response:** `text/event-stream` SSE stream

---

### GET `/api/chat/sessions`

List the current user's chat sessions.

- **Auth required:** Yes
- **Response `200`:** `ChatSession[]`

---

### GET `/api/chat/sessions/:id`

Get messages in a specific chat session.

- **Auth required:** Yes (session owner)
- **Response `200`:** `ChatMessage[]`

---

### DELETE `/api/chat/sessions/:id`

Delete a chat session and its messages.

- **Auth required:** Yes (session owner)
- **Response `200`:** `{ "message": "Session deleted" }`

---

### POST `/api/properties/search/semantic`

Search properties using natural language (vector similarity).

- **Auth required:** Yes
- **Body:** `{ "query": "cozy apartment near metro with parking" }`
- **Response `200`:** `Property[]` (ordered by similarity score)

---

### POST `/api/ai/generate-description`

Generate an attractive property description using GPT-4o.

- **Auth required:** Yes (agent)
- **Body:**
  ```json
  {
    "property_data": {
      "title": "...", "bedrooms": 3, "bathrooms": 2, "area_m2": 120,
      "city": "CDMX", "amenities": ["pool", "gym"]
    }
  }
  ```
- **Response `200`:** `{ "description": "Stunning 3-bedroom apartment..." }`

---

### POST `/api/ai/estimate-price`

Estimate a property price using comparable data and LLM analysis.

- **Auth required:** Yes
- **Body:** `{ "property_data": { ... } }`
- **Response `200`:**
  ```json
  {
    "estimated_price": 3500000,
    "range": { "min": 3200000, "max": 3800000 },
    "confidence": 0.82,
    "reasoning": "Based on 5 comparable properties in the area..."
  }
  ```

---

### POST `/api/ai/cv/optimize`

Optimize a CV for impact and clarity (SSE stream).

- **Auth required:** Yes
- **Body:** `{ "cv_text": "..." }`
- **Response:** `text/event-stream` SSE stream

---

### POST `/api/ai/cv/adapt`

Adapt a CV to match a specific job description (SSE stream).

- **Auth required:** Yes
- **Body:** `{ "cv_text": "...", "job_description": "..." }`
- **Response:** `text/event-stream` SSE stream

---

### POST `/api/ai/cv/score`

Score a CV and provide ATS analysis.

- **Auth required:** Yes
- **Body:** `{ "cv_text": "..." }`
- **Response `200`:**
  ```json
  {
    "score": 78,
    "ats_score": 85,
    "strengths": ["Clear structure", "Quantified achievements"],
    "weaknesses": ["Missing keywords for target role"],
    "suggestions": ["Add technical skills section", "Include LinkedIn URL"]
  }
  ```

---

### POST `/api/ai/cv/cover-letter`

Generate a tailored cover letter (SSE stream).

- **Auth required:** Yes
- **Body:**
  ```json
  {
    "position": "Senior Frontend Engineer",
    "company": "Acme Corp",
    "experience": "5 years building React Native apps..."
  }
  ```
- **Response:** `text/event-stream` SSE stream
