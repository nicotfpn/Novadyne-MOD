"""Coletor de avisos/erros e geração de relatório (JSON + Markdown)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .errors import Issue
from .io_utils import write_text_atomic


@dataclass
class ReportStats:
    discovered: list[str] = field(default_factory=list)
    pages_created: list[str] = field(default_factory=list)
    pages_updated: list[str] = field(default_factory=list)
    pages_removed: list[str] = field(default_factory=list)
    missing_descriptions: list[str] = field(default_factory=list)
    missing_translations: list[str] = field(default_factory=list)
    missing_textures: list[str] = field(default_factory=list)
    missing_models: list[str] = field(default_factory=list)
    unknown_types: list[str] = field(default_factory=list)
    broken_links: list[str] = field(default_factory=list)


class Reporter:
    """Registra issues e estatísticas e produz build/wiki/report.{json,md}."""

    def __init__(self, strict: bool = False, verbose: bool = False, acknowledged: list[str] | None = None):
        self.strict = strict
        self.verbose = verbose
        self.acknowledged = set(acknowledged) if acknowledged else set()
        self.issues: list[Issue] = []
        self.stats = ReportStats()
        self.catalog_report: dict | None = None

    def set_catalog_report(self, data: dict) -> None:
        """Anexa o relatório derivado do catálogo (Fase 3)."""
        self.catalog_report = data

    # -- issues -----------------------------------------------------------

    def warning(self, message: str, *, path: str | None = None, context: str | None = None) -> None:
        self.issues.append(Issue("warning", message, path, context))

    def error(self, message: str, *, path: str | None = None, context: str | None = None) -> None:
        self.issues.append(Issue("error", message, path, context))

    # -- stats ------------------------------------------------------------

    def note_discovered(self, entry_id: str) -> None:
        self.stats.discovered.append(entry_id)

    def note_page_created(self, rel: str) -> None:
        self.stats.pages_created.append(rel)

    def note_page_updated(self, rel: str) -> None:
        self.stats.pages_updated.append(rel)

    def note_page_removed(self, rel: str) -> None:
        self.stats.pages_removed.append(rel)

    def note_missing_description(self, entry_id: str) -> None:
        self.stats.missing_descriptions.append(entry_id)

    def note_missing_translation(self, key: str) -> None:
        self.stats.missing_translations.append(key)

    def note_missing_texture(self, entry_id: str) -> None:
        self.stats.missing_textures.append(entry_id)

    def note_missing_model(self, entry_id: str) -> None:
        self.stats.missing_models.append(entry_id)

    def note_unknown_type(self, type_name: str, source: str) -> None:
        self.stats.unknown_types.append(f"{type_name} ({source})")

    def note_broken_link(self, link: str) -> None:
        self.stats.broken_links.append(link)

    # -- resumo -----------------------------------------------------------

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def ok(self) -> bool:
        """Sem erros; em modo estrito, também sem avisos não reconhecidos."""
        if self.errors:
            return False
        if self.strict:
            unacknowledged_warnings = [w for w in self.warnings if w.message not in self.acknowledged]
            if unacknowledged_warnings:
                return False
        return True

    def issues_for_report(self) -> list[dict]:
        return [{"severity": i.severity, "message": i.message, "path": i.path} for i in self.issues]

    def write_report(self, build_dir: Path) -> None:
        data = {
            "ok": self.ok,
            "strict": self.strict,
            "acknowledged": sorted(self.acknowledged),
            "stats": {
                "discovered": sorted(set(self.stats.discovered)),
                "pages_created": sorted(set(self.stats.pages_created)),
                "pages_updated": sorted(set(self.stats.pages_updated)),
                "pages_removed": sorted(set(self.stats.pages_removed)),
                "missing_descriptions": sorted(set(self.stats.missing_descriptions)),
                "missing_translations": sorted(set(self.stats.missing_translations)),
                "missing_textures": sorted(set(self.stats.missing_textures)),
                "missing_models": sorted(set(self.stats.missing_models)),
                "unknown_types": sorted(set(self.stats.unknown_types)),
                "broken_links": sorted(set(self.stats.broken_links)),
            },
            "issues": self.issues_for_report(),
            "summary": {
                "warnings": len(self.warnings),
                "errors": len(self.errors),
            },
        }
        if self.catalog_report is not None:
            data["catalog"] = self.catalog_report
        build_dir.mkdir(parents=True, exist_ok=True)
        write_text_atomic(
            build_dir / "report.json",
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        write_text_atomic(build_dir / "report.md", self._render_markdown(data))

    def _render_markdown(self, data: dict) -> str:
        from .report_builder import render_report_markdown

        lines = ["# Relatório da Wiki", ""]
        status = "OK" if data["ok"] else "FALHOU"
        lines.append(f"**Status:** {status}  ")
        lines.append(f"**Modo estrito:** {data['strict']}  ")
        lines.append(
            f"**Resumo:** {data['summary']['warnings']} avisos, {data['summary']['errors']} erros"
        )
        lines.append("")
        stats = data["stats"]
        labels = [
            ("discovered", "Conteúdos descobertos"),
            ("pages_created", "Páginas criadas"),
            ("pages_updated", "Páginas atualizadas"),
            ("pages_removed", "Páginas removidas"),
            ("missing_descriptions", "Descrições ausentes"),
            ("missing_translations", "Traduções ausentes"),
            ("missing_textures", "Texturas ausentes"),
            ("missing_models", "Modelos ausentes"),
            ("unknown_types", "Tipos desconhecidos"),
            ("broken_links", "Links quebrados"),
        ]
        for key, label in labels:
            values = stats[key]
            if values:
                lines.append(f"## {label} ({len(values)})")
                lines.append("")
                for value in values:
                    lines.append(f"- {value}")
                lines.append("")
        catalog_section = render_report_markdown(data)
        if catalog_section:
            lines.append(catalog_section)
        if data["issues"]:
            lines.append("## Issues")
            lines.append("")
            for issue in data["issues"]:
                where = f" `{issue['path']}`" if issue.get("path") else ""
                lines.append(f"- **[{issue['severity'].upper()}]**{where} {issue['message']}")
            lines.append("")
        return "\n".join(lines) + "\n"
