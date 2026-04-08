# Component & Screen Map — Habitat AI

---

## Base UI Components (`components/ui/`)

| Component | Props | Status |
|-----------|-------|--------|
| Button | `variant` (primary/secondary/outline/danger), `size` (sm/md/lg), `onPress`, `loading`, `disabled` | ⏳ Pending |
| Input | `label`, `error`, `type` (text/password/email/phone), `placeholder`, `value`, `onChange` | ⏳ Pending |
| Card | `children`, `onPress`, `elevated`, `className` | ⏳ Pending |
| Avatar | `uri`, `size` (sm/md/lg), `fallback` (initials string) | ⏳ Pending |
| Badge | `text`, `variant` (success/warning/danger/info), `size` | ⏳ Pending |
| Skeleton | `width`, `height`, `borderRadius` | ⏳ Pending |
| EmptyState | `title`, `description`, `icon`, `actionLabel`, `onAction` | ⏳ Pending |
| Toast | `message`, `type` (success/error/info), `duration` | ⏳ Pending |
| Modal | `visible`, `onClose`, `title`, `children` | ⏳ Pending |
| SearchBar | `value`, `onChange`, `placeholder`, `onFilter` | ⏳ Pending |

---

## Property Components (`components/property/`)

| Component | Props | Status |
|-----------|-------|--------|
| PropertyCard | `property`, `onPress`, `onFavorite`, `isFavorite` | ⏳ Pending |
| PropertyGallery | `images`, `onImagePress` | ⏳ Pending |
| PropertyFilters | `filters`, `onChange`, `onApply`, `onClear`, `resultsCount` | ⏳ Pending |
| PropertyMap | `properties`, `onMarkerPress`, `initialRegion` | ⏳ Pending |
| MortgageCalculator | `price`, `currency` | ⏳ Pending |
| PriceEstimator | `propertyData`, `onEstimate` | ⏳ Pending |

---

## Chat Components (`components/chat/`)

| Component | Props | Status |
|-----------|-------|--------|
| ChatBubble | `message`, `isOwn`, `timestamp`, `isRead` | ⏳ Pending |
| ChatInput | `value`, `onChange`, `onSend`, `placeholder` | ⏳ Pending |
| StreamingText | `text`, `isStreaming` | ⏳ Pending |

---

## Shared Components (`components/shared/`)

| Component | Props | Status |
|-----------|-------|--------|
| AgentCard | `agent`, `onContact`, `onCall` | ⏳ Pending |

---

## Client Screens

| Screen | Route | Phase | Status |
|--------|-------|-------|--------|
| Welcome / Splash | `/` | 1 | ⏳ Pending |
| Login | `(auth)/login` | 1 | ⏳ Pending |
| Register | `(auth)/register` | 1 | ⏳ Pending |
| Home | `(tabs)/index` | 2 | ⏳ Pending |
| Explore | `(tabs)/explore` | 2 | ⏳ Pending |
| Map | `(tabs)/map` | 4 | ⏳ Pending |
| Favorites | `(tabs)/favorites` | 2 | ⏳ Pending |
| Profile | `(tabs)/profile` | 1 | ⏳ Pending |
| Property Detail | `property/[id]` | 2 | ⏳ Pending |
| Chat with AI | `(tabs)/chat` | 6 | ⏳ Pending |
| My Appointments | `appointments/` | 4 | ⏳ Pending |
| My Alerts | `alerts/` | 5 | ⏳ Pending |

---

## Agent Screens

| Screen | Route | Phase | Status |
|--------|-------|-------|--------|
| Dashboard | `(agent)/dashboard` | 2 | ⏳ Pending |
| My Properties | `(agent)/properties/` | 2 | ⏳ Pending |
| Create Property | `(agent)/properties/create` | 2 | ⏳ Pending |
| Edit Property | `(agent)/properties/[id]` | 2 | ⏳ Pending |
| Clients CRM | `(agent)/clients/` | 3 | ⏳ Pending |
| Client Detail | `(agent)/clients/[id]` | 3 | ⏳ Pending |
| Add Client | `(agent)/clients/create` | 3 | ⏳ Pending |
| Agenda | `(agent)/agenda` | 4 | ⏳ Pending |
| Analytics | `(agent)/analytics` | 5 | ⏳ Pending |
| CV Tool | `(agent)/cv-tool` | 6 | ⏳ Pending |
