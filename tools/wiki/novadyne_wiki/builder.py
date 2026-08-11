"""Montagem da árvore wiki/docs e geração do mkdocs.yml.

O builder reconstrói `wiki/docs` do zero a cada execução (é descartável),
copia os assets do tema, escreve as páginas manuais sem front matter e
valida os links. Retorna um manifesto de arquivos (relativo -> SHA-256)
usado pelo modo --check para provar idempotência.
"""

from __future__ import annotations

from . import io_utils, theme, validate
from .config import assemble_config, build_nav, write_mkdocs_config
from .content import load_manual_pages
from .pages import generate_catalog_pages
from .paths import (
    DISPOSABLE_DIRS,
    TEXTURES_DIR,
    WIKI_CONFIG,
    WIKI_CONTENT,
    WIKI_CUSTOM_CONFIG,
    WIKI_DOCS,
    WIKI_THEME,
)


def build_site(
    reporter,
    *,
    catalog: dict | None = None,
    content_dir=WIKI_CONTENT,
    docs_dir=WIKI_DOCS,
    theme_dir=WIKI_THEME,
    textures_dir=TEXTURES_DIR,
    custom_config=WIKI_CUSTOM_CONFIG,
    config_path=WIKI_CONFIG,
    clean: bool = False,
) -> dict:
    """Monta a árvore docs e retorna o manifesto dos arquivos escritos.

    Com `clean=True`, as pastas descartáveis (wiki/generated, wiki/docs,
    build/wiki) são apagadas antes. A árvore docs é sempre reconstruída.
    """
    if clean:
        for directory in DISPOSABLE_DIRS:
            io_utils.wipe_dir(directory)
    if docs_dir.exists():
        io_utils.wipe_dir(docs_dir, extra_allowed=(docs_dir,))
    docs_dir.mkdir(parents=True, exist_ok=True)

    pages = load_manual_pages(content_dir)
    if catalog:
        pages = pages + generate_catalog_pages(catalog)

    theme_files = theme.copy_theme_assets(theme_dir=theme_dir, dest_assets=docs_dir / "assets")
    texture_files = theme.copy_texture_assets(textures_dir=textures_dir, dest_assets=docs_dir / "assets")

    manifest: dict[str, str] = {}
    for rel in theme_files + texture_files:
        dest = (docs_dir / "assets" / rel).resolve()
        manifest[dest.relative_to(docs_dir).as_posix()] = io_utils.file_digest(dest)

    for page in pages:
        dest = docs_dir / page.dest_rel
        body = page.body if page.body.endswith("\n") else page.body + "\n"
        io_utils.write_text_atomic(dest, body)
        rel = dest.relative_to(docs_dir).as_posix()
        manifest[rel] = io_utils.file_digest(dest)

    nav = build_nav(pages)
    write_mkdocs_config(config_path, assemble_config(nav, custom_path=custom_config))
    manifest[config_path.name] = io_utils.file_digest(config_path)

    validate.validate_docs_links(docs_dir, reporter)
    return manifest
