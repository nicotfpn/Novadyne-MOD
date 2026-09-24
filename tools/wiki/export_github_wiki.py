"""Export generated wiki Markdown as flat pages for GitHub's native Wiki."""

import argparse
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
BASE = "https://github.com/nicotfpn/Novadyne-MOD"
LINK = re.compile(r'(?P<prefix>\]\(|\bsrc=")(?P<url>[^)"\s]+)')


def convert(source: Path, content: str) -> str:
    def replace(match: re.Match[str]) -> str:
        url = match.group("url")
        if url.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        name, sep, fragment = url.partition("#")
        target = (source.parent / name).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            raise ValueError(f"Broken link in {source.relative_to(ROOT)}: {url}")
        if target == WIKI / "README.md":
            result = f"{BASE}/wiki/Home"
        elif target.suffix == ".md" and target.parent in (WIKI, WIKI / "itens"):
            result = f"{BASE}/wiki/{target.stem}"
        elif target.is_relative_to(WIKI / "assets"):
            result = f"https://raw.githubusercontent.com/nicotfpn/Novadyne-MOD/main/{target.relative_to(ROOT).as_posix()}"
        else:
            result = f"{BASE}/blob/main/{target.relative_to(ROOT).as_posix()}"
        return match.group("prefix") + result + (sep + quote(fragment) if sep else "")

    return LINK.sub(replace, content)


def export(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    pages = sorted(WIKI.glob("*.md")) + sorted((WIKI / "itens").glob("*.md"))
    for source in pages:
        name = "Home.md" if source.name == "README.md" else source.name
        (destination / name).write_text(convert(source, source.read_text(encoding="utf-8")), encoding="utf-8")
    (destination / "_Sidebar.md").write_text(
        "## NovaDyne\n\n"
        "- [Início](Home)\n- [Progressão](progressao)\n- [Receitas](receitas)\n"
        "- [Máquinas](maquinas)\n- [Materiais](materiais)\n- [Valves](valves)\n"
        "- [Instalação e testes](testar)\n- [Manutenção](manutencao)\n",
        encoding="utf-8",
    )
    print(f"Exported {len(pages)} pages and sidebar to {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    export(parser.parse_args().destination)
