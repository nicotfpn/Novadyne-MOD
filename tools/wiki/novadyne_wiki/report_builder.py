"""Montagem do relatório de catálogo (build/wiki/report.{json,md}) — Fase 3.

O relatório é derivado do próprio catálogo (garantindo consistência entre
relatório e catálogo) e das métricas de cobertura dos scanners. Nenhum
timestamp entra na saída comparada pelo modo ``--check``.
"""

from __future__ import annotations


def _counts(values: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        result[value] = result.get(value, 0) + 1
    return dict(sorted(result.items()))


def build_catalog_report(catalog: dict, scan_summary: dict | None = None) -> dict:
    """Deriva as estatísticas do relatório a partir do catálogo."""
    scan_summary = scan_summary or {}

    entries = catalog.get("entries", [])
    recipes = catalog.get("recipes", [])
    tags = catalog.get("tags", [])

    entries_by_type = _counts([e.get("type", "?") for e in entries])
    recipes_by_type = _counts([r.get("type", "?") for r in recipes])
    tags_by_registry = _counts([t.get("registry", "?") for t in tags])

    languages = list(catalog.get("generation", {}).get("languages", []))
    missing_translations = sorted(
        e["id"] for e in entries
        if e.get("type") in ("item", "block", "entity")
        and not e.get("translations")
    )
    missing_textures = sorted(
        e["id"] for e in entries
        if any("textura ausente" in w for w in e.get("warnings", []))
    )
    missing_models = sorted(
        e["id"] for e in entries if any("modelo ausente" in w or "registro sem modelo" in w
                                          for w in e.get("warnings", []))
    )
    broken_references = sorted(
        set(catalog.get("generation", {}).get("broken_references", []))
    )
    orphan_assets = sorted(
        set(catalog.get("generation", {}).get("orphan_assets", []))
    )
    unknown_recipe_types = sorted(
        set(catalog.get("generation", {}).get("unknown_recipe_types", []))
    )
    broken_tags = sorted(
        t["id"] for t in tags if t.get("missing_refs")
    )
    tag_cycles = sorted(
        t["id"] for t in tags if t.get("cycle")
    )

    return {
        "mod": catalog.get("mod", {}),
        "entries_total": len(entries),
        "entries_by_type": entries_by_type,
        "recipes_total": len(recipes),
        "recipes_by_type": recipes_by_type,
        "tags_total": len(tags),
        "tags_by_registry": tags_by_registry,
        "languages": languages,
        "missing_translations": missing_translations,
        "missing_textures": missing_textures,
        "missing_models": missing_models,
        "broken_references": broken_references,
        "orphan_assets": orphan_assets,
        "unknown_recipe_types": unknown_recipe_types,
        "broken_tags": broken_tags,
        "tag_cycles": tag_cycles,
        "unresolved_registrations": sorted(
            set(scan_summary.get("unresolved_registrations", []))
        ),
        "ignored_files": sorted(
            scan_summary.get("ignored_files", []),
            key=lambda item: item.get("path", ""),
        ),
        "scanner_coverage": dict(scan_summary.get("scanner_coverage", {})),
    }


def render_report_markdown(data: dict) -> str:
    """Renderiza o relatório completo em Markdown (parte do catálogo)."""
    lines: list[str] = []
    catalog = data.get("catalog", {})
    if not catalog:
        return ""

    lines.append("## Catálogo")
    lines.append("")
    lines.append(f"**Entradas:** {catalog['entries_total']}  ")
    lines.append(f"**Receitas:** {catalog['recipes_total']}  ")
    lines.append(f"**Tags:** {catalog['tags_total']}  ")
    lines.append("")
    lines.append("### Entradas por tipo")
    lines.append("")
    lines.append("| Tipo | Quantidade |")
    lines.append("|---|---|")
    for type_name, count in catalog["entries_by_type"].items():
        lines.append(f"| {type_name} | {count} |")
    lines.append("")
    lines.append("### Receitas por tipo")
    lines.append("")
    lines.append("| Tipo | Quantidade |")
    lines.append("|---|---|")
    for type_name, count in catalog["recipes_by_type"].items():
        lines.append(f"| {type_name} | {count} |")
    lines.append("")
    lines.append("### Tags por registry")
    lines.append("")
    lines.append("| Registry | Quantidade |")
    lines.append("|---|---|")
    for registry, count in catalog["tags_by_registry"].items():
        lines.append(f"| {registry} | {count} |")
    lines.append("")

    if catalog.get("languages"):
        lines.append("### Idiomas encontrados")
        lines.append("")
        for language in catalog["languages"]:
            lines.append(f"- {language}")
        lines.append("")

    sections = [
        ("missing_translations", "Traduções ausentes"),
        ("missing_textures", "Texturas ausentes"),
        ("missing_models", "Modelos ausentes"),
        ("broken_references", "Referências quebradas"),
        ("orphan_assets", "Assets órfãos"),
        ("unknown_recipe_types", "Tipos de receita desconhecidos"),
        ("broken_tags", "Tags quebradas"),
        ("tag_cycles", "Ciclos de tags"),
        ("unresolved_registrations", "Registros não resolvidos"),
    ]
    for key, label in sections:
        values = catalog.get(key) or []
        if not values:
            continue
        lines.append(f"### {label} ({len(values)})")
        lines.append("")
        for value in values:
            lines.append(f"- {value}")
        lines.append("")

    if catalog.get("ignored_files"):
        lines.append("### Arquivos ignorados")
        lines.append("")
        for item in catalog["ignored_files"]:
            reason = item.get("reason", "")
            where = f" `{item['path']}`" if item.get("path") else ""
            lines.append(f"-{where} {reason}")
        lines.append("")

    coverage = catalog.get("scanner_coverage") or {}
    if coverage:
        lines.append("### Cobertura por scanner")
        lines.append("")
        lines.append("| Scanner | Métrica | Valor |")
        lines.append("|---|---|---|")
        for scanner, metrics in sorted(coverage.items()):
            if not isinstance(metrics, dict):
                continue
            first = True
            for metric, value in sorted(metrics.items()):
                if isinstance(value, list):
                    value = ", ".join(str(item) for item in value)
                lines.append(f"| {scanner if first else ''} | {metric} | {value} |")
                first = False
        lines.append("")

    return "\n".join(lines) + "\n"
