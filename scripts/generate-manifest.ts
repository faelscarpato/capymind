#!/usr/bin/env tsx
/**
 * generate-manifest.ts
 *
 * Regenerates catalog/documents.json by scanning repository Markdown files
 * with valid document-meta frontmatter. Also updates catalog/projects.json if needed
 * (but projects are separately curated).
 */

import { readdir, readFile, stat, writeFile, mkdir } from 'fs/promises';
import { join, relative, resolve, dirname } from 'path';
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

interface Manifest {
  description: string;
  version: string;
  generated_at: string;
  documents: DocMeta[];
}

async function walkDir(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      const name = entry.name.toLowerCase();
      if (['node_modules', '.git', 'dist', '.next', 'out', 'build', 'indexes', 'catalog', 'schemas', 'ai/contracts'].includes(name)) continue;
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile() && fullPath.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

function deriveId(path: string): string {
  // projects/capyops-main/overview.md -> projects-capyops-main-overview
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

async function main() {
  console.log('📦 Generating catalog/documents.json manifest...\n');

  const allMds = await walkDir(rootDir);
  const documents: DocMeta[] = [];

  for (const filePath of allMds) {
    const meta = await extractMeta(filePath);
    if (meta) {
      documents.push(meta);
    }
  }

  // Sort by path
  documents.sort((a, b) => a.path.localeCompare(b.path));

  const manifest: Manifest = {
    description: "Auto-generated catalog of canonical documents in CapyMind.",
    version: "1.0.0",
    generated_at: new Date().toISOString(),
    documents
  };

  const outPath = join(rootDir, 'catalog', 'documents.json');
  await writeFile(outPath, JSON.stringify(manifest, null, 2));

  console.log(`✅ Manifest written: ${outPath} (${documents.length} documents)`);
}

main().catch((e) => {
  console.error('Manifest generation failed:', e);
  process.exit(1);
});
