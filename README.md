# Quest Bot — The Handler

A real-world, story-driven adventure system for a parent + kid. You give time/location/conditions; **The Handler** assembles a bespoke operation from recon-derived modules. Quests log memories, artifacts, and progress into replayable packs.

## Structure
- `/app` — single-file Quest Console (source of truth)
- `/schemas` — quest + appearance schema references
- `/experiments` — all prototypes / mockups preserved
- `/backend/worker` — Cloudflare Worker + D1 (recon → modules → quest)

## AI Providers
The worker supports two providers, switchable via `AI_PROVIDER` in wrangler.toml:

| Provider | Env Var (model) | Env Var (key) | Default model |
|---|---|---|---|
| **OpenRouter** | `OPENROUTER_MODEL` | `OPENROUTER_API_KEY` | `anthropic/claude-3.5-sonnet` |
| **OpenAI** | `OPENAI_MODEL` | `OPENAI_API_KEY` | `gpt-4o` |

Set API keys as secrets (not plaintext vars):
```bash
cd backend/worker
wrangler secret put OPENROUTER_API_KEY
wrangler secret put OPENAI_API_KEY
```

## D1 Sync
The worker exposes offline-first sync endpoints:
- `POST /api/sync/push` — client pushes local changes (recon, modules, feedback)
- `GET /api/sync/pull?since=<ISO timestamp>` — client pulls server changes since last sync

The app includes `syncPush()` and `syncPull()` client helpers that track sync state in localStorage.

## Deploy (Worker)
```bash
cd backend/worker
wrangler d1 create questing
# Copy the database_id into wrangler.toml
wrangler d1 migrations apply questing --local
wrangler d1 migrations apply questing
wrangler deploy
```

## Publish to makerapp.cc
The app is published as an unlisted app at `makerapp.cc/apps/quest-console/`.

1. Copy `app/index.html` into the makerapp.cc repo:
   ```
   makerapp.cc/apps/quest-console/index.html
   ```
2. Place Handler audio files at:
   ```
   makerapp.cc/apps/quest-console/assets/audio/handler/
   ```
3. In `app/index.html`, set:
   - `API_BASE` = your deployed worker URL (e.g. `https://quest-handler.<account>.workers.dev`)
   - `AUDIO_BASE` = `https://makerapp.cc/apps/quest-console/assets/audio/handler`

The app is unlisted — no link from the makerapp.cc homepage. Access directly via URL only.

## Quick Start (local)
Open `app/index.html` in a browser. The app works offline for quest management. Set `API_BASE` to connect to the worker for AI-powered recon/quest generation.

## API Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/api/ping` | Health check + provider info |
| POST | `/api/recon/add` | Ingest recon → extract modules |
| GET | `/api/recon/list` | List recon items |
| GET | `/api/modules/list` | List modules (optional `?tag=`) |
| POST | `/api/quest/generate` | Generate quest from modules |
| POST | `/api/sync/push` | Push client changes to D1 |
| GET | `/api/sync/pull` | Pull server changes since timestamp |
