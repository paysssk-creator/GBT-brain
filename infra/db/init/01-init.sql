-- ==========================================
-- GBT ?????? - ????
-- ==========================================

-- 1. ???????
CREATE DATABASE gbt_creator;
\c gbt_creator
CREATE EXTENSION vector;
CREATE TABLE IF NOT EXISTS app_state (
    key TEXT PRIMARY KEY,
    value JSONB,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    config JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Cline ?????
CREATE DATABASE gbt_cline;
\c gbt_cline
CREATE EXTENSION vector;
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    summary TEXT,
    messages JSONB,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS knowledge (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    content TEXT,
    embedding vector(1536),
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT,
    status TEXT DEFAULT 'pending',
    result JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Brain ????? (????)
CREATE DATABASE gbt_brain;
\c gbt_brain
CREATE EXTENSION vector;
CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT,
    embedding vector(1536),
    tags TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS learnings (
    id TEXT PRIMARY KEY,
    insight TEXT,
    embedding vector(1536),
    source TEXT,
    confidence REAL DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS patterns (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    evidence TEXT,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    problem TEXT,
    options JSONB,
    chosen TEXT,
    rationale TEXT,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ??
CREATE INDEX ON notes USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON learnings USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON patterns USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON decisions USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON sessions USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON knowledge USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
