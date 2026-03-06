import csv
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path

SOURCE_ROOT = Path(r"D:\novosproj")
OUTPUT_ROOT = SOURCE_ROOT / "capymind"
IGNORED_DIRS = {"node_modules", ".git", ".next", "dist", "build", "coverage", "release", "out", "bin", "obj", ".wrangler", ".turbo", ".cache", "vendor", "target", "__pycache__"}
HEAVY_SCAN_ROOTS = [SOURCE_ROOT / "projects", SOURCE_ROOT / "archive"]
LIGHT_SOURCE_DIRS = [SOURCE_ROOT / "knowledge", SOURCE_ROOT / "docs", SOURCE_ROOT / "prompts", SOURCE_ROOT / "datasets", SOURCE_ROOT / "data", SOURCE_ROOT / "schemas", SOURCE_ROOT / "references", SOURCE_ROOT / "scripts"]
MARKER_FILES = {"package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml", "requirements.txt", "docker-compose.yml", "docker-compose.yaml"}
MAX_TREE_LINES = 120
MAX_IMPORTANT_FILES = 12
MAX_DERIVED_SIZE = 300_000
MAX_HEAVY_FILES = 30


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clean_output_root() -> None:
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    ensure_dir(OUTPUT_ROOT)


_slug_counts = Counter()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-") or "project"
    _slug_counts[value] += 1
    return value if _slug_counts[value] == 1 else f"{value}-{_slug_counts[value]}"


def iter_files(path: Path, include_ignored: bool = False):
    for root, dirs, files in os.walk(path):
        if not include_ignored:
            dirs[:] = [item for item in dirs if item not in IGNORED_DIRS]
        for file_name in files:
            yield Path(root) / file_name


def dir_size(path: Path) -> int:
    total = 0
    for file_path in iter_files(path, include_ignored=False):
        try:
            total += file_path.stat().st_size
        except OSError:
            pass
    return total


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except Exception:
            return ""
    except Exception:
        return ""


def safe_write(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    encoded = content.encode("utf-8")
    if len(encoded) > MAX_DERIVED_SIZE:
        raise ValueError(f"Refusing to write oversized derived file: {path} ({len(encoded)} bytes)")
    path.write_text(content, encoding="utf-8", newline="\n")


def parse_package_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}


def detect_package_manager(project_root: Path) -> str:
    if (project_root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (project_root / "yarn.lock").exists():
        return "yarn"
    if (project_root / "bun.lock").exists() or (project_root / "bun.lockb").exists():
        return "bun"
    if (project_root / "package-lock.json").exists():
        return "npm"
    return "unknown"


def detect_languages(project_root: Path) -> list[str]:
    exts = Counter()
    for file_path in iter_files(project_root):
        suffix = file_path.suffix.lower()
        if suffix:
            exts[suffix] += 1
    languages = []
    if exts[".ts"] or exts[".tsx"]:
        languages.append("TypeScript")
    if exts[".js"] or exts[".jsx"]:
        languages.append("JavaScript")
    if exts[".py"]:
        languages.append("Python")
    if exts[".rs"]:
        languages.append("Rust")
    if exts[".go"]:
        languages.append("Go")
    if exts[".java"]:
        languages.append("Java")
    if exts[".cs"]:
        languages.append("C#")
    if not languages:
        languages.append("Unknown")
    return languages


def detect_stack(project_root: Path) -> dict:
    package_json = parse_package_json(project_root / "package.json")
    deps = set((package_json.get("dependencies") or {}).keys())
    deps |= set((package_json.get("devDependencies") or {}).keys())
    framework = []
    build_tool = []
    libs = []
    capabilities = []

    def add_once(container: list[str], value: str) -> None:
        if value and value not in container:
            container.append(value)

    if (project_root / "package.json").exists():
        add_once(framework, "Node.js")
    if "next" in deps or (project_root / "next.config.js").exists() or (project_root / "next.config.ts").exists():
        add_once(framework, "Next.js")
    if "react" in deps:
        add_once(framework, "React")
    if "vite" in deps or (project_root / "vite.config.ts").exists() or (project_root / "vite.config.js").exists():
        add_once(framework, "Vite")
        add_once(build_tool, "Vite")
    if "electron" in deps:
        add_once(framework, "Electron")
    if (project_root / "src-tauri").exists() or (project_root / "src-tauri" / "Cargo.toml").exists():
        add_once(framework, "Tauri")
        add_once(build_tool, "Cargo")
    if (project_root / "Cargo.toml").exists():
        add_once(framework, "Rust")
        add_once(build_tool, "Cargo")
    if (project_root / "go.mod").exists():
        add_once(framework, "Go")
    if (project_root / "pyproject.toml").exists() or (project_root / "requirements.txt").exists():
        add_once(framework, "Python")
    if (project_root / "docker-compose.yml").exists() or (project_root / "docker-compose.yaml").exists():
        add_once(build_tool, "Docker Compose")

    for candidate in ["tailwindcss", "supabase", "firebase", "prisma", "drizzle-orm", "zod", "redux", "@reduxjs/toolkit", "react-router-dom", "lucide-react", "axios", "openai", "@google/genai"]:
        if candidate in deps:
            libs.append(candidate)

    if (project_root / "app" / "api").exists() or (project_root / "src" / "app" / "api").exists() or (project_root / "server").exists() or (project_root / "api").exists() or (project_root / "functions").exists():
        capabilities.append("API")
    if (project_root / "supabase").exists() or (project_root / "prisma").exists() or (project_root / "migrations").exists() or (project_root / "src" / "db").exists():
        capabilities.append("Database")
    if any(token in deps for token in ["next-auth", "@supabase/supabase-js", "firebase-auth", "clerk", "auth0"]):
        capabilities.append("Auth")
    if any(token in str(project_root).lower() for token in ["dashboard", "admin", "ops"]):
        capabilities.append("Dashboard")
    if any(token in deps for token in ["@radix-ui/react-dialog", "tailwindcss", "antd", "@mui/material"]):
        capabilities.append("UI Kit")

    return {"framework": framework or ["Unknown"], "language": detect_languages(project_root), "build_tool": build_tool or ["Unknown"], "package_manager": detect_package_manager(project_root), "libs": libs[:8], "capabilities": capabilities, "package_json": package_json}


def detect_project_type(project_root: Path, stack: dict) -> str:
    frameworks = {item.lower() for item in stack["framework"]}
    project_name = project_root.name.lower()
    if "tauri" in frameworks or "electron" in frameworks:
        return "desktop-app"
    if "next.js" in frameworks or "react" in frameworks or "vite" in frameworks:
        return "web-app"
    if "python" in frameworks:
        return "python-app"
    if "go" in frameworks:
        return "go-service"
    if "rust" in frameworks:
        return "rust-app"
    if "portfolio" in project_name:
        return "portfolio-site"
    return "software-project"


def first_readme_excerpt(project_root: Path) -> str:
    for candidate in [project_root / "README.md", project_root / "readme.md"]:
        if candidate.exists():
            lines = [line.strip() for line in read_text(candidate).splitlines() if line.strip()]
            for line in lines[:20]:
                if not line.startswith("#"):
                    return line[:240]
            if lines:
                return lines[0][:240]
    return ""


def detect_entry_points(project_root: Path) -> list[str]:
    candidates = ["package.json", "README.md", "src/main.ts", "src/main.tsx", "src/index.ts", "src/index.tsx", "src/App.tsx", "app/page.tsx", "app/layout.tsx", "server/index.js", "server.js", "main.py", "Cargo.toml", "src-tauri/Cargo.toml", "docker-compose.yml", "docker-compose.yaml"]
    hits = []
    for rel in candidates:
        if (project_root / rel).exists():
            hits.append(rel.replace("\\", "/"))
    return hits[:8]


def collect_important_files(project_root: Path) -> list[dict]:
    candidates = [("package.json", "Defines project name, scripts, and dependencies."), ("README.md", "Summarizes intent and usage."), ("vite.config.ts", "Shows the Vite build pipeline."), ("vite.config.js", "Shows the Vite build pipeline."), ("next.config.js", "Shows the Next.js runtime config."), ("next.config.ts", "Shows the Next.js runtime config."), ("tsconfig.json", "Defines the TypeScript baseline."), ("tailwind.config.ts", "Captures the visual token and utility setup."), ("tailwind.config.js", "Captures the visual token and utility setup."), ("docker-compose.yml", "Describes local services and integrations."), ("docker-compose.yaml", "Describes local services and integrations."), ("Cargo.toml", "Declares the Rust crate and dependencies."), ("src-tauri/Cargo.toml", "Defines the desktop shell."), ("src/main.tsx", "Likely UI entry point."), ("src/main.ts", "Likely UI entry point."), ("src/App.tsx", "Likely root component."), ("app/page.tsx", "Likely home page."), ("app/layout.tsx", "Likely app shell."), ("server/index.js", "Likely server entry point."), ("main.py", "Likely Python entry point.")]
    results = []
    for rel, reason in candidates:
        path = project_root / rel
        if path.exists():
            results.append({"path": rel.replace("\\", "/"), "reason": reason})
    if len(results) < MAX_IMPORTANT_FILES:
        for extra in [project_root / "src" / "app", project_root / "src" / "components", project_root / "app" / "api", project_root / "supabase", project_root / "functions", project_root / "public", project_root / "src-tauri"]:
            if extra.exists():
                results.append({"path": extra.relative_to(project_root).as_posix(), "reason": "Key directory for architecture reading."})
            if len(results) >= MAX_IMPORTANT_FILES:
                break
    return results[:MAX_IMPORTANT_FILES]


def build_tree(project_root: Path) -> str:
    lines = [project_root.name + "/"]
    count = 1

    def walk(path: Path, prefix: str = "") -> None:
        nonlocal count
        if count >= MAX_TREE_LINES:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        except OSError:
            return
        entries = [entry for entry in entries if entry.name not in IGNORED_DIRS][:16]
        for idx, child in enumerate(entries):
            if count >= MAX_TREE_LINES:
                return
            connector = "└── " if idx == len(entries) - 1 else "├── "
            label = child.name + ("/" if child.is_dir() else "")
            lines.append(prefix + connector + label)
            count += 1
            if child.is_dir():
                extension = "    " if idx == len(entries) - 1 else "│   "
                walk(child, prefix + extension)

    walk(project_root)
    if count >= MAX_TREE_LINES:
        lines.append("... tree truncated ...")
    return "\n".join(lines) + "\n"


def infer_purpose(project_root: Path, excerpt: str, stack: dict) -> str:
    lower_name = project_root.name.lower().replace("-", " ")
    if "ops" in lower_name:
        return "Operational software focused on dashboards, internal flow, and integrations."
    if "portfolio" in lower_name:
        return "Institutional or personal portfolio website."
    if "chat" in lower_name or "jarvis" in lower_name or "ai" in lower_name:
        return "AI-oriented product with chat, assistant, or automation behavior."
    if "factory" in lower_name or "mes" in lower_name or "erp" in lower_name:
        return "Operational or industrial management system."
    if excerpt:
        return excerpt[:220]
    frameworks = ", ".join(stack["framework"])
    return f"Software project based on {frameworks}."


def generate_project_docs(project_root: Path, slug: str) -> dict:
    project_dir = OUTPUT_ROOT / "projects" / slug
    ensure_dir(project_dir)
    stack = detect_stack(project_root)
    excerpt = first_readme_excerpt(project_root)
    purpose = infer_purpose(project_root, excerpt, stack)
    detected_type = detect_project_type(project_root, stack)
    important_files = collect_important_files(project_root)
    entry_points = detect_entry_points(project_root)
    size_mb = dir_size(project_root) / (1024 * 1024)
    ai_hooks = []
    if "API" in stack["capabilities"]:
        ai_hooks.append("API routes are available for agents or automation.")
    if "Database" in stack["capabilities"]:
        ai_hooks.append("A data layer exists and can support indexing or copilots.")
    if any(token in project_root.name.lower() for token in ["chat", "ai", "jarvis"]):
        ai_hooks.append("The theme suggests a natural fit for prompts or assistant workflows.")
    if not ai_hooks:
        ai_hooks.append("Can receive structured docs, semantic indexing, and operational prompts.")
    manifest = {"project_name": project_root.name, "slug": slug, "original_path": str(project_root), "detected_type": detected_type, "main_stack": stack["framework"] + stack["language"], "important_files": [item["path"] for item in important_files], "entry_points": entry_points, "notes": purpose}
    readme = f"# {project_root.name}\n\n- Original path: `{project_root}`\n- Detected type: `{detected_type}`\n- Approx analyzed size: `{size_mb:.2f} MB` (excluding `node_modules` and ignored build folders)\n- Main stack: {', '.join(stack['framework'] + stack['language'])}\n\n{purpose}\n"
    stack_md = f"# Stack\n\n- Framework: {', '.join(stack['framework'])}\n- Language: {', '.join(stack['language'])}\n- Build tool: {', '.join(stack['build_tool'])}\n- Package manager: {stack['package_manager']}\n- Main libs: {', '.join(stack['libs']) if stack['libs'] else 'Not identified'}\n- Capabilities detected: {', '.join(stack['capabilities']) if stack['capabilities'] else 'Not identified'}\n"
    summary_md = f"# Summary\n\n{purpose}\n\n## Quick view\n- Project location: `{project_root}`.\n- Working classification: `{detected_type}`.\n- Likely entry points: {', '.join(entry_points) if entry_points else 'not confidently detected'}.\n- AI integration points: {' '.join(ai_hooks)}\n"
    important_md = "# Important Files\n\n"
    if important_files:
        for item in important_files:
            important_md += f"- `{item['path']}`: {item['reason']}\n"
    else:
        important_md += "- No standard key file detected; review the project root manually.\n"
    safe_write(project_dir / "README.md", readme)
    safe_write(project_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    safe_write(project_dir / "tree.txt", build_tree(project_root))
    safe_write(project_dir / "stack.md", stack_md)
    safe_write(project_dir / "summary.md", summary_md)
    safe_write(project_dir / "important-files.md", important_md)
    return {"name": project_root.name, "slug": slug, "path": project_root, "size_mb": round(size_mb, 2), "type": detected_type, "stack": stack, "purpose": purpose, "light_path": project_dir}


def count_light_materials() -> dict:
    stats = {"documents": 0, "prompts": 0, "datasets": 0, "jsons": 0}
    for root in LIGHT_SOURCE_DIRS:
        if not root.exists():
            continue
        for file_path in iter_files(root, include_ignored=False):
            suffix = file_path.suffix.lower()
            if root.name == "prompts":
                stats["prompts"] += 1
            elif root.name == "datasets":
                stats["datasets"] += 1
            elif suffix in {".json", ".jsonl", ".csv"}:
                stats["jsons"] += 1
            elif suffix in {".md", ".txt"}:
                stats["documents"] += 1
    return stats


def list_review_items() -> list[Path]:
    review_items = []
    known = {"capymind", "projects", "archive", "knowledge", "docs", "prompts", "datasets", "data", "schemas", "references", "scripts", "assets", ".gitignore", "build_capymind_temp.py"}
    for child in sorted(SOURCE_ROOT.iterdir(), key=lambda item: item.name.lower()):
        if child.name in known:
            continue
        if child.name.startswith("PROJETOS") or child.name.startswith("MAIS PROJETOS"):
            continue
        review_items.append(child)
    return review_items


def build_heavy_file_list(projects_info: list[dict]) -> list[tuple[int, Path]]:
    files = []
    for info in projects_info:
        for file_path in iter_files(info["path"], include_ignored=False):
            try:
                size = file_path.stat().st_size
            except OSError:
                continue
            if size >= 1_000_000:
                files.append((size, file_path))
    files.sort(reverse=True, key=lambda item: item[0])
    return files[:MAX_HEAVY_FILES]


def build_tree_overview(projects_info: list[dict]) -> str:
    tree_text = "capymind/\n"
    for name in ["README.md", "INVENTORY.md", "MIGRATION_PLAN.md", "CLEANUP_PLAN.md", "PROJECT_CATALOG.md", "REPO_RULES.md", "PROPOSED_TREE.txt", "FINAL_TREE.txt", "FILE_MANIFEST.csv", "HEAVY_CONTENT_REPORT.md", ".gitignore"]:
        tree_text += f"├── {name}\n"
    for folder in ["knowledge", "docs", "prompts", "datasets", "data", "schemas", "references", "indexes", "projects", "scripts", "archive"]:
        tree_text += f"├── {folder}/\n"
    tree_text += "\nprojects/\n"
    for info in projects_info[:40]:
        tree_text += f"├── {info['slug']}/\n"
        for file_name in ["README.md", "manifest.json", "tree.txt", "stack.md", "summary.md", "important-files.md"]:
            tree_text += f"│   ├── {file_name}\n"
    if len(projects_info) > 40:
        tree_text += "...\n"
    return tree_text


def generate_global_files(projects_info: list[dict], heavy_files: list[tuple[int, Path]], light_stats: dict, review_items: list[Path]) -> None:
    for folder in ["knowledge", "docs", "prompts", "datasets", "data", "schemas", "references", "indexes", "archive", "projects", "scripts"]:
        ensure_dir(OUTPUT_ROOT / folder)
    safe_write(OUTPUT_ROOT / "knowledge" / "README.md", "# Knowledge\n\nArea for notes, summaries, and derived knowledge.\n")
    safe_write(OUTPUT_ROOT / "docs" / "README.md", "# Docs\n\nDerived documentation without full project copies.\n")
    safe_write(OUTPUT_ROOT / "prompts" / "README.md", "# Prompts\n\nLight prompt base for reuse and automation.\n")
    safe_write(OUTPUT_ROOT / "datasets" / "README.md", "# Datasets\n\nSmall derived datasets and indexes.\n")
    safe_write(OUTPUT_ROOT / "data" / "README.md", "# Data\n\nSmall JSON, CSV, and manifest files.\n")
    safe_write(OUTPUT_ROOT / "schemas" / "README.md", "# Schemas\n\nSchemas and structural contracts derived from the corpus.\n")
    safe_write(OUTPUT_ROOT / "references" / "README.md", "# References\n\nPointers to original paths and legacy source areas.\n")
    safe_write(OUTPUT_ROOT / "indexes" / "README.md", "# Indexes\n\nGlobal indexes for navigation.\n")
    safe_write(OUTPUT_ROOT / "archive" / "README.md", "# Archive\n\nHistorical notes only, never full code dumps.\n")
    safe_write(OUTPUT_ROOT / "scripts" / "README.md", "# Scripts\n\nUtilities to rebuild the light knowledge base.\n")
    safe_write(OUTPUT_ROOT / "README.md", f"# capymind\n\nLightweight knowledge base for documentation, AI workflows, and automation.\n\n## Principles\n- No full source code copies.\n- Only summaries, manifests, trees, indexes, and references.\n- Keeps the repository commit-ready for GitHub.\n\n## Current scope\n- Heavy projects cataloged: {len(projects_info)}\n- Heavy files flagged (>1 MB, outside ignored folders): {len(heavy_files)}\n- Manual review items: {len(review_items)}\n")
    safe_write(OUTPUT_ROOT / "INVENTORY.md", f"# INVENTORY\n\n- Heavy projects detected: {len(projects_info)}\n- Light documents found in source areas: {light_stats['documents']}\n- Prompts found: {light_stats['prompts']}\n- Datasets found: {light_stats['datasets']}\n- Small JSON/CSV files found: {light_stats['jsons']}\n- Heavy files ignored/flagged: {len(heavy_files)}\n- Review items: {len(review_items)}\n\n## Analyzed scope\n- `projects/`: main contamination area with copied projects.\n- `archive/`: legacy versions that also should not remain as official structure.\n- `knowledge/`, `docs/`, `prompts/`, `datasets/`, `data/`, `schemas/`, `references/`, and `scripts/`: treated as light context sources.\n")
    safe_write(OUTPUT_ROOT / "MIGRATION_PLAN.md", "# MIGRATION PLAN\n\n## Applied logic\n- Detect heavy project copies inside the current repository shape.\n- Generate one light representation per project in `projects/<slug>/`.\n- Keep only derived documentation, manifests, trees, and references.\n- Exclude full copies, installed dependencies, and build output from the final structure.\n\n## Classification rules\n- `summarize`: create README, summary, and stack notes for projects.\n- `index`: generate catalogs, inventories, and manifests.\n- `catalog`: register metadata and source paths.\n- `reference`: point to original locations without copying content.\n- `ignore`: keep heavy, binary, and generated artifacts out of the light repo.\n- `review`: register ambiguous items for manual follow-up.\n")
    safe_write(OUTPUT_ROOT / "CLEANUP_PLAN.md", "# CLEANUP PLAN\n\n## Sanitization strategy\n1. Treat `projects/` and `archive/versions/` as contaminated areas.\n2. Preserve only the light representation in `capymind/projects/`.\n3. Do not promote full copies as official repository structure.\n4. Remove heavy copies in a later manual cleanup step after validation.\n\n## Correct final structure\n- Top level with README, reports, manifests, and light directories only.\n- `projects/<slug>/` with exactly six derived files per project.\n- `archive/` reserved for notes, never raw project dumps.\n")
    safe_write(OUTPUT_ROOT / "REPO_RULES.md", "# REPO RULES\n\n- This repo does not keep full code copies.\n- This repo keeps derived knowledge, manifests, summaries, and references.\n- Heavy copies must stay out of the official structure.\n- `node_modules`, builds, caches, heavy assets, binaries, and databases do not enter.\n- Derived files must stay small, readable, and versionable.\n")
    tree_text = build_tree_overview(projects_info)
    safe_write(OUTPUT_ROOT / "PROPOSED_TREE.txt", tree_text)
    safe_write(OUTPUT_ROOT / "FINAL_TREE.txt", tree_text)
    catalog = "# PROJECT CATALOG\n\n"
    for info in projects_info:
        stack_line = ", ".join(info["stack"]["framework"] + info["stack"]["language"])
        catalog += f"## {info['name']}\n- slug: `{info['slug']}`\n- original path: `{info['path']}`\n- stack: {stack_line}\n- purpose: {info['purpose']}\n- status: `heavy-copy-documented`\n- light folder: `projects/{info['slug']}`\n\n"
    safe_write(OUTPUT_ROOT / "PROJECT_CATALOG.md", catalog)
    heavy_report = "# HEAVY CONTENT REPORT\n\n## Heavy project folders detected\n"
    for info in projects_info:
        heavy_report += f"- Heavy folder: `{info['path']}`\n  Approx size: `{info['size_mb']:.2f} MB` (excluding `node_modules` and ignored build folders)\n  Reason: a full project copy should not remain inside a lightweight knowledge repo.\n  Light replacement: `projects/{info['slug']}`\n"
    heavy_report += "\n## Heavy files observed\n"
    if heavy_files:
        for size, path in heavy_files:
            heavy_report += f"- `{path}`: `{size / (1024 * 1024):.2f} MB`\n"
    else:
        heavy_report += "- No files above 1 MB outside ignored directories.\n"
    safe_write(OUTPUT_ROOT / "HEAVY_CONTENT_REPORT.md", heavy_report)
    with (OUTPUT_ROOT / "FILE_MANIFEST.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["origem", "tipo", "classificacao", "acao", "destino", "motivo"])
        for info in projects_info:
            writer.writerow([str(info["path"]), info["type"], "project", "summarize", f"projects/{info['slug']}", "Replaced by a lightweight knowledge representation."])
            writer.writerow([str(info["path"]), info["type"], "project", "reference", f"projects/{info['slug']}/manifest.json", "Original path kept only as a pointer."])
        for root in LIGHT_SOURCE_DIRS:
            if root.exists():
                writer.writerow([str(root), "light-directory", root.name, "catalog", f"indexes/{root.name}-index.md", "Cataloged as an existing light content area."])
        for path in review_items:
            writer.writerow([str(path), "unclassified", "review", "review", "indexes/review-items.md", "Item falls outside the main taxonomy."])
    references_md = "# Source References\n\n## Existing light areas\n"
    for root in LIGHT_SOURCE_DIRS:
        if root.exists():
            references_md += f"- `{root}`\n"
    references_md += "\n## Contaminated areas\n"
    for root in HEAVY_SCAN_ROOTS:
        if root.exists():
            references_md += f"- `{root}`\n"
    safe_write(OUTPUT_ROOT / "references" / "source-paths.md", references_md)
    review_md = "# Review Items\n\n"
    if review_items:
        for item in review_items:
            review_md += f"- `{item}`\n"
    else:
        review_md += "- No manual review items.\n"
    safe_write(OUTPUT_ROOT / "indexes" / "review-items.md", review_md)
    light_index = "# Light Source Index\n\n"
    for root in LIGHT_SOURCE_DIRS:
        if not root.exists():
            continue
        files = list(iter_files(root, include_ignored=False))
        light_index += f"## {root.name}\n- path: `{root}`\n- files detected: {len(files)}\n"
        for file_path in files[:12]:
            light_index += f"- `{file_path}`\n"
        if len(files) > 12:
            light_index += f"- ... +{len(files) - 12} files\n"
        light_index += "\n"
    safe_write(OUTPUT_ROOT / "indexes" / "light-source-index.md", light_index)
    gitignore = "\n".join(["node_modules/", ".next/", "dist/", "build/", "coverage/", "release/", "out/", "*.zip", "*.exe", "*.dll", "*.bin", "*.pdf", "*.mp4", "*.mov", "*.sqlite", "*.db", "*.tar", "*.gz", "*.7z", "*.rar", ".env", ".env.*", ".DS_Store", "Thumbs.db", ""])
    safe_write(OUTPUT_ROOT / ".gitignore", gitignore)


def detect_heavy_projects() -> list[Path]:
    project_roots = []
    for scan_root in HEAVY_SCAN_ROOTS:
        if not scan_root.exists():
            continue
        for root, dirs, files in os.walk(scan_root):
            dirs[:] = [item for item in dirs if item not in IGNORED_DIRS]
            file_names = set(files)
            has_csproj = any(file_name.endswith(".sln") or file_name.endswith(".csproj") for file_name in file_names)
            if file_names.intersection(MARKER_FILES) or has_csproj:
                project_roots.append(Path(root))
                dirs[:] = []
    return sorted(project_roots)


def main() -> None:
    script_source = Path(__file__).read_text(encoding="utf-8")
    clean_output_root()
    projects = detect_heavy_projects()
    projects_info = []
    for project_root in projects:
        slug = slugify(project_root.name)
        projects_info.append(generate_project_docs(project_root, slug))
    light_stats = count_light_materials()
    review_items = list_review_items()
    heavy_files = build_heavy_file_list(projects_info)
    generate_global_files(projects_info, heavy_files, light_stats, review_items)
    safe_write(OUTPUT_ROOT / "scripts" / "build_capymind.py", script_source)
    summary = {"projects": len(projects_info), "heavy_files": len(heavy_files), "review_items": len(review_items), "output_root": str(OUTPUT_ROOT)}
    safe_write(OUTPUT_ROOT / "data" / "build-summary.json", json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
