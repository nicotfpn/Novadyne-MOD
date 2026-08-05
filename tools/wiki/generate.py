#!/usr/bin/env python3
"""Ponto de entrada do gerador da wiki do NovaDyne.

Uso: python tools/wiki/generate.py [--check] [--strict] [--clean] [--verbose] [--build] [--serve]
"""

from __future__ import annotations

import sys

from novadyne_wiki.cli import main

if __name__ == "__main__":
    sys.exit(main())
