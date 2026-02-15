# Quest Bot — The Handler

A real-world, story-driven adventure system for a parent + kid. You give time/location/conditions; **The Handler** assembles a bespoke operation from recon-derived modules. Quests log memories, artifacts, and progress into replayable packs.

## Structure
- /app — single-file Quest Console (source of truth)
- /schemas — quest + appearance schema references
- /experiments — all prototypes / mockups preserved
- /backend/worker — Cloudflare Worker + D1 (recon → modules → quest)

## Quick Start (local)
Open:
- app/index.html

Set `API_BASE` + `AUDIO_BASE` inside the HTML to point at your worker + audio folder.

## Deploy (Worker)
cd backend/worker
wrangler d1 create questing
wrangler d1 migrations apply questing --local
wrangler d1 migrations apply questing
wrangler deploy
