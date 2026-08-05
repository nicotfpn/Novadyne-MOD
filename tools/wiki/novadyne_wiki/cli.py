"""CLI do gerador da wiki (Fase 2: fundação).

Comandos:
    python tools/wiki/generate.py            # gera catálogo + docs + mkdocs.yml + relatório
    python tools/wiki/generate.py --check    # para CI: falha em erros ou não-idempotência
    python tools/wiki/generate.py --strict   # avisos passam a ser erros
    python tools/wiki/generate.py --clean    # apaga pastas descartáveis antes
    python tools/wiki/generate.py --verbose  # imprime detalhes
    python tools/wiki/generate.py --build    # após gerar, executa `mkdocs build`
    python tools/wiki/generate.py --serve    # após gerar, executa `mkdocs serve`
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from .builder import build_site
from .catalog import CatalogBuilder, write_catalog
from .errors import WikiError
from .io_utils import file_digest
from .paths import BUILD_WIKI, WIKI_CONFIG, WIKI_DIR
from .reporter import Reporter


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="generate.py",
        description="Gerador da wiki do NovaDyne (Fase 2: fundação).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Modo de verificação para CI: falha se houver erros ou se a geração não for idempotente.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Avisos passam a ser erros.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Apaga as pastas geradas (wiki/generated, wiki/docs, build/wiki) antes de gerar.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Imprime detalhes da geração.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Após gerar, executa `mkdocs build` para compilar o site.",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Após gerar, executa `mkdocs serve` (bloqueia até Ctrl+C).",
    )
    return parser.parse_args(argv)


def run_generation(reporter: Reporter, *, clean: bool = False) -> dict:
    """Executa o pipeline completo e retorna o manifesto de arquivos."""
    manifest = build_site(reporter, clean=clean)
    catalog = CatalogBuilder(reporter).build()
    write_catalog(catalog, BUILD_WIKI / "catalog.json")
    manifest["catalog.json"] = file_digest(BUILD_WIKI / "catalog.json")
    return manifest


def _idempotency_check(clean: bool) -> bool:
    first = run_generation(Reporter(strict=False), clean=clean)
    second = run_generation(Reporter(strict=False), clean=False)
    if first == second:
        return True
    differing = sorted(set(first) ^ set(second))
    print("ERRO: a geração não é idempotente.", file=sys.stderr)
    for key in differing:
        print(f"  diferença em: {key}", file=sys.stderr)
    return False


def _print_summary(reporter: Reporter, args: argparse.Namespace) -> None:
    status = "OK" if reporter.ok else "FALHOU"
    print(
        f"Gerador da wiki: {status} "
        f"({len(reporter.warnings)} avisos, {len(reporter.errors)} erros)"
    )
    for issue in reporter.errors:
        print(f"  [ERRO] {issue.render()}", file=sys.stderr)
    if args.verbose:
        for issue in reporter.warnings:
            print(f"  [AVISO] {issue.render()}")
        print(f"  relatório: {BUILD_WIKI / 'report.md'}")


def _run_mkdocs(command: str) -> int:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "mkdocs", command, "-f", str(WIKI_CONFIG)],
            cwd=str(WIKI_DIR),
        )
        return 0
    except FileNotFoundError:
        print(
            "mkdocs não encontrado. Instale as dependências com:\n"
            "  python -m pip install -r tools/wiki/requirements.txt",
            file=sys.stderr,
        )
        return 1
    except subprocess.CalledProcessError:
        return 1


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    reporter = Reporter(strict=args.strict, verbose=args.verbose)
    try:
        run_generation(reporter, clean=args.clean)
    except WikiError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    reporter.write_report(BUILD_WIKI)

    ok = reporter.ok
    if args.check and ok:
        ok = _idempotency_check(args.clean)

    if args.build and ok:
        code = _run_mkdocs("build")
        ok = code == 0
    elif args.serve and ok:
        code = _run_mkdocs("serve")
        ok = code == 0

    _print_summary(reporter, args)
    return 0 if ok else 1
