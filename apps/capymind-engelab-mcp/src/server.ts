import express, { Request, Response } from 'express';
import { randomUUID } from 'node:crypto';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { z } from 'zod';
import { getProjectContext, listEngenLabProjects, searchEngenLabDoc, type Discipline } from './lib/engelab-data.js';
import { SAFETY_NOTICE, withSafetyNotice } from './lib/safety.js';

const PORT = Number(process.env.PORT ?? 3000);
const SERVER_NAME = 'capymind-engelab-mcp';
const SERVER_VERSION = '0.1.0';

const disciplineSchema = z.enum(['estrutural', 'eletrico', 'hidrossanitario', 'plus', 'geral']).optional();

function createMcpServer() {
  const server = new McpServer({
    name: SERVER_NAME,
    version: SERVER_VERSION,
  });

  server.tool(
    'get_safety_notice',
    'Return the mandatory EngenLab technical and educational use boundary notice.',
    {},
    async () => {
      const payload = withSafetyNotice({
        title: 'EngenLab technical safety notice',
        usage_boundary: SAFETY_NOTICE,
      });

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'list_engelab_projects',
    'List EngenLab Doc project-model groups by discipline.',
    {
      discipline: disciplineSchema.describe('Optional discipline filter: estrutural, eletrico, hidrossanitario, plus or geral.'),
    },
    async ({ discipline }) => {
      const payload = listEngenLabProjects(discipline as Discipline | undefined);

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'search_engelab_doc',
    'Search the EngenLab Doc library using curated MVP metadata. Returns source paths and safety boundary.',
    {
      query: z.string().min(2).describe('Search query, such as estrutural, elétrica, prompt de geração, checklist or módulo 15.'),
      discipline: disciplineSchema.describe('Optional discipline filter.'),
      limit: z.number().int().min(1).max(20).optional().describe('Maximum number of results. Default: 5. Maximum: 20.'),
    },
    async ({ query, discipline, limit }) => {
      const payload = searchEngenLabDoc({ query, discipline: discipline as Discipline | undefined, limit });

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'get_project_context',
    'Get structured context for an EngenLab Doc project group by ID or title fragment.',
    {
      project_id: z.string().min(2).describe('Project group ID, for example estrutural-01-20, eletrico-21-35, hidrossanitario-36-50, plus-modulo-15-estruturas.'),
    },
    async ({ project_id }) => {
      const payload = getProjectContext(project_id);

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  return server;
}

const app = express();
app.use(express.json({ limit: '1mb' }));

app.get('/health', (_req: Request, res: Response) => {
  res.status(200).json({
    status: 'ok',
    service: SERVER_NAME,
    version: SERVER_VERSION,
    timestamp: new Date().toISOString(),
  });
});

app.post('/mcp', async (req: Request, res: Response) => {
  const server = createMcpServer();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
  });

  res.on('close', () => {
    transport.close().catch(() => undefined);
    server.close().catch(() => undefined);
  });

  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.get('/mcp', async (_req: Request, res: Response) => {
  res.status(405).json({
    error: 'Method not allowed',
    message: 'Use POST /mcp for Streamable HTTP MCP requests.',
  });
});

app.listen(PORT, () => {
  console.log(`${SERVER_NAME} ${SERVER_VERSION} listening on port ${PORT}`);
});
