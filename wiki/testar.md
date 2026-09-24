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

## Teste visual dos lados

Coloque um baú à direita de um Macerator que esteja virado para o norte. Na GUI, observe o mapa colorido: branco = nenhum, azul = entrada, laranja = saída, roxo = entrada/saída. Passe o mouse para ler a direção. Clique em **Dir.** até ficar laranja, ligue **Auto saída** e processe argila. O Ceramic Powder deve entrar no baú sem retirar a argila do input. Desligue Auto saída: o produto deve ficar na máquina. Troque o quadradinho para roxo: o lado deve permitir alimentar a máquina e retirar produtos. Quebre e recoloque a máquina apenas depois de conferir que a configuração persiste ao fechar e abrir a GUI e ao sair e entrar no mundo.

## Teste da limpeza

```mcfunction
/give @s novadyne:litografia
/give @s novadyne:part_electronic_dirty_silicon_wafer
/give @s minecraft:water_bucket
```

Coloque a Lithography no mesmo quadrado 5 × 5 do Test Power Hub. Insira o wafer no slot de entrada e a água no slot do balde. Após 120 ticks, espere 1 Etched Silicon Wafer no output e 1 balde vazio no slot do balde.

## Teste dos geradores

```mcfunction
/give @s novadyne:fuel_generator
/give @s novadyne:energy_cable 8
/give @s minecraft:oak_planks 16
/give @s novadyne:basic_solar_generator
/give @s novadyne:advanced_solar_generator
```

Ligue o Fuel Generator à máquina com até 128 Energy Cables, abra a GUI e coloque tábuas no slot de combustível. Ele gera 80 FE/t e transfere até 80 FE/t para a rede. O slot da direita guarda recipientes vazios (por exemplo, um balde após queimar lava); se estiver ocupado, a máquina aguarda antes de consumir o combustível. Quando o armazenamento de energia enche, a queima pausa.

Coloque os solares sob céu aberto: o básico gera 40 FE/t de dia e 0 à noite; o avançado, 100 FE/t de dia e 25 FE/t à noite. Clique com o botão direito para ver a energia guardada. Conecte a máquina diretamente ou por Energy Cables.

## Teste da água encanada

```mcfunction
/give @s novadyne:water_sink
/give @s novadyne:fluid_pipe 8
/give @s novadyne:part_electronic_dirty_silicon_wafer
```

Coloque o Water Sink, uma linha contínua de cabos de fluido e a Lithography nas extremidades. O cabo encosta no sink e na máquina; curvas e subidas também funcionam. O tanque da Lithography recebe água em até 16 ticks (4.000 mB) e mostra seu volume na GUI. Com energia FE e saída livre, cada wafer consome 1.000 mB. O balde continua sendo uma alternativa; se houver água suficiente no tanque, ele não é consumido.

## Checklist visual dos conduítes

1. Coloque um Fluid Pipe e um Energy Cable separados, no ar. Cada um deve mostrar só o núcleo central, sem braços.
2. Faça `Water Sink → Fluid Pipe → Fluid Pipe → Lithography`. Cada tubo deve ter braços só na direção dos dois vizinhos. Observe a água subir na GUI da Lithography. Encoste um Macerator ao lado de um tubo: não deve surgir um braço para ele.
3. Faça `Fuel Generator → Energy Cable → Energy Cable → Macerator`. Ponha carvão ou tábuas no gerador e abra a GUI do Macerator; a energia deve subir. Um bloco de pedra ao lado do cabo não deve receber um braço.
4. Quebre o cabo do meio: os braços desse lado devem desaparecer e a energia deixar de chegar ao Macerator. Recoloque-o e teste curvas, subidas e descidas.
5. Ponha um balde de lava no Fuel Generator. O balde vazio deve aparecer no slot de saída. O gerador não deve consumir outro balde se esse slot estiver ocupado por um item incompatível. Retire os itens e quebre o gerador: tudo que estava nos slots deve cair.
6. Deixe cada Solar Generator sob céu aberto e clique com o botão direito para conferir a energia. O Basic gera de dia; o Advanced também gera à noite em taxa menor. Ligue cada um ao Macerator por Energy Cables.

Use uma picareta de pedra ou superior para recolher os cabos. Verifique também se ambos parecem finos no mundo, no inventário e na barra de atalhos.

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
