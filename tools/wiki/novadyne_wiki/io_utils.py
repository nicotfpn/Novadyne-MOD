"""Utilitários de I/O: UTF-8 explícito, escrita atômica, caminhos seguros."""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from pathlib import Path

from .errors import WikiError


def read_text(path: Path) -> str:
    """Lê um arquivo como UTF-8, com mensagem de erro contextualizada."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise WikiError(f"não foi possível ler o arquivo: {exc}", path=str(path)) from exc


def _atomic_write(path: Path, content, *, binary: bool = False) -> None:
    """Escreve conteúdo de forma atômica (arquivo temporário + rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".wiki-tmp-", suffix=".tmp")
    try:
        if binary:
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
        else:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
        os.replace(tmp_name, str(path))
    except OSError as exc:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise WikiError(f"não foi possível escrever o arquivo: {exc}", path=str(path)) from exc


def write_text_atomic(path: Path, content: str) -> None:
    """Escreve texto UTF-8 de forma atômica (arquivo temporário + rename)."""
    _atomic_write(path, content)


def write_bytes_atomic(path: Path, content: bytes) -> None:
    """Escreve bytes de forma atômica (arquivo temporário + rename)."""
    _atomic_write(path, content, binary=True)


def ensure_inside_root(path: Path, root: Path, what: str = "caminho") -> Path:
    """Garante que *path* esteja dentro de *root*, normalizado e absoluto.

    Usado para impedir que caminhos vindos de JSON saiam das pastas permitidas.
    """
    resolved = path.resolve()
    root_resolved = root.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise WikiError(
            f"{what} escapa da pasta permitida: {resolved} (fora de {root_resolved})",
            path=str(path),
        ) from exc
    return resolved


def safe_relative(asset_path: Path, allowed_roots: tuple[Path, ...]) -> str:
    """Converte um caminho absoluto em relativo POSIX a partir da primeira
    raiz permitida que o contém. Lança WikiError se o caminho escapar."""
    resolved = asset_path.resolve()
    for root in allowed_roots:
        root_resolved = root.resolve()
        try:
            rel = resolved.relative_to(root_resolved)
            return rel.as_posix()
        except ValueError:
            continue
    raise WikiError(
        f"caminho fora das pastas permitidas: {resolved}",
        path=str(asset_path),
    )


_SLUG_RE = re.compile(r"[^a-z0-9_.-]+")


def slugify(value: str) -> str:
    """Gera um slug estável e seguro a partir de um texto."""
    normalized = value.strip().lower()
    return _SLUG_RE.sub("-", normalized).strip("-")


def file_digest(path: Path) -> str:
    """SHA-256 de um arquivo, para detecção de mudanças/idempotência."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def iter_files(root: Path, suffixes: tuple[str, ...] | None = None) -> list[Path]:
    """Lista arquivos de forma ordenada e estável (independente do FS)."""
    if not root.exists():
        return []
    result = [p for p in root.rglob("*") if p.is_file()]
    if suffixes is not None:
        result = [p for p in result if p.suffix in suffixes]
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def wipe_dir(directory: Path, *, extra_allowed: tuple[Path, ...] = ()) -> None:
    """Remove uma pasta descartável. Valida a localização antes de apagar.

    `extra_allowed` permite autorizar explicitamente uma pasta que não está
    em DISPOSABLE_DIRS (usado quando o builder recebe pastas alternativas,
    ex: diretórios temporários em testes).
    """
    from .paths import DISPOSABLE_DIRS

    resolved = directory.resolve()
    allowed = tuple(d.resolve() for d in DISPOSABLE_DIRS) + tuple(
        a.resolve() for a in extra_allowed
    )
    if resolved not in allowed:
        raise WikiError(
            f"recusa em apagar pasta fora das pastas geradas: {resolved}",
            path=str(directory),
        )
    if not resolved.exists():
        return
    for child in list(resolved.iterdir()):
        if child.is_dir():
            import shutil

            shutil.rmtree(child)
        else:
            child.unlink()
