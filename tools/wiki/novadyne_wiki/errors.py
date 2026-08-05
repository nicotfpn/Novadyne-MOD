"""Erros e severidades do gerador.

O gerador diferencia avisos (warnings) de erros fatais. Em modo estrito,
avisos sobem para erros. Em modo normal, avisos não interrompem a geração.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class WikiError(Exception):
    """Erro fatal do gerador. Carrega contexto (arquivo/linha quando houver)."""

    def __init__(self, message: str, *, path: str | None = None, context: str | None = None):
        self.message = message
        self.path = path
        self.context = context
        if path and context:
            super().__init__(f"{path}: {message} (contexto: {context})")
        elif path:
            super().__init__(f"{path}: {message}")
        else:
            super().__init__(message)


@dataclass
class Issue:
    """Um aviso ou erro registrado durante a geração."""

    severity: str  # "warning" | "error"
    message: str
    path: str | None = None
    context: str | None = None

    def render(self) -> str:
        parts: list[str] = []
        if self.path:
            parts.append(str(self.path))
        parts.append(self.message)
        if self.context:
            parts.append(f"(contexto: {self.context})")
        return ": ".join(parts)
