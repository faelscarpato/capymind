import { getAgentContext } from './agent-contexts.js';
import { withSafetyNotice } from './safety.js';

type RoutingCandidate = {
  agentId: string;
  label: string;
  module: string;
  keywords: string[];
};

const ROUTING_CANDIDATES: RoutingCandidate[] = [
  {
    agentId: 'engenlab-estrutural-projetos-ia-01',
    label: 'EngenLab Estrutural IA — Projetos 01 a 20',
    module: '01_ESTRUTURAL',
    keywords: ['estrutural', 'estrutura', 'pilar', 'viga', 'laje', 'fundacao', 'sapata', 'baldrame', 'prancha estrutural', 'dwg estrutural'],
  },
  {
    agentId: 'engenlab-eletrico-projetos-ia-02',
    label: 'EngenLab Elétrico IA — Projetos 21 a 35',
    module: '02_ELETRICO',
    keywords: ['eletrico', 'elétrica', 'instalacao eletrica', 'circuito', 'disjuntor', 'tomada', 'interruptor', 'quadro de cargas', 'pontos eletricos'],
  },
  {
    agentId: 'engenlab-hidrossanitario-projetos-ia-03',
    label: 'EngenLab Hidrossanitário IA — Projetos 36 a 50',
    module: '03_HIDROSSANITARIO',
    keywords: ['hidrossanitario', 'hidráulico', 'hidraulico', 'sanitario', 'esgoto', 'agua fria', 'agua quente', 'tubulacao', 'reservatorio', 'caixa de gordura'],
  },
  {
    agentId: 'engenlab-prompts-modulares-ia-04',
    label: 'EngenLab Prompts Modulares IA — Módulo 04',
    module: '04_PROMPTS_MODULARES',
    keywords: ['prompt', 'prompts', 'prompt modular', 'melhorar prompt', 'template de prompt', 'prompt negativo', 'engenharia de prompt'],
  },
  {
    agentId: 'engenlab-revit-prompt-ia-08',
    label: 'EngenLab Revit Prompt IA — Bônus 08',
    module: '08_BONUS/PROMPT_REVIT',
    keywords: ['revit', 'bim', 'familia', 'família', 'vistas', 'pranchas revit', 'lod', 'parametros', 'parâmetros', 'modelagem'],
  },
  {
    agentId: 'engenlab-calculo-estrutural-ia-09',
    label: 'EngenLab Cálculo Estrutural IA — Módulo 09',
    module: '09_CALCULO_ESTRUTURAL_IA',
    keywords: ['calculo estrutural', 'cálculo estrutural', 'hipoteses', 'hipóteses', 'cargas', 'combinacoes', 'combinações', 'dimensionamento', 'memoria de calculo'],
  },
  {
    agentId: 'engenlab-compatibilizacao-ia-modulo-10',
    label: 'EngenLab Compatibilização IA — Módulo 10',
    module: 'PLUS_MODULOS_10_14 / Módulo 10',
    keywords: ['compatibilizacao', 'compatibilização', 'interferencia', 'interferência', 'conflito', 'matriz de interferencias', 'coordenação', 'arquitetura estrutura instalacoes'],
  },
  {
    agentId: 'engenlab-orcamentos-quantitativos-ia-modulo-11',
    label: 'EngenLab Orçamentos e Quantitativos IA — Módulo 11',
    module: 'PLUS_MODULOS_10_14 / Módulo 11',
    keywords: ['orcamento', 'orçamento', 'quantitativo', 'quantitativos', 'insumos', 'bdi', 'planilha', 'composicao', 'composição', 'levantamento'],
  },
  {
    agentId: 'engenlab-planejamento-obra-ia-modulo-12',
    label: 'EngenLab Planejamento de Obra IA — Módulo 12',
    module: 'PLUS_MODULOS_10_14 / Módulo 12',
    keywords: ['planejamento', 'cronograma', 'eap', 'sequenciamento', 'prazo', 'dependencias', 'dependências', 'obra', 'produtividade'],
  },
  {
    agentId: 'engenlab-vistorias-relatorios-ia-modulo-13',
    label: 'EngenLab Vistorias e Relatórios IA — Módulo 13',
    module: 'PLUS_MODULOS_10_14 / Módulo 13',
    keywords: ['vistoria', 'relatorio', 'relatório', 'inspecao', 'inspeção', 'fotos', 'evidencias', 'evidências', 'ocorrencia', 'patologia'],
  },
  {
    agentId: 'engenlab-seguranca-trabalho-obras-ia-modulo-14',
    label: 'EngenLab Segurança do Trabalho em Obras IA — Módulo 14',
    module: 'PLUS_MODULOS_10_14 / Módulo 14',
    keywords: ['seguranca do trabalho', 'segurança do trabalho', 'sst', 'epi', 'epc', 'risco', 'riscos', 'pgr', 'pcmso', 'obra segura', 'nr'],
  },
  {
    agentId: 'engenlab-estruturas-ia-modulo-15',
    label: 'EngenLab Estruturas IA — Módulo 15',
    module: 'PLUS_MODULO_15_ESTRUTURAS',
    keywords: ['modulo 15', 'módulo 15', 'estruturas com ia', 'prompt estrutural avançado', 'memorial estrutural', 'relatorio estrutural', 'checklist estrutural'],
  },
];

function normalizeText(value: string): string {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function scoreCandidate(candidate: RoutingCandidate, normalizedTask: string, normalizedHints: string[]): { score: number; matched: string[] } {
  const matched: string[] = [];
  let score = 0;

  const candidateModule = normalizeText(candidate.module);
  const candidateAgentId = normalizeText(candidate.agentId);
  const candidateLabel = normalizeText(candidate.label);

  for (const hint of normalizedHints) {
    if (!hint) continue;
    if (candidateModule.includes(hint) || candidateAgentId.includes(hint) || candidateLabel.includes(hint)) {
      score += 6;
      matched.push(`hint:${hint}`);
    }
  }

  for (const keyword of candidate.keywords) {
    const normalizedKeyword = normalizeText(keyword);
    if (normalizedTask.includes(normalizedKeyword)) {
      score += normalizedKeyword.length > 8 ? 4 : 2;
      matched.push(keyword);
    }
  }

  return { score, matched };
}

export function routeAgentForTask(params: {
  task: string;
  module?: string;
  discipline?: string;
  sourcePath?: string;
  includeContext?: boolean;
}) {
  const normalizedTask = normalizeText(params.task);
  const normalizedHints = [params.module, params.discipline, params.sourcePath].filter(Boolean).map((item) => normalizeText(String(item)));

  const ranked = ROUTING_CANDIDATES
    .map((candidate) => {
      const score = scoreCandidate(candidate, normalizedTask, normalizedHints);
      return {
        agent_id: candidate.agentId,
        label: candidate.label,
        module: candidate.module,
        score: score.score,
        matched_terms: score.matched,
      };
    })
    .sort((a, b) => b.score - a.score);

  const best = ranked[0];
  const confidence = best.score >= 8 ? 'high' : best.score >= 4 ? 'medium' : 'low';
  const alternatives = ranked.slice(1, 4).filter((item) => item.score > 0);

  const basePayload = {
    task: params.task,
    selected_agent_id: best.agent_id,
    selected_agent_name: best.label,
    selected_module: best.module,
    confidence,
    score: best.score,
    matched_terms: best.matched_terms,
    alternatives,
    routing_policy: 'Keyword and module-hint routing for PromptDesk MVP. Human confirmation is recommended before executing high-risk technical workflows.',
    next_step: 'Use get_agent_context with selected_agent_id, or set includeContext=true to retrieve the selected context in the same response.',
  };

  if (params.includeContext) {
    return withSafetyNotice({
      ...basePayload,
      selected_agent_context: getAgentContext(best.agent_id),
    });
  }

  return withSafetyNotice(basePayload);
}
