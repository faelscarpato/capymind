/**
 * MCP Server Edge Function
 *
 * Implements Model Context Protocol (JSON-RPC 2.0 over HTTP) for CapyMind.
 *
 * Tools provided:
 *   - search_knowledge
 *   - get_project_context
 *   - build_context_pack
 *   - resolve_citation
 *   - get_policy
 *
 * Authentication: Bearer token (same API keys as REST API).
 *
 * Reference: https://github.com/modelcontextprotocol/spec
 */

import { serve } from 'https://deno.land/std@0.170.0/http/server.ts';
import { createClient } from 'npm:@supabase/supabase-js@2';

const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const supabase = createClient(supabaseUrl, supabaseKey);

interface RpcRequest {
  jsonrpc: '2.0';
  id?: number | string | null;
  method: string;
  params?: any;
}

interface RpcResponse {
  jsonrpc: '2.0';
  id: number | string | null;
  result?: any;
  error?: { code: number; message: string; data?: any };
}

function jsonResponse(obj: any): Response {
  return new Response(JSON.stringify(obj), {
    headers: { 'Content-Type': 'application/json' }
  });
}

function errorResponse(code: number, message: string, id: number | string | null): RpcResponse {
  return { jsonrpc: '2.0', id, error: { code, message } };
}

// ---- Tool implementations ----

async function search_knowledge(params: any): Promise<any> {
  const { query, limit = 10 } = params;
  const { data, error } = await supabase
    .from('documents')
    .select('id, path, title, doc_type, status, sensitivity, canonical, tags')
    .textSearch('title', `'${query}'`, { config: 'english', typeof: 'websearch' })
    .or(`title.ilike.%${query}%`)
    .eq('status', 'active')
    .limit(limit);

  if (error) throw error;
  return { results: data || [] };
}

async function get_project_context(params: any): Promise<any> {
  const { slug } = params;
  if (!slug) throw { code: -32602, message: 'slug required' };

  const { data: project, error } = await supabase.from('projects').select('*').eq('slug', slug).single();
  if (error) throw { code: -32000, message: 'Project not found' };

  // Also get related overview document if available
  const { data: doc } = await supabase
    .from('documents')
    .select('content')
    .eq('path', `projects/${slug}/overview.md`)
    .single();
  return { project, overview: doc?.content };
}

async function build_context_pack(params: any): Promise<any> {
  const { query, limit = 5 } = params;
  const { data: docs } = await supabase
    .from('documents')
    .select('id, path, title, content')
    .textSearch('title', `'${query}'`, { config: 'english' })
    .eq('status', 'active')
    .limit(limit);

  const sources: any[] = [];
  for (const doc of docs || []) {
    // Basic extraction: return first 500 chars of content
    const snippet = doc.content?.replace(/^---\n[\s\S]*?\n---\n/, '').substring(0, 500);
    sources.push({ path: doc.path, title: doc.title, snippet });
  }
  return { query, sources, generated_at: new Date().toISOString() };
}

async function resolve_citation(params: any): Promise<any> {
  const { document_id, section } = params;
  const { data, error } = await supabase
    .from('documents')
    .select('path, title, content')
    .eq('id', document_id)
    .single();
  if (error || !data) throw { code: -32000, message: 'Document not found' };
  return { document: { path: data.path, title: data.title, section } };
}

async function get_policy(params: any): Promise<any> {
  const { policy_name } = params;
  if (!policy_name) throw { code: -32602, message: 'policy_name required' };
  // Map common policy names to docs paths
  const mapping: Record<string, string> = {
    'anti-prompt-injection': 'ai/policies/anti-prompt-injection.md',
    'retrieval-safety': 'ai/policies/retrieval-safety.md',
    'security': 'docs/governance/security-policy.md',
    'citation': 'docs/reference/citation-policy.md',
    'taxonomy': 'docs/reference/taxonomy.md'
  };
  const path = mapping[policy_name];
  if (!path) throw { code: -32000, message: 'Unknown policy' };

  const { data, error } = await supabase.from('documents').select('content').eq('path', path).single();
  if (error) throw { code: -32000, message: 'Policy not found' };
  return { policy: policy_name, path, content: data.content };
}

// ---- Auth middleware for MCP ----
async function authenticate(req: Request): Promise<boolean> {
  const auth = req.headers.get('authorization') || req.headers.get('x-api-key');
  if (!auth) return false;
  const token = auth.replace('Bearer ', '');
  // Simplified: just check that key exists in api_keys
  const { data } = await supabase
    .from('api_keys')
    .select('id')
    .eq('key_hash', token)
    .eq('is_active', true)
    .limit(1);
  return !!data && data.length > 0;
}

// ---- Main handler ----
async function handler(req: Request): Promise<Response> {
  // Only accept POST
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Authenticate
  const ok = await authenticate(req);
  if (!ok) {
    return jsonResponse(errorResponse(-32000, 'Unauthorized', null));
  }

  let body: any;
  try {
    body = await req.json();
  } catch {
    return jsonResponse(errorResponse(-32700, 'Parse error', null));
  }

  const rpcReq: RpcRequest = body;

  // Prepare response template
  const response: RpcResponse = {
    jsonrpc: '2.0',
    id: rpcReq.id
  };

  try {
    // Only support `initialize` and `initialized` notification as per MCP spec minimally
    if (rpcReq.method === 'initialize') {
      response.result = {
        capabilities: { tools: {} },
        serverInfo: { name: 'capymind-mcp', version: '1.0.0' }
      };
    } else if (rpcReq.method === 'tools/list') {
      response.result = {
        tools: [
          {
            name: 'search_knowledge',
            description: 'Search knowledge base',
            inputSchema: {
              type: 'object',
              properties: { query: { type: 'string' }, limit: { type: 'integer' } }
            }
          },
          {
            name: 'get_project_context',
            description: 'Get project overview and metadata',
            inputSchema: {
              type: 'object',
              properties: { slug: { type: 'string' } }
            }
          },
          {
            name: 'build_context_pack',
            description: 'Retrieve chunks and build context pack',
            inputSchema: {
              type: 'object',
              properties: { query: { type: 'string' }, limit: { type: 'integer' } }
            }
          },
          {
            name: 'resolve_citation',
            description: 'Fetch full document excerpt for citation',
            inputSchema: {
              type: 'object',
              properties: { document_id: { type: 'string' }, section: { type: 'string' } }
            }
          },
          {
            name: 'get_policy',
            description: 'Get policy document by name',
            inputSchema: {
              type: 'object',
              properties: { policy_name: { type: 'string' } }
            }
          }
        ]
      };
    } else if (rpcReq.method === 'tools/call') {
      const { name, arguments: args } = rpcReq.params || {};
      let result: any;
      switch (name) {
        case 'search_knowledge':
          result = await search_knowledge(args);
          break;
        case 'get_project_context':
          result = await get_project_context(args);
          break;
        case 'build_context_pack':
          result = await build_context_pack(args);
          break;
        case 'resolve_citation':
          result = await resolve_citation(args);
          break;
        case 'get_policy':
          result = await get_policy(args);
          break;
        default:
          throw { code: -32601, message: 'Method not found' };
      }
      response.result = { content: [{ type: 'text', text: JSON.stringify(result) }] };
    } else if (rpcReq.method === 'ping' || rpcReq.method === 'mcp.ping') {
      response.result = { pong: true };
    } else {
      throw { code: -32601, message: 'Method not found' };
    }
  } catch (e: any) {
    response.error = {
      code: e.code || -32603,
      message: e.message || 'Internal error',
      data: e
    };
  }

  return jsonResponse(response);
}

console.log('🚀 CapyMind MCP server started');
serve(handler);
