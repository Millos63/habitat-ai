# Guía rápida para correr Habitat AI

Este archivo resume **todo lo necesario para instalar y ejecutar** el proyecto.

## 1) Requisitos previos

Instala y verifica estas herramientas:

- **Git**
- **Node.js** (recomendado: 18+)
- **npm** (viene con Node)
- **Python** (3.12+)
- **Docker Desktop** (incluye Docker Compose)
- **Expo Go** en tu celular (opcional, para probar móvil)

Verificación rápida:

```bash
git --version
node -v
npm -v
python3 --version
docker --version
docker compose version
```

---

## 2) Ruta correcta del proyecto

En tu caso, la carpeta real del repo es:

```bash
cd /Users/millos63/habitat-ai/habitat-ai
```

> Importante: Si ejecutas comandos Expo fuera de `mobile/`, verás el error de `package.json` no encontrado.

---

## 3) Backend

### Opción A (recomendada): con Docker

Desde la raíz del repo:

```bash
cd /Users/millos63/habitat-ai/habitat-ai
cp backend/.env.example backend/.env
docker compose -f docker/docker-compose.yml up --build
```

Servicios:
- API: http://localhost:8000
- Health: http://localhost:8000/api/health

---

### Opción B: local sin Docker

Necesitas PostgreSQL + Redis corriendo localmente.

```bash
cd /Users/millos63/habitat-ai/habitat-ai/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 4) Mobile (Expo)

```bash
cd /Users/millos63/habitat-ai/habitat-ai/mobile
npm install
```

### Arrancar en modo normal

```bash
npx expo start
```

### Arrancar con túnel

```bash
npx expo start --tunnel
```

Si llegara a pedir ngrok:

```bash
npx expo install @expo/ngrok
```

---

## 5) Variable de API para móvil (recomendado)

El móvil usa `EXPO_PUBLIC_API_URL`. Crea archivo `.env` en `mobile/`:

```bash
cd /Users/millos63/habitat-ai/habitat-ai/mobile
echo 'EXPO_PUBLIC_API_URL=http://<TU_IP_LOCAL>:8000/api' > .env
```

Ejemplo:

```bash
EXPO_PUBLIC_API_URL=http://192.168.1.10:8000/api
```

> Si pruebas en celular físico, **no uses `localhost`** para la API.

---

## 6) Flujo recomendado (2 terminales)

### Terminal 1 (backend)

```bash
cd /Users/millos63/habitat-ai/habitat-ai
docker compose -f docker/docker-compose.yml up --build
```

### Terminal 2 (mobile)

```bash
cd /Users/millos63/habitat-ai/habitat-ai/mobile
npx expo start --tunnel
```

---

## 7) Tests backend

```bash
cd /Users/millos63/habitat-ai/habitat-ai/backend
python -m pytest tests/ -v
```

---

## 8) Problemas comunes

- **Error:** `The expected package.json path ... does not exist`
  - Solución: ejecuta Expo dentro de `mobile/`.

- **La app móvil no conecta al backend**
  - Verifica que backend esté arriba en `:8000`.
  - Usa tu IP local en `EXPO_PUBLIC_API_URL`.
  - Revisa firewall/red Wi‑Fi (misma red para PC y celular).
