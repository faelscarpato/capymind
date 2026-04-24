/**
 * capymind-api Edge Function
 *
 * Public REST API for CapyMind knowledge pack.
 *
 * Endpoints:
 *   GET  /v1/health
 *   GET  /v1/projects
 *   GET  /v1/projects/:slug
 *   GET  /v1/documents/:id
 *   POST /v1/search          -> search-result schema
 *   POST /v1/context-pack    -> context-pack schema
 *   GET  /v1/llms.txt        -> plain text index
 *   GET  /openapi.json       -> OpenAPI spec
 *
 * Authentication: Bearer token (API key) or x-api-key header for public endpoints.
 * Rate limiting: basic in-memory per key (restart resets).
 */

import { serve } from 'https://deno.land/std@0.170.0/http/server.ts';
import { createClient } from 'npm:@supabase/supabase-js@2';
import { define, validate } from 'npm:zod@3';
import { json } from 'https://deno.land/std@0.170.0/http/mod.ts';

const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const supabase = createClient(supabaseUrl, supabaseServiceKey);

// Simple in-memory rate limiter: key -> {count, reset}
const rateLimits = new Map<string, { count: number; reset: number }>();

const RATE_LIMIT = 120; // requests per minute
const RATE_WINDOW = 60 * 1000; // 1 minute

interface Request {
  method: string;
  url: URL;
  headers: Headers;
  body?: any;
}

function unauthorized(message = 'Unauthorized'): Response {
  return new Response(JSON.stringify({ error: message }), {
    status: 401,
    headers: { 'Content-Type': 'application/json' }
  });
}

function forbidden(message = 'Forbidden'): Response {
  return new Response(JSON.stringify({ error: message }), {
    status: 403,
    headers: { 'Content-Type': 'application/json' }
  });
}

function notFound(message = 'Not found'): Response {
  return new Response(JSON.stringify({ error: message }), {
    status: 404,
    headers: { 'Content-Type': 'application/json' }
  });
}

function errorResponse(message: string, status = 500): Response {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

// --- Authentication Middleware ---
async function authenticate(req: Request): Promise<string | null> {
  const authHeader = req.headers.get('authorization');
  const apiKeyHeader = req.headers.get('x-api-key');

  let token: string | null = null;
  if (authHeader?.startsWith('Bearer ')) {
    token = authHeader.slice(7);
  } else if (apiKeyHeader) {
    token = apiKeyHeader;
  }

  if (!token) return null;

  // Simple hash (SHA-256) of token? We stored key_hash in DB.
  // For demo, we'll query plain but in production store hash.
  const { data, error } = await supabase
    .from('api_keys')
    .select('id, key_hash, is_active')
    .eq('key_hash', token) // In real life, compare hash; for demo assume token stored as plain
    .single();

  if (error || !data || !data.is_active) {
    return null;
  }

  // Update last_used
  await supabase.from('api_keys').update({ last_used_at: new Date().toISOString() }).eq('id', data.id);

  return data.id; // api_key id
}

// --- Rate Limiting ---
function checkRateLimit(apiKeyId: string): boolean {
  const now = Date.now();
  const record = rateLimits.get(apiKeyId);
  if (!record || now > record.reset) {
    rateLimits.set(apiKeyId, { count: 1, reset: now + RATE_WINDOW });
    return true;
  }
  if (record.count >= RATE_LIMIT) {
    return false;
  }
  record.count++;
  return true;
}

// --- Handlers ---

async function handleHealth() {
  return new Response(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
}

async function handleProjects(req: Request) {
  const { data, error } = await supabase.from('projects').select('*').eq('status', 'active').order('name');
  if (error) return errorResponse(error.message);
  return json(data || []);
}

async function handleProjectBySlug(req: Request, slug: string) {
  const { data, error } = await supabase.from('projects').select('*').eq('slug', slug).single();
  if (error) return notFound('Project not found');
  return json(data);
}

async function handleDocumentById(req: Request, id: string) {
  const { data, error } = await supabase.from('documents').select('*').eq('id', id).single();
  if (error) return notFound('Document not found');
  // Filter sensitive fields based on audience? For now, return all.
  return json(data);
}

async function handleSearch(req: Request) {
  let body: any;
  try {
    body = await req.json?.();
  } catch {
    return errorResponse('Invalid JSON', 400);
  }
  const query = (body?.query || '').trim();
  const limit = Math.min(body?.limit || 10, 50);
  const offset = body?.offset || 0;

  if (!query) return errorResponse('Query is required', 400);

  // Simple full-text search using Supabase textSearch on title + tags + path
  const { data, error } = await supabase
    .from('documents')
    .select('id, path, title, doc_type, status, sensitivity, canonical, tags')
    .textSearch('title', `'${query}'`, { config: 'english', typeof: 'websearch' })
    .or(`title.ilike.%${query}%,tags.cs.{${query}}`)
    .eq('status', 'active')
    .limit(limit)
    .range(offset, offset + limit - 1);

  if (error) return errorResponse(error.message);

  // Build response per search-result.schema.json
  const results: any[] = (data || []).map((row: any) => ({
    path: row.path,
    score: 1.0, // simplistic
    title: row.title,
    doc_type: row.doc_type,
    status: row.status,
    sensitivity: row.sensitivity,
    canonical: row.canonical,
    tags: row.tags
  }));

  return json({ query, total: data?.length || 0, limit, offset, results });
}

async function handleContextPack(req: Request) {
  let body: any;
  try {
    body = await req.json?.();
  } catch {
    return errorResponse('Invalid JSON', 400);
  }
  const query = (body?.query || '').trim();
  const limit = Math.min(body?.limit || 5, 20);

  if (!query) return errorResponse('Query is required', 400);

  // Retrieve matching document chunks (top chunks)
  // For now, fetch documents matching query, then their chunks (first few)
  const { data: docs, error } = await supabase
    .from('documents')
    .select('id, path, title, doc_type, status, sensitivity, canonical')
    .textSearch('title', `'${query}'`, { config: 'english', typeof: 'websearch' })
    .or(`title.ilike.%${query}%`)
    .eq('status', 'active')
    .limit(limit);

  if (error) return errorResponse(error.message);

  const sources: any[] = [];
  for (const doc of docs || []) {
    const { data: chunks } = await supabase
      .from('document_chunks')
      .select('content, chunk_index, metadata')
      .eq('document_id', doc.id)
      .limit(3); // first few chunks

    for (const chunk of chunks || []) {
      sources.push({
        path: doc.path,
        chunk_index: chunk.chunk_index,
        score: 1.0,
        text: chunk.content,
        metadata: chunk.metadata
      });
    }
  }

  return json({
    query,
    pack_version: '1.0.0',
    generated_at: new Date().toISOString(),
    summary: `Retrieved ${sources.length} chunks from ${docs?.length} documents.`,
    sources,
    notes: 'MVP context pack — no ranking or embeddings applied.'
  });
}

async function handleLlmsTxt(req: Request) {
  // Try to read from filesystem first; fallback to DB document path=llms.txt
  try {
    const filePath = new URL('../../llms.txt', import.meta.url);
    const content = await Deno.readTextFile(filePath);
    return new Response(content, {
      status: 200,
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    });
  } catch (e) {
    // fallback to DB
    const { data } = await supabase.from('documents').select('content').eq('path', 'llms.txt').single() as any;
    if (data?.content) {
      return new Response(data.content, {
         status: 200,
         headers: { 'Content-Type': 'text/plain; charset=utf-8' }
      });
    }
    return notFound('llms.txt not found');
  }
}

async function handleOpenAPISpec(req: Request) {
  const spec = {
    openapi: '3.0.0',
    info: { title: 'CapyMind API', version: '1.0.0' },
    paths: {
      '/v1/health': { get: { summary: 'Health check', responses: { '200': { description: 'OK' } } } },
      '/v1/projects': { get: { summary: 'List projects', responses: { '200': { description: 'List' } } } },
      '/v1/projects/{slug}': { get: { summary: 'Get project by slug', responses: { '200': {}, '404': {} } } },
      '/v1/documents/{id}': { get: { summary: 'Get document by id', responses: { '200': {}, '404': {} } } },
      '/v1/search': { post: { summary: 'Search documents', requestBody: { content: { 'application/json': { schema: { type: 'object', properties: { query: { type: 'string' } } } } } }, responses: { '200': { description: 'Search results' } } } },
      '/v1/context-pack': { post: { summary: 'Build context pack', requestBody: { content: { 'application/json': { schema: { type: 'object', properties: { query: { type: 'string' }, limit: { type: 'integer' } } } } } }, responses: { '200': {} } } },
      '/v1/llms.txt': { get: { summary: 'Public index', responses: { '200': { description: 'text/plain' } } } }
    }
  };
  return json(spec);
}

// --- Main Request Handler ---

async function handler(req: Request): Promise<Response> {
  const now = Date.now();

  try {
    const url = new URL((req as any).url || (req as any).request?.url || '');
    const path = url.pathname;

    // CORS preflight
    if ((req as any).method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
          'Access-Control-Allow-Headers': 'authorization,x-api-key,content-type'
        }
      });
    }

    const method = (req as any).method;

    // Public endpoints (no auth)
    if (path === '/v1/health' && method === 'GET') {
      return handleHealth();
    }
    if (path === '/openapi.json' && method === 'GET') {
      return handleOpenAPISpec(req);
    }
    if (path === '/v1/llms.txt' && method === 'GET') {
      return handleLlmsTxt(req);
    }

    // Protected endpoints require API key auth
    const apiKeyId = await authenticate(req);
    if (!apiKeyId) {
      return unauthorized();
    }

    // Rate limit per API key
    if (!checkRateLimit(apiKeyId)) {
      return new Response(JSON.stringify({ error: 'Rate limit exceeded' }), {
        status: 429,
        headers: { 'Content-Type': 'application/json', 'Retry-After': '60' }
      });
    }

    // Log usage event (fire and forget)
    supabase.from('usage_events').insert({
      api_key_id: apiKeyId,
      endpoint: path,
      method: method,
      created_at: new Date().toISOString()
    }).catch(() => {});

    // Routing
    if (path === '/v1/projects' && method === 'GET') {
      return handleProjects(req);
    }
    if (path.startsWith('/v1/projects/') && method === 'GET') {
      const slug = path.split('/')[3];
      return handleProjectBySlug(req, slug);
    }
    if (path === '/v1/search' && method === 'POST') {
      return handleSearch(req);
    }
    if (path === '/v1/context-pack' && method === 'POST') {
      return handleContextPack(req);
    }
    if (path.startsWith('/v1/documents/') && method === 'GET') {
      const id = path.split('/')[3];
      return handleDocumentById(req, id);
    }

    return notFound('Endpoint not found');
  } catch (e) {
    console.error(e);
    return errorResponse('Internal server error');
  }
}

console.log('🚀 CapyMind API started');
serve(handler as any);
