-- supabase/migrations/001_init_capymind.sql
-- Initial CapyMind knowledge pack schema
-- Compatible with standard PostgreSQL (no pgvector dependency)
--
-- If you want vector search later, you can add pgvector extension and extend document_chunks.

-- Enable required extensions
create extension if not exists "uuid-ossp";

-- Table: projects
create table projects (
  id uuid primary key default uuid_generate_v4(),
  slug text unique not null,
  name text not null,
  description text,
  domain text,
  status text not null default 'active', -- active, experimental, deprecated, archived
  repository text,
  tags text[],
  owners text[],
  sensitivity text default 'internal', -- public, internal, confidential, restricted
  canonical boolean default true,
  documentation text, -- path to canonical overview.md
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table projects is 'Project catalog derived from PROJECT_CATALOG.md';
comment on column projects.slug is 'Kebab-case identifier matching projects/<slug>/ folder name';

-- Table: documents
create table documents (
  id uuid primary key default uuid_generate_v4(),
  path text unique not null, -- repository-relative path
  title text not null,
  doc_type text not null, -- guide, reference, policy, etc.
  domain text,
  status text not null default 'draft',
  version text,
  owners text[],
  tags text[],
  sensitivity text default 'internal',
  last_updated date,
  audience text[], -- human, agent
  canonical boolean default false,
  citability text, -- full, excerpt-only, summary-only, restricted
  description text,
  content text, -- full raw markdown content
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table documents is 'Index of canonical documents in the knowledge pack';
create index idx_documents_status on documents(status);
create index idx_documents_doc_type on documents(doc_type);
create index idx_documents_domain on documents(domain);
create index idx_documents_canonical on documents(canonical) where canonical = true;
create index idx_documents_sensitivity on documents(sensitivity);

-- Table: document_chunks (for RAG/text search)
create table document_chunks (
  id uuid primary key default uuid_generate_v4(),
  document_id uuid references documents(id) on delete cascade not null,
  chunk_index integer not null,
  content text not null,
  metadata jsonb default '{}'::jsonb, -- includes section heading, chunk boundaries
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table document_chunks is 'Chunked content for semantic search';
create index idx_chunks_document_id on document_chunks(document_id);
-- Full-text search on content
create index idx_chunks_content_tsv on document_chunks using gin (to_tsvector('english', content));

-- Table: api_keys
create table api_keys (
  id uuid primary key default uuid_generate_v4(),
  key_hash text unique not null, -- SHA-256 hash of the API key
  name text,
  owner text,
  allowed_origin text,
  rate_limit_per_minute integer default 60,
  is_active boolean default true,
  first_used_at timestamp with time zone,
  last_used_at timestamp with time zone,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table api_keys is 'API keys for public REST API access';

-- Table: usage_events
create table usage_events (
  id uuid primary key default uuid_generate_v4(),
  api_key_id uuid references api_keys(id),
  endpoint text not null, -- e.g., '/v1/search'
  method text default 'GET',
  status_code integer,
  latency_ms integer,
  tokens_used integer,
  query_text text,
  client_ip inet,
  user_agent text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table usage_events is 'API usage audit log';
create index idx_usage_events_api_key on usage_events(api_key_id);
create index idx_usage_events_created on usage_events(created_at);

-- Table: mcp_sessions
create table mcp_sessions (
  id uuid primary key default uuid_generate_v4(),
  session_token text unique not null,
  client_id text not null,
  api_key_id uuid references api_keys(id),
  expires_at timestamp with time zone not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  last_accessed_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table mcp_sessions is 'MCP protocol sessions for agent connections';
create index idx_mcp_sessions_token on mcp_sessions(session_token);
create index idx_mcp_sessions_client on mcp_sessions(client_id);

-- Table: eval_runs (for retrieval quality evaluation)
create table eval_runs (
  id uuid primary key default uuid_generate_v4(),
  query text not null,
  expected_doc_ids uuid[],
  retrieved_doc_ids uuid[],
  scores float[],
  feedback text,
  run_by text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

comment on table eval_runs is 'Evaluation runs for retrieval quality and safety';

-- End of migration
