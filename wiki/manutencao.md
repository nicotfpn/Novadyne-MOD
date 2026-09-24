[Início](README.md) · [Receitas](receitas.md) · [Máquinas](maquinas.md) · [Materiais](materiais.md) · [Valves](valves.md) · [Progressão](progressao.md) · [Como testar](testar.md)

---

# Como manter esta wiki

A documentação nasce em `wiki/` neste repositório e é publicada na Wiki nativa do GitHub pelo workflow **Publish GitHub Wiki**. O índice fonte é `wiki/README.md` e vira a página Home.

## Atualizar

```bash
python -m pip install -r tools/wiki/requirements.txt
python tools/wiki/generate.py
python tools/wiki/generate.py --check
```

Use Linux com as fontes DejaVu Sans (`fonts-dejavu-core`). O gerador lê as receitas JSON, os itens registrados, nomes, texturas e constantes das máquinas. Processos especiais em Java têm uma descrição revisada em `tools/wiki/processes.json`; ao mudar essas classes, revise esse catálogo e atualize seus hashes de origem.

O workflow **Wiki** confere fontes, páginas, imagens e links em cada mudança relevante. Se ele ficar vermelho após mudar uma receita, regenere a wiki e inclua os arquivos atualizados no commit. `--check` não altera arquivos e não acessa a rede.

Imagens de craft e processo são diagramas gerados a partir de dados. Blocos e máquinas são desenhados em perspectiva a partir das texturas de suas faces; não são capturas do cliente Minecraft. Texturas vanilla e suas fontes estão em [créditos](assets/vanilla/SOURCES.md).
