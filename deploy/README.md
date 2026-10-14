# EDGE RESCUE — Cloud Deployment Guide

Two containerized Cloud Run services (scale-to-zero, zero idle charges):

```
edge-rescue-backend   → FastAPI               (1 GB / 1 CPU)
edge-rescue-frontend  → React + nginx         (256 MB / 1 CPU)
```

Gemma 4 26B runs via **Google AI Studio API** — no self-hosted GPU needed.

---

## Prerequisites

```bash
# Install gcloud CLI: https://cloud.google.com/sdk/docs/install
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Install Docker Desktop (needed to build images locally)
```

---

## Step 0 — One-time project setup

```bash
bash gcp-setup.sh
```

---

## Step 1 — Get a Gemini API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create an API key
3. Model used: `gemma-4-26b-a4b-it`

```bash
export GEMINI_API_KEY="your-key-here"
```

> **Offline Fallback Guarantee**: If `GEMINI_API_KEY` is unset or the API returns an error, the algorithm top pick and rule-based classifier are used automatically (`ai_available: false`). The UI always receives a valid, prioritized result.

---

## Step 2 — Databases (Managed or Local)

| Service | Provider | Free tier |
|---------|----------|-----------|
| Postgres | [Neon](https://neon.tech) / Supabase | 0.5 GB |
| Redis | [Upstash](https://upstash.com) | 10k commands/day |

```bash
export DB_URL="postgresql+asyncpg://user:pass@ep-xxx.neon.tech/edgerescue?sslmode=require"
export REDIS_URL="redis://:password@host.upstash.io:port"
```

---

## Step 3 — Deploy Backend (FastAPI)

```bash
# GEMINI_API_KEY, DB_URL, REDIS_URL must be set
bash deploy-backend-gcp.sh
```

Copy the output URL:
```bash
export BACKEND_URL="https://edge-rescue-backend-xxxx-uc.a.run.app"
```

---

## Step 4 — Deploy Frontend (React + nginx)

```bash
# BACKEND_URL must be set
bash deploy-frontend-gcp.sh
```

`VITE_API_URL` is baked into the static bundle at build time via `--build-arg`.

---

## Full Deploy Cheatsheet

```bash
bash gcp-setup.sh                          # once

export GEMINI_API_KEY="your-key"
export DB_URL="postgresql+asyncpg://..."
export REDIS_URL="redis://..."

bash deploy-backend-gcp.sh
export BACKEND_URL="https://edge-rescue-backend-xxxx-uc.a.run.app"

bash deploy-frontend-gcp.sh
```

---

## Environment Variables

| Service | Variable | Value |
|---------|----------|-------|
| Backend | `DATABASE_URL` | Postgres URL (PostgreSQL + asyncpg) |
| Backend | `REDIS_URL` | Redis URL |
| Backend | `GEMINI_API_KEY` | Google AI Studio key |
| Backend | `GEMMA_MODEL` | `gemma-4-26b-a4b-it` |
| Frontend | `VITE_API_URL` | Cloud Run backend URL (baked at build) |

---

## Architecture

```
Browser ──► edge-rescue-frontend (Cloud Run / nginx)
                │
                │ REST + WebSocket
                ▼
         edge-rescue-backend (Cloud Run / FastAPI)
                │                    │
           PostgreSQL             Redis pub/sub
           (Neon / Supabase)      (Upstash / Local)
                │
                │ HTTPS (Gemini API)
                ▼
         Google AI Studio
         Gemma 4 26B (gemma-4-26b-a4b-it)
```

---

## Local Development

```bash
# Start Postgres + Redis via Docker Compose
docker compose up -d

# Backend
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Frontend
cd frontend && npm install && npm run dev
```
