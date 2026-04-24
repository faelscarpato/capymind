#!/usr/bin/env tsx
/**
 * build-index.ts
 *
 * Builds a searchable index JSON from all Markdown documents in the repository
 * that have valid frontmatter. Output: indexes/search-index.jsonl (line-delimited JSON)
 */

import { readdir, readFile, stat, mkdir, writeFile } from 'fs/promises';
import { join, relative, resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

interface IndexEntry {
  id: string;
  path: string;
  title: string;
  doc_type?: string;
  domain?: string;
  status: string;
  sensitivity?: string;
  tags?: string[];
  excerpt: string;
  last_updated?: string;
}

async function walkDir(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      // skip node_modules, .git, dist, etc.
      const name = entry.name.toLowerCase();
      if (['node_modules', '.git', 'dist', '.next', 'out', 'build'].includes(name)) continue;
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile() && fullPath.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

function extractExcerpt(content: string, maxLen = 200): string {
  // Remove frontmatter
  const withoutFrontmatter = content.replace(/^---\n[\s\S]*?\n---\n/, '');
  // Remove headings, code blocks, HTML tags
  const plain = withoutFrontmatter
    .replace(/#{1,6}\s/g, '')
    .replace(/`{3}[\s\S]*?`{3}/g, '')
    .replace(/<[^>]+>/g, '')
    .replace(/\n+/g, ' ')
    .trim();
  if (plain.length <= maxLen) return plain;
  return plain.substring(0, maxLen).replace(/\s+\S*$/, '') + '…';
}

async function main() {
  const outDir = join(rootDir, 'indexes');
  await mkdir(outDir, { recursive: true });
  const outPath = join(outDir, 'search-index.jsonl');

  const allMds = await walkDir(rootDir);
  const entries: IndexEntry[] = [];

  for (const fullPath of allMds) {
    const relPath = relative(rootDir, fullPath).replace(/\\/g, '/');

    try {
      const content = await readFile(fullPath, 'utf-8');
      const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n/);
      let frontmatter: any = {};

      if (frontmatterMatch) {
        try {
          frontmatter = yaml.parse(frontmatterMatch[1]);
        } catch (e) {
          // skip invalid frontmatter
          continue;
        }
      } else {
        // Require frontmatter for indexing
        continue;
      }

      const { id, title, doc_type, domain, status, sensitivity, tags, last_updated } = frontmatter;
      if (!id || !title || !status) {
        // skip incomplete metadata
        continue;
      }

      const excerpt = extractExcerpt(content);

      entries.push({
        id: relPath.replace(/\.md$/, '').replace(/\//g, '-'),
        path: relPath,
        title,
        doc_type,
        domain,
        status,
        sensitivity,
        tags,
        excerpt,
        last_updated
      });

    } catch (e) {
      // skip unreadable
    }
  }

  // Write JSONL
  const lines = entries.map(e => JSON.stringify(e));
  await writeFile(outPath, lines.join('\n') + '\n');

  console.log(`📦 Index built: ${outPath} (${entries.length} entries)`);
}

main().catch((e) => {
  console.error('Index build failed:', e);
  process.exit(1);
});
