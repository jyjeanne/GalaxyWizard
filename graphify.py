# Copyright (C) 2026 Jeremy Jeanne <jyjeanne@gmail.com>
#
# This file is part of GalaxyWizard.
#
# GalaxyWizard is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""Graphify: build an AI-ready knowledge graph of the GalaxyWizard codebase.

Statically analyses the source tree with the stdlib ``ast`` module (no
third-party dependencies) and produces two artifacts:

* ``doc/graph/knowledge_graph.json`` — a machine-readable knowledge graph
  (packages, modules, classes, functions and the imports / inherits /
  uses relations between them) designed to be fed to AI assistants,
  graph databases or visualization tools.
* ``doc/knowledge-graph.md`` — a human-readable architecture report with
  Mermaid diagrams that render directly in the GitHub web UI.

Usage::

    poetry run galaxywizard-graphify
    # or
    python graphify.py
"""

import ast
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = REPO_ROOT / "src"
DOC_DIR = REPO_ROOT / "doc"
GRAPH_DIR = DOC_DIR / "graph"
GRAPH_JSON = GRAPH_DIR / "knowledge_graph.json"
REPORT_MD = DOC_DIR / "knowledge-graph.md"

SCHEMA = "galaxywizard-knowledge-graph/1"

# Directories under src/ that are not application code (data files are
# exec()'d DSL scripts, test is legacy scaffolding — see the matching
# excludes in pyproject.toml; assets and locale hold no Python).
EXCLUDED_DIRS = {"data", "test", "assets", "locale"}

# Package shown for the top-level src/*.py modules in aggregated views,
# matching the "core" grouping used by generate_uml.py.
CORE_PACKAGE = "core"


class ClassInfo:
    def __init__(self, module: str, name: str, node: ast.ClassDef):
        self.module = module
        self.name = name
        self.qualname = f"{module}.{name}"
        self.doc = first_doc_line(ast.get_docstring(node))
        self.lineno = node.lineno
        self.bases = node.bases  # resolved after all modules are parsed
        self.methods = [
            n.name
            for n in node.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]


class ModuleInfo:
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.package = name.split(".")[0] if "." in name else CORE_PACKAGE
        self.doc = ""
        self.loc = 0
        self.classes: list[ClassInfo] = []
        self.functions: list[str] = []
        self.internal_imports: set[str] = set()
        self.external_imports: set[str] = set()
        # Local name -> fully qualified internal target: either a module
        # ("engine.Unit") or a name inside one ("engine.Unit.Unit").
        self.bindings: dict[str, str] = {}
        self.tree: ast.Module | None = None


def first_doc_line(doc: str | None) -> str:
    if not doc:
        return ""
    return doc.strip().splitlines()[0].strip()


def discover_modules() -> dict[str, ModuleInfo]:
    """Map dotted module names (relative to src/) to ModuleInfo objects."""
    modules: dict[str, ModuleInfo] = {}
    for path in sorted(SRC_DIR.rglob("*.py")):
        rel = path.relative_to(SRC_DIR)
        if rel.parts[0] in EXCLUDED_DIRS:
            continue
        if rel.name == "__init__.py":
            # Package markers are all empty in this codebase.
            continue
        name = ".".join(rel.with_suffix("").parts)
        modules[name] = ModuleInfo(name, path)
    return modules


def parse_module(info: ModuleInfo, module_names: set[str]) -> None:
    """Fill *info* with docstring, definitions and import edges."""
    source = info.path.read_text(encoding="utf-8")
    info.loc = sum(1 for line in source.splitlines() if line.strip())
    tree = ast.parse(source, filename=str(info.path))
    info.tree = tree
    info.doc = first_doc_line(ast.get_docstring(tree))

    internal_roots = {n.split(".")[0] for n in module_names}

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            info.classes.append(ClassInfo(info.name, node.name, node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info.functions.append(node.name)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root not in internal_roots:
                    info.external_imports.add(root)
                    continue
                # `import engine.Unit` targets the submodule; plain
                # `import util` targets the module itself.
                target = alias.name if alias.name in module_names else root
                if target in module_names:
                    info.internal_imports.add(target)
                info.bindings[alias.asname or root] = target
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                # The codebase imports relative to src/ (absolute style);
                # relative imports do not occur in practice.
                continue
            base = node.module or ""
            root = base.split(".")[0]
            if root not in internal_roots:
                info.external_imports.add(root)
                continue
            for alias in node.names:
                submodule = f"{base}.{alias.name}"
                if submodule in module_names:
                    # from engine import Unit  ->  module engine.Unit
                    info.internal_imports.add(submodule)
                    info.bindings[alias.asname or alias.name] = submodule
                elif base in module_names:
                    # from engine.Unit import Unit  ->  class in a module
                    info.internal_imports.add(base)
                    info.bindings[alias.asname or alias.name] = submodule


def resolve_class(
    ref: ast.expr, info: ModuleInfo, classes: dict[str, ClassInfo]
) -> str | None:
    """Resolve an AST expression to an internal class qualname, if any."""
    if isinstance(ref, ast.Name):
        local = f"{info.name}.{ref.id}"
        if local in classes:
            return local
        target = info.bindings.get(ref.id)
        if target in classes:
            return target
    elif isinstance(ref, ast.Attribute) and isinstance(ref.value, ast.Name):
        module = info.bindings.get(ref.value.id)
        if module:
            qualname = f"{module}.{ref.attr}"
            if qualname in classes:
                return qualname
    return None


def external_name(ref: ast.expr) -> str | None:
    """Render an AST base-class expression as dotted text, if simple."""
    if isinstance(ref, ast.Name):
        return ref.id
    if isinstance(ref, ast.Attribute):
        value = external_name(ref.value)
        return f"{value}.{ref.attr}" if value else None
    return None


def build_graph(modules: dict[str, ModuleInfo]) -> dict:
    """Assemble the knowledge-graph dict from parsed modules."""
    classes = {c.qualname: c for m in modules.values() for c in m.classes}
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_edges: set[tuple[str, str, str]] = set()

    def add_edge(kind: str, source: str, target: str) -> None:
        key = (kind, source, target)
        if key not in seen_edges:
            seen_edges.add(key)
            edges.append({"kind": kind, "source": source, "target": target})

    packages = sorted({m.package for m in modules.values()})
    for package in packages:
        nodes.append(
            {
                "id": f"package:{package}",
                "kind": "package",
                "name": package,
                "path": "src" if package == CORE_PACKAGE else f"src/{package}",
            }
        )

    for info in modules.values():
        nodes.append(
            {
                "id": f"module:{info.name}",
                "kind": "module",
                "name": info.name,
                "package": info.package,
                "path": str(info.path.relative_to(REPO_ROOT)),
                "doc": info.doc,
                "loc": info.loc,
                "external_imports": sorted(info.external_imports),
            }
        )
        add_edge("contains", f"package:{info.package}", f"module:{info.name}")
        for target in sorted(info.internal_imports):
            if target != info.name:
                add_edge("imports", f"module:{info.name}", f"module:{target}")

        for func in info.functions:
            nodes.append(
                {
                    "id": f"function:{info.name}.{func}",
                    "kind": "function",
                    "name": func,
                    "module": info.name,
                }
            )
            add_edge(
                "contains", f"module:{info.name}", f"function:{info.name}.{func}"
            )

    for cls in classes.values():
        info = modules[cls.module]
        bases_internal: list[str] = []
        bases_external: list[str] = []
        for base in cls.bases:
            resolved = resolve_class(base, info, classes)
            if resolved:
                bases_internal.append(resolved)
            else:
                text = external_name(base)
                if text and text != "object":
                    bases_external.append(text)
        nodes.append(
            {
                "id": f"class:{cls.qualname}",
                "kind": "class",
                "name": cls.name,
                "module": cls.module,
                "doc": cls.doc,
                "line": cls.lineno,
                "methods": cls.methods,
                "external_bases": bases_external,
            }
        )
        add_edge("contains", f"module:{cls.module}", f"class:{cls.qualname}")
        for parent in bases_internal:
            add_edge("inherits", f"class:{cls.qualname}", f"class:{parent}")

    # "uses" edges: a module references a class defined in another module.
    for info in modules.values():
        assert info.tree is not None
        for node in ast.walk(info.tree):
            if isinstance(node, (ast.Name, ast.Attribute)):
                qualname = resolve_class(node, info, classes)
                if qualname and classes[qualname].module != info.name:
                    add_edge("uses", f"module:{info.name}", f"class:{qualname}")

    external_usage: dict[str, int] = defaultdict(int)
    for info in modules.values():
        for dep in info.external_imports:
            external_usage[dep] += 1

    return {
        "schema": SCHEMA,
        "generated_by": "graphify.py",
        "project": "GalaxyWizard",
        "stats": {
            "packages": len(packages),
            "modules": len(modules),
            "classes": len(classes),
            "functions": sum(len(m.functions) for m in modules.values()),
            "methods": sum(len(c.methods) for c in classes.values()),
            "lines_of_code": sum(m.loc for m in modules.values()),
            "external_dependencies": dict(
                sorted(external_usage.items(), key=lambda kv: (-kv[1], kv[0]))
            ),
        },
        "edge_kinds": {
            "contains": "structural ownership (package>module>class/function)",
            "imports": "source module imports target module",
            "inherits": "source class subclasses target class",
            "uses": "source module references target class",
        },
        "nodes": nodes,
        "edges": edges,
    }


def mermaid_id(name: str) -> str:
    return name.replace(".", "_")


def package_diagram(graph: dict) -> str:
    """Mermaid graph of package-level dependencies, weighted by imports."""
    module_pkg = {
        n["name"]: n["package"] for n in graph["nodes"] if n["kind"] == "module"
    }
    weights: dict[tuple[str, str], int] = defaultdict(int)
    for edge in graph["edges"]:
        if edge["kind"] != "imports":
            continue
        src = module_pkg[edge["source"].removeprefix("module:")]
        dst = module_pkg[edge["target"].removeprefix("module:")]
        if src != dst:
            weights[(src, dst)] += 1
    lines = ["graph LR"]
    for pkg in sorted({p for pair in weights for p in pair} | set(module_pkg.values())):
        lines.append(f"    {mermaid_id(pkg)}[{pkg}]")
    for (src, dst), count in sorted(weights.items()):
        lines.append(f"    {mermaid_id(src)} -->|{count}| {mermaid_id(dst)}")
    return "\n".join(lines)


def inheritance_diagram(graph: dict) -> str:
    """Mermaid graph of the internal class hierarchy (child --> parent)."""
    lines = ["graph BT"]
    involved: set[str] = set()
    edges = [e for e in graph["edges"] if e["kind"] == "inherits"]
    for edge in edges:
        involved.add(edge["source"])
        involved.add(edge["target"])
    for node_id in sorted(involved):
        qualname = node_id.removeprefix("class:")
        lines.append(f'    {mermaid_id(qualname)}["{qualname}"]')
    for edge in sorted(edges, key=lambda e: (e["source"], e["target"])):
        src = mermaid_id(edge["source"].removeprefix("class:"))
        dst = mermaid_id(edge["target"].removeprefix("class:"))
        lines.append(f"    {src} --> {dst}")
    return "\n".join(lines)


def md_cell(text: str, limit: int = 90) -> str:
    text = text.replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def build_report(graph: dict) -> str:
    stats = graph["stats"]
    modules = [n for n in graph["nodes"] if n["kind"] == "module"]
    classes = [n for n in graph["nodes"] if n["kind"] == "class"]

    fan_in: dict[str, int] = defaultdict(int)
    fan_out: dict[str, int] = defaultdict(int)
    for edge in graph["edges"]:
        if edge["kind"] == "imports":
            fan_out[edge["source"].removeprefix("module:")] += 1
            fan_in[edge["target"].removeprefix("module:")] += 1

    parts = [
        "# GalaxyWizard Knowledge Graph\n",
        "\n<!-- This file is AUTO-GENERATED by graphify.py — do not edit by hand.\n"
        "     Regenerate with: poetry run galaxywizard-graphify -->\n",
        "\nAn automatically generated knowledge graph and architecture report of\n"
        "the GalaxyWizard codebase. The machine-readable graph (for AI\n"
        "assistants, graph databases or visualization tools) lives in\n"
        "[`doc/graph/knowledge_graph.json`](graph/knowledge_graph.json);\n"
        "this page is the human-readable summary. For pyreverse UML class\n"
        "diagrams see [architecture.md](architecture.md).\n",
        "\nTo regenerate after changing the code:\n\n"
        "```bash\npoetry run galaxywizard-graphify\n```\n",
    ]

    parts.append("\n## Codebase at a glance\n\n")
    parts.append("| Metric | Count |\n|---|---|\n")
    for label, key in [
        ("Packages", "packages"),
        ("Modules", "modules"),
        ("Classes", "classes"),
        ("Top-level functions", "functions"),
        ("Methods", "methods"),
        ("Non-blank lines of code", "lines_of_code"),
    ]:
        parts.append(f"| {label} | {stats[key]} |\n")
    externals = ", ".join(
        f"`{name}` ({count})"
        for name, count in stats["external_dependencies"].items()
    )
    parts.append(f"\nExternal dependencies by importing-module count: {externals}.\n")

    parts.append(
        "\n## Package dependencies\n\n"
        "Import relationships aggregated to package level. An arrow\n"
        "`A -->|n| B` means *n modules in A import modules in B*\n"
        "(`core` groups the top-level `src/*.py` modules).\n\n"
        f"```mermaid\n{package_diagram(graph)}\n```\n"
    )

    parts.append(
        "\n## Class inheritance\n\n"
        "Internal class hierarchy — an arrow `Child --> Parent` means\n"
        "*Child subclasses Parent*. Classes whose only base is `object` or\n"
        "an external library class are omitted (external bases are listed\n"
        "per class in the JSON graph).\n\n"
        f"```mermaid\n{inheritance_diagram(graph)}\n```\n"
    )

    parts.append(
        "\n## Key modules\n\n"
        "Modules ranked by how many other modules import them (fan-in) —\n"
        "changes here have the widest impact.\n\n"
        "| Module | Imported by | Imports | Classes | LOC |\n"
        "|---|---|---|---|---|\n"
    )
    class_count = defaultdict(int)
    for cls in classes:
        class_count[cls["module"]] += 1
    ranked = sorted(
        modules, key=lambda m: (-fan_in[m["name"]], -fan_out[m["name"]], m["name"])
    )
    for mod in ranked[:10]:
        name = mod["name"]
        parts.append(
            f"| `{name}` | {fan_in[name]} | {fan_out[name]} "
            f"| {class_count[name]} | {mod['loc']} |\n"
        )

    parts.append("\n## Module inventory\n")
    by_package: dict[str, list[dict]] = defaultdict(list)
    for mod in modules:
        by_package[mod["package"]].append(mod)
    for package in sorted(by_package):
        path = "src" if package == CORE_PACKAGE else f"src/{package}"
        parts.append(f"\n### `{package}` ({path})\n\n")
        parts.append("| Module | Classes | LOC | Summary |\n|---|---|---|---|\n")
        for mod in sorted(by_package[package], key=lambda m: m["name"]):
            names = ", ".join(
                c["name"] for c in classes if c["module"] == mod["name"]
            )
            parts.append(
                f"| `{mod['name']}` | {md_cell(names, 60)} | {mod['loc']} "
                f"| {md_cell(mod['doc'])} |\n"
            )

    return "".join(parts)


def main() -> None:
    modules = discover_modules()
    if not modules:
        raise SystemExit(f"No Python modules found under {SRC_DIR}")
    print(f"Analyzing {len(modules)} modules under src/ ...")
    module_names = set(modules)
    for info in modules.values():
        parse_module(info, module_names)

    graph = build_graph(modules)
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_JSON.write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote {GRAPH_JSON.relative_to(REPO_ROOT)} "
        f"({len(graph['nodes'])} nodes, {len(graph['edges'])} edges)"
    )

    REPORT_MD.write_text(build_report(graph), encoding="utf-8")
    print(f"Wrote {REPORT_MD.relative_to(REPO_ROOT)}")
    print("Done. View doc/knowledge-graph.md on GitHub for the rendered report.")


if __name__ == "__main__":
    sys.exit(main())
