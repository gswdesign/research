-- =============================================================================
-- PostgreSQL Initialization Script for ZITADEL
-- =============================================================================
-- This script runs on first PostgreSQL startup
-- ZITADEL handles its own schema migrations, so we just ensure the DB exists
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create additional indexes for performance (optional)
-- ZITADEL will create its own tables and indexes during initialization

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL initialized for ZITADEL';
END $$;
