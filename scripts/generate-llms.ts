#!/usr/bin/env tsx
/**
 * generate-llms.ts
 *
 * Generates llms.txt and llms-full.txt from the current repository structure
 * and document index. Respects existing format and ordering heuristics.
 */

import { readFile, writeFile, mkdir } from 'fs/promises';
import { join, relative, resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import yaml from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

interface DocMeta {
  title?: string;
  doc_type?: string;
  status?: string;
  sensitivity?: string;
  tags?: string[];
}

interface IndexEntry {
  id: string;
  path: string;
  title: string;
  doc_type?: string;
  domain?: string;
  status: string;
  sensitivity?: string;
  tags?: string[];
  excerpt?: string;
}

const LLMS_HEADER = `# CapyMind
> Base de conhecimento leve do ecossistema Capy, preparada para MCP, IA, automações e navegação humana.

Este repositório contém documentação derivada, índices, resumos de projetos, prompts, datasets descritos e referências. Ele **não** contém cópias integrais dos projetos-fonte.

## Start here
- [README.md](./README.md): visão geral do repositório.
- [MCP_GUIDE.md](./MCP_GUIDE.md): como navegar este acervo com IA.
- [KNOWLEDGE_MAP.md](./KNOWLEDGE_MAP.md): mapa principal das áreas do repositório.
- [REPO_RULES.md](./REPO_RULES.md): o que entra e o que não entra.

## Core knowledge
- [knowledge/technical/capy-ecosystem-overview.md](./knowledge/technical/capy-ecosystem-overview.md): panorama técnico do ecossistema Capy.
- [knowledge/operations/capy-ops-and-ml-workflows.md](./knowledge/operations/capy-ops-and-ml-workflows.md): fluxos operacionais e sinais do CapyOps.
- [knowledge/business/mercado-livre-operations.md](./knowledge/business/mercado-livre-operations.md): operação comercial e Mercado Livre.
- [knowledge/products/petala-decor-catalog-notes.md](./knowledge/products/petala-decor-catalog-notes.md): catálogo e contexto de produto da Pétala Decor.
- [knowledge/ai/prompt-engineering-notes.md](./knowledge/ai/prompt-engineering-notes.md): notas centrais sobre prompts e fluxos de IA.

## Featured projects
- [projects/_featured.md](./projects/_featured.md): seleção rápida dos projetos prioritários.
- [PROJECT_CATALOG.md](./PROJECT_CATALOG.md): catálogo completo dos projetos detectados.

## Collections
- [prompts/_index.md](./prompts/_index.md): prompts catalogados.
- [datasets/_index.md](./datasets/_index.md): bases descritas e candidatas.
- [docs/_index.md](./docs/_index.md): notas arquiteturais, sistêmicas e de UX.
- [references/_index.md](./references/_index.md): referências técnicas, comerciais, contratos e materiais externos.
- [assets/_index.md](./assets/_index.md): catálogos e notas de ativos visuais.

## Guidance
- Para perguntas sobre um projeto específico, abra a pasta em \`projects/<slug>/\` e leia \`overview.md\`, \`stack.md\`, \`architecture.md\` e \`integrations.md\`.
- Para perguntas sobre operação, priorize \`knowledge/business\`, \`knowledge/operations\`, \`datasets\` e \`references/commercial\`.
- Para perguntas sobre IA, priorize \`knowledge/ai\`, \`prompts\` e \`references/technical\`.
- Para rastreabilidade, use \`source-path.md\` em cada projeto.

## Full index
- [llms-full.txt](./llms-full.txt): versão expandida do índice para navegação mais ampla.
`;

function categorizeEntry(entry: IndexEntry): string {
  const type = entry.doc_type || 'doc';
  const domain = entry.domain || 'general';
  return `${domain}/${type}`;
}

function rankingKey(entry: IndexEntry): number {
  // Lower numbers rank higher
  const statusOrder: Record<string, number> = {
    'active': 0,
    'draft': 2,
    'deprecated': 4,
    'archived': 5
  };
  const status = statusOrder[entry.status] ?? 3;
  const typeBonus = ['reference', 'policy', 'guide'].includes(entry.doc_type || '') ? 0 : 1;
  return status + typeBonus;
}

async function loadIndex(): Promise<IndexEntry[]> {
  const indexPath = join(rootDir, 'indexes', 'search-index.jsonl');
  try {
    const content = await readFile(indexPath, 'utf-8');
    const lines = content.trim().split('\n');
    return lines.map(l => JSON.parse(l) as IndexEntry).filter(e => e.status === 'active');
  } catch {
    return [];
  }
}

async function generateLlmsTxt(entries: IndexEntry[]): Promise<string> {
  const lines: string[] = [];
  lines.push('# CapyMind');
  lines.push('> Base de conhecimento leve do ecossistema Capy, preparada para MCP, IA, automações e navegação humana.');
  lines.push('');
  lines.push('Este repositório contém documentação derivada, índices, resumos de projetos, prompts, datasets descritos e referências. Ele **não** contém cópias integrais dos projetos-fonte.');
  lines.push('');
  lines.push('## Start here');
  lines.push('- [README.md](./README.md): visão geral do repositório.');
  lines.push('- [MCP_GUIDE.md](./MCP_GUIDE.md): como navegar este acervo com IA.');
  lines.push('- [KNOWLEDGE_MAP.md](./KNOWLEDGE_MAP.md): mapa principal das áreas do repositório.');
  lines.push('- [REPO_RULES.md](./REPO_RULES.md): o que entra e o que não entra.');
  lines.push('');
  lines.push('## Core knowledge');

  const coreEntries = entries.filter(e =>
    ['knowledge/technical/capy-ecosystem-overview.md',
     'knowledge/operations/capy-ops-and-ml-workflows.md',
     'knowledge/business/mercado-livre-operations.md',
     'knowledge/products/petala-decor-catalog-notes.md',
     'knowledge/ai/prompt-engineering-notes.md']
      .includes(e.path)
  );
  for (const e of coreEntries) {
    lines.push(`- [${e.path}](${e.path}): ${e.title}`);
  }
  lines.push('');
  lines.push('## Featured projects');
  lines.push('- [projects/_featured.md](./projects/_featured.md): seleção rápida dos projetos prioritários.');
  lines.push('- [PROJECT_CATALOG.md](./PROJECT_CATALOG.md): catálogo completo dos projetos detectados.');
  lines.push('');
  lines.push('## Collections');
  const collections = [
    'prompts/_index.md',
    'datasets/_index.md',
    'docs/_index.md',
    'references/_index.md',
    'assets/_index.md'
  ];
  for (const path of collections) {
    const e = entries.find(en => en.path === path);
    if (e) lines.push(`- [${path}](${path}): ${e.title}`);
  }
  lines.push('');
  lines.push('## Guidance');
  lines.push('- Para perguntas sobre um projeto específico, abra a pasta em `projects/<slug>/` e leia `overview.md`, `stack.md`, `architecture.md` e `integrations.md`.');
  lines.push('- Para perguntas sobre operação, priorize `knowledge/business`, `knowledge/operations`, `datasets` e `references/commercial`.');
  lines.push('- Para perguntas sobre IA, priorize `knowledge/ai`, `prompts` e `references/technical`.');
  lines.push('- Para rastreabilidade, use `source-path.md` em cada projeto.');
  lines.push('');
  lines.push('## Full index');
  lines.push('- [llms-full.txt](./llms-full.txt): versão expandida do índice para navegação mais ampla.');
  return lines.join('\n');
}

async function generateLlmsFullTxt(entries: IndexEntry[]): Promise<string> {
  const lines: string[] = [];
  lines.push('# CapyMind — Full Index');
  lines.push('> índice expandido de todos os documentos ativos');
  lines.push('');

  // Group by doc_type
  const groups: Record<string, IndexEntry[]> = {};
  for (const e of entries) {
    const type = e.doc_type || 'misc';
    if (!groups[type]) groups[type] = [];
    groups[type].push(e);
  }

  for (const type of Object.keys(groups).sort()) {
    lines.push(`## ${type.charAt(0).toUpperCase() + type.slice(1)}`);
    lines.push('');
    const sorted = groups[type].sort((a,b) => rankingKey(a) - rankingKey(b));
    for (const e of sorted) {
      lines.push(`- [${e.title}](${e.path}) — ${e.excerpt?.substring(0,80) || ''}`);
    }
    lines.push('');
  }
  return lines.join('\n');
}

async function main() {
  console.log('📄 Generating llms.txt and llms-full.txt...\n');

  const entries = await loadIndex();

  if (entries.length === 0) {
    console.warn('Warning: index is empty; running build-index first...');
    // We could spawn build-index but for now just exit
    console.error('❌ No index entries. Run npm run build:index first.');
    process.exit(1);
  }

  const indexesDir = join(rootDir, 'indexes');
  await mkdir(indexesDir, { recursive: true });

  const llmsTxt = await generateLlmsTxt(entries);
  await writeFile(join(rootDir, 'llms.txt'), llmsTxt);

  const llmsFullTxt = await generateLlmsFullTxt(entries);
  await writeFile(join(rootDir, 'llms-full.txt'), llmsFullTxt);

  console.log('✅ llms.txt and llms-full.txt updated.');
}

main().catch((e) => {
  console.error('llms generation failed:', e);
  process.exit(1);
});
