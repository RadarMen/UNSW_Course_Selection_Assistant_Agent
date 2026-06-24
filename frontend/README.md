# UNSW Course Assistant Frontend

Vue3 + Vite frontend MVP for the FastAPI backend.

## Run

```bash
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

Backend default:

```text
http://127.0.0.1:8000
```

In development, Vite proxies `/api/*` to the backend to avoid browser CORS issues without changing backend code.

To change the backend address, create `.env`:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```
