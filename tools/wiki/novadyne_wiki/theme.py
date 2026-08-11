"""Assets do tema (wiki/theme) e texturas do mod copiados para a árvore docs.

O tema vive em `wiki/theme/` e as texturas em
`src/main/resources/assets/novadyne/textures/` (fontes de verdade, versionadas).
Ambos são copiados para `wiki/docs/assets/` a cada geração. A árvore docs
permanece descartável e é reconstruída do zero.
"""

from __future__ import annotations

from . import io_utils


def copy_theme_assets(*, theme_dir, dest_assets) -> list[str]:
    """Copia wiki/theme/** para docs/assets/** preservando a estrutura.

    Retorna a lista de caminhos relativos copiados (ordem estável).
    """
    if not theme_dir.exists():
        return []
    copied: list[str] = []
    for path in io_utils.iter_files(theme_dir):
        rel = path.relative_to(theme_dir).as_posix()
        dest = dest_assets / rel
        io_utils.write_bytes_atomic(dest, path.read_bytes())
        copied.append(rel)
    return copied


def copy_texture_assets(*, textures_dir, dest_assets) -> list[str]:
    """Copia as texturas do mod para docs/assets/textures/**.

    Preserva a estrutura interna (item/, block/, gui/ etc.). Os caminhos
    retornados são relativos a *dest_assets* (prefixados com "textures/"),
    para que o manifesto do builder trate tema e texturas de forma uniforme.
    """
    if not textures_dir.exists():
        return []
    copied: list[str] = []
    for path in io_utils.iter_files(textures_dir):
        rel = path.relative_to(textures_dir).as_posix()
        dest = dest_assets / "textures" / rel
        io_utils.write_bytes_atomic(dest, path.read_bytes())
        copied.append(f"textures/{rel}")
    return copied
