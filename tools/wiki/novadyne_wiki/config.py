"""Configuração do MkDocs (wiki/mkdocs.yml), gerada pelo gerador.

A configuração base fica neste módulo. Um arquivo opcional
`wiki/mkdocs.custom.yml` permite sobrescrever campos sem editar o arquivo
gerado (merge profundo de dicionários; listas são substituídas). A navegação
(`nav`) é sempre reconstruída pelo gerador a partir das páginas carregadas.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from . import io_utils

BASE_CONFIG: dict = {
    "site_name": "NovaDyne",
    "site_description": "Wiki do mod NovaDyne para Minecraft (NeoForge 26.1.2)",
    "site_url": "https://nicotfpn.github.io/Novadyne-MOD/",
    "repo_url": "https://github.com/nicotfpn/Novadyne-MOD",
    "docs_dir": "docs",
    "site_dir": "site",
    "theme": {
        "name": "material",
        "language": "pt-BR",
        "palette": [
            {
                "scheme": "default",
                "primary": "indigo",
                "accent": "cyan",
                "toggle": {"icon": "material/brightness-7", "name": "Modo escuro"},
            },
            {
                "scheme": "slate",
                "primary": "indigo",
                "accent": "cyan",
                "toggle": {"icon": "material/brightness-4", "name": "Modo claro"},
            },
        ],
        "features": [
            "navigation.instant",
            "navigation.tracking",
            "navigation.expand",
            "navigation.top",
            "toc.follow",
        ],
        "font": False,
    },
    "extra_css": ["assets/css/novadyne.css"],
    "markdown_extensions": [
        "admonition",
        "attr_list",
        "md_in_html",
        "tables",
        "pymdownx.details",
        "pymdownx.highlight",
        "pymdownx.superfences",
        "pymdownx.tabbed",
    ],
    "plugins": ["search"],
}

_HOME_TITLE = "Home"


def deep_merge(base: dict, override: dict) -> dict:
    """Merge profundo: dicionários são mesclados recursivamente; o resto é
    substituído pelo valor do override. Nunca modifica as entradas de entrada."""
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_custom_config(custom_path) -> dict:
    """Carrega wiki/mkdocs.custom.yml (merge manual opcional)."""
    if not custom_path.exists():
        return {}
    text = io_utils.read_text(custom_path)
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        from .errors import WikiError

        raise WikiError(f"mkdocs.custom.yml inválido: {exc}", path=str(custom_path)) from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        from .errors import WikiError

        raise WikiError("mkdocs.custom.yml deve ser um mapeamento YAML", path=str(custom_path))
    return data


def _section_title(section: str) -> str:
    return section.replace("_", " ").replace("-", " ").strip().title()


def build_nav(pages: list) -> list:
    """Constrói a navegação a partir das páginas (manuais e geradas).

    - `index.md` vira "Home" (primeiro item).
    - Páginas em subpastas viram seções agrupadas pelo primeiro nível.
    - Ordenação estável por `order` (front matter) e depois por título.

    As páginas geradas por categoria (itens/, blocos/, maquinas/, misc/)
    formam seções automaticamente.
    """
    home = None
    by_section: dict[str, list] = {}
    for page in pages:
        if page.dest_rel == "index.md":
            home = page
            continue
        parts = Path(page.dest_rel).parts
        section = parts[0] if len(parts) > 1 else ""
        by_section.setdefault(section, []).append(page)

    nav: list = []
    if home is not None:
        nav.append({_HOME_TITLE: home.dest_rel})

    for section in sorted(by_section):
        items = by_section[section]
        items.sort(key=lambda p: (p.order, p.title.lower()))
        entries = [
            {page.nav_title or page.title: page.dest_rel}
            for page in items
        ]
        if section:
            nav.append({_section_title(section): entries})
        else:
            nav.extend(entries)
    return nav


def assemble_config(nav: list, *, custom_path=None) -> dict:
    """Monta o dict final do mkdocs.yml: base + custom + nav gerado."""
    if custom_path is None:
        from .paths import WIKI_CUSTOM_CONFIG

        custom_path = WIKI_CUSTOM_CONFIG
    config = deep_merge(BASE_CONFIG, load_custom_config(custom_path))
    config["nav"] = nav
    return config


def write_mkdocs_config(path, config: dict) -> None:
    """Serializa o mkdocs.yml com YAML UTF-8 e escrita atômica."""
    io_utils.write_text_atomic(
        path,
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False, default_flow_style=False),
    )
