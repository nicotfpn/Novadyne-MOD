"""Layout de pastas do projeto e do gerador.

Todos os caminhos derivam de PROJECT_ROOT (descoberto a partir da localização
deste módulo). Nunca use caminhos absolutos fora deste módulo.
"""

from __future__ import annotations

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent  # tools/wiki/novadyne_wiki
TOOLS_WIKI_DIR = _PACKAGE_DIR.parent  # tools/wiki
PROJECT_ROOT = TOOLS_WIKI_DIR.parent.parent  # raiz do repositório

# Diretórios do mod (fontes de verdade)
MAIN_JAVA = PROJECT_ROOT / "src" / "main" / "java"
MAIN_RESOURCES = PROJECT_ROOT / "src" / "main" / "resources"
ASSETS_DIR = MAIN_RESOURCES / "assets"
DATA_DIR = MAIN_RESOURCES / "data"
GENERATED_RESOURCES = PROJECT_ROOT / "src" / "generated" / "resources"

# Saída intermediária (descartável)
BUILD_WIKI = PROJECT_ROOT / "build" / "wiki"

# Árvore da wiki
WIKI_DIR = PROJECT_ROOT / "wiki"
WIKI_CONTENT = WIKI_DIR / "content"  # manual, nunca sobrescrito
WIKI_GENERATED = WIKI_DIR / "generated"  # páginas geradas, descartável
WIKI_DOCS = WIKI_DIR / "docs"  # árvore montada para o MkDocs, descartável
WIKI_THEME = WIKI_DIR / "theme"  # assets do tema (CSS/JS locais)
WIKI_CONFIG = WIKI_DIR / "mkdocs.yml"  # gerado
WIKI_CUSTOM_CONFIG = WIKI_DIR / "mkdocs.custom.yml"  # opcional, manual

# Estrutura interna da árvore docs
DOCS_ASSETS = WIKI_DOCS / "assets"

# Diretórios descartáveis que o gerador pode limpar com segurança.
DISPOSABLE_DIRS = (WIKI_GENERATED, WIKI_DOCS, BUILD_WIKI)

# Arquivo de avisos reconhecidos
ACKNOWLEDGED_WARNINGS = TOOLS_WIKI_DIR / "acknowledged_warnings.json"

# Prefixo obrigatório das páginas geradas.
GENERATED_BANNER = "<!-- AUTO-GENERATED: DO NOT EDIT DIRECTLY -->"
