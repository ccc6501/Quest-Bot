CREATE TABLE IF NOT EXISTS recon_items (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  type TEXT NOT NULL,
  title TEXT,
  source_url TEXT,
  raw_text TEXT,
  parse_status TEXT NOT NULL,
  quality_score REAL DEFAULT 0.5,
  quality_notes TEXT
);

CREATE TABLE IF NOT EXISTS modules (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  tags TEXT NOT NULL,
  vibe TEXT,
  weather_fit TEXT,
  duration_fit TEXT,
  range_fit TEXT,
  location_hint TEXT,
  confidence REAL DEFAULT 0.6,
  payload TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS module_sources (
  module_id TEXT NOT NULL,
  recon_id TEXT NOT NULL,
  note TEXT,
  PRIMARY KEY (module_id, recon_id)
);

CREATE TABLE IF NOT EXISTS feedback (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  kind TEXT NOT NULL,
  target_id TEXT NOT NULL,
  rating INTEGER,
  note TEXT,
  action TEXT
);
