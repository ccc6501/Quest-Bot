#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
#  Quest Bot — one-command deploy
#  Prerequisites: npm, wrangler (npm i -g wrangler)
#  Run: bash deploy.sh
# ─────────────────────────────────────────────

WORKER_DIR="$(cd "$(dirname "$0")/backend/worker" && pwd)"
TOML="$WORKER_DIR/wrangler.toml"
DB_NAME="questing"

echo "▸ Quest Bot deploy"
echo ""

# 1. Check wrangler auth
if ! wrangler whoami &>/dev/null; then
  echo "✗ Not logged in. Running: wrangler login"
  wrangler login
fi
echo "✓ Authenticated"

# 2. Create D1 database if wrangler.toml still has PLACEHOLDER
CURRENT_ID=$(grep 'database_id' "$TOML" | head -1 | sed 's/.*= *"\(.*\)"/\1/')
if [[ "$CURRENT_ID" == "PLACEHOLDER" ]] || [[ "$CURRENT_ID" == "a1b2c3d4-5678-90ab-cdef-1234567890ab" ]]; then
  echo "▸ Creating D1 database '$DB_NAME'..."
  CREATE_OUT=$(wrangler d1 create "$DB_NAME" 2>&1) || true
  NEW_ID=$(echo "$CREATE_OUT" | grep -oP 'database_id\s*=\s*"\K[^"]+' || true)
  if [[ -z "$NEW_ID" ]]; then
    # Database might already exist — list and grab it
    NEW_ID=$(wrangler d1 list --json 2>/dev/null | python3 -c "
import sys,json
for db in json.load(sys.stdin):
    if db.get('name')=='$DB_NAME':
        print(db['uuid']); break
" 2>/dev/null || true)
  fi
  if [[ -z "$NEW_ID" ]]; then
    echo "✗ Could not create or find D1 database. Check output above."
    exit 1
  fi
  sed -i "s|database_id = \"$CURRENT_ID\"|database_id = \"$NEW_ID\"|" "$TOML"
  echo "✓ D1 database created: $NEW_ID"
else
  echo "✓ D1 database_id already set: $CURRENT_ID"
fi

# 3. Apply migrations
echo "▸ Applying D1 migrations..."
cd "$WORKER_DIR"
wrangler d1 migrations apply "$DB_NAME" --remote
echo "✓ Migrations applied"

# 4. Set API key as secret (not in plaintext toml)
echo ""
echo "▸ Setting OPENROUTER_API_KEY secret..."
echo "  Paste your OpenRouter API key when prompted (or hit Enter to skip if already set):"
wrangler secret put OPENROUTER_API_KEY || echo "  (skipped — set it later with: wrangler secret put OPENROUTER_API_KEY)"

# 5. Deploy worker
echo ""
echo "▸ Deploying worker..."
wrangler deploy
echo "✓ Worker deployed"

# 6. Remind about static files + route
WORKER_URL=$(wrangler deployments list --json 2>/dev/null | python3 -c "
import sys,json
d=json.load(sys.stdin)
if isinstance(d,list) and d:
    print(d[0].get('url',''))
" 2>/dev/null || echo "(check dashboard)")

echo ""
echo "═══════════════════════════════════════════"
echo "  ✓ Worker live at: $WORKER_URL"
echo ""
echo "  Remaining steps:"
echo "  1. Upload app/index.html + robots.txt"
echo "     to your host at /x/relay-7f3c/"
echo ""
echo "  2. Route the worker under makerapp.cc/api/*"
echo "     → Cloudflare dashboard > Workers & Pages"
echo "     → quest-handler > Settings > Triggers"
echo "     → Add Route: makerapp.cc/api/*"
echo "     (or uncomment routes in wrangler.toml"
echo "      and redeploy)"
echo ""
echo "  3. Open https://makerapp.cc/x/relay-7f3c/"
echo "     The console auto-uses same-origin /api/*"
echo "═══════════════════════════════════════════"
