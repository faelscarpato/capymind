import { normalizeLimit, normalizeQuery, withSafetyNotice } from './safety.js';

export type Discipline = 'estrutural' | 'eletrico' | 'hidrossanitario' | 'plus' | 'geral';

export interface EngenLabProject {
  id: string;
  title: string;
  discipline: Discipline;
  range: string;
  summary: string;
  likelyPaths: string[];
  contentTypes: string[];
}

export interface SearchResult {
  title: string;
  type: 'project' | 'prompt' | 'module' | 'notice' | 'guide';
  discipline: Discipline;
  summary: string;
  source_paths: string[];
  score: number;
}

const PROJECT_GROUPS: EngenLabProject[] = [
  {
    id: 'estrutural-01-20',
    title: 'Projetos-modelo estruturais 01 a 20',
    discipline: 'estrutural',
    range: '01-20',
    summary: 'Projetos e materiais referenciais de estruturas, incluindo PDFs referenciais, pranchas A3, DWGs, memoriais conceituais, checklists, prompts e avisos técnicos.',
    likelyPaths: ['01_ESTRUTURAL/'],
    contentTypes: ['PDF referencial', 'Imagem de prancha A3', 'DWG referencial', 'Memorial descritivo conceitual', 'Checklist de estudo', 'Prompt de geração', 'Aviso técnico'],
  },
  {
    id: 'eletrico-21-35',
    title: 'Projetos-modelo elétricos 21 a 35',
    discipline: 'eletrico',
    range: '21-35',
    summary: 'Projetos e materiais referenciais de instalações elétricas para estudo, organização documental e prompts técnicos.',
    likelyPaths: ['02_ELETRICO/'],
    contentTypes: ['PDF referencial', 'Imagem de prancha A3', 'DWG referencial', 'Memorial descritivo conceitual', 'Checklist de estudo', 'Prompt de geração', 'Aviso técnico'],
  },
  {
    id: 'hidrossanitario-36-50',
    title: 'Projetos-modelo hidrossanitários 36 a 50',
    discipline: 'hidrossanitario',
    range: '36-50',
    summary: 'Projetos e materiais referenciais de água fria, água quente, esgoto, ventilação e sistemas relacionados.',
    likelyPaths: ['03_HIDROSSANITARIO/'],
    contentTypes: ['PDF referencial', 'Imagem de prancha A3', 'DWG referencial', 'Memorial descritivo conceitual', 'Checklist de estudo', 'Prompt de geração', 'Aviso técnico'],
  },
  {
    id: 'plus-modulos-10-14',
    title: 'Módulos IA 10 a 14',
    discipline: 'plus',
    range: '10-14',
    summary: 'Módulos adicionais de IA aplicada à engenharia e obra, incluindo documentação, compatibilização, orçamento, planejamento, vistorias e segurança do trabalho.',
    likelyPaths: ['PLUS_MODULOS_10_14/'],
    contentTypes: ['Módulos educacionais', 'Prompts', 'Checklists', 'Documentação técnica'],
  },
  {
    id: 'plus-modulo-15-estruturas',
    title: 'Módulo IA 15 — Estruturas',
    discipline: 'plus',
    range: '15',
    summary: 'Módulo adicional focado em estruturas com IA, prompts estruturais, modelos de documentação e apoio educacional.',
    likelyPaths: ['PLUS_MODULO_15_ESTRUTURAS/'],
    contentTypes: ['Prompts estruturais', 'Modelos de memorial', 'Relatórios', 'Checklists'],
  },
];

const PROMPT_AREAS: SearchResult[] = [
  {
    title: 'Prompts modulares técnicos',
    type: 'prompt',
    discipline: 'geral',
    summary: 'Prompts técnicos por disciplina e por ferramenta para geração de documentação, estudo de projetos, análise conceitual, compatibilização, orçamento, planejamento, vistorias e segurança do trabalho.',
    source_paths: ['04_PROMPTS_MODULARES/'],
    score: 0.9,
  },
  {
    title: 'Matriz e controle dos 50 projetos',
    type: 'guide',
    discipline: 'geral',
    summary: 'Matriz para localizar projetos, verificar disciplinas, controlar o acervo e orientar navegação pela biblioteca.',
    source_paths: ['07_MATRIZ_E_CONTROLE/Matriz_50_Projetos.csv', '07_MATRIZ_E_CONTROLE/Matriz_50_Projetos.md'],
    score: 0.86,
  },
  {
    title: 'Guia de uso e avisos técnicos',
    type: 'notice',
    discipline: 'geral',
    summary: 'Guias, avisos técnicos, índice, checklist e termos de uso para orientar uso responsável da biblioteca.',
    source_paths: ['00_GUIA_DE_USO/'],
    score: 0.84,
  },
  {
    title: 'Módulo de cálculo estrutural com IA',
    type: 'module',
    discipline: 'estrutural',
    summary: 'Módulo de apoio ao cálculo estrutural com IA para estudo, documentação e organização técnica, sem substituir dimensionamento profissional.',
    source_paths: ['09_CALCULO_ESTRUTURAL_IA/'],
    score: 0.82,
  },
  {
    title: 'Catálogo CapyGPTs',
    type: 'guide',
    discipline: 'geral',
    summary: 'Landing page estática para apresentar agentes GPT especializados, com busca, filtros, categorias e cards de agentes.',
    source_paths: ['capygpts/'],
    score: 0.78,
  },
];

function projectToSearchResult(project: EngenLabProject, score = 0.8): SearchResult {
  return {
    title: project.title,
    type: 'project',
    discipline: project.discipline,
    summary: project.summary,
    source_paths: project.likelyPaths,
    score,
  };
}

export function listEngenLabProjects(discipline?: Discipline) {
  const projects = discipline ? PROJECT_GROUPS.filter((item) => item.discipline === discipline) : PROJECT_GROUPS;
  return withSafetyNotice({
    repository: 'faelscarpato/engelab_doc',
    count: projects.length,
    projects,
  });
}

export function searchEngenLabDoc(params: { query: string; discipline?: Discipline; limit?: number }) {
  const query = normalizeQuery(params.query);
  const limit = normalizeLimit(params.limit, 5, 20);
  const lowered = query.toLowerCase();

  const projectResults = PROJECT_GROUPS
    .filter((project) => !params.discipline || project.discipline === params.discipline)
    .map((project) => {
      const haystack = [project.title, project.discipline, project.range, project.summary, ...project.contentTypes, ...project.likelyPaths]
        .join(' ')
        .toLowerCase();
      const score = haystack.includes(lowered) ? 0.95 : lowered.split(' ').some((token) => haystack.includes(token)) ? 0.74 : 0.45;
      return projectToSearchResult(project, score);
    });

  const promptResults = PROMPT_AREAS
    .filter((item) => !params.discipline || item.discipline === params.discipline || item.discipline === 'geral')
    .map((item) => {
      const haystack = [item.title, item.discipline, item.summary, ...item.source_paths].join(' ').toLowerCase();
      const score = haystack.includes(lowered) ? Math.max(item.score, 0.94) : lowered.split(' ').some((token) => haystack.includes(token)) ? item.score : item.score - 0.25;
      return { ...item, score };
    });

  const results = [...projectResults, ...promptResults]
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  return withSafetyNotice({
    repository: 'faelscarpato/engelab_doc',
    query,
    discipline: params.discipline ?? 'all',
    count: results.length,
    results,
    note: 'Initial MVP search uses curated repository metadata. Full-text indexing should be wired in the next iteration.',
  });
}

export function getProjectContext(projectId: string) {
  const normalized = normalizeQuery(projectId).toLowerCase();
  const project = PROJECT_GROUPS.find((item) => item.id === normalized || item.title.toLowerCase().includes(normalized));

  if (!project) {
    return withSafetyNotice({
      found: false,
      project_id: projectId,
      message: 'Project group not found in the curated MVP metadata. Use list_engelab_projects to inspect available IDs.',
    });
  }

  return withSafetyNotice({
    found: true,
    repository: 'faelscarpato/engelab_doc',
    project,
    recommended_use: [
      'Locate the project folder in the source path.',
      'Review the PDF, DWG, prompt, checklist and notice together.',
      'Use the result as study/reference context only.',
    ],
  });
}
