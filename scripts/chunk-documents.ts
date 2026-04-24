#!/usr/bin/env tsx
/**
 * chunk-documents.ts
 *
 * Processes ingested documents and creates text chunks for search.
 * Uses full-text search (no pgvector required).
 *
 * Environment:
 * - SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (required for DB access)
 */

import 'dotenv/config';
import { readFile } from 'fs/promises';
import { join, relative, dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

let supabase: any = null;
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required.');
  process.exit(1);
}

try {
  const { createClient } = await import('@supabase/supabase-js');
  supabase = createClient(supabaseUrl, supabaseKey);
  console.log('✅ Connected to Supabase:', supabaseUrl);
} catch (e) {
  console.error('Failed to load Supabase client:', e);
  process.exit(1);
}

interface DocumentRow {
  id: string;
  path: string;
  content: string;
}

interface Chunk {
  documentId: string;
  chunkIndex: number;
  content: string;
  section?: string;
  metadata: Record<string, any>;
}

/**
 * Simple chunker: splits by headings (#), then groups lines into blocks
 * of ~500 characters.
 */
function chunkMarkdown(body: string): Chunk[] {
  const lines = body.split('\n');
  const chunks: Chunk[] = [];
  let currentSection = '';
  let buffer = '';
  let chunkIndex = 0;

  const flush = (force = false) => {
    if (buffer.length > 500 || force) {
      chunks.push({
        documentId: '',
        chunkIndex: chunkIndex++,
        content: buffer.trim(),
        section: currentSection || undefined,
        metadata: {}
      });
      buffer = '';
    }
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (line.startsWith('#')) {
      flush();
      currentSection = line.replace(/^#+\s/, '');
      continue;
    }
    if (line.length === 0) {
      if (buffer.length > 0) buffer += '\n';
      continue;
    }
    const withSpace = buffer.length > 0 ? '\n' + line : line;
    if (buffer.length + withSpace.length > 800) {
      flush();
      buffer = line;
    } else {
      buffer += withSpace;
    }
  }
  flush(true);
  return chunks;
}

async function fetchDocuments(): Promise<DocumentRow[]> {
  const { data, error } = await supabase
    .from('documents')
    .select('id, path, content')
    .eq('status', 'active')
    .not('content', 'is', null);

  if (error) {
    throw new Error(`Failed to fetch documents: ${error.message}`);
  }
  return data || [];
}

async function upsertChunks(documentId: string, chunks: Chunk[]) {
  for (const chunk of chunks) {
    const { error } = await supabase.from('document_chunks').insert({
      document_id: documentId,
      chunk_index: chunk.chunkIndex,
      content: chunk.content,
      metadata: { section: chunk.section }
    } as any);
    if (error) {
      console.error(`❌ Chunk insert error for doc ${documentId} chunk ${chunk.chunkIndex}:`, error.message);
    }
  }
}

async function main() {
  console.log('📦 Chunking documents...\n');

  const documents = await fetchDocuments();
  console.log(`Fetched ${documents.length} documents.\n`);

  let totalChunks = 0;
  for (const doc of documents) {
    // Strip frontmatter to get body
    const contentMatch = doc.content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    const body = contentMatch ? contentMatch[2] : doc.content;
    const chunks = chunkMarkdown(body);
    for (const c of chunks) {
      c.documentId = doc.id;
    }
    await upsertChunks(doc.id, chunks);
    totalChunks += chunks.length;
    console.log(`  ✅ ${doc.path} → ${chunks.length} chunks`);
  }

  console.log(`\n🎉 Created ${totalChunks} chunks total.\n`);
}

main().catch((e) => {
  console.error('Chunking failed:', e);
  process.exit(1);
});
