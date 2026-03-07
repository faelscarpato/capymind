from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'capymind'
IGNORE_DIRS = {
    'node_modules', '.git', '.next', 'dist', 'build', 'coverage', 'vendor',
    'venv', '.venv', 'target', 'out', '.turbo', '.cache', 'bin', 'obj'
}
HEAVY_FILE_LIMIT = 1_000_000


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value).strip('-')
    return value or 'item'


def ensure(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write(path: Path, content: str) -> None:
    ensure(path.parent)
    path.write_text(content.strip() + '\n', encoding='utf-8')


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding='latin-1')
        except Exception:
            return ''
    except Exception:
        return ''


def read_json(path: Path) -> dict:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def unwrap_project(path: Path) -> Path | None:
    if not path.exists() or not path.is_dir():
        return None
    markers = ['package.json', 'pyproject.toml', 'Cargo.toml', 'README.md', 'readme.md']
    if any((path / marker).exists() for marker in markers):
        return path
    subdirs = [child for child in path.iterdir() if child.is_dir() and child.name not in IGNORE_DIRS]
    candidates = [child for child in subdirs if any((child / marker).exists() for marker in markers)]
    if len(candidates) == 1:
        return candidates[0]
    same_name = [child for child in candidates if slugify(child.name) == slugify(path.name)]
    if same_name:
        return same_name[0]
    return None


def detect_projects() -> list[Path]:
    seen: set[Path] = set()
    found: list[Path] = []

    def add(path: Path | None) -> None:
        if not path or not path.exists():
            return
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        found.append(resolved)

    base_2025 = ROOT / 'projects' / '2025'
    if base_2025.exists():
        for child in sorted(base_2025.iterdir(), key=lambda item: item.name.lower()):
            if child.is_dir():
                add(unwrap_project(child))

    active_base = ROOT / 'projects' / 'active'
    add(active_base / 'capypos')
    ops = active_base / 'ops'
    if ops.exists():
        add(ops / 'capy-workspace (7)')
        add((ops / 'capyops-main (3)' / 'capyops-main') if (ops / 'capyops-main (3)').exists() else None)
        add((ops / 'capyops' / 'capyops-main') if (ops / 'capyops').exists() else None)
        add((ops / 'capyops' / 'capyops-main' / 'CAPYOPS-V3') if (ops / 'capyops').exists() else None)
        add(unwrap_project(ops / 'Nova pasta'))
        add(unwrap_project(ops / 'Nova pasta (2)'))

    archive_versions = ROOT / 'archive' / 'versions'
    if archive_versions.exists():
        for child in sorted(archive_versions.iterdir(), key=lambda item: item.name.lower()):
            if child.is_dir():
                add(unwrap_project(child))

    add(ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'PETALA DECOR')
    return found


def file_exists_any(path: Path, names: list[str]) -> bool:
    return any((path / name).exists() for name in names)


def first_lines(text: str, limit: int = 6) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return ' '.join(lines[:limit])


def walk_limited(path: Path, max_depth: int = 3):
    base_depth = len(path.parts)
    for current, dirs, files in __import__('os').walk(path):
        current_path = Path(current)
        depth = len(current_path.parts) - base_depth
        dirs[:] = [name for name in sorted(dirs) if name not in IGNORE_DIRS]
        if depth > max_depth:
            dirs[:] = []
            continue
        yield current_path, dirs, sorted(files)


def collect_tree(path: Path, max_depth: int = 3, max_lines: int = 60) -> str:
    lines = [f'{path.name}/']
    for current_path, dirs, files in walk_limited(path, max_depth=max_depth):
        depth = len(current_path.relative_to(path).parts)
        if depth == 0:
            children = dirs + files[:8]
        else:
            children = dirs[:8] + files[:8]
        for name in children:
            if len(lines) >= max_lines:
                lines.append('...')
                return '\n'.join(lines)
            indent = '  ' * depth
            suffix = '/' if (current_path / name).is_dir() else ''
            lines.append(f'{indent}- {name}{suffix}')
    return '\n'.join(lines)

def detect_stack(project_path: Path) -> dict:
    package = read_json(project_path / 'package.json')
    readme = read_text(project_path / 'README.md')
    deps = {**package.get('dependencies', {}), **package.get('devDependencies', {})}
    dep_names = set(deps.keys())
    scripts = package.get('scripts', {})

    frameworks: list[str] = []
    languages: list[str] = []
    toolchain: list[str] = []
    libs: list[str] = []
    signals: list[str] = []

    if 'next' in dep_names or file_exists_any(project_path, ['next.config.js', 'next.config.ts']):
        frameworks.append('Next.js')
    if 'react' in dep_names:
        frameworks.append('React')
    if 'vite' in dep_names or file_exists_any(project_path, ['vite.config.ts', 'vite.config.js']):
        frameworks.append('Vite')
    if 'electron' in dep_names:
        frameworks.append('Electron')
    if (project_path / 'src-tauri').exists() or (project_path / 'Cargo.toml').exists():
        frameworks.append('Tauri')
    if (project_path / 'server').exists() or (project_path / 'backend').exists() or 'express' in dep_names:
        frameworks.append('Backend service')

    if file_exists_any(project_path, ['tsconfig.json', 'tsconfig.app.json', 'tsconfig.node.json']):
        languages.append('TypeScript')
    if package:
        languages.append('JavaScript')
    if file_exists_any(project_path, ['pyproject.toml', 'requirements.txt']):
        languages.append('Python')
    if (project_path / 'Cargo.toml').exists() or (project_path / 'src-tauri' / 'Cargo.toml').exists():
        languages.append('Rust')
    if list(project_path.glob('*.csproj')):
        languages.append('C#')

    if (project_path / 'package-lock.json').exists():
        toolchain.append('npm')
    if (project_path / 'pnpm-lock.yaml').exists():
        toolchain.append('pnpm')
    if (project_path / 'yarn.lock').exists():
        toolchain.append('yarn')
    if (project_path / 'bun.lockb').exists():
        toolchain.append('bun')
    if (project_path / 'src-tauri').exists():
        toolchain.append('cargo')

    lib_rules = {
        'Supabase': lambda: any('supabase' in dep for dep in dep_names),
        'Tailwind CSS': lambda: any('tailwind' in dep for dep in dep_names) or file_exists_any(project_path, ['tailwind.config.ts', 'tailwind.config.js']),
        'Radix UI': lambda: any(dep.startswith('@radix-ui/') for dep in dep_names),
        'shadcn/ui': lambda: (project_path / 'components.json').exists(),
        'React Query': lambda: '@tanstack/react-query' in dep_names,
        'Zustand': lambda: 'zustand' in dep_names,
        'Chart.js': lambda: 'chart.js' in dep_names,
        'Zod': lambda: 'zod' in dep_names,
        'Upstash Redis': lambda: '@upstash/redis' in dep_names,
        'Mercado Livre API': lambda: 'mercado' in readme.lower() or 'oauth/mercadolivre' in readme.lower(),
        'OpenAI': lambda: any('openai' in dep for dep in dep_names) or 'openai' in readme.lower(),
        'Gemini': lambda: 'gemini' in readme.lower() or 'gemini' in project_path.name.lower(),
    }
    for label, rule in lib_rules.items():
        if rule():
            libs.append(label)

    feature_rules = {
        'API': lambda: (project_path / 'app' / 'api').exists() or (project_path / 'pages' / 'api').exists() or (project_path / 'server').exists() or (project_path / 'backend').exists(),
        'Banco': lambda: any(term in dep_names for term in ['@supabase/supabase-js', 'pg', 'mysql2', 'sqlite3', 'prisma']),
        'Auth': lambda: any(term in dep_names for term in ['next-auth', '@clerk/nextjs']) or 'oauth' in readme.lower() or 'auth' in readme.lower(),
        'Dashboard': lambda: 'dashboard' in readme.lower() or 'dashboard' in project_path.name.lower(),
        'UI kit': lambda: (project_path / 'components.json').exists() or 'tailwind' in ' '.join(dep_names),
        'Storage': lambda: '@upstash/redis' in dep_names or 'storage' in readme.lower(),
        'Desktop': lambda: 'electron' in dep_names or (project_path / 'src-tauri').exists(),
    }
    for label, rule in feature_rules.items():
        if rule():
            signals.append(label)

    if scripts:
        signals.append('Scripts de build e desenvolvimento presentes')

    confidence = 'alta' if package or len(frameworks) >= 2 else 'media' if frameworks or languages else 'baixa'
    return {
        'frameworks': list(dict.fromkeys(frameworks)),
        'languages': list(dict.fromkeys(languages)),
        'toolchain': list(dict.fromkeys(toolchain)),
        'libs': list(dict.fromkeys(libs)),
        'signals': list(dict.fromkeys(signals)),
        'package': package,
        'readme': readme,
        'confidence': confidence,
    }


def infer_domain(name: str, path: Path) -> str:
    text = f'{name} {path}'.lower()
    if 'petala' in text or 'mercado livre' in text or 'cofre' in text:
        return 'comercial / catalogo'
    if any(term in text for term in ['capyops', 'workspace', 'mes', 'factory', 'pos']):
        return 'operacoes / saas'
    if any(term in text for term in ['universe', 'verse', 'agente', 'chat', 'ai', 'vision', 'ide', 'creator']):
        return 'ia / produto'
    if any(term in text for term in ['pages', 'station', 'viewport', 'portfolio']):
        return 'site / branding'
    if any(term in text for term in ['contrato', 'assinatura']):
        return 'documentos / contratos'
    if 'bocaaberta' in text:
        return 'transparencia / dados'
    return 'experimental / revisar'


def infer_purpose(slug: str, stack: dict, readme: str) -> str:
    lower = f'{slug} {readme}'.lower()
    if 'petala' in lower:
        return 'Catalogo digital e operacao comercial integrada ao Mercado Livre.'
    if 'capyops' in lower or 'workspace' in lower:
        return 'Painel operacional para gestao, analytics e fluxos internos.'
    if 'universe' in lower or 'verse' in lower:
        return 'Hub de ferramentas e experiencias do ecossistema Capy.'
    if 'chat' in lower or 'agente' in lower or 'ai' in lower:
        return 'Interface de IA para conversa, automacao ou assistencia.'
    if 'vision' in lower or 'img' in lower:
        return 'Ferramenta visual orientada a criacao, leitura ou analise.'
    if 'deal' in lower or 'box' in lower or 'mes' in lower or 'factory' in lower:
        return 'Aplicacao de negocio com foco em operacao, dados ou produtividade.'
    if 'bocaaberta' in lower:
        return 'Plataforma orientada a dados, historias e transparencia.'
    return 'Projeto de software com sinais suficientes para catalogacao tecnica, mas com objetivo parcial ou experimental.'


def detect_status(path: Path) -> str:
    path_text = str(path).lower()
    if 'active' in path_text or 'mercado livre' in path_text:
        return 'ativo ou em uso recente'
    if 'archive' in path_text:
        return 'arquivado / referencia'
    if '2026' in path_text:
        return 'iteracao recente'
    return 'snapshot de trabalho'


def collect_key_files(project_path: Path, limit: int = 10) -> list[str]:
    preferred = [
        'README.md', 'package.json', 'tsconfig.json', 'tsconfig.app.json', 'vite.config.ts', 'vite.config.js',
        'next.config.ts', 'next.config.js', 'components.json', 'app/page.tsx', 'src/main.tsx', 'src/main.jsx',
        'src-tauri/tauri.conf.json', 'electron.js', 'server/package.json', 'backend/requirements.txt', 'docs/routes.json'
    ]
    results: list[str] = []
    for item in preferred:
        candidate = project_path / item
        if candidate.exists():
            results.append(item)
        if len(results) >= limit:
            return results
    for current_path, dirs, files in walk_limited(project_path, max_depth=2):
        for file_name in files:
            rel = str((current_path / file_name).relative_to(project_path)).replace('\\', '/')
            if rel not in results:
                results.append(rel)
            if len(results) >= limit:
                return results
    return results


def collect_data_files(project_path: Path, limit: int = 8) -> list[str]:
    extensions = {'.json', '.csv', '.xlsx', '.sql', '.db'}
    results: list[str] = []
    for current_path, dirs, files in walk_limited(project_path, max_depth=2):
        for file_name in files:
            if Path(file_name).suffix.lower() in extensions:
                rel = str((current_path / file_name).relative_to(project_path)).replace('\\', '/')
                results.append(rel)
            if len(results) >= limit:
                return results
    return results


def find_heavy_files(base_paths: list[Path], limit: int = 40) -> list[tuple[Path, int]]:
    heavy: list[tuple[Path, int]] = []
    for base in base_paths:
        if not base.exists():
            continue
        for current_path, dirs, files in walk_limited(base, max_depth=4):
            dirs[:] = [name for name in dirs if name not in IGNORE_DIRS]
            for file_name in files:
                candidate = current_path / file_name
                try:
                    size = candidate.stat().st_size
                except OSError:
                    continue
                if size >= HEAVY_FILE_LIMIT:
                    heavy.append((candidate.resolve(), size))
    heavy.sort(key=lambda item: item[1], reverse=True)
    return heavy[:limit]


def dir_size_mb(path: Path) -> float:
    total = 0
    for current, dirs, files in __import__('os').walk(path):
        dirs[:] = [name for name in dirs if name not in IGNORE_DIRS]
        for file_name in files:
            try:
                total += (Path(current) / file_name).stat().st_size
            except OSError:
                pass
    return round(total / (1024 * 1024), 2)


def project_payload(project_path: Path, used_slugs: set[str]) -> dict:
    stack = detect_stack(project_path)
    package = stack['package']
    readme = stack['readme']
    generic_names = {'my-v0-project', 'vite_react_shadcn_ts', '@figma/my-make-file', 'news-portal'}
    package_name = (package.get('name') or '').strip()
    raw_name = project_path.name if package_name.lower() in generic_names or not package_name else package_name
    slug = slugify(project_path.name)
    if slug in used_slugs:
        slug = slugify(f'{project_path.parent.name}-{project_path.name}')
    counter = 2
    base_slug = slug
    while slug in used_slugs:
        slug = f'{base_slug}-{counter}'
        counter += 1
    used_slugs.add(slug)
    domain = infer_domain(raw_name, project_path)
    purpose = infer_purpose(slug, stack, readme)
    status = detect_status(project_path)
    summary = package.get('description') or first_lines(readme) or purpose
    tags = sorted({slug.split('-')[0], *[item.lower() for item in stack['frameworks'][:3]], domain.split('/')[0].strip()})
    return {
        'name': raw_name,
        'slug': slug,
        'path': project_path,
        'stack': stack,
        'domain': domain,
        'purpose': purpose,
        'status': status,
        'summary': summary,
        'key_files': collect_key_files(project_path),
        'data_files': collect_data_files(project_path),
        'tree': collect_tree(project_path),
        'tags': [tag for tag in tags if tag],
    }


def project_docs(info: dict) -> dict[str, str]:
    path = info['path']
    stack = info['stack']
    integrations = []
    for label in ['Mercado Livre API', 'OpenAI', 'Gemini', 'Supabase', 'Upstash Redis']:
        if label in stack['libs']:
            integrations.append(label)
    if 'Next.js' in stack['frameworks']:
        integrations.append('Vercel / deploy web plausivel')
    if not integrations:
        integrations.append('Nenhum conector externo forte detectado por estrutura; revisar manualmente se necessario.')
    ui_signals = []
    if 'Tailwind CSS' in stack['libs']:
        ui_signals.append('Tailwind CSS presente.')
    if 'Radix UI' in stack['libs'] or 'shadcn/ui' in stack['libs']:
        ui_signals.append('Sinais de design system baseado em componentes reutilizaveis.')
    if any('dashboard' in item.lower() for item in [info['slug'], info['summary']]):
        ui_signals.append('Projeto parece priorizar interfaces de painel.')
    if not ui_signals:
        ui_signals.append('Sinais visuais limitados; interface precisa de leitura manual adicional.')

    data_notes = info['data_files'] or ['Nenhum dataset local evidente nas primeiras camadas da estrutura.']
    key_files_md = '\n'.join(f'- `{item}`: arquivo-chave para leitura tecnica ou ponto de entrada provavel.' for item in info['key_files'])
    data_files_md = '\n'.join(f'- `{item}`' for item in data_notes)
    tree_md = f"```text\n{info['tree']}\n```"
    frameworks = ', '.join(stack['frameworks']) or 'Nao detectado com confianca'
    languages = ', '.join(stack['languages']) or 'Nao detectado com confianca'
    toolchain = ', '.join(stack['toolchain']) or 'Nao detectado com confianca'
    libs = ', '.join(stack['libs']) or 'Sem bibliotecas-chave suficientemente claras'
    signals = ', '.join(stack['signals']) or 'Sem sinais arquiteturais fortes nas camadas lidas'
    tags = ', '.join(info['tags'])
    summary = info['summary']

    return {
        'overview.md': f"# {info['name']}\n\nResumo curto: {summary}\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n- Slug: `{info['slug']}`\n- Tipo percebido: {info['domain']}\n- Status percebido: {info['status']}\n- Tags: {tags}\n\n## Inferido\n- Objetivo central: {info['purpose']}\n- A classificacao acima combina nome, stack, README e localizacao da pasta.\n\n## Relevancia\n- Projeto relevante para o ecossistema documental do usuario.\n- A documentacao derivada em `capymind` substitui a copia integral do projeto para fins de GitHub e consulta por IA.\n\n## Observacoes\n- O codigo-fonte completo permaneceu fora do `capymind`.\n- Arquivos relacionados: [stack](./stack.md), [architecture](./architecture.md), [key-files](./key-files.md).",
        'purpose.md': f"# Purpose\n\nResumo curto: leitura funcional do problema que o projeto parece resolver.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n- Nome do projeto: {info['name']}\n- Sinal principal: {summary}\n\n## Inferido\n- Problema que parece resolver: {info['purpose']}\n- Publico-alvo percebido: {'time interno / operacao' if 'operacoes' in info['domain'] else 'usuarios finais ou clientes'}\n- Natureza de uso: {'interno e operacional' if 'operacoes' in info['domain'] else 'produto, experimento ou interface comercial'}\n\n## Relevancia\n- Ajuda a entender porque este projeto existe dentro do ecossistema e como ele conversa com IA, operacao ou catalogo.\n\n## Observacoes\n- Esta leitura e parcialmente inferida a partir de README, nome e sinais de stack.",
        'stack.md': f"# Stack\n\nResumo curto: stack tecnico detectado de forma heuristica.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n- Linguagens: {languages}\n- Frameworks: {frameworks}\n- Toolchain: {toolchain}\n- Bibliotecas principais: {libs}\n- Sinais funcionais: {signals}\n- Confianca da deteccao: {stack['confidence']}\n\n## Inferido\n- A stack sugere {'aplicacao web moderna' if 'Next.js' in stack['frameworks'] or 'React' in stack['frameworks'] else 'aplicacao com stack mista ou customizada'}.\n\n## Relevancia\n- Esta pagina ajuda IA e humanos a localizar rapidamente os blocos tecnicos do projeto.\n\n## Observacoes\n- A deteccao foi feita sem copiar o projeto para o repositrio documental.",
        'architecture.md': f"# Architecture\n\nResumo curto: leitura estrutural do projeto.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n- Modulos aparentes: {'app/src/components/lib/hooks/services/assets' if (path / 'src').exists() or (path / 'app').exists() else 'estrutura parcial ou compacta'}\n- Separacao frontend/backend: {'sim' if (path / 'server').exists() or (path / 'backend').exists() or (path / 'app' / 'api').exists() else 'nao evidente'}\n- Desktop shell: {'sim' if 'Desktop' in stack['signals'] else 'nao'}\n\n## Inferido\n- Risco estrutural: {'ha variantes e snapshots paralelos do mesmo projeto no corpus' if 'active' in str(path).lower() or 'archive' in str(path).lower() else 'sem risco estrutural forte identificado nas primeiras camadas'}\n- A organizacao indica {'produto em evolucao continua' if info['status'] != 'arquivado / referencia' else 'base de referencia ou snapshot historico'}.\n\n## Relevancia\n- Permite navegar o projeto sem mover a arvore completa para dentro do repositorio leve.\n\n## Observacoes\n- A leitura esta limitada as primeiras camadas de pastas e arquivos-chave.",
        'structure.md': f"# Structure\n\nResumo curto: arvore resumida e segura do projeto.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n{tree_md}\n\n## Inferido\n- Pastas pesadas e de build foram omitidas de proposito: `{', '.join(sorted(IGNORE_DIRS))}`.\n\n## Relevancia\n- Esta visao substitui a necessidade de copiar a arvore inteira para o `capymind`.\n\n## Observacoes\n- Conteudo interno dos arquivos nao foi reproduzido.",
        'key-files.md': f"# Key Files\n\nResumo curto: arquivos mais importantes para entender o projeto.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n{key_files_md}\n\n## Inferido\n- Entry points provaveis: `{info['key_files'][0] if info['key_files'] else 'revisao manual necessaria'}`.\n\n## Relevancia\n- Facilita onboarding tecnico e leitura orientada por IA.\n\n## Observacoes\n- A lista foi limitada aos arquivos com maior sinal estrutural.",
        'integrations.md': f"# Integrations\n\nResumo curto: integracoes percebidas e pontos de conexao.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n" + '\n'.join(f'- {item}' for item in integrations) + "\n\n## Inferido\n- Outras integracoes so devem ser assumidas apos leitura manual de codigo ou variaveis de ambiente.\n\n## Relevancia\n- Resume pontos de integracao possiveis para IA, APIs externas, deploy e operacao.\n\n## Observacoes\n- Inferencias fracas nao foram promovidas a fato.",
        'data-notes.md': f"# Data Notes\n\nResumo curto: sinais de dados, schemas e bases locais.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n{data_files_md}\n\n## Inferido\n- Se o projeto usa banco remoto, isso pode nao aparecer na primeira camada da pasta.\n\n## Relevancia\n- Ajuda a localizar estruturas que podem alimentar IA, analytics e documentacao.\n\n## Observacoes\n- Bases pesadas continuam fora do `capymind`.",
        'ui-notes.md': f"# UI Notes\n\nResumo curto: sinais de interface, design system e experiencia visual.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n" + '\n'.join(f'- {item}' for item in ui_signals) + f"\n\n## Inferido\n- Frameworks visuais detectados: {', '.join(stack['libs']) or 'sinais discretos'}\n\n## Relevancia\n- Serve para mapear componentes, dashboards e consistencia visual sem abrir a base completa.\n\n## Observacoes\n- Validacao visual final exige execucao ou leitura mais profunda do frontend.",
        'roadmap-notes.md': f"# Roadmap Notes\n\nResumo curto: lacunas e proximos passos percebidos.\n\n## Origem\n- Caminho original: `{path}`\n\n## Detectado\n- Status atual percebido: {info['status']}\n- Variantes correlatas no corpus: {'sim' if any(token in str(path).lower() for token in ['archive', 'active', '(1)', '(2)', '(3)']) else 'nao evidente'}\n\n## Inferido\n- Proximos passos plausiveis: consolidar variantes, reduzir duplicatas e alinhar documentacao com a versao principal.\n- Areas em evolucao: stack, integracoes e UX, conforme sinais encontrados.\n\n## Relevancia\n- Direciona manutencao do conhecimento sem inventar features prontas.\n\n## Observacoes\n- Esta pagina registra inferencias e nao promessas de produto.",
        'source-path.md': f"# Source Path\n\nResumo curto: rastreabilidade do material analisado.\n\n## Origem\n- Caminho original absoluto: `{path.resolve()}`\n\n## Detectado\n- O projeto foi lido no local acima.\n- Nenhuma copia integral foi movida para dentro do `capymind`.\n\n## Relevancia\n- Mantem rastreabilidade para auditoria, IA e revisao humana.\n\n## Observacoes\n- Este repositorio guarda somente conhecimento derivado, indices e resumos em markdown.",
    }

PROMPT_SOURCES = [
    {
        'category': 'coding',
        'slug': 'codegen-instructions',
        'title': 'Codegen Instructions',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'codegen_instructions.md',
        'objective': 'Orientar geracao de codigo com restricoes de arquitetura, UX e implementacao.',
        'tool': 'Codex / GPT / agentes de coding',
    },
    {
        'category': 'coding',
        'slug': 'system-prompt-for-gpt',
        'title': 'System Prompt For GPT',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'PART_II_SYSTEM_PROMPT_FOR_GPT.md',
        'objective': 'Definir comportamento de agente para respostas tecnicas e consistentes.',
        'tool': 'GPT / assistentes conversacionais',
    },
    {
        'category': 'analysis',
        'slug': 'full-search-ai-prompt',
        'title': 'Full Search AI Prompt',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'full-search-ai-prompt.md',
        'objective': 'Guiar pesquisa, coleta e sintese com foco em abrangencia.',
        'tool': 'Agentes de pesquisa',
    },
    {
        'category': 'analysis',
        'slug': 'agent-system-prompt',
        'title': 'Agent System Prompt',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'prompt-engineering-2026' / 'Templates & Exemplos' / 'agent-system-prompt.md',
        'objective': 'Modelar prompts-base para agentes especializados.',
        'tool': 'Sistemas multiagente',
    },
    {
        'category': 'image',
        'slug': 'vision-to-code-pattern',
        'title': 'Vision To Code Pattern',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'prompt-engineering-2026' / 'Templates & Exemplos' / 'example-1-vision-to-code' / 'example-1-README.md',
        'objective': 'Converter referencia visual em especificacao de interface ou codigo.',
        'tool': 'Modelos multimodais',
    },
    {
        'category': 'coding',
        'slug': 'function-calling-template',
        'title': 'Function Calling Template',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'prompt-engineering-2026' / 'Templates & Exemplos' / 'function-calling-template.md',
        'objective': 'Padronizar prompts com chamadas de ferramenta e estrutura de funcoes.',
        'tool': 'Agentes com tools',
    },
    {
        'category': 'marketing',
        'slug': 'design-system-2026-ready',
        'title': 'Design System 2026 Ready',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'design system 2026-ready.md',
        'objective': 'Guiar direcao visual e linguagem de produto.',
        'tool': 'IA de design / produto',
    },
    {
        'category': 'business',
        'slug': 'blueprint-strategic-prompt',
        'title': 'Blueprint Prompt',
        'source': ROOT / 'knowledge' / 'prompt-engineering' / 'blueprint.md',
        'objective': 'Estruturar analise e planejamento de produto ou negocio.',
        'tool': 'IA estrategica',
    },
]

DATASET_DOCS = [
    {
        'path': TARGET / 'datasets' / 'structured' / 'mercado-livre-anuncios.md',
        'title': 'Mercado Livre Anuncios',
        'source': ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'anuncios.csv',
        'summary': 'Base tabular de anuncios com ids, preco, visitas, imagens e performance comercial.',
        'fields': 'id, product_id, ml_item_id, permalink, title, price, thumbnail, sold_quantity, visits, images_count',
    },
    {
        'path': TARGET / 'datasets' / 'structured' / 'mercado-livre-produtos.md',
        'title': 'Mercado Livre Produtos',
        'source': ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'produtos.csv',
        'summary': 'Base de produtos relacionada ao catalogo comercial da operacao.',
        'fields': 'campos ligados a produto, sku, agrupamentos e dados de anuncio',
    },
    {
        'path': TARGET / 'datasets' / 'structured' / 'mercado-livre-taxas-e-gestao.md',
        'title': 'Mercado Livre Taxas e Gestao',
        'source': ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'planilha_taxas_ml.xlsx',
        'summary': 'Planilhas operacionais de taxa, gestao e margem para a operacao comercial.',
        'fields': 'comissoes, frete, margem, repasse, estoque e controle gerencial',
    },
    {
        'path': TARGET / 'datasets' / 'extracted' / 'capy-ai-verse-prompt-tool-datasets.md',
        'title': 'Capy AI Verse Prompts e Tools',
        'source': ROOT / 'projects' / '2025' / 'capy-ai-verse-main' / 'capy-ai-verse-main' / 'prompts.json',
        'summary': 'Conjunto leve de prompts e ferramentas associado ao projeto Capy AI Verse.',
        'fields': 'prompts, categorias, tools, metadados de interface',
    },
    {
        'path': TARGET / 'datasets' / 'extracted' / 'bocaaberta-investigative-datasets.md',
        'title': 'BocaAberta Investigative Datasets',
        'source': ROOT / 'projects' / '2025' / 'bocaaberta-oz-initial-scaffold' / 'bocaaberta-oz-initial-scaffold' / 'data' / 'stories.json',
        'summary': 'Colecao de arquivos JSON com historias, casos, fontes e gastos.',
        'fields': 'stories, cases, sources, expenditures, archives',
    },
    {
        'path': TARGET / 'datasets' / 'candidates' / 'capybox-api-and-geodata.md',
        'title': 'CapyBox API and Geodata',
        'source': ROOT / 'projects' / '2025' / 'capybox-main' / 'capybox-main' / 'api-docs.json',
        'summary': 'OpenAPI e dados geograficos auxiliares usados pelo projeto CapyBox.',
        'fields': 'rotas de API, estados, municipios e configuracoes auxiliares',
    },
]

REFERENCE_DOCS = [
    (TARGET / 'references' / 'technical' / 'prompt-engineering-reference-pack.md', 'Prompt Engineering Reference Pack', ROOT / 'knowledge' / 'prompt-engineering', 'Pacote de referencia tecnica sobre engenharia de prompt, function calling e exemplos de agentes.'),
    (TARGET / 'references' / 'technical' / 'openapi-and-routes-signals.md', 'OpenAPI and Routes Signals', ROOT / 'projects' / '2025' / 'capybox-main' / 'capybox-main' / 'api-docs.json', 'Materiais que descrevem contratos de API e auditorias de rotas.'),
    (TARGET / 'references' / 'commercial' / 'mercado-livre-commercial-documents.md', 'Mercado Livre Commercial Documents', ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE', 'Conjunto de planilhas, apresentacoes e PDFs ligados a operacao comercial no Mercado Livre.'),
    (TARGET / 'references' / 'contracts' / 'shipping-and-declaration-documents.md', 'Shipping and Declaration Documents', ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'VENDAS', 'Documentos de venda, declaracao e expedicao ligados ao fluxo logistico.'),
    (TARGET / 'references' / 'external' / 'mercado-livre-api-reference.md', 'Mercado Livre API Reference', ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'api ml.pdf', 'Referencia externa de API e contexto operacional associado ao marketplace.'),
    (TARGET / 'references' / 'inspirations' / 'design-and-product-direction.md', 'Design and Product Direction', ROOT / 'knowledge' / 'prompt-engineering' / 'UI UX 2026.md', 'Materiais de inspiracao sobre produto, UX e direcao visual.'),
]

ASSET_DOCS = [
    (TARGET / 'assets' / 'catalogs' / 'petala-decor-product-catalog.md', 'Pétala Decor Product Catalog', ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'COFRES', 'Agrupamentos de imagens de cofres e variacoes de produto usados no catalogo.'),
    (TARGET / 'assets' / 'visual-assets' / 'mercado-livre-visual-asset-groups.md', 'Mercado Livre Visual Asset Groups', ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE' / 'FOTOS', 'Lotes visuais e imagens promocionais ligados a anuncios e apresentacao comercial.'),
    (TARGET / 'assets' / 'product-assets' / 'petala-decor-media-batches.md', 'Pétala Decor Media Batches', ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE', 'Imagens, mockups, capturas e videos comerciais que nao devem ser copiados em massa.'),
    (TARGET / 'assets' / 'diagrams' / 'prompt-and-system-diagram-signals.md', 'Prompt and System Diagram Signals', ROOT / 'knowledge' / 'prompt-engineering' / 'exported-assets', 'Assets exportados e diagramas auxiliares usados como referencia visual e de estrutura.'),
]

POWERSHELL_SCRIPT = r'''param(
    [string]$SourceRoot = (Get-Location).Path,
    [string]$DestinationRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [string[]]$AllowedExtensions = @('.md')
)

$ErrorActionPreference = 'Stop'
$folders = @('knowledge','knowledge\\business','knowledge\\products','knowledge\\operations','knowledge\\technical','knowledge\\commercial','knowledge\\ai','knowledge\\branding','projects','prompts','prompts\\generation','prompts\\analysis','prompts\\coding','prompts\\image','prompts\\business','prompts\\marketing','datasets','datasets\\structured','datasets\\extracted','datasets\\candidates','docs','docs\\architecture','docs\\systems','docs\\flows','docs\\ui-ux','docs\\api','references','references\\technical','references\\commercial','references\\contracts','references\\inspirations','references\\external','assets','assets\\catalogs','assets\\visual-assets','assets\\product-assets','assets\\diagrams','archive','scripts')
$ignoredDirs = @('node_modules','.git','.next','dist','build','coverage','vendor','venv','.venv','target','out','.turbo','.cache')
$logDir = Join-Path $DestinationRoot 'scripts\\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logPath = Join-Path $logDir ('organize_repo_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
function Log([string]$m){$line='[' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + '] ' + $m; Add-Content -LiteralPath $logPath -Value $line; Write-Host $line}
function Ensure-Structure { foreach($folder in $folders){ New-Item -ItemType Directory -Force -Path (Join-Path $DestinationRoot $folder) | Out-Null } }
function Category([string]$relative){ $lower=$relative.ToLowerInvariant(); if($lower -match 'prompt'){return 'prompts'}; if($lower -match 'mercado livre|petala'){return 'knowledge\\commercial'}; if($lower -match 'dataset|csv|xlsx|json'){return 'datasets\\candidates'}; return 'archive' }
function UniquePath([string]$candidate){ if(-not (Test-Path -LiteralPath $candidate)){ return $candidate }; $dir=Split-Path -Parent $candidate; $stem=[IO.Path]::GetFileNameWithoutExtension($candidate); $ext=[IO.Path]::GetExtension($candidate); $i=1; do { $next=Join-Path $dir ($stem + '-' + $i.ToString('000') + $ext); $i++ } while(Test-Path -LiteralPath $next); return $next }
Ensure-Structure
Log ('organization started | source=' + $SourceRoot + ' | destination=' + $DestinationRoot)
Get-ChildItem -LiteralPath $SourceRoot -File -Recurse -Force | ForEach-Object {
    $full=$_.FullName
    if($full.StartsWith($DestinationRoot,[StringComparison]::OrdinalIgnoreCase)){ Log ('ignored destination self-scan | source=' + $full); return }
    foreach($ignored in $ignoredDirs){ if($full -match ([regex]::Escape('\\' + $ignored + '\\'))){ Log ('ignored by directory rule | source=' + $full); return } }
    if($AllowedExtensions -notcontains $_.Extension.ToLowerInvariant()){ Log ('ignored by extension | source=' + $full); return }
    $relative = Resolve-Path -LiteralPath $full | ForEach-Object { $_.Path.Substring((Resolve-Path $SourceRoot).Path.Length).TrimStart('\\') }
    $category = Category $relative
    $targetDir = Join-Path $DestinationRoot $category
    $target = UniquePath (Join-Path $targetDir $_.Name)
    Copy-Item -LiteralPath $full -Destination $target -Force:$false
    Log ('copied | source=' + $full + ' | target=' + $target)
}
Log 'organization finished'
'''

BASH_SCRIPT = r'''#!/usr/bin/env bash
set -euo pipefail
SOURCE_ROOT="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINATION_ROOT="${2:-$(cd "$SCRIPT_DIR/.." && pwd)}"
LOG_DIR="$DESTINATION_ROOT/scripts/logs"
LOG_PATH="$LOG_DIR/organize_repo_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOG_DIR"
folders=(knowledge knowledge/business knowledge/products knowledge/operations knowledge/technical knowledge/commercial knowledge/ai knowledge/branding projects prompts prompts/generation prompts/analysis prompts/coding prompts/image prompts/business prompts/marketing datasets datasets/structured datasets/extracted datasets/candidates docs docs/architecture docs/systems docs/flows docs/ui-ux docs/api references references/technical references/commercial references/contracts references/inspirations references/external assets assets/catalogs assets/visual-assets assets/product-assets assets/diagrams archive scripts)
ignored_dirs=(node_modules .git .next dist build coverage vendor venv .venv target out .turbo .cache)
log(){ printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" | tee -a "$LOG_PATH"; }
for folder in "${folders[@]}"; do mkdir -p "$DESTINATION_ROOT/$folder"; done
category(){ local lower="${1,,}"; if [[ "$lower" == *prompt* ]]; then echo prompts; elif [[ "$lower" == *"mercado livre"* || "$lower" == *petala* ]]; then echo knowledge/commercial; elif [[ "$lower" == *.csv || "$lower" == *.xlsx || "$lower" == *.json ]]; then echo datasets/candidates; else echo archive; fi; }
unique_target(){ local c="$1"; [[ ! -e "$c" ]] && { printf '%s\n' "$c"; return; }; local dir stem ext i next; dir="$(dirname "$c")"; stem="$(basename "$c")"; ext=""; [[ "$stem" == *.* ]] && ext=".${stem##*.}" && stem="${stem%.*}"; i=1; while true; do next="$dir/${stem}-$(printf '%03d' "$i")$ext"; [[ ! -e "$next" ]] && { printf '%s\n' "$next"; return; }; i=$((i+1)); done; }
log "organization started | source=$SOURCE_ROOT | destination=$DESTINATION_ROOT"
while IFS= read -r -d '' file_path; do
  [[ "$file_path" == "$DESTINATION_ROOT"* ]] && { log "ignored destination self-scan | source=$file_path"; continue; }
  skip=false; for ignored in "${ignored_dirs[@]}"; do [[ "$file_path" == *"/$ignored/"* || "$file_path" == *"\\$ignored\\"* ]] && skip=true; done; [[ "$skip" == true ]] && { log "ignored by directory rule | source=$file_path"; continue; }
  [[ "${file_path##*.}" != md ]] && { log "ignored by extension | source=$file_path"; continue; }
  rel="${file_path#$SOURCE_ROOT/}"; catdir="$(category "$rel")"; mkdir -p "$DESTINATION_ROOT/$catdir"; target="$(unique_target "$DESTINATION_ROOT/$catdir/$(basename "$file_path")")"; cp -n "$file_path" "$target"; log "copied | source=$file_path | target=$target"
done < <(find "$SOURCE_ROOT" -type f -print0)
log 'organization finished'
'''


def write_prompt_docs() -> list[Path]:
    created = []
    for item in PROMPT_SOURCES:
        source_text = read_text(item['source'])
        excerpt = '\n'.join(source_text.splitlines()[:20]).strip() or 'Fonte sem trecho legivel nas primeiras linhas.'
        path = TARGET / 'prompts' / item['category'] / f"{item['slug']}.md"
        write(path, f"# {item['title']}\n\nResumo curto: prompt catalogado como ativo de conhecimento.\n\n## Origem\n- Caminho original: `{item['source']}`\n\n## Detectado\n- Categoria: {item['category']}\n- Objetivo: {item['objective']}\n- Ferramenta-alvo percebida: {item['tool']}\n\n## Prompt Original Consolidado\n```md\n{excerpt}\n```\n\n## Inferido\n- O prompt pode ser reutilizado como base ou adaptado para pipelines internos.\n\n## Relevancia\n- Mantem a biblioteca de prompts navegavel para IA e consulta humana.\n\n## Observacoes\n- O texto foi mantido em versao leve; revisar o original para contexto completo quando necessario.")
        created.append(path)
    return created


def write_dataset_docs() -> list[Path]:
    created = []
    for item in DATASET_DOCS:
        write(item['path'], f"# {item['title']}\n\nResumo curto: base descrita em markdown, sem ingestao massiva do arquivo original.\n\n## Origem\n- Caminho original: `{item['source']}`\n\n## Detectado\n- Finalidade percebida: {item['summary']}\n- Estrutura / campos: {item['fields']}\n\n## Inferido\n- Pode alimentar analytics, site, operacao comercial ou enriquecimento para IA, dependendo do pipeline.\n\n## Relevancia\n- Preserva conhecimento util sobre a base sem carregar CSV, XLSX ou JSON pesados para o repositorio.\n\n## Observacoes\n- Consultar a origem para leitura integral ou exportacoes futuras controladas.")
        created.append(item['path'])
    return created


def write_reference_docs() -> list[Path]:
    created = []
    for path, title, source, summary in REFERENCE_DOCS:
        write(path, f"# {title}\n\nResumo curto: referencia documentada de forma leve.\n\n## Origem\n- Caminho original: `{source}`\n\n## Detectado\n- Natureza do material: {summary}\n\n## Inferido\n- O material serve como base de consulta, compliance, operacao ou arquitetura.\n\n## Relevancia\n- Centraliza referencias sem copiar PDFs, contratos ou pacotes externos para o repositorio.\n\n## Observacoes\n- Revisao manual pode aprofundar campos e extrair trechos especificos quando houver necessidade real.")
        created.append(path)
    return created


def write_asset_docs() -> list[Path]:
    created = []
    for path, title, source, summary in ASSET_DOCS:
        count = 0
        if source.exists() and source.is_dir():
            try:
                count = len([child for child in source.iterdir()])
            except OSError:
                count = 0
        write(path, f"# {title}\n\nResumo curto: catalogo leve de ativos visuais.\n\n## Origem\n- Caminho original: `{source}`\n\n## Detectado\n- Tipo de ativo: catalogo visual / lote de midia\n- Quantidade aproximada observada: {count if count else 'nao estimada nas primeiras camadas'}\n- Utilidade: {summary}\n\n## Inferido\n- Os ativos apoiam catalogo, branding, vendas ou interfaces.\n\n## Relevancia\n- Evita copiar imagens e videos em massa para o `capymind`, mantendo apenas o indice util.\n\n## Observacoes\n- Usar a origem para selecionar ativos especificos em fluxos futuros.")
        created.append(path)
    return created


def write_indexes(projects: list[dict], prompt_docs: list[Path], dataset_docs: list[Path], reference_docs: list[Path], asset_docs: list[Path]) -> None:
    projects_lines = ['# Projects Index', '', 'Resumo curto: indice dos projetos documentados no repositorio.', '', '## Projetos']
    for info in projects:
        projects_lines.append(f"- [{info['name']}](./{info['slug']}/overview.md): {info['domain']} | origem `{info['path']}`")
    write(TARGET / 'projects' / '_index.md', '\n'.join(projects_lines))

    def simple_index(title: str, items: list[Path], base: Path) -> str:
        lines = [f'# {title}', '', 'Resumo curto: indice navegavel do dominio.', '', '## Itens']
        for item in items:
            lines.append(f"- [{item.stem}](./{item.relative_to(base).as_posix()}): `{item}`")
        return '\n'.join(lines)

    write(TARGET / 'prompts' / '_index.md', simple_index('Prompts Index', prompt_docs, TARGET / 'prompts'))
    write(TARGET / 'datasets' / '_index.md', simple_index('Datasets Index', dataset_docs, TARGET / 'datasets'))
    write(TARGET / 'references' / '_index.md', simple_index('References Index', reference_docs, TARGET / 'references'))
    write(TARGET / 'assets' / '_index.md', simple_index('Assets Index', asset_docs, TARGET / 'assets'))
    write(TARGET / 'docs' / '_index.md', '# Docs Index\n\nResumo curto: indice das notas arquiteturais e sistêmicas.\n\n## Itens\n- [capy-project-patterns](./architecture/capy-project-patterns.md)\n- [operational-systems-overview](./systems/operational-systems-overview.md)\n- [ingestion-and-governance](./flows/ingestion-and-governance.md)\n- [design-system-signals](./ui-ux/design-system-signals.md)\n- [integration-signals](./api/integration-signals.md)')
    write(TARGET / 'archive' / '_index.md', '# Archive Index\n\nResumo curto: indice das referencias historicas e snapshots mantidos apenas como rastreio.\n\n## Observacoes\n- O conteudo bruto historico permanece fora do `capymind`.\n- Variantes e copias antigas aparecem em relatórios e filas de revisao, nao como estrutura oficial do repo.')


def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)

    for folder in [
        TARGET / 'knowledge' / 'business', TARGET / 'knowledge' / 'products', TARGET / 'knowledge' / 'operations', TARGET / 'knowledge' / 'technical',
        TARGET / 'knowledge' / 'commercial', TARGET / 'knowledge' / 'ai', TARGET / 'knowledge' / 'branding', TARGET / 'projects', TARGET / 'prompts' / 'generation',
        TARGET / 'prompts' / 'analysis', TARGET / 'prompts' / 'coding', TARGET / 'prompts' / 'image', TARGET / 'prompts' / 'business', TARGET / 'prompts' / 'marketing',
        TARGET / 'datasets' / 'structured', TARGET / 'datasets' / 'extracted', TARGET / 'datasets' / 'candidates', TARGET / 'docs' / 'architecture', TARGET / 'docs' / 'systems',
        TARGET / 'docs' / 'flows', TARGET / 'docs' / 'ui-ux', TARGET / 'docs' / 'api', TARGET / 'references' / 'technical', TARGET / 'references' / 'commercial',
        TARGET / 'references' / 'contracts', TARGET / 'references' / 'inspirations', TARGET / 'references' / 'external', TARGET / 'assets' / 'catalogs', TARGET / 'assets' / 'visual-assets',
        TARGET / 'assets' / 'product-assets', TARGET / 'assets' / 'diagrams', TARGET / 'archive', TARGET / 'scripts'
    ]:
        ensure(folder)

    projects = []
    used_slugs: set[str] = set()
    for project_path in detect_projects():
        info = project_payload(project_path, used_slugs)
        project_dir = TARGET / 'projects' / info['slug']
        for file_name, content in project_docs(info).items():
            write(project_dir / file_name, content)
        projects.append(info)

    prompt_docs = write_prompt_docs()
    dataset_docs = write_dataset_docs()
    reference_docs = write_reference_docs()
    asset_docs = write_asset_docs()
    write_indexes(projects, prompt_docs, dataset_docs, reference_docs, asset_docs)

    write(TARGET / 'knowledge' / 'overview.md', '# Knowledge Overview\n\nResumo curto: visao geral do corpus transformado em base de conhecimento leve.\n\n## Detectado\n- Projetos do ecossistema Capy, operacao Mercado Livre, prompt engineering e referencias tecnicas/comerciais.\n- O corpus contem duplicatas, variantes e ativos pesados fora do escopo de um repositrio Git leve.\n\n## Relevancia\n- Esta pagina introduz a navegacao pelo `capymind` e aponta para projetos, prompts, datasets e referencias.\n\n## Observacoes\n- Ver tambem [PROJECT_CATALOG.md](../PROJECT_CATALOG.md) e [KNOWLEDGE_MAP.md](../KNOWLEDGE_MAP.md).')
    write(TARGET / 'knowledge' / 'business' / 'mercado-livre-operations.md', '# Mercado Livre Operations\n\nResumo curto: panorama da operacao comercial detectada no corpus.\n\n## Origem\n- Caminho principal: `PROJETOS 2026/MERCADO LIVRE`\n\n## Detectado\n- Planilhas de taxa, gestao e desempenho.\n- Bases `anuncios.csv` e `produtos.csv`.\n- Documentos de vendas, ativos visuais e um projeto web dedicado em `PETALA DECOR`.\n\n## Inferido\n- O conjunto apoia cadastro, precificacao, anuncios, margem e acompanhamento comercial.\n\n## Relevancia\n- Este dominio conecta operacao real, catalogo, analytics e integracao com IA.\n\n## Observacoes\n- Os arquivos comerciais brutos nao foram copiados para o repositorio.')
    write(TARGET / 'knowledge' / 'products' / 'petala-decor-catalog-notes.md', '# Pétala Decor Catalog Notes\n\nResumo curto: notas sobre a linha de produtos e seu catalogo digital.\n\n## Origem\n- Caminhos principais: `PROJETOS 2026/MERCADO LIVRE/PETALA DECOR` e `PROJETOS 2026/MERCADO LIVRE/COFRES`\n\n## Detectado\n- Projeto Next.js com integracao Mercado Livre.\n- Colecoes de imagens de cofres, mockups e ativos promocionais.\n\n## Inferido\n- A marca usa o repositorio-fonte para operacao comercial, exibicao de catalogo e possivel sincronizacao de anuncios.\n\n## Relevancia\n- Serve como elo entre produto fisico, e-commerce e automacao documental.\n\n## Observacoes\n- Ver tambem [Pétala Decor Product Catalog](../../assets/catalogs/petala-decor-product-catalog.md).')
    write(TARGET / 'knowledge' / 'operations' / 'capy-ops-and-ml-workflows.md', '# Capy Ops and ML Workflows\n\nResumo curto: sinais operacionais recorrentes nos projetos ligados a CapyOps e workspace.\n\n## Detectado\n- Variantes de `capyops`, `capy-workspace` e `capypos`.\n- Auditorias de rota, TWA e UI reports em alguns snapshots.\n\n## Inferido\n- Existe um nucleo operacional com multiplas iteracoes para dashboard, rotina comercial e processos internos.\n\n## Relevancia\n- Orienta consolidacao de conhecimento sem transformar o `capymind` em monorepo.\n\n## Observacoes\n- Consolidacoes de versao devem ser decididas fora deste repositorio.')
    write(TARGET / 'knowledge' / 'technical' / 'capy-ecosystem-overview.md', '# Capy Ecosystem Overview\n\nResumo curto: padroes tecnicos recorrentes no ecossistema Capy.\n\n## Detectado\n- Predominio de React, Next.js, Vite, Tailwind, shadcn/ui e integracoes como Supabase.\n- Alguns projetos usam Electron ou Tauri para experiencia desktop.\n\n## Inferido\n- O ecossistema privilegia apps web modernos, paineis, agentes de IA e iteracoes rapidas de produto.\n\n## Relevancia\n- Ajuda a IA e equipes humanas a entender o padrao arquitetural dominante.\n\n## Observacoes\n- Ver tambem [capy-project-patterns](../../docs/architecture/capy-project-patterns.md).')
    write(TARGET / 'knowledge' / 'commercial' / 'marketplace-sales-materials.md', '# Marketplace Sales Materials\n\nResumo curto: materiais comerciais detectados ao redor da operacao de marketplace.\n\n## Detectado\n- PDFs, PPTX, DOCX, videos, mockups e arquivos de apoio comercial em `PROJETOS 2026/MERCADO LIVRE`.\n\n## Inferido\n- Parte do acervo serve a venda, treinamento, apresentacao e organizacao de anuncios.\n\n## Relevancia\n- O conhecimento comercial foi reduzido a indice e referencia para manter o repo leve.\n\n## Observacoes\n- Ativos pesados aparecem no `HEAVY_CONTENT_REPORT.md`.')
    write(TARGET / 'knowledge' / 'ai' / 'prompt-engineering-notes.md', '# Prompt Engineering Notes\n\nResumo curto: panorama da biblioteca de prompts e instrucoes encontradas no corpus.\n\n## Origem\n- Caminho principal: `knowledge/prompt-engineering`\n\n## Detectado\n- Guias extensos de engenharia de prompt.\n- Templates de function calling, agentes e visao para codigo.\n- Materiais de UX, design system e pesquisa com IA.\n\n## Inferido\n- O usuario mantem uma base de instrucoes reaproveitaveis para desenvolvimento, pesquisa e automacao.\n\n## Relevancia\n- Este e um dos nucleos mais fortes do `capymind` para uso por IA.\n\n## Observacoes\n- Ver tambem [prompts/_index.md](../../prompts/_index.md).')
    write(TARGET / 'knowledge' / 'branding' / 'brand-asset-signals.md', '# Brand Asset Signals\n\nResumo curto: sinais de identidade visual e ativos de marca encontrados.\n\n## Detectado\n- Lotes de imagens, mockups, renders e capturas em materiais comerciais e de prompt engineering.\n\n## Inferido\n- O corpus mistura produto, branding e operacao visual.\n\n## Relevancia\n- Indexa o tema sem duplicar bibliotecas de imagem.\n\n## Observacoes\n- Ver tambem [assets/_index.md](../../assets/_index.md).')

    write(TARGET / 'docs' / 'architecture' / 'capy-project-patterns.md', '# Capy Project Patterns\n\nResumo curto: padroes arquiteturais observados entre os projetos Capy.\n\n## Detectado\n- Next.js e Vite aparecem com frequencia.\n- Estruturas com `app`, `src`, `components`, `lib`, `hooks`, `services` e `docs/routes.json` sao recorrentes.\n- Variantes desktop via Electron/Tauri aparecem em projetos operacionais.\n\n## Relevancia\n- Ajuda na leitura cruzada dos projetos e na consolidacao de convencoes.\n\n## Observacoes\n- O objetivo aqui e documentar padroes, nao normalizar codigo automaticamente.')
    write(TARGET / 'docs' / 'systems' / 'operational-systems-overview.md', '# Operational Systems Overview\n\nResumo curto: sistemas operacionais e comerciais identificados no acervo.\n\n## Detectado\n- CapyOps, Capy Workspace, CapyPOS e Pétala Decor compoem o nucleo operacional mais claro.\n\n## Relevancia\n- Resume onde estao os sistemas com impacto direto em rotina, catalogo e vendas.\n\n## Observacoes\n- Alguns nomes existem em variantes duplicadas; a fila de revisao aponta essas situacoes.')
    write(TARGET / 'docs' / 'flows' / 'ingestion-and-governance.md', '# Ingestion and Governance\n\nResumo curto: regras praticas da ingestao aplicada neste rebuild.\n\n## Detectado\n- Somente markdowns e scripts leves entram na estrutura final.\n- Projetos inteiros, builds, dependencias e ativos pesados ficam fora.\n\n## Relevancia\n- Define o padrao de manutencao do `capymind`.\n\n## Observacoes\n- Novas ingestoes devem repetir a mesma disciplina para evitar contaminar o repositorio.')
    write(TARGET / 'docs' / 'ui-ux' / 'design-system-signals.md', '# Design System Signals\n\nResumo curto: sinais de UI kit, design system e padroes visuais.\n\n## Detectado\n- Tailwind, shadcn/ui, Radix UI e dashboards aparecem em varios projetos.\n- Materiais de prompt engineering reforcam direcao visual e templates de produto.\n\n## Relevancia\n- Apoia alinhamento entre documentacao, UX e prompts de geracao visual.\n\n## Observacoes\n- Ativos visuais completos permanecem na origem.')
    write(TARGET / 'docs' / 'api' / 'integration-signals.md', '# Integration Signals\n\nResumo curto: integracoes tecnicas visiveis no corpus.\n\n## Detectado\n- Supabase, Upstash Redis, Mercado Livre API, OAuth, TWA e auditorias de rota.\n\n## Relevancia\n- Permite localizar rapidamente projetos com dependencia de servicos externos.\n\n## Observacoes\n- Confirmacoes finais exigem leitura de configuracoes e ambiente fora deste repo.')

    heavy_dirs = [(info['path'], dir_size_mb(info['path']), info['slug']) for info in projects]
    heavy_dirs.sort(key=lambda item: item[1], reverse=True)
    heavy_files = find_heavy_files([ROOT / 'PROJETOS 2026' / 'MERCADO LIVRE', ROOT / 'knowledge' / 'prompt-engineering'])

    project_catalog_rows = ['| Nome | Slug | Dominio | Stack resumida | Origem | Documentacao |', '| --- | --- | --- | --- | --- | --- |']
    for info in projects:
        stack_line = ', '.join(info['stack']['frameworks'][:3] + info['stack']['libs'][:2]) or 'stack parcial'
        project_catalog_rows.append(f"| {info['name']} | `{info['slug']}` | {info['domain']} | {stack_line} | `{info['path']}` | [overview](./projects/{info['slug']}/overview.md) |")

    review_items = [
        '`projects/active/ops/Nova pasta` e `Nova pasta (2)` precisam de nome e papel confirmados.',
        '`PROJETOS 2026/CAPY2.0` contem muitas variantes e snapshots; exige consolidacao manual antes de entrar como catalogo principal.',
        '`fwefwef.txt` no root segue sem classificacao semantica util.',
        'Arquivos legados no root (`INVENTORY.md`, `MIGRATION_PLAN.md`, `MOVE_MAP.csv`, `PROPOSED_TREE.txt`, `RELOCATION_LOG.md`) ficaram fora do repo final e merecem decisao de descarte ou arquivo historico.',
    ]

    write(TARGET / 'README.md', '# capymind\n\nRepositorio leve de conhecimento derivado do ecossistema do usuario.\n\n## Neste estagio\n- O repo guarda markdowns navegaveis, indices, resumos e rastreabilidade.\n- Projetos completos, builds, dependencias e ativos pesados permanecem fora.\n\n## Entradas principais\n- [PROJECT_CATALOG.md](./PROJECT_CATALOG.md)\n- [KNOWLEDGE_MAP.md](./KNOWLEDGE_MAP.md)\n- [INVENTORY.md](./INVENTORY.md)\n- [HEAVY_CONTENT_REPORT.md](./HEAVY_CONTENT_REPORT.md)')
    write(TARGET / 'REPO_RULES.md', '# Repo Rules\n\n## Filosofia\n- Este repo nao guarda codigo completo.\n- Este repo guarda conhecimento derivado, indices e referencias.\n- Todo resumo deve apontar para a origem.\n\n## O que entra\n- Markdowns uteis, scripts leves e indices navegaveis.\n\n## O que nao entra\n- Projetos inteiros, `src/` completos, `node_modules`, `.next`, `dist`, `build`, `coverage`, videos, zips e lotes pesados de imagens.\n\n## Regra operacional\n- Sempre resumir, catalogar e referenciar antes de pensar em copiar qualquer coisa.')
    write(TARGET / 'PROJECT_CATALOG.md', '# Project Catalog\n\nResumo curto: catalogo dos projetos detectados e documentados.\n\n' + '\n'.join(project_catalog_rows))
    write(TARGET / 'KNOWLEDGE_MAP.md', '# Knowledge Map\n\nResumo curto: mapa navegavel do repositorio.\n\n## Conhecimento\n- [knowledge/overview.md](./knowledge/overview.md)\n- [Mercado Livre operations](./knowledge/business/mercado-livre-operations.md)\n- [Pétala Decor catalog](./knowledge/products/petala-decor-catalog-notes.md)\n- [Prompt engineering notes](./knowledge/ai/prompt-engineering-notes.md)\n\n## Projetos\n- [projects/_index.md](./projects/_index.md)\n\n## Prompts\n- [prompts/_index.md](./prompts/_index.md)\n\n## Datasets\n- [datasets/_index.md](./datasets/_index.md)\n\n## Docs\n- [docs/_index.md](./docs/_index.md)\n\n## References\n- [references/_index.md](./references/_index.md)\n\n## Assets\n- [assets/_index.md](./assets/_index.md)')
    write(TARGET / 'INGESTION_LOG.md', '# Ingestion Log\n\nResumo curto: decisoes relevantes tomadas na reconstrucao do repo.\n\n## Detectado\n- Projetos e snapshots pesados ficaram fora do repositrio final.\n- O foco foi em markdowns derivados, catalogos e caminhos de origem.\n- O escopo principal cobriu projetos Capy, Pétala Decor, operacao Mercado Livre e biblioteca de prompts.\n\n## Catalogado\n- Projetos documentados: ' + str(len(projects)) + '\n- Prompts catalogados: ' + str(len(prompt_docs)) + '\n- Datasets descritos: ' + str(len(dataset_docs)) + '\n\n## Ignorado\n- Pastas `node_modules`, `.next`, `dist`, `build`, `coverage`, videos e imagens pesadas.\n\n## Revisao\n- Ver [REVIEW_QUEUE.md](./REVIEW_QUEUE.md) para ambiguidades remanescentes.')
    write(TARGET / 'REVIEW_QUEUE.md', '# Review Queue\n\nResumo curto: itens que exigem decisao humana ou consolidacao extra.\n\n## Itens\n' + '\n'.join(f'- {item}' for item in review_items))
    heavy_lines = ['# Heavy Content Report', '', 'Resumo curto: conteudo pesado, inadequado ou incompatível com um repositorio leve.', '', '## Pastas pesadas tratadas como origem externa']
    for path, size_mb, slug in heavy_dirs[:25]:
        heavy_lines.append(f'- `{path}` | tamanho aproximado: {size_mb} MB | motivo: copia integral ou snapshot de aplicacao | substituicao leve: `projects/{slug}/`')
    heavy_lines.append('')
    heavy_lines.append('## Arquivos pesados ignorados')
    for file_path, size in heavy_files[:25]:
        heavy_lines.append(f'- `{file_path}` | {round(size / (1024 * 1024), 2)} MB | motivo: arquivo pesado fora do escopo documental leve')
    write(TARGET / 'HEAVY_CONTENT_REPORT.md', '\n'.join(heavy_lines))
    write(TARGET / 'INVENTORY.md', '# Inventory\n\nResumo curto: panorama do conteudo mapeado para o `capymind`.\n\n## Detectado\n- Projetos documentados: ' + str(len(projects)) + '\n- Prompts catalogados: ' + str(len(prompt_docs)) + '\n- Datasets descritos: ' + str(len(dataset_docs)) + '\n- Referencias registradas: ' + str(len(reference_docs)) + '\n- Catalogos de assets: ' + str(len(asset_docs)) + '\n- Itens pesados sinalizados: ' + str(len(heavy_dirs[:25]) + len(heavy_files[:25])) + '\n- Itens em revisao: ' + str(len(review_items)) + '\n\n## Panorama\n- O repositorio final prioriza conhecimento leve, navegavel e versionavel.\n- O corpus bruto permanece fora da estrutura oficial do repo.\n\n## Observacoes\n- O catalogo principal de projetos esta em [PROJECT_CATALOG.md](./PROJECT_CATALOG.md).')
    write(TARGET / '.gitignore', '# logs locais\nscripts/logs/\n\n# seguranca adicional\nnode_modules/\n.next/\ndist/\nbuild/\ncoverage/\n*.zip\n*.mp4\n*.png\n*.jpg\n*.jpeg\n*.webp\n*.pdf\n*.xlsx\n*.csv\n*.json\n*.db\n')
    write(TARGET / 'scripts' / 'organize_repo.ps1', POWERSHELL_SCRIPT)
    write(TARGET / 'scripts' / 'organize_repo.sh', BASH_SCRIPT)
    write(TARGET / 'scripts' / 'rebuild_capymind_markdown.py', read_text(Path(__file__)))

if __name__ == '__main__':
    main()
