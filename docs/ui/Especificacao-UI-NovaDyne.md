# NovaDyne — sistema de UI de máquinas

Versão 1.0 · 13 de outubro de 2026 · especificação de reprodução e implementação.

## 1. O que este documento entrega

Este é o contrato visual e técnico para replicar a UI aprovada da Litografia em outras máquinas, sem redesenhar cada tela. Inclui medidas em pixels lógicos do Minecraft, cores, componentes, abas, sincronização, preenchimento das barras, comportamento dos slots e critérios de validação.

O documento não afirma que essa UI está implementada no mod. Até esta entrega, existem prévias de navegador; não houve execução de Minecraft ou Gradle. O layout original foi aprovado pelo usuário; as medidas normalizadas abaixo são uma especificação proposta para implementação, não medidas já validadas em jogo. Preservam a composição aprovada e corrigem as proporções aproximadas do HTML para o grid real de slots do Minecraft.

O pacote de referência acompanha uma prévia HTML autocontida, tabela JSON de medidas/cores e captura atualizada. HTML é uma referência de aparência e interação, não código NeoForge. A implementação deve usar fonte nativa, menus reais e valores do servidor.

### Ordem de autoridade

1. Decisões explícitas do usuário registradas neste documento.
2. Regras de funcionamento e segurança do repositório atual.
3. Medidas e componentes deste contrato.
4. Captura e HTML como apoio visual.

Se uma captura antiga conflitar com a tabela atual, seguir a tabela. Não manter azul para entrada: o usuário mudou entrada para vermelho, saída para azul e ambos para roxo.

## 2. Ambiente e limite da referência

Na cópia local consultada: Minecraft `26.1.2`, NeoForge `26.1.2.76`, ModDevGradle `2.0.141`. Os arquivos usam `GuiGraphicsExtractor`, `Identifier`, `RenderPipelines` e `ResourceHandlerSlot`. Confirmar a versão do checkout real antes de implementar. Não importar exemplos de APIs 1.20/1.21 apenas por semelhança do nome.

Arquivos de referência inspecionados:

- `src/main/java/com/novadyne/client/screen/AbstractMachineScreen.java`.
- `src/main/java/com/novadyne/client/screen/LitografiaScreen.java`.
- `src/main/java/com/novadyne/common/menu/AbstractMachineMenu.java`.
- `src/main/java/com/novadyne/common/menu/LitografiaMenu.java`.
- `src/main/java/com/novadyne/common/blockentity/LitografiaBlockEntity.java`.
- `src/main/resources/assets/novadyne/textures/item/valve_tier_1.png`.

A cópia de referência não substitui a leitura do repo atual. Há trabalho de lados independentes ocorrendo em outra sessão; inspecionar sua entrega e preservar alterações locais. Não sobrescrever essa implementação com o snapshot antigo.

## 3. Decisões visuais confirmadas

- Aparência Minecraft Java: painel cinza, slots rebaixados, botões texturizados discretamente e fonte nativa do jogo.
- Nada de imagem gerada por IA para inventar a GUI. Texturas pixeladas, desenho determinístico e screenshots reais.
- Não copiar a identidade visual ou a arquitetura completa do Mekanism. Usar suas ideias de organização/fluidez como referência.
- Entrada → progresso → saída na região de processamento.
- Barras JUNTAS à direita: fluido à esquerda, FE à direita.
- Slot do balde imediatamente à esquerda da barra de fluido.
- Sem rótulos permanentes “Água”, “FE”, “Material”, “Entrada”, “Resultado”, “Saída”, “Balde” ou similares na área principal. Informações em tooltip.
- Título da máquina e nome do inventário permanecem.
- Entrada vazia pode mostrar indicação discreta do material aceito. Saída tem moldura de coleta distinta, mas neutra.
- Silhueta de balde no slot vazio de balde; silhueta de válvula nos slots vazios de válvula. Nunca apresentar essas indicações como itens reais.
- Quatro abas externas quadradas, quando suportadas, no canto superior direito: energia, fluido, itens, válvulas.
- Energia: raio; fluido: balde; itens: baú quadrado; válvulas: ícone do item real do mod.
- Aba de válvulas com DOIS slots. A segunda válvula ainda exige implementação funcional e migração de inventário.
- Só mostrar recursos realmente disponíveis na máquina.

## 4. Design tokens: não inventar uma paleta por máquina

Todos os números desta seção são pixels lógicos, não pixels de screenshot nem pixels físicos do monitor. A escala de GUI do jogo aplica o aumento de tamanho.

| Token | Valor | Regra |
|---|---|---|
| Painel principal | 176 × 166 | Perfil padrão das máquinas simples |
| Margem estrutural | 8 | Área útil do painel |
| Slot desenhado | 18 × 18 | Moldura com interior 16 × 16 |
| Item/área do Slot | 16 × 16 | Origem 1 px após moldura |
| Passo do inventário | 18 | Sem gaps extras entre molduras |
| Aba externa | 18 × 18 | Ícone 12–14 px centralizado |
| Intervalo entre abas | 3 | Coluna compacta |
| Painel externo | 92 px de largura | Altura conforme conteúdo |
| Barra externa | 10 × 56 | Interior 6 × 52; borda 2 px |
| Distância entre barras | 2 | Fluido antes de energia |
| Progresso | 24 × 17 | Recorte horizontal, sem esticar seta |
| Fonte | `this.font` / fonte do jogo | Sem TTF próprio em produção |
| Texto padrão | escala 1 | Não reduzir arbitrariamente |
| Tooltip | nativo | Sem HTML/overlay próprio |

| Papel visual | HEX opaco |
|---|---|
| Painel | `#C6C6C6` |
| Destaque da moldura | `#F3F3F3` |
| Sombra da moldura | `#565656` |
| Contorno | `#202020` |
| Interior do slot | `#898989` |
| Texto sobre cinza | `#404040` |
| Texto sobre botão escuro | `#FFFFFF` |
| Desligado | `#DEDEDE` |
| Entrada / INPUT | `#D76565` — vermelho |
| Saída / OUTPUT | `#64A8D8` — azul |
| Entrada e saída / BOTH | `#B08ACB` — roxo |
| FE/preenchimento | `#D8AD36` |
| Água, fallback visual | `#4C92C7` |

ARGB deve incluir alpha `FF` para elementos opacos. As cores exatas são tokens propostos; a associação vermelho/entrada, azul/saída e roxo/ambos é decisão confirmada.

A faixa amarela no ícone de energia identifica o recurso. Ela NÃO indica que a face está em saída. Cor do recurso e cor do modo são sistemas diferentes.

### Botões

Desenhar textura-base cinza estática, com variação de luminância pequena, sem ruído calculado por frame. Borda escura externa de 1 px; highlight interno no topo/esquerda e sombra em baixo/direita. Nada de cantos arredondados, glow, blur ou gradiente suave. Usar sprites compartilhados ou os sprites vanilla apropriados à versão, sem achatar/esticar detalhes.

- Normal: cinza texturizado, ícone legível.
- Hover: contorno claro e highlight discreto; não mudar tamanho/posição.
- Selecionado: contorno claro contínuo e fundo mais escuro/rebaixado.
- Pressionado: aparência rebaixada; não deslocar o hitbox.
- Desativado: reduzir contraste e bloquear ação; não mostrar recursos inexistentes apenas desativados.
- Foco por teclado: indicação visível distinta do hover.

## 5. Layout canônico da Litografia

Origem `M=(leftPos,topPos)` no canto superior esquerdo do painel principal. Coordenadas abaixo são relativas a M. Não somar M duas vezes ao desenhar labels em métodos cuja pose já foi traduzida.

### Área principal

| Elemento | x | y | w | h | Observação |
|---|---:|---:|---:|---:|---|
| Fundo | 0 | 0 | 176 | 166 | Não inclui abas/drawer |
| Título | 8 | 6 | — | 9 | Medir fonte real, truncar antes da marca |
| Marca NovaDyne | 126 | 7 | 42 | 8 | Opcional; omitir em nomes longos |
| Indicador de estado | após título + 4 | 9 | 3 | 3 | Não colidir com marca |
| Moldura de entrada | 26 | 36 | 18 | 18 | Item/Slot em (27,37) |
| Seta | 50 | 36 | 24 | 17 | Progresso da receita |
| Moldura de saída | 82 | 36 | 18 | 18 | Item/Slot em (83,37) |
| Moldura de balde | 124 | 36 | 18 | 18 | Item/Slot em (125,37) |
| Barra de fluido | 146 | 24 | 10 | 56 | Interior (148,26), 6×52 |
| Barra de FE | 158 | 24 | 10 | 56 | Interior (160,26), 6×52 |
| Nome do inventário | 8 | 74 | — | 9 | Não sobrepor primeira linha |
| Primeiro slot do jogador: moldura | 8 | 85 | 18 | 18 | Item/Slot em (9,86) |
| Primeira hotbar: moldura | 8 | 143 | 18 | 18 | Item/Slot em (9,144) |

Para o inventário, item `x=9+18*col`, `y=86+18*row`, `col=0..8`, `row=0..2`. Hotbar: `x=9+18*col`, `y=144`. Isso preserva as posições do inventário encontradas no menu de referência. A textura do slot fica 1 px acima/esquerda da origem do item.

Nenhum item pode ocupar uma moldura diferente da posição real de seu Slot. Não desenhar todos os itens manualmente por cima de uma imagem e deixar o menu antigo em outro lugar.

### Externo: abas e painel aberto

| Elemento | x | y | w | h |
|---|---:|---:|---:|---:|
| Coluna de abas | 182 | 4 | 18 | variável |
| Aba energia | 182 | 4 | 18 | 18 |
| Aba fluido, se presente | 182 | 25 | 18 | 18 |
| Aba itens, com fluido presente | 182 | 46 | 18 | 18 |
| Aba válvulas, com todas presentes | 182 | 67 | 18 | 18 |
| Painel aberto | 204 | 4 | 92 | até 146 |

Filtrar recursos ausentes ANTES de calcular os índices visuais. Sem fluido, itens sobe para y=25 e válvulas para y=46. Não deixar um buraco que parece botão invisível.

O conjunto padrão reserva largura de 296 px lógicos e altura de 166. Calcular a origem levando em conta esse envelope externo, mesmo com drawer fechado, para que abrir uma aba NÃO faça a máquina saltar lateralmente. A textura principal continua com largura 176. Não usar largura expandida como UV do fundo principal.

Pode ser necessário ajustar campos/hooks de `AbstractContainerScreen` para centralização e hit testing; conferir assinatura na versão atual. Não simplesmente alterar `imageWidth=296` e presumir que todos os métodos continuam corretos.

### Interior do drawer

Coordenadas relativas ao drawer (204,4):

| Componente | Posição |
|---|---|
| Título | (8,8), largura máxima 76 |
| Cima | (32,32), 14×14 |
| Esquerda | (12,52), 14×14 |
| Frente | (32,52), 14×14 |
| Direita | (52,52), 14×14 |
| Baixo | (32,72), 14×14 |
| Trás | (52,72), 14×14 |
| Ajuda curta de faces | (8,94), até três linhas de 9 px |
| Ejetar itens, só em Itens | (8,124), 76×16 |
| Válvula 1: moldura | (16,32), 18×18 |
| Válvula 2: moldura | (42,32), 18×18 |
| Estado de válvulas | (8,58), até 76 px |

Usar tooltip com nome completo das faces. A ajuda curta pode ser omitida se não couber em tradução; não reduzir fonte. Drawer de válvulas vazio pode ter altura 90; efeitos instalados podem estender até 146 sem sobrepor inventário.

## 6. Perfis reutilizáveis e recursos condicionais

Cada máquina declara conteúdo real, não uma lista de controles que ela gostaria de ter. Usar um perfil pequeno, sem framework genérico de UI.

Exemplo de contrato conceitual, não API existente:

```text
MachineUiProfile
  energy: supported, capacitySource, allowedModes
  fluids: supported, tankCount, acceptedTypes, bucketRefillSupported
  items: slotRoles, allowedModes, autoEjectSupported
  valves: supported, socketCount, validItems
  process: inputSlots, outputSlots, progressSource
  layout: SIMPLE_176 ou variante explicitamente necessária
```

| Tipo | O que aparece |
|---|---|
| Consumidor simples sem fluido | Entrada/seta/saída, FE e abas de energia/itens; válvulas se suporta |
| Litografia | Água+FE, balde, itens e duas válvulas conforme esta especificação |
| Máquina com tanque, mas sem baldes | Barra/aba de fluido, sem slot de balde |
| Máquina com vários inputs/outputs | Mesmo kit; ampliar zona de processo em variante própria, sem espremer inventário |
| Gerador futuro | Reutilizar kit apenas após autorização; modos de FE baseados em suporte real |
| Bloco sem inventário | Não inventar aba de itens ou inventário da máquina |

Sem fluido, FE permanece em (158,24) e não aparece uma barra vazia em (146,24). Não substituir água por um segundo recurso fictício para preencher espaço.

Para layouts complexos, preservar escala de slot, fonte, botões, paleta e sistema de abas. Só coordenadas específicas do processo variam. Evitar copiar toda a Screen para cada máquina.

## 7. Comportamento das abas e faces

Ao abrir a máquina, drawer fechado por padrão. Na captura de referência ele pode estar aberto para demonstrar conteúdo. A aba selecionada é estado local de cada jogador, não configuração persistente da máquina.

- Clicar em uma aba abre o conteúdo dela.
- Clicar em outra troca o conteúdo sem alterar modos.
- Clicar novamente na aba ativa fecha o drawer.
- Uma aba aberta por vez.
- Ao redimensionar, preservar seleção se recurso ainda existe; recalcular bounds, não preservar coordenadas antigas.
- Controles ocultos não renderizam, não recebem hover/clique, não entram na navegação de foco.
- Estado exibido de faces vem do servidor. Não “confirmar” uma alteração só porque o cliente clicou.
- Clicar numa face solicita ciclo por modos permitidos. Nenhum modo não suportado pode ser enviado/aplicado com sucesso.
- Consumidores: energia apenas OFF/INPUT. Água de entrada: fluido apenas OFF/INPUT. Itens: modos atuais preservados conforme filtros de slots.
- Input vermelho, output azul, ambos roxo, off branco em todas as telas e legendas.
- Modos relacionam-se a faces RELATIVAS: rotação acompanha frente/trás/esquerda/direita.
- Configurar itens não limita água/energia na mesma face.

Separar ID de recurso do índice da aba visual. Uma máquina sem fluido não pode interpretar o segundo botão como FLUID apenas por posição. A ação de rede deve identificar recurso e face explicitamente. Reutilizar protocolo existente se seguro; não escolher IDs que colidam com auto-output.

Servidor valida menu/container do jogador, `stillValid`, recurso suportado, face e modo. Não aceitar uma seleção local como autorização para mexer em outra máquina.

## 8. Slots: estética e proteção real

### Entrada

Moldura vanilla rebaixada. Indicação cinza discreta de material aceito apenas com slot vazio. Litografia aceita mais de um material; não afirmar que só aceita wafer. Tooltip explica a lista; a indicação de wafer é um exemplo visual. Não alternar símbolos rapidamente nem gerar partículas para indicar aceitação.

### Saída

Moldura dupla cinza neutra, detalhe de bandeja na base. Não usar vermelho/azul funcional como decoração que contradiz modo de face. Inserção manual, por shift-click e automação continuam bloqueadas conforme regras reais do output.

### Balde

Silhueta deve parecer balde, nunca triângulo. Item real substitui a silhueta. O sistema existente deixa balde vazio? Conferir e preservar esse comportamento: não inventar um slot adicional de retorno sem inspecionar inventário. A barra mostra o TANQUE, não a quantidade no balde nem animação fictícia de enchimento do item.

### Duas válvulas: decisão visual versus gameplay

Dois slots reais na aba, com silhuetas. Na referência atual há só um slot de válvula. Proposta de migração: preservar índices antigos 0 entrada, 1 balde, 2 válvula A, 3 output; acrescentar válvula B como índice 4. Não inserir B no meio e deslocar output de um save existente. Validar armazenamento e serialização antes de escolher isso definitivamente.

Atualizar contagem de slots, shift-click, filtros, automação e testes. Saves antigos não podem perder a válvula A. Ausência de B no save significa vazio, não reset do inventário. Não expor válvulas à automação por acidente.

**Armadilha importante:** os slots da aba devem continuar registrados e sincronizados mesmo fechada. Ocultar só o sprite não oculta o Slot. Criar subtipo de Slot com visibilidade/atividade do cliente compatível com a API atual; conferir `isActive`/hit testing, tooltip, teclas numéricas, duplo clique e arrasto. Coordenadas do drawer devem ser iguais em cliente e servidor. A seleção local controla exibição, não validade server-side. Servidor deve continuar rejeitando itens inválidos e operações que violem o inventário.

Não remover/recriar slots do Menu ao trocar aba e não reorganizar seus índices. Isso quebra sincronização e shift-click. Não mover para (0,0) ou fora da tela como única proteção. A área externa deve contar como área interna da GUI para que clicar nela não jogue o item carregado no mundo.

Válvulas 2×/lote 4× estão em planejamento. Combinação, repetição de tipos, energia e custos ainda NÃO foram aprovados. O documento autoriza padrão visual, não inventa balanceamento.

## 9. Dados em tempo real: quem manda em quê

Arquitetura recomendada para este projeto:

```text
BlockEntity no servidor: inventário, FE, tanque, receita, modos e estado real
Menu: view de slots e sincronização de valores para cada jogador
Screen: renderização dos valores sincronizados e estado local das abas
Animação visual: suavização limitada; nunca altera o valor do servidor
```

Usar `Slot` para ItemStacks e `ContainerData`/`DataSlot` para inteiros simples. A documentação NeoForge 26.1 descreve checagem dos menus por tick e o patch que transmite o int completo; não impor o limite vanilla de 16 bits indiscriminadamente. Valores `long` continuam exigindo representação apropriada. [Fonte oficial: Menus](https://docs.neoforged.net/docs/inventories/menus/).

### Contrato mínimo de leitura da UI

| Campo | Tipo conceitual | Uso |
|---|---|---|
| energyStored / energyCapacity | long, não negativo | Barra e tooltip de FE |
| fluidStored / fluidCapacity | long ou int conforme tanque | Barra e tooltip de fluido |
| fluidIdentity | ID + componentes quando relevantes | Sprite, cor e nome corretos |
| progress / maxProgress | int | Seta |
| processSequence | contador de ciclos, se necessário | Impedir interpolação entre receitas |
| machineStatus | enum compacto | Motivo real/indicador |
| modes por recurso | 6 valores válidos | Botões de faces |
| autoEject | boolean | Botão dos itens |
| valveStacks | slots reais | Ícones/efeitos instalados |

Água fixa na Litografia permite identidade conhecida; uma máquina que aceita diferentes fluidos precisa sincronizar identidade e quantidade consistentemente. Não assumir que toda barra azul é água.

Priorizar sincronização do menu enquanto aberto. Não enviar o estado completo a todos os jogadores do servidor a cada tick. Com dois jogadores olhando a mesma máquina, ambos recebem valores reais; suas abas abertas continuam independentes.

A referência já divide `long` de FE em dois ints alto/baixo. Preservar o mecanismo se correto e compatível com a versão; não converter capacidade para int. Se as duas metades chegam em mensagens separadas, a renderização pode observar estado intermediário: ler/publicar o snapshot no tick do cliente, validar limites e testar os pontos de carry. Se ocorrer inconsistência, usar snapshot atômico apropriado, não apenas clamp para esconder o erro.

Payload customizado só se necessário para identidade/componentes, consistência atômica ou estado que o menu atual não resolve. Nesse caso, incluir container/identidade e sequência, validar destinatário atual e descartar mensagens de menus já fechados. O registro e envio de payloads devem seguir a API oficial da versão, não tutorial antigo. [Fonte oficial: Payloads](https://docs.neoforged.net/docs/networking/payload/).

## 10. Barras enchendo: especificação de animação

### 10.1 O significado

O player precisa ver o tanque ganhar/perder fluido e a energia subir/descer enquanto a GUI está aberta. Isso não requer GIF nem vídeo. São recortes de sprites cuja altura varia com os valores sincronizados.

Valores exatos no tooltip = último snapshot válido do servidor. Suavização só modifica a altura desenhada. Não mostrar tooltip de 800 FE enquanto o servidor informou 1.000 FE apenas porque a barra está transitando.

### 10.2 Preenchimento base, sem divisão inteira

Pseudocódigo independente de assinatura NeoForge:

```java
double ratio(long amount, long capacity) {
    if (capacity <= 0) return 0.0;
    return Math.max(0.0, Math.min(1.0, (double) amount / (double) capacity));
}

int fillPixels(double ratio, int innerHeight) {
    if (ratio <= 0.0) return 0;
    if (ratio >= 1.0) return innerHeight;
    return Math.max(1, Math.min(innerHeight, (int) Math.floor(ratio * innerHeight)));
}

// Preencher de baixo para cima, em coordenadas inteiras:
int pixels = fillPixels(displayRatio, 52);
int yStart = innerY + 52 - pixels;
drawClippedFill(innerX, yStart, 6, pixels);
drawFrameAfterFill();
```

Não fazer `height * energy / capacity` usando apenas inteiros: na referência inspecionada a energia/progresso usam expressões inteiras antes do `ceil`, que não suaviza nada e pode truncar/estourar. Converter para double ANTES da divisão/produto e clamping dos valores. `capacity=0` não provoca divisão por zero. Positivo mínimo pode desenhar 1 px; tooltip continua exato.

### 10.3 Suavização recomendada, limitada e honesta

Esta é uma proposta do padrão NovaDyne, não uma obrigação da API:

- Primeiro snapshot ao abrir: desenhar quantidade real imediatamente; não animar de vazio até cheio.
- Novo snapshot: atualizar alvo imediatamente.
- Barra: transição linear curta de 50 ms, com tempo monotônico. Se alvos chegarem durante a transição, partir do valor visual atual para o novo alvo.
- Mudança grande (diferença absoluta de ratio ≥ 0,25), tanque vazio/cheio, identidade de fluido trocada, capacidade alterada ou tela reaberta: snap imediato.
- Sem extrapolação de consumo/produção. Se servidor atrasar, manter o último valor conhecido, não inventar fluxo.
- Ao chegar em 0/1, não continuar exibindo fluido residual/energia inexistente por uma easing longa.
- Quantizar altura final em pixels lógicos inteiros. Não deslocar bordas por meio pixel para “suavizar”.
- Permitir desligar suavização por opção de cliente, se realmente necessária. Com ela desligada, a barra usa snapshot sem atraso visual adicional.
- Não usar interpolação exponencial sem tempo limite: pode nunca chegar exatamente a zero e varia com FPS se implementada errado.

Exemplo conceitual:

```text
onSnapshot(amount, capacity, type, now):
  target = ratio(amount, capacity)
  if first OR boundary OR largeJump OR capacityChanged OR typeChanged:
    startRatio = targetRatio = target
    startTime = now; duration = 0
  else:
    startRatio = currentDisplay(now)
    targetRatio = target
    startTime = now; duration = 50ms

currentDisplay(now):
  t = clamp((now-startTime)/duration, 0, 1), ou 1 se duration=0
  return startRatio + (targetRatio-startRatio)*t
```

50 ms é a proposta inicial para jogo nominal a 20 ticks/s. Não prometer tempo real sem latência de rede. Validar em servidor dedicado e TPS reduzido. Se houver custo/complexidade sem benefício perceptível na barra de 52 px, usar atualização direta por snapshot: correção primeiro.

### 10.4 Fluido: textura e identidade

Usar sprite STILL do fluido e tint correspondente ao fluido/componentes, conforme API cliente da versão. Recortar/tilear dentro da barra, sem esticar uma textura de água por 52 px nem pintar um retângulo azul para qualquer fluido.

A animação do sprite de água, quando fornecida pelo atlas, é administrada pelo jogo. Não recarregar textura nem criar frame manualmente a cada render. Fallback fixo azul é aceitável apenas para prévia ou enquanto falta um sprite; registrar a limitação.

Desenhar preenchimento, depois moldura. Recorte deve impedir água sobre a borda. Restaurar scissor/pose se alterados. Trocar água por outro fluido atualiza sprite, cor, nome e valor juntos; tanque vazio não mantém o nome antigo como se contivesse líquido.

Referência de comportamento observada em fontes locais oficiais do Mekanism: barra de FE calcula altura; fluid gauge seleciona textura STILL, tint e desenha sprite tileado. Não copiar classes/APIs inteiras: o checkout consultado pode ser de versão diferente do NovaDyne. Links e commit no fim.

### 10.5 Energia

FE usa sprite amarelo estático, recortado pela altura. Uma linha clara no topo do preenchimento é opcional e deve ficar dentro da barra. Sem pulsar continuamente, partículas ou brilho caro. Valores/sentido não dependem da cor de INPUT/OUTPUT das faces.

Se quiser indicar fluxo depois, taxa FE/t deve vir de contabilização real no servidor, não diferença de duas amostras da barra (que mistura entradas e saídas). Não é requisito desta fase.

### 10.6 Progresso

Seta preenche da esquerda para direita com `progress/maxProgress`. Reutilizar o mesmo sprite-base e overlay em todas as máquinas.

- `maxProgress<=0`: seta vazia, sem animação fictícia.
- Receita parada: preencher só até progresso real; não continuar por relógio local.
- Receita trocada, concluída, cancelada ou progresso diminui/reset: snap, não interpolar de 100% para 0% atravessando o ciclo seguinte.
- Suavização opcional de até 50 ms apenas em incrementos do mesmo ciclo; sem extrapolação.
- Lote 4× é um ciclo real, não quatro setas/itens fantasmas.

## 11. Indicador de estado e tooltips

Ponto 3×3 após o título; não texto permanente na área da receita. Nome acessível e tooltip mostram motivo. Se tiver múltiplos bloqueios, mostrar um principal e listar outros no tooltip.

Proposta de prioridade determinística: desligada manualmente/redstone → saída sem espaço → material ausente/receita inválida → fluido insuficiente para receita atual → energia insuficiente → processando → pronta. Ajustar se a máquina não possuir um desses estados. Não dizer “sem água” para receita que não consome água.

| Estado | Cor proposta | Tooltip |
|---|---|---|
| Processando | amarelo | Progresso, receita e lote reais |
| Pronta/ociosa | cinza claro | Aguardando receita/ação |
| Sem material | cinza | Material necessário |
| Sem energia | vermelho | Energia insuficiente |
| Sem fluido | vermelho | Fluido necessário e quantidade |
| Output bloqueado | vermelho | Saída sem espaço |
| Desligada/redstone | cinza escuro | Motivo de desligamento |

Não determinar status varrendo receitas/mundo a cada frame. Computar na lógica existente de processo/servidor e sincronizar um estado compacto. Nenhuma piscada obrigatória. Tooltips podem ser criados/atualizados quando valores mudam ou há hover, não com formatação pesada em todo frame.

FE: `Energia: 12.000 / 20.000 FE`; fluido: `Água: 2.000 / 4.000 <unidade>`. Usar a unidade real do armazenamento: não rotular automaticamente como mB sem conferir a API/projeto. Para Litografia, verificar se 1.000 representa um balde antes de traduzir unidade.

Slot de saída: `Saída — não aceita inserção`; face: `Energia · Frente · Entrada`; válvula: item, efeito aplicável e custo aprovados. Texto nativo traduzido pt-BR/en-US. Evitar fonte mini para fazer texto caber.

## 12. Arquitetura enxuta de componentes compartilhados

Reutilizar `AbstractMachineScreen`/Menu atuais e extrair só componentes repetidos. Nomes abaixo são sugestões, não classes existentes:

| Componente | Responsabilidade |
|---|---|
| `MachineUiLayout` | Retângulos/origens compartilhados por Screen/Menu |
| `ResourceTabButton` | Ícone, acento, tooltip, selected/focus |
| `SideModeButton` | Face relativa, modo sincronizado e ação |
| `ResourceDrawer` | Visibilidade/bounds/painel de lados |
| `VerticalGauge` | Moldura, preenchimento e tooltip |
| `ProgressArrow` | Ratio de ciclo e recorte horizontal |
| `EmptySlotHint` | Silhueta apenas no slot vazio |
| `ValvePanel` | Dois slots reais e efeitos confirmados |
| `VisualValueTransition` | Estado de suavização em tempo monotônico |

Menu/BlockEntity definem lógica e permissões. Screen não deve consumir FE, água, itens ou receitas. Layout serve como uma única fonte de coordenadas; não duplicar números divergentes em Java e PNG.

Widgets criados em `init`, com bounds recalculados ao resize; render apenas submete elementos. GuiGraphicsExtractor/AbstractContainerScreen são o caminho documentado para a versão inspecionada. [Fonte oficial: Screens](https://docs.neoforged.net/docs/rendering/screens/).

Não adicionar biblioteca externa, editor em jogo ou dependency apenas para montar quatro abas. Não usar imagemgen, GIF, polling HTTP, leitura de arquivo ou varredura de chunks no render.

## 13. Escalas, hitboxes e integração com outras GUIs

Usar coordenadas lógicas inteiras e nearest-neighbor dos sprites do jogo. Testar GUI Scale Auto/1/2/3/4 onde disponível. Envelope 296×166 cabe em área lógica 320×240 com margem, mas isso é cálculo, não prova de funcionamento.

- Tooltip fica no topo da renderização e respeita bounds da janela.
- Drawer conta como região interna para cliques com item carregado.
- Abas/drawer não provocam descarte de item por “clique fora”.
- Slot da aba fechada não é clicável, hoverável nem narrado como presente.
- Aba ativa expõe estado acessível; cor nunca é única informação.
- Resize não deixa widgets antigos recebendo cliques.
- Se JEI/EMI estiver presente, fornecer área de exclusão correspondente ao drawer/abas pela integração suportada, sem assumir dependência obrigatória.
- Na janela menor que o envelope, adotar uma política explícita e testar; não encolher apenas a textura mantendo hitboxes normais. Se não houver solução segura, sinalizar limitação em vez de ocultar controles silenciosamente.
- Não trocar posições do inventário quando uma aba abre.

## 14. Válvulas: planejamento separado

Ideias do usuário: velocidade 2× e produção de até quatro wafers por operação. Proposta de lote: consumir quatro receitas para obter quatro resultados, permitindo lote menor com insumos disponíveis. Ainda requer confirmação de gameplay.

Não fixar nesta implementação visual: stack de efeitos, duplicatas, multiplicadores finais, consumo extra, velocidade máxima ou receitas das válvulas.

Ao implementar depois: definir lote/efeitos no começo do ciclo; troca de válvula não altera retroativamente o processamento; validar saída, materiais e água/FE; proteger contra perda/duplicação. Para receitas com falha/sucesso aleatório, não reutilizar um único sorteio para todo lote sem decisão explícita. Dois slots não significam automaticamente dois bônus cumulativos.

## 15. Checklist obrigatório de aceite

### Visual

- [ ] Fonte nativa, sem bitmap text embutido em PNG para strings traduzíveis.
- [ ] Slots 18×18; item em inset 1; inventário 9×3 + hotbar 9.
- [ ] Entrada, saída e balde coincidem com coordenadas reais do Menu.
- [ ] Balde junto ao tanque; fluido à esquerda de FE.
- [ ] Sem rótulos permanentes indesejados na área de processo.
- [ ] Ícones de aba quadrados e ordem energia/fluido/itens/válvulas.
- [ ] Vermelho entrada, azul saída, roxo ambos, branco desligado.
- [ ] Duas válvulas visíveis só na aba apropriada.
- [ ] Silhuetas desaparecem ao colocar itens.
- [ ] Hover/focus/selected/disabled legíveis; nenhuma sobreposição.
- [ ] Textos pt-BR/en-US cabem com fonte nativa.

### Atualização e animação

- [ ] Abrir tanque 75% cheio mostra 75% imediatamente.
- [ ] Inserir/remover FE e fluido com GUI aberta atualiza sem reabrir.
- [ ] Zero realmente vazio; cheio exatamente no limite; capacidade zero segura.
- [ ] Variações mínimas não tremem/borram a moldura.
- [ ] Tooltip numérico usa snapshot real, não quantidade interpolada.
- [ ] Tempo de suavização independe de FPS; verificar 30/60/144 FPS.
- [ ] 32-bit/long com valores 32767, 65536, 2³¹ e 2³² não truncam.
- [ ] Mudança de fluido troca nome, sprite e tint sem frame de identidade falsa.
- [ ] Progresso parado não continua; reset não interpola entre ciclos.
- [ ] Lag/TPS baixo não causa previsão fictícia de produção.

### Interação e segurança

- [ ] Drawer fechado não recebe clique/drag/duplo clique/teclas de slot.
- [ ] Clicar drawer carregando item não joga item no mundo.
- [ ] Aba local não altera estado para outro jogador.
- [ ] Face inválida/modo não suportado rejeitados no servidor.
- [ ] Output protegido em clique, shift-click e automação.
- [ ] Válvulas têm filtros e persistência corretos; saves antigos preservados.
- [ ] Alterações de lados independentes e referências antigas de capabilities continuam corretas.
- [ ] Abrir/fechar/resize não cria widgets duplicados ou slots extras.

### Evidência de entrega

Separar código escrito, revisão estática, testes automatizados executados e verificação manual em jogo. Não marcar checkbox por intenção. Screenshots HTML não aprovam hitboxes de Minecraft. Se execução local é proibida, manter os testes de jogo pendentes e dar roteiro reproduzível ao usuário.

## 16. Sequência segura de implementação

1. Ler AGENTS, STATUS e git; preservar estado e descobrir entrega atual dos lados.
2. Mapear slots, capabilities, sincronização, idiomas e widgets atuais.
3. Criar layout/componentes compartilhados mínimos, sem mexer em receitas.
4. Integrar Litografia piloto com barras reais e três abas de lados.
5. Planejar migração do segundo slot de válvula; implementar só com escopo funcional autorizado.
6. Adicionar e testar a aba de válvulas, inclusive slots ocultos.
7. Validar escalas, inputs, servidor dedicado, save antigo e multiplayer.
8. Aplicar os perfis às outras máquinas; não copiar Screen inteira.
9. Revisar diff e documentar pendências; commit/push só se autorizado.

Restrições anteriores continuam relevantes: não alterar OpenCode, wiki, gerador ou hashes; não remover cabos; não implementar transmissor por área; não executar Gradle/Minecraft localmente enquanto essa restrição estiver ativa.

## 17. Prompt de handoff para outra IA

```text
Implemente o padrão de UI do documento Especificacao-UI-NovaDyne.md,
usando o pacote de referência como contrato visual, não como código Java.
Leia o documento inteiro, AGENTS.md, docs/STATUS.md e o estado do Git.
Confira a versão real e a entrega atual dos lados independentes antes de editar.

Use Litografia como piloto. Crie componentes reutilizáveis e layout compartilhado,
não uma Screen diferente do zero para cada máquina. Preserve filtros, saves,
receitas, slots e a autoridade do servidor. Fonte nativa Minecraft; painel cinza;
abas externas quadradas de raio/balde/baú/válvula; barras juntas, fluido à esquerda
de FE; balde junto ao fluido; sem rótulos permanentes sobre slots/barras.
Modo INPUT vermelho, OUTPUT azul, BOTH roxo, OFF branco.

Sincronize dados reais pelo menu. Renderize preenchimento recortado e opcionalmente
suavizado por até 50ms, sem previsão de valores. Tooltip sempre usa snapshot real.
Teste slots ocultos do drawer: não basta esconder a textura. UI sem fluido não tem
aba/barra/balde. Aba de válvulas deve acomodar dois slots, mas a segunda válvula
precisa de migração funcional e filtros: confirme escopo antes de ampliar gameplay.

Não invente balanceamento de velocidade 2x/lote 4x. Não copie APIs de outra versão.
Não altere wiki/OpenCode, não remova cabos, não faça commit/push/merge e não execute
Gradle/Minecraft localmente sem nova autorização. Separe implementação, revisão e
testes executados. Atualize o checkpoint com arquivos, decisões e pendências.
```

## 18. Fontes e proveniência

Consulta feita em 13/10/2026. Conteúdo técnico externo usado como base, decisões de estilo/animação/medidas propostas pelo projeto.

- [NeoForge — Screens, documentação 26.1](https://docs.neoforged.net/docs/rendering/screens/): Screen/container, coordenadas relativas, fonte e renderização da versão.
- [NeoForge — Menus, documentação 26.1](https://docs.neoforged.net/docs/inventories/menus/): slots e sincronização de inteiros, checagem por tick e patch de int completo.
- [NeoForge — Payloads, documentação 26.1](https://docs.neoforged.net/docs/networking/payload/): alternativa quando o menu não resolve o estado necessário.
- [Mekanism — barra de FE](https://github.com/mekanism/Mekanism/blob/feb19590eb4bc0f7ebb4aaa295f2e2c681ab5c63/src/main/java/mekanism/client/gui/element/bar/GuiVerticalPowerBar.java).
- [Mekanism — fluid gauge](https://github.com/mekanism/Mekanism/blob/feb19590eb4bc0f7ebb4aaa295f2e2c681ab5c63/src/main/java/mekanism/client/gui/element/gauge/GuiFluidGauge.java).
- [Mekanism — recorte/tile do gauge](https://github.com/mekanism/Mekanism/blob/feb19590eb4bc0f7ebb4aaa295f2e2c681ab5c63/src/main/java/mekanism/client/gui/element/gauge/GuiGauge.java).

Mekanism foi inspecionado na cópia local oficial no commit indicado; serve de referência de comportamento, não de garantia de compatibilidade de APIs. Não usar texturas do Mekanism no mod.

Fonte bitmap da prévia: atlas ASCII de Minecraft recuperado para demonstração; produção usa fonte e recursos do jogo. Sprites de wafer/válvula da referência pertencem ao projeto NovaDyne. Botões e composição da prévia são determinísticos. Captura atualizada é referência; estados e progresso do HTML são ilustrativos, não telemetria do Minecraft.

## 19. Pendências explícitas

O usuário aprovou a direção visual, não testou as medidas normalizadas no jogo. Precisam de aprovação/validação: limites de texto, adaptação a layouts mais complexos, política para janela minúscula, efeitos/custos das duas válvulas e migração do segundo slot. O padrão serve para executar com poucos esclarecimentos, mas não permite adivinhar regras de gameplay ainda não decididas.

## 20. Primeiro perfil de máquina: Macerador

Ver também `Perfil-UI-Macerador.md` no pacote de referência. A cópia inspecionada usa FE (10.000 FE de capacidade, parâmetro de 20 FE/tick, ciclo base de 120 ticks), dois slots de receita e um slot auxiliar de válvula; sem tanque, fluido ou balde. As posições antigas dos slots pertencem ao painel legado de 310 px e não são coordenadas para copiar para o padrão compacto.

Receitas observadas: bola de argila → pó cerâmico; wafer de silício falho → camada de cobre OU wafer base, com resultado aleatório. Para esse wafer o ciclo só começa com saída vazia. A UI deve indicar input, seta, output e FE; não exibir controles de fluido. O input não deve insinuar que aceita apenas um material. A aba de válvulas deve espelhar a contagem real de sockets após confirmar a branch de trabalho.

Este perfil é uma observação da cópia de referência. Estado funcional, filtros por capability, pausa/consumo de energia, configuração de lados e quantidade de válvulas devem ser conferidos no repo atualizado. Nenhum gameplay foi alterado ao escrever o perfil.

## 21. Extensão futura do universo NovaDyne

O projeto deve poder crescer para armas, veículos e exploração espacial até a Lua. A visão do usuário é a viagem parecer natural e contínua, sem tela de carregamento visível, com a ambição de exploração de No Man's Sky. Isso não muda os critérios da UI industrial em escopo e não autoriza implementar gameplay espacial nesta fase.

Separar sistema de design de template de tela: reusar fonte, cores, textura de botões, slots, ícones, tooltips, barras e regras de estado; criar layouts especializados para máquinas, HUD/painel de veículos, armas e telemetria de foguete. Equipamentos futuros podem compartilhar leitura de energia/combustível sem usar a mesma organização de seis faces.

Tratar continuidade da viagem como objetivo de experiência, não promessa técnica. Antes de construir Lua/voo sem loading, será preciso prototipar o modelo de mundo, dimensões/distância, limites de chunks/memória, renderização de transição, salvamento e multiplayer. Começar por um trecho pequeno veículo→lançamento→chegada e medir no PC alvo; aceitar transição diegética discreta se streaming contínuo não couber no modelo escolhido. Não comprometer a experiência “sem tela” sem um teste jogável.

### 21.1 Nações, fortalezas e presença espacial (conceito futuro)

Nova proposta de mundo: gerar fortalezas de nações fictícias com diferentes níveis de tecnologia. A faixa inicial imaginada inclui nações mais simples, com estruturas menores e defesa por lanças. Nações mais avançadas podem ter complexos maiores, defesas modernas e torres de mísseis que utilizam armamentos adicionados ao NovaDyne. O tipo de estrutura e defesa deve vir de um perfil tecnológico da nação, não de regras soltas por bloco.

A visão espacial se conecta à identidade da nação. Uma nação avançada poderá possuir uma base de lançamento no mundo e uma base própria na Lua. A viagem de foguete saindo daquela base teria como destino a base lunar correspondente da mesma nação. O objetivo de longo prazo é dar uma sensação de continuidade e de mundo conectado; a proposta anterior de voo sem tela de carregamento continua sendo uma ambição a validar tecnicamente, não uma promessa de implementação.

Antes de definir geração procedural ou combate, decidir: se haverá várias nações em um mundo; como são escolhidas as tecnologias; se as fortalezas são ocupadas, hostis, neutras ou negociáveis; como o jogador obtém acesso a lançadores e bases lunares; e se uma base lunar pode ser construída ou descoberta. Evitar estereótipos que equiparem culturas reais a níveis de tecnologia. Tratar esses pontos como questões em aberto até um protótipo de mundo e progressão ser aprovado.

Essa expansão é futura. Não altera o contrato visual das máquinas nem os critérios de aceitação da UI industrial nesta fase.

### 21.2 Identidade e defesa das nações (propostas em aberto)

Cada nação poderá ter um nome e uma cor gerados aleatoriamente por mundo, além de uma atitude passiva ou hostil. A identidade gerada precisa permanecer estável no mundo salvo, e cor deve vir acompanhada de nome, emblema ou forma para não depender só da percepção de cor. A atitude deve ter sinais legíveis ao jogador antes de uma resposta armada; uma possível escala é ignorar, advertir e atacar, ainda sem decisão.

Nações de tecnologia alta podem proteger fortalezas com forcefields. Atravessar/romper a defesa deve exigir tecnologia conquistada pelo jogador. Laser é uma possibilidade, não a solução já escolhida. Candidatos de design: laser de sobrecarga apontado a um emissor; desativar vários emissores/nós em sequência; ou interferir na rede de energia da fortaleza. Cada opção pode criar custo, exposição e risco próprios e evitar que qualquer laser comum funcione como chave universal.

A geração, persistência e comportamento são conceitos para uma fase futura. Ainda não estão definidos nomes, paleta, proporção de atitudes, relações/diplomacia, escalonamento de defesa, vulnerabilidades, custos ou condições de vitória. Não implementar até a progressão e o protótipo de nações serem priorizados.

### 21.3 Canhão laser orbital (ideia de arma de fim de jogo)

O usuário imaginou um satélite que lança um laser orbital colossal, capaz de desintegrar tudo no impacto. Esse canhão pode representar tecnologia de fim de jogo e talvez servir para vencer ou romper forcefields de fortalezas avançadas. Preservar a fantasia de poder destrutivo extremo; os limites de jogo ainda precisam de design próprio.

Possíveis relações com a mecânica de forcefield: atingir um emissor para abrir uma brecha, sobrecarregar o campo ou destruir a estrutura protegida. Possíveis restrições a estudar: satélite em órbita, muita energia, recarga longa, marcação clara de alvo e área de impacto limitada. São hipóteses, não especificação fechada.

Ainda não definido: quem controla o satélite, como é construído/acessado, mira e alcance, custo, recarga, relação com escudos, destruição de blocos/terreno e defesas contra o raio. Não implementar antes de definir o sistema de nações, espaço e armamentos.


### 21.4 Controller portátil e mira do canhão orbital

O usuário propôs um dispositivo portátil chamado Controller, visualmente inspirado em um console de mão/PSP e em um aparelho da série Loki. Seu uso seria contextual: clicar/usá-lo em uma arma ou sistema compatível abre uma tela de configuração. O primeiro caso é o satélite/canhão orbital: o Controller mostra um mapa no qual o jogador seleciona onde o laser vai mirar.

Fluxo candidato: abrir Controller no satélite/sistema autorizado; mostrar mapa tático; selecionar o alvo; mostrar posição e área aproximada de impacto e validade do alcance; confirmar ou abortar a mira. Como o canhão orbital é destrutivo, separar seleção de alvo da confirmação do disparo pode evitar ativação acidental. Essa confirmação é uma sugestão de UX, ainda não regra fechada.

A família visual do Controller deve reutilizar o design system NovaDyne, com layout portátil próprio e informação contextual. No futuro, ele pode configurar armas e veículos compatíveis; não transformar cada tela em cópia da máquina industrial.

Questões em aberto: forma de obtenção (item, bloco ou ambos), interação e permissões, uso remoto ou proximidade, origem dos dados do mapa/terreno conhecido, precisão e alcance, energia/bateria, estado de mira e autorização do disparo. Implementação futura, após a mecânica do satélite e a identidade do Controller serem definidas.


### 21.5 Ideias selecionadas pelo usuário para explorar

Em 13/10/2026, o usuário selecionou quatro propostas para continuar desenvolvendo:

- **Controller/mapa tático:** revelar informações de nações e fortalezas conforme exploração ou escaneamento; incluir território conhecido, alcance de defesas e informação útil sobre forcefields.
- **Infiltração:** permitir caminhos para lidar com fortificações, como invasão de sistemas, sabotagem dos emissores ou evitar detecção, além do ataque orbital destrutivo.
- **Relações reativas:** as ações do jogador podem alterar a atitude de uma nação; uma facção passiva pode ficar hostil, e uma hostil pode eventualmente mudar de atitude após interação/missão. Diplomacia permanece em aberto.
- **Bases lunares especializadas:** bases de nações diferentes podem oferecer funções distintas (combustível, armamentos, pesquisa, veículos).

O sistema de avisos/escalada de mira das torres foi sugerido, mas não selecionado pelo usuário e não deve ser tratado como requisito. Todas as propostas selecionadas ainda precisam de desenho de progressão, limites, persistência e testes antes de qualquer implementação.


### 21.6 Expansão selecionada — exploração, projetos e infraestrutura

Em 13/10/2026, o usuário aprovou as sete propostas abaixo como parte da visão futura do NovaDyne:

1. **Destroços de tecnologia:** veículos abatidos, satélites caídos e bases abandonadas podem oferecer peças recuperáveis e projetos que o jogador aprende a fabricar.
2. **Projetos exclusivos das nações:** especializações tecnológicas (escudos, veículos, armamentos orbitais, entre outras) incentivam explorar e negociar com nações diferentes.
3. **Veículos modulares:** peças como motor, bateria, blindagem, armazenamento e armamento podem ser trocadas. O Controller mostra componentes instalados e configura funções compatíveis.
4. **Rover lunar:** veículo para explorar a Lua, transportar minérios e retornar à base, com possíveis módulos de mineração e pesquisa.
5. **Base espacial própria:** o jogador pode construir infraestrutura por módulos, começando por energia/armazenamento e expandindo para laboratório, hangar e plataforma de lançamento.
6. **Rede de satélites:** satélites de reconhecimento revelam informações no mapa; satélites de comunicação ampliam o alcance do Controller; o laser orbital integra essa família.
7. **Reivindicação de fortalezas:** conquistar uma instalação ou recuperar uma base abandonada e transformá-la em base própria, aproveitando máquinas e defesas.

Loop de progressão selecionado: explorar → encontrar/recuperar tecnologia e projetos → fabricar nas máquinas → montar equipamentos e infraestrutura → explorar locais mais avançados. Projetos, receitas, custos, desbloqueios, geração de estruturas, ownership e regras de conquista ainda precisam de especificação; a seleção aprova a direção de design.

