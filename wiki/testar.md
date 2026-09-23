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
/give @s novadyne:test_power_hub
/give @s novadyne:macerator
/give @s minecraft:clay_ball 8
```

Coloque o Test Power Hub e o Macerator no mesmo nível, até dois blocos de distância nos eixos norte/sul e leste/oeste. O bloco fornece energia a cada máquina NovaDyne no quadrado 5 × 5 centrado nele. Abra a GUI do Macerator e coloque argila no input. Cada unidade leva 120 ticks (6 s a 20 TPS) e produz 1 Ceramic Powder.

## Teste da limpeza

```mcfunction
/give @s novadyne:litografia
/give @s novadyne:part_electronic_dirty_silicon_wafer
/give @s minecraft:water_bucket
```

Coloque a Lithography no mesmo quadrado 5 × 5 do Test Power Hub. Insira o wafer no slot de entrada e a água no slot do balde. Após 120 ticks, espere 1 Etched Silicon Wafer no output e 1 balde vazio no slot do balde.

## Teste da água encanada

```mcfunction
/give @s novadyne:water_sink
/give @s novadyne:fluid_pipe 8
/give @s novadyne:part_electronic_dirty_silicon_wafer
```

Coloque o Water Sink, uma linha contínua de cabos de fluido e a Lithography nas extremidades. O cabo encosta no sink e na máquina; curvas e subidas também funcionam. O tanque da Lithography recebe água em até 16 ticks (4.000 mB) e mostra seu volume na GUI. Com energia FE e saída livre, cada wafer consome 1.000 mB. O balde continua sendo uma alternativa; se houver água suficiente no tanque, ele não é consumido.

## Diagnóstico

| Sintoma | O que conferir |
| --- | --- |
| Não processa | Energia suficiente, input correto e output livre |
| Engraving ou reciclagem parou | Retire todo o conteúdo do output; ambos os resultados precisam poder caber |
| Limpeza parou | Confira o balde de água ou o tanque (mínimo de 1.000 mB); confirme cabos conectados e saída livre |
| Não dropou ao minerar | Use picareta de pedra ou superior |
| JAR não aparece em Artifacts | Confirme que a execução do workflow terminou com marca verde e que a conta está conectada ao GitHub |
| Build verde, mas há erro visual | Os testes automatizados verificam o código e alguns processos; registre o erro visto no cliente |

## Sobre os testes automatizados

O [workflow de build](https://github.com/nicotfpn/Novadyne-MOD/actions/workflows/build.yml) compila o mod e executa testes de registro, energia e processamento em um servidor Minecraft. Aparência, interface e interação com outros mods precisam de verificação dentro do jogo.
