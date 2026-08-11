"""Carga de conteúdo manual (wiki/content) com front matter YAML.

Textos manuais nunca são sobrescritos pelo gerador: o gerador apenas os lê
e os renderiza na árvore docs. A pasta de origem permanece intacta.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import io_utils
from .errors import WikiError

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


@dataclass
class ManualPage:
    """Uma página manual lida de wiki/content/."""

    source: Path
    dest_rel: str  # caminho relativo dentro de wiki/docs, ex: "index.md"
    title: str
    id: str | None = None  # id de conteúdo registrado (ex: novadyne:pure_silicon)
    nav_title: str | None = None
    category: str | None = None
    order: int = 100
    body: str = ""


def _load_yaml_front_matter(text: str, path: Path) -> tuple[dict, str]:
    match = _FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    raw, body = match.group(1), match.group(2)
    try:
        import yaml  # PyYAML (dependência fixada)

        data = yaml.safe_load(raw)
    except ImportError as exc:  # pragma: no cover
        raise WikiError("PyYAML não instalado; rode: pip install -r tools/wiki/requirements.txt", path=str(path)) from exc
    except yaml.YAMLError as exc:
        raise WikiError(f"front matter YAML inválido: {exc}", path=str(path)) from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise WikiError("front matter deve ser um mapeamento YAML", path=str(path))
    return data, body


def _read_yaml_sidecar(path: Path) -> dict:
    """Carrega um arquivo YAML puro (ex: descrição editorial), se existir."""
    if not path.exists():
        return {}
    text = io_utils.read_text(path)
    try:
        import yaml

        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise WikiError(f"YAML inválido: {exc}", path=str(path)) from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise WikiError("arquivo YAML deve ser um mapeamento", path=str(path))
    return data


def load_manual_pages(content_dir: Path) -> list[ManualPage]:
    """Carrega todos os *.md de wiki/content/ (recursivo, ordenado).

    A subpasta `entries/` é ignorada aqui: os arquivos dela são descrições
    anexadas a entradas do catálogo (ver `load_entry_description`) e não
    viram páginas independentes na navegação.
    """
    pages: list[ManualPage] = []
    if not content_dir.exists():
        return pages
    for path in io_utils.iter_files(content_dir, suffixes=(".md",)):
        rel = path.relative_to(content_dir).as_posix()
        if rel.startswith("entries/"):
            continue
        text = io_utils.read_text(path)
        fm, body = _load_yaml_front_matter(text, path)
        rel = path.relative_to(content_dir).as_posix()
        title = fm.get("title") or _title_from_filename(rel)
        pages.append(
            ManualPage(
                source=path,
                dest_rel=rel,
                title=str(title),
                id=fm.get("id"),
                nav_title=str(fm["nav_title"]) if fm.get("nav_title") else None,
                category=fm.get("category"),
                order=int(fm.get("order", 100)),
                body=body.strip(),
            )
        )
    return sorted(pages, key=lambda p: (p.dest_rel,))


def _title_from_filename(rel: str) -> str:
    name = Path(rel).stem
    return name.replace("_", " ").replace("-", " ").title()


def load_entry_description(content_dir: Path, entry_id: str) -> ManualPage | None:
    """Retorna a página manual anexada a um conteúdo registrado, se existir.

    Convenção: wiki/content/entries/<slug>.md com front matter `id:`.
    """
    if not content_dir.exists():
        return None
    entries_dir = content_dir / "entries"
    if not entries_dir.exists():
        return None
    for path in io_utils.iter_files(entries_dir, suffixes=(".md",)):
        text = io_utils.read_text(path)
        fm, body = _load_yaml_front_matter(text, path)
        if fm.get("id") == entry_id:
            return ManualPage(
                source=path,
                dest_rel=path.relative_to(content_dir).as_posix(),
                title=str(fm.get("title") or entry_id),
                id=entry_id,
                body=body.strip(),
            )
    return None
