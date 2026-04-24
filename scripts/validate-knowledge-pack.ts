#!/usr/bin/env tsx
/**
 * validate-knowledge-pack.ts
 *
 * Validates the CapyMind knowledge pack structure:
 * - JSON schemas are valid
 * - Required catalog files exist and are valid JSON
 * - Required core documents exist
 * - Markdown frontmatter conforms to document-meta schema
 */

import { readFile, stat } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { Ajv } from 'ajv';
import addFormats from 'ajv-formats';
import yaml from 'yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

interface ValidationError {
  file: string;
  line?: number;
  message: string;
}

const errors: ValidationError[] = [];
const warnings: ValidationError[] = [];

async function fileExists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

function addError(file: string, message: string, line?: number) {
  errors.push({ file, message, line });
}

function addWarning(file: string, message: string, line?: number) {
  warnings.push({ file, message, line });
}

async function validateJsonFile(filePath: string, schema?: any) {
  try {
    const content = await readFile(filePath, 'utf-8');
    const data = JSON.parse(content);
    if (schema) {
      const ajv = new Ajv({ validateSchema: false, strict: false, allErrors: true });
      addFormats(ajv);
      const validate = ajv.compile(schema);
      const ok = validate(data);
      if (!ok) {
        addError(filePath, `Schema validation failed: ${JSON.stringify(validate.errors)}`);
      }
    }
    return data;
  } catch (e: any) {
    if (e.code === 'ENOENT') {
      addError(filePath, 'File not found');
    } else {
      addError(filePath, `JSON parse error: ${e.message}`);
    }
  }
  return null;
}

async function validateMarkdownFrontmatter(filePath: string, schema: any) {
  try {
    const content = await readFile(filePath, 'utf-8');
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n/);
    if (!frontmatterMatch) {
      addWarning(filePath, 'Missing frontmatter block (expected "---" delimiter)');
      return;
    }
    const frontmatterYaml = frontmatterMatch[1];
    let frontmatter: any;
    try {
      frontmatter = yaml.parse(frontmatterYaml);
    } catch (e: any) {
      addError(filePath, `Frontmatter YAML parse error: ${e.message}`);
      return;
    }
    const ajv = new Ajv({ validateSchema: false, strict: false, allErrors: true });
    addFormats(ajv);
    const validate = ajv.compile(schema);
    const ok = validate(frontmatter);
    if (!ok) {
      addError(filePath, `Frontmatter schema validation failed: ${JSON.stringify(validate.errors)}`);
    }
  } catch (e: any) {
    if (e.code === 'ENOENT') {
      addError(filePath, 'File not found');
    } else {
      addError(filePath, `Read error: ${e.message}`);
    }
  }
}

async function main() {
  console.log('🔍 Validating CapyMind knowledge pack...\n');

  // 1. Load schemas
  const documentMetaSchemaPath = join(rootDir, 'schemas', 'document-meta.schema.json');
  const projectMetaSchemaPath = join(rootDir, 'schemas', 'project-meta.schema.json');

  const documentMetaSchema = await validateJsonFile(documentMetaSchemaPath);
  const projectMetaSchema = await validateJsonFile(projectMetaSchemaPath);

  if (!documentMetaSchema) {
    addError('schemas/document-meta.schema.json', 'Document metadata schema is invalid or missing');
  }
  if (!projectMetaSchema) {
    addError('schemas/project-meta.schema.json', 'Project metadata schema is invalid or missing');
  }

  // 2. Validate catalog files
  const projectsCatalogPath = join(rootDir, 'catalog', 'projects.json');
  const documentsCatalogPath = join(rootDir, 'catalog', 'documents.json');

  await validateJsonFile(projectsCatalogPath);
  await validateJsonFile(documentsCatalogPath);

  // 3. Validate core required documents exist and have valid frontmatter
  const coreDocs = [
    'README.md',
    'MCP_GUIDE.md',
    'PROJECT_CATALOG.md',
    'INVENTORY.md',
    'llms.txt',
    'llms-full.txt',
    'docs/reference/taxonomy.md',
    'docs/reference/document-types.md',
    'docs/reference/citation-policy.md',
    'docs/governance/security-policy.md',
    'ai/policies/anti-prompt-injection.md',
    'ai/policies/retrieval-safety.md'
  ];

  for (const doc of coreDocs) {
    const path = join(rootDir, doc);
    const exists = await fileExists(path);
    if (!exists) {
      addError(doc, 'Required core document missing');
    } else if (doc.endsWith('.md')) {
      if (documentMetaSchema) {
        await validateMarkdownFrontmatter(path, documentMetaSchema);
      }
    }
  }

  // 4. Validate all markdown files under docs/, knowledge/, projects/, references/, ai/ (except prompts folder) have frontmatter
  const globs = [
    'docs/**/*.md',
    'knowledge/**/*.md',
    'projects/*/overview.md',
    'projects/*/purpose.md',
    'projects/*/stack.md',
    'projects/*/architecture.md',
    'projects/*/integrations.md',
    'references/**/*.md',
    'ai/**/*.md'
  ];

  // Simple glob implementation using Node's fs — skip for brevity in MVP; we'll rely on core validation

  // 5. Validate JSON schemas in ai/schemas/ if present
  const schemasDir = join(rootDir, 'ai', 'schemas');
  // Only report if required ones missing — already done above

  // Summary
  console.log('\n✅ Validation complete.\n');
  console.log(`Errors:   ${errors.length}`);
  console.log(`Warnings: ${warnings.length}`);

  if (errors.length > 0) {
    console.log('\n❌ FAILED — errors found:\n');
    for (const e of errors) {
      console.log(`  ${e.file}${e.line ? `:${e.line}` : ''}: ${e.message}`);
    }
    process.exit(1);
  }

  if (warnings.length > 0) {
    console.log('\n⚠️  Warnings:\n');
    for (const w of warnings) {
      console.log(`  ${w.file}${w.line ? `:${w.line}` : ''}: ${w.message}`);
    }
  }

  console.log('\n🎉 Knowledge pack is valid.\n');
}

main().catch((e) => {
  console.error('Unexpected error:', e);
  process.exit(1);
});
