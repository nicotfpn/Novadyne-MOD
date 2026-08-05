"""Validações da árvore docs montada: links internos e referências de assets.

Fase 2 cobre links Markdown e imagens das páginas geradas. As fases 7+
ampliam com ids, slugs, receitas e modo estrito mais completo.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import io_utils

_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _is_internal(target: str) -> bool:
    lowered = target.lower()
    return not (
        lowered.startswith(("http://", "https://", "mailto:", "tel:", "//"))
        or target.startswith("#")
    )


def _resolve_target(base: Path, docs_root: Path, target: str) -> Path | None:
    """Resolve um link relativo para um caminho dentro de docs_root.

    Trata fragmentos (#...), diretórios (-> index.md) e omissão de extensão
    .md. Retorna None quando o link escapa da árvore docs.
    """
    clean = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean:
        return None
    candidate = (base / clean).resolve()
    try:
        candidate.relative_to(docs_root.resolve())
    except ValueError:
        return None
    if candidate.is_dir():
        candidate = candidate / "index.md"
    if candidate.is_file():
        return candidate
    if candidate.suffix == "":
        alt = candidate.with_suffix(".md")
        if alt.is_file():
            return alt
    return candidate if candidate.exists() else None


def validate_docs_links(docs_dir, reporter) -> None:
    """Registra avisos para links internos quebrados nas páginas de docs/."""
    if not docs_dir.exists():
        return
    docs_root = docs_dir.resolve()
    for path in io_utils.iter_files(docs_dir, suffixes=(".md",)):
        text = io_utils.read_text(path)
        rel = path.relative_to(docs_dir).as_posix()
        for match in _MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not _is_internal(target):
                continue
            resolved = _resolve_target(path.parent, docs_root, target)
            if resolved is None or not resolved.exists():
                reporter.warning(
                    f"link interno quebrado: {target}",
                    path=rel,
                    context=f"{rel} -> {target}",
                )
                reporter.note_broken_link(f"{rel} -> {target}")
