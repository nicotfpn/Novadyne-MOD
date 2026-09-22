[Início](README.md) · [Receitas](receitas.md) · [Máquinas](maquinas.md) · [Materiais](materiais.md) · [Valves](valves.md) · [Progressão](progressao.md) · [Como testar](testar.md)

---

# Instalar e testar

## Baixar o mod

1. Abra [Actions → Build](https://github.com/nicotfpn/Novadyne-MOD/actions/workflows/build.yml).
2. Escolha uma execução da `main` com marca verde. Em **Artifacts**, baixe `novadyne-jar` (é preciso estar conectado ao GitHub).
3. Extraia o ZIP e coloque o `.jar` em `mods` de uma instalação **Minecraft 26.1.2 + NeoForge 26.1.2.76**, com Java 25.
4. Use um mundo novo em criativo e habilite comandos. Para isolar problemas, comece com NovaDyne apenas.

## Teste rápido do Macerator

```mcfunction
/give @s novadyne:macerator
/give @s minecraft:clay_ball 8
```

Coloque a máquina e anote as coordenadas. Substitua X, Y e Z pelos números do bloco:

```mcfunction
/data merge block X Y Z {energy:10000L}
```

Abra a GUI e coloque argila no input. Cada unidade leva 120 ticks (6 s a 20 TPS) e produz 1 Ceramic Powder. O comando é uma facilidade de teste; não adiciona um gerador ao survival.

## Teste da limpeza

```mcfunction
/give @s novadyne:litografia
/give @s novadyne:part_electronic_dirty_silicon_wafer
/give @s minecraft:water_bucket
```

Abasteça energia pelo mesmo comando. Coloque wafer no slot de entrada e água no slot do balde. Após 120 ticks, espere 1 Etched Silicon Wafer no output e 1 balde vazio no slot do balde.

## Diagnóstico

| Sintoma | O que conferir |
| --- | --- |
| Não processa | Energia suficiente, input correto e output livre |
| Engraving ou reciclagem parou | Retire todo o conteúdo do output; ambos os resultados precisam poder caber |
| Limpeza parou | Retire o balde vazio e coloque outro balde de água |
| Não dropou ao minerar | Use picareta de pedra ou superior |
| JAR não aparece em Artifacts | Confirme que a execução do workflow terminou com marca verde e que a conta está conectada ao GitHub |
| Build verde, mas há erro visual | Os testes automatizados verificam o código e alguns processos; registre o erro visto no cliente |

## Sobre os testes automatizados

O [workflow de build](https://github.com/nicotfpn/Novadyne-MOD/actions/workflows/build.yml) compila o mod e executa testes de registro, energia e processamento em um servidor Minecraft. Aparência, interface e interação com outros mods precisam de verificação dentro do jogo.
