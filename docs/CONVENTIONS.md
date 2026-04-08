# Coding Conventions — Habitat AI

---

## Python (Backend)

### General

- **Async/await** on all endpoint handlers and service functions — no synchronous blocking calls.
- **Type hints** are mandatory on every function parameter and return value.
- **Pydantic v2** for all input validation and response serialization.
- One responsibility per function — keep service functions small and composable.

### Endpoint Naming

- URLs in **English**, **kebab-case**.
- Examples: `/api/properties/search-semantic`, `/api/auth/refresh-token`, `/api/uploads/avatar`.
- No verbs in resource URLs (the HTTP method provides the verb).

### Model Naming

- SQLAlchemy models in **singular PascalCase**: `User`, `Property`, `Client`, `Appointment`.
- Table names in **plural snake_case** (set via `__tablename__`): `users`, `properties`, `clients`.

### Service Naming

- Services are **async functions**, not classes.
- Function names describe the action: `create_property`, `get_property_by_id`, `search_properties_semantic`.
- Services live in `backend/app/services/` with a matching resource name: `property_service.py`, `auth_service.py`.

### File Structure

```
backend/app/
├── models/
│   ├── user.py
│   ├── property.py
│   └── ...
├── schemas/
│   ├── user.py          # UserBase, UserCreate, UserUpdate, UserResponse
│   ├── property.py
│   └── ...
├── routers/
│   ├── auth.py
│   ├── properties.py
│   └── ...
├── services/
│   ├── auth_service.py
│   ├── property_service.py
│   └── ...
```

### Example — Service Function

```python
async def create_property(
    db: AsyncSession,
    agent_id: UUID,
    data: PropertyCreate,
) -> PropertyResponse:
    property_obj = Property(**data.model_dump(), agent_id=agent_id)
    db.add(property_obj)
    await db.commit()
    await db.refresh(property_obj)
    return PropertyResponse.model_validate(property_obj)
```

### Example — Router Handler

```python
@router.post("/", response_model=PropertyResponse, status_code=201)
async def create_property_endpoint(
    data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_agent),
) -> PropertyResponse:
    return await create_property(db, current_user.id, data)
```

---

## TypeScript (Mobile)

### Components

- **Functional components** with arrow functions — no class components.
- **NativeWind** (`className` prop) for all styles — no StyleSheet objects.
- Component files in **PascalCase**: `PropertyCard.tsx`, `LoginForm.tsx`.
- One component per file.

```tsx
// ✅ Correct
const PropertyCard = ({ property, onPress }: PropertyCardProps) => {
  return (
    <Pressable className="bg-white rounded-xl p-4 shadow-sm" onPress={onPress}>
      <Text className="text-lg font-semibold">{property.title}</Text>
    </Pressable>
  );
};

export default PropertyCard;
```

### Hooks

- Hook files in **camelCase** with `use` prefix: `useProperties.ts`, `useAuth.ts`.
- Hooks live in `mobile/hooks/`.
- Data-fetching hooks wrap TanStack Query — return `{ data, isLoading, error }`.

```ts
// ✅ Correct
const useProperties = (filters: PropertyFilters) => {
  return useQuery({
    queryKey: ['properties', filters],
    queryFn: () => propertiesService.getAll(filters),
  });
};

export default useProperties;
```

### Services

- Service files in **camelCase** with `.service.ts` suffix: `properties.service.ts`, `auth.service.ts`.
- Services live in `mobile/services/`.
- Every function is typed with explicit parameter and return types.

```ts
// ✅ Correct
const propertiesService = {
  getAll: async (filters: PropertyFilters): Promise<Property[]> => {
    const response = await api.get('/properties', { params: filters });
    return response.data.data;
  },
};

export default propertiesService;
```

### Types

- Type files in **camelCase** with `.types.ts` suffix: `property.types.ts`, `user.types.ts`.
- Types live in `mobile/types/`.
- One file per entity.
- Use `interface` for objects, `type` for unions/intersections.

### Stores

- Store files in **camelCase** with `Store` suffix: `authStore.ts`, `themeStore.ts`.
- Use Zustand only for auth and theme state.

---

## API Naming Conventions

| Pattern | HTTP Method | URL | Description |
|---------|------------|-----|-------------|
| List | GET | `/api/{resource}` | Return paginated list |
| Detail | GET | `/api/{resource}/:id` | Return single item |
| Create | POST | `/api/{resource}` | Create new item |
| Full Update | PUT | `/api/{resource}/:id` | Replace entire item |
| Partial Update | PATCH | `/api/{resource}/:id` | Update specific fields |
| Remove | DELETE | `/api/{resource}/:id` | Delete item |

---

## API Response Format

### Success (single item or action)

```json
{ "data": { ... } }
```

### Success (list)

```json
[{ ... }, { ... }]
```
Header: `X-Total-Count: 42`

### Error

```json
{ "detail": "Human-readable error message" }
```

HTTP status codes:
- `200` — Success
- `201` — Created
- `400` — Bad Request (validation error)
- `401` — Unauthorized (missing/invalid token)
- `403` — Forbidden (insufficient permissions)
- `404` — Not Found
- `422` — Unprocessable Entity (Pydantic validation)
- `429` — Too Many Requests (rate limit)
- `500` — Internal Server Error

---

## Git Conventions

### Commit Format

```
type(scope): short description in imperative mood
```

| Type | When to use |
|------|------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `chore` | Build process, dependency updates, config |
| `perf` | Performance improvement |
| `ci` | CI/CD configuration |
| `build` | Build system changes |
| `style` | Formatting, whitespace (no logic change) |

### Scopes

**Backend scopes:** `auth`, `properties`, `clients`, `appointments`, `chat`, `ai`, `db`, `config`, `upload`

**Mobile scopes:** `ui`, `home`, `explore`, `detail`, `favorites`, `profile`, `crm`, `agenda`, `map`, `chat-ui`

**General scopes:** `deps`, `docker`, `ci`, `docs`

### Examples

```
feat(properties): add semantic search endpoint
fix(auth): handle expired token refresh correctly
docs: update API contracts for phase 3
chore(deps): upgrade FastAPI to 0.111
test(properties): add unit tests for property service
ci: add GitHub Actions workflow for backend tests
```

### Branch Naming

| Pattern | When to use |
|---------|------------|
| `feature/phase-X.X-description` | New feature tied to a phase |
| `fix/description` | Bug fix |
| `hotfix/description` | Urgent production fix |
| `release/vX.X.X` | Release preparation |

### Examples

```
feature/phase-1.1-authentication
feature/phase-2.1-property-catalog
fix/jwt-expiry-handling
hotfix/property-image-upload-crash
release/v1.0.0
```
