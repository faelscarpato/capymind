#!/usr/bin/env tsx
/**
 * check-secrets.ts
 *
 * Scans repository files for potential secrets, API keys, passwords, tokens.
 * Uses simple pattern matching — not a substitute for dedicated secret scanners,
 * but provides basic hygiene.
 */

import { readdir, readFile } from 'fs/promises';
import { join, relative, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

interface Finding {
  file: string;
  line: number;
  type: string;
  snippet: string;
}

const findings: Finding[] = [];

// Common secret patterns (simplified)
const SECRET_PATTERNS = [
  { name: 'AWS Access Key', regex: /(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}/ },
  { name: 'AWS Secret Key', regex: /aws.{0,20}?['\"][0-9a-zA-Z\/+]{40}['\"]/i },
  { name: 'Generic API Key', regex: /(api[-_]?key|apikey|api[-_]?secret)['\"]?\s*[:=]\s*['"]?[0-9a-zA-Z_-]{20,}['"]?/i },
  { name: 'Bearer Token', regex: /bearer\s+[0-9a-zA-Z_-]{20,}/i },
  { name: 'Private Key', regex: /-----BEGIN [A-Z ]+ PRIVATE KEY-----/ },
  { name: 'GitHub Token', regex: /(?:ghp|gho|ghu|ghs|ghr)_[0-9a-zA-Z]{36}/ },
  { name: 'Google API Key', regex: /AIza[0-9A-Za-z_-]{35}/ },
  { name: 'Slack Token', regex: /xox[baprs]-([0-9a-zA-Z]{10,48})/ },
  { name: 'JWT Token', regex: /eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*/ },
  { name: 'Password in config', regex: /(?:password|passwd|pwd)\s*[:=]\s*['"][^'"]{5,}['"]/i },
  { name: 'Connection string', regex: /(?:mongodb|postgres|mysql|redis):\/\/[^\s]+/i },
  { name: 'Secret generic', regex: /(?:secret|token|key)['\"]?\s*[:=]\s*['"][^'"]{8,}['"]/i }
];

async function scanFile(filePath: string) {
  const relPath = relative(rootDir, filePath).replace(/\\/g, '/');

  // Skip binary files, node_modules, .git
  if (/node_modules|\.git|dist|\.next|out|build/.test(relPath)) return;
  if (!filePath.endsWith('.md') && !filePath.endsWith('.json') && !filePath.endsWith('.ts') && !filePath.endsWith('.js') && !filePath.endsWith('.env')) {
    return;
  }

  try {
    const content = await readFile(filePath, 'utf-8');
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      for (const pattern of SECRET_PATTERNS) {
        if (pattern.regex.test(line)) {
          // Skip obvious placeholders and examples
          const placeholderPatterns = [
            /your[-_]\w+/i,
            /<[^>]+>/,
            /example/i,
            /xxx+/i,
            /REDACTED/i,
            /YOUR_[A-Z_]+/,
            /\[.*\]/  // bracketed placeholders
          ];
          const isPlaceholder = placeholderPatterns.some(p => p.test(line));
          if (isPlaceholder) break; // ignore this match

          findings.push({
            file: relPath,
            line: i + 1,
            type: pattern.name,
            snippet: line.trim().substring(0, 100)
          });
          break; // one finding per line is enough
        }
      }
    }
  } catch (e) {
    // ignore
  }
}

async function walkDir(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkDir(fullPath));
    } else if (entry.isFile()) {
      files.push(fullPath);
    }
  }
  return files;
}

async function main() {
  console.log('🔍 Scanning for potential secrets...\n');

  const allFiles = await walkDir(rootDir);

  for (let i = 0; i < allFiles.length; i++) {
    await scanFile(allFiles[i]);
  }

  console.log(`✅ Scanned ${allFiles.length} files.\n`);

  if (findings.length > 0) {
    console.log(`❌ Potential secrets found (${findings.length}):\n`);
    for (const f of findings) {
      console.log(`  ${f.file}:${f.line} [${f.type}] → ${f.snippet}`);
    }
    process.exit(1);
  } else {
    console.log('🎉 No secrets detected.\n');
  }
}

main().catch((e) => {
  console.error('Secret scan failed:', e);
  process.exit(1);
});
