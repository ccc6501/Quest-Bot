-- Tracks per-client sync state for offline-first D1 sync
CREATE TABLE IF NOT EXISTS sync_ledger (
  client_id TEXT PRIMARY KEY,
  last_push_at TEXT NOT NULL,
  last_push_count INTEGER DEFAULT 0,
  last_pull_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index for pull queries filtering by created_at
CREATE INDEX IF NOT EXISTS idx_recon_items_created ON recon_items(created_at);
CREATE INDEX IF NOT EXISTS idx_modules_created ON modules(created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback(created_at);
