import express, { Request, Response } from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { z } from 'zod';
import { getAgentContext, getStructuralAgentContext, listAgentCatalog } from './lib/agent-contexts.js';
import { routeAgentForTask } from './lib/agent-router.js';
import { buildAgentContext, getProjectContext, listEngenLabProjects, searchEngenLabDoc, type Discipline } from './lib/engelab-data.js';
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

  server.tool(
    'build_agent_context',
    'Build a bounded context pack for another GPT or agent workflow using EngenLab Doc metadata and CapyMind safety rules.',
    {
      query: z.string().min(2).describe('Context objective, for example montar prompt estrutural, localizar projetos elétricos or estudar módulo 15.'),
      discipline: disciplineSchema.describe('Optional discipline filter.'),
      limit: z.number().int().min(1).max(20).optional().describe('Maximum number of recommended sources. Default: 5. Maximum: 20.'),
    },
    async ({ query, discipline, limit }) => {
      const payload = buildAgentContext({ query, discipline: discipline as Discipline | undefined, limit });

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'list_agent_catalog',
    'List available EngenLab PromptDesk agents exposed by the CapyMind MCP catalog.',
    {},
    async () => {
      const payload = listAgentCatalog();

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'get_agent_context',
    'Return the fixed context/system prompt and PromptDesk configuration for an agent by agent_id.',
    {
      agent_id: z.string().min(2).describe('Agent ID, for example engenlab-estruturas-ia-modulo-15.'),
    },
    async ({ agent_id }) => {
      const payload = getAgentContext(agent_id);

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'route_agent_for_task',
    'Select the best EngenLab PromptDesk agent for a user task using task text plus optional module, discipline or sourcePath hints.',
    {
      task: z.string().min(2).describe('User task or workflow description to route to the best PromptDesk agent.'),
      module: z.string().optional().describe('Optional module hint, such as 01_ESTRUTURAL, 08_BONUS/PROMPT_REVIT or PLUS_MODULOS_10_14.'),
      discipline: z.string().optional().describe('Optional discipline hint, such as Estrutural, BIM/Revit, Planejamento de Obra or Segurança do Trabalho.'),
      sourcePath: z.string().optional().describe('Optional source path hint from the EngenLab Doc library.'),
      includeContext: z.boolean().optional().describe('When true, include the selected agent context in the same response.'),
    },
    async ({ task, module, discipline, sourcePath, includeContext }) => {
      const payload = routeAgentForTask({ task, module, discipline, sourcePath, includeContext });

      return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        structuredContent: payload,
      };
    },
  );

  server.tool(
    'get_structural_agent_context',
    'Return the fixed system/context prompt, PromptDesk configuration and quick commands for EngenLab Estruturas IA — Módulo 15.',
    {},
    async () => {
      const payload = getStructuralAgentContext();

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
    // Stateless mode keeps the MVP simple for connector testing.
    // Add persistent session storage before enabling advanced bidirectional flows.
    sessionIdGenerator: undefined,
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
    message: 'This MCP endpoint uses Streamable HTTP. Use POST /mcp from an MCP client.',
  });
});

app.listen(PORT, () => {
  console.log(`${SERVER_NAME} ${SERVER_VERSION} listening on port ${PORT}`);
});
