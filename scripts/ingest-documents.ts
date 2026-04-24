#!/usr/bin/env tsx
/**
 * ingest-documents.ts
 *
 * Ingests Markdown documents from the repository into the CapyMind database
 * (Supabase capymind.documents table). This script is idempotent — it upserts
 * documents by path.
 *
 * Environment variables:
 * - SUPABASE_URL: Supabase project URL
 * - SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY: API key
 *
 * If env vars are missing, the script performs a dry-run (prints what would be ingested).
 */

import 'dotenv/config'; // Load .env file
import { readdir, readFile, stat } from 'fs/promises';
import { join, relative, dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

interface DocMeta {
  id: string;
  path: string;
  title: string;
  doc_type?: string;
  domain?: string;
  status: string;
  version?: string;
  owners?: string[];
  tags?: string[];
  sensitivity?: string;
  last_updated?: string;
  audience?: string[];
  canonical?: boolean;
  citability?: string;
  description?: string;
}

// Attempt to load Supabase client if env is present
let supabase: any = null;
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

if (supabaseUrl && supabaseKey) {
  try {
    const { createClient } = await import('@supabase/supabase-js');
    supabase = createClient(supabaseUrl, supabaseKey);
    console.log('✅ Connected to Supabase:', supabaseUrl);
  } catch (e) {
    console.error('Failed to load Supabase client:', e);
    process.exit(1);
  }
} else {
  console.log('⚠️  SUPABASE_URL or key not set — running in DRY-RUN mode (no DB changes).');
}

async function walkDir(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      const name = entry.name.toLowerCase();
      if (['node_modules', '.git', 'dist', '.next', 'out', 'build', 'indexes', 'catalog'].includes(name)) continue;
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile() && fullPath.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

function deriveId(path: string): string {
  return path.replace(/\.md$/, '').replace(/\//g, '-');
}

async function extractMeta(filePath: string): Promise<DocMeta | null> {
  try {
    const content = await readFile(filePath, 'utf-8');
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n/);
    if (!frontmatterMatch) return null;
    const frontmatter: any = yaml.parse(frontmatterMatch[1]);
    const required = ['id', 'title', 'doc_type', 'status'];
    for (const r of required) {
      if (!frontmatter[r]) return null;
    }
    return {
      id: frontmatter.id || deriveId(relative(rootDir, filePath).replace(/\\/g, '/')),
      path: relative(rootDir, filePath).replace(/\\/g, '/'),
      title: frontmatter.title,
      doc_type: frontmatter.doc_type,
      domain: frontmatter.domain,
      status: frontmatter.status,
      version: frontmatter.version,
      owners: frontmatter.owners,
      tags: frontmatter.tags,
      sensitivity: frontmatter.sensitivity,
      last_updated: frontmatter.last_updated,
      audience: frontmatter.audience,
      canonical: frontmatter.canonical,
      citability: frontmatter.citability,
      description: frontmatter.description
    };
  } catch {
    return null;
  }
}

async function upsertDocument(meta: DocMeta, content: string) {
  if (supabase) {
    const { data, error } = await supabase
      .from('documents')
      .upsert(
        {
          path: meta.path,
          title: meta.title,
          doc_type: meta.doc_type,
          domain: meta.domain,
          status: meta.status,
          version: meta.version,
          owners: meta.owners,
          tags: meta.tags,
          sensitivity: meta.sensitivity,
          last_updated: meta.last_updated ? new Date(meta.last_updated) : null,
          audience: meta.audience,
          canonical: meta.canonical,
          citability: meta.citability,
          description: meta.description,
          content: content,
          updated_at: new Date()
        },
        { onConflict: 'path' }
      );
    if (error) {
      console.error(`❌ Failed upsert ${meta.path}:`, error.message);
      return false;
    }
    return true;
  } else {
    console.log(`[DRY-RUN] Would upsert document: ${meta.path} (${meta.doc_type})`);
    return true;
  }
}

async function main() {
  console.log('📥 Starting document ingestion...\n');

  const allMds = await walkDir(rootDir);
  console.log(`Found ${allMds.length} Markdown files.\n`);

  let ingested = 0;
  let skipped = 0;

  for (const filePath of allMds) {
    const meta = await extractMeta(filePath);
    if (!meta) {
      skipped++;
      continue;
    }
    const content = await readFile(filePath, 'utf-8');
    const ok = await upsertDocument(meta, content);
    if (ok) ingested++;
  }

  console.log(`\n✅ Ingested: ${ingested} documents.`);
  console.log(`⚠️  Skipped (no valid frontmatter): ${skipped} files.\n`);
}

main().catch((e) => {
  console.error('Ingestion failed:', e);
  process.exit(1);
});
