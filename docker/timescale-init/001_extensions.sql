-- ── TimescaleDB Initialization ───────────────────────────
-- Runs once when the PostgreSQL container is first created.
-- Sets up TimescaleDB extension and row-level security.
-- ─────────────────────────────────────────────────────────

-- Enable TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pg_trgm for text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Enable Row Level Security helper
-- RLS policies are created by Alembic migrations alongside tables,
-- but we enable the extension infrastructure here.

-- Create a read-only role for analytics queries
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'purecast_readonly') THEN
        CREATE ROLE purecast_readonly;
    END IF;
END
$$;

GRANT CONNECT ON DATABASE purecast TO purecast_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO purecast_readonly;
