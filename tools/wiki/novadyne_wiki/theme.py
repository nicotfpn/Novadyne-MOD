"""Assets do tema (wiki/theme) copiados para a árvore docs.

O tema vive em `wiki/theme/` (fonte de verdade, versionada) e é copiado para
`wiki/docs/assets/` a cada geração. A árvore docs permanece descartável e é
reconstruída do zero.
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
