#!/usr/bin/env tsx
/**
 * check-links.ts
 *
 * Scans all Markdown files for internal links (file:// or relative paths) and verifies
 * that the target file exists in the repository.
 */

import { readdir, readFile, stat } from 'fs/promises';
import { join, relative, resolve, dirname, isAbsolute } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

interface LinkCheck {
  file: string;
  line: number;
  target: string;
  ok: boolean;
}

const issues: LinkCheck[] = [];
const checked = new Set<string>();

function isInternalLink(link: string): boolean {
  // Exclude http[s]:// and mailto: etc.
  if (/^https?:\/\//i.test(link)) return false;
  if (/^mailto:/i.test(link)) return false;
  if (/^#/.test(link)) return false; // anchor only, same file
  return true;
}

async function fileExists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function walkDir(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      const name = entry.name.toLowerCase();
      if (['node_modules', '.git', 'dist', '.next', 'out', 'build'].includes(name)) continue;
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile() && fullPath.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

function extractLinks(content: string): string[] {
  // Match markdown links: [text](path)
  const mdLinkRegex = /\[[^\]]*\]\(([^)]+)\)/g;
  const links: string[] = [];
  let match;
  while ((match = mdLinkRegex.exec(content)) !== null) {
    const target = match[1].split('#')[0]; // drop anchor
    if (target && isInternalLink(target)) {
      links.push(target);
    }
  }
  return links;
}

async function checkFile(filePath: string) {
  const relPath = relative(rootDir, filePath).replace(/\\/g, '/');
  try {
    const content = await readFile(filePath, 'utf-8');
    const lines = content.split('\n');
    const links = extractLinks(content);

    for (const rawLink of links) {
      let targetPath = rawLink;
      // Resolve relative to file's directory
      const fileDir = dirname(filePath);
      let fullTarget = join(fileDir, targetPath);
      // Normalize
      fullTarget = resolve(fullTarget);

      // Check if exists
      const exists = await fileExists(fullTarget);
      if (!exists) {
        // Find line number
        const lineNum = content.substring(0, content.indexOf(rawLink)).split('\n').length;
        issues.push({ file: relPath, line: lineNum, target: rawLink, ok: false });
      }
    }
  } catch (e) {
    // ignore
  }
}

async function main() {
  console.log('🔗 Checking internal links in Markdown...\n');

  const allMds = await walkDir(rootDir);

  // Process files in parallel but limited
  const BATCH = 20;
  for (let i = 0; i < allMds.length; i += BATCH) {
    const batch = allMds.slice(i, i + BATCH);
    await Promise.all(batch.map(checkFile));
  }

  console.log(`✅ Scanned ${allMds.length} files.\n`);

  if (issues.length > 0) {
    console.log(`❌ Broken internal links found (${issues.length}):\n`);
    for (const issue of issues) {
      console.log(`  ${issue.file}:${issue.line} → ${issue.target}`);
    }
    process.exit(1);
  } else {
    console.log('🎉 No broken internal links.\n');
  }
}

main().catch((e) => {
  console.error('Link check failed:', e);
  process.exit(1);
});
