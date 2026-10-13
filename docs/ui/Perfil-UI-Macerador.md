# Perfil de UI — Macerador

## Estado desta definição

Primeira máquina mapeada para replicar o padrão visual NovaDyne. Conteúdo conferido numa cópia de referência local, não na implementação de lados do OpenCode que está somente no computador do usuário. Antes de codificar, conferir o branch/arquivos atuais e corrigir qualquer divergência.

## O que a máquina faz na referência

| Aspecto | Comportamento observado |
|---|---|
| Energia | Consumidor; capacidade 10.000 FE; uso configurado 20 FE/tick |
| Fluido | Não possui tanque |
| Balde | Não aceita balde |
| Slots de receita | 0 entrada, 1 saída |
| Auxiliar | Slot 2 para válvula existente |
| Inventário da máquina | 3 slots |
| Duração base | 120 ticks |
| Receita A | Bola de argila → 1 pó cerâmico |
| Receita B | Wafer de silício falho → resultado aleatório: camada de cobre ou wafer base |
| Saída para wafer falho | Só inicia se saída estiver vazia, porque qualquer um dos dois resultados precisa caber |
| Inserção | Menu mostra input, saída bloqueia inserção e slot de válvula aceita válvula válida |

Valores são observação de código, não confirmação de balanceamento no jogo. Energia total de 2.400 FE por receita só é inferível se a máquina realmente consumir 20 FE em cada um dos 120 ticks; confirmar a lógica de pausa/consumo em `AbstractMachineBlockEntity` antes de afirmar ou mostrar esse total.

## O que aparece na UI padrão

- Barra vertical de FE no local padrão da máquina; tooltip com FE armazenada e capacidade.
- Sem aba de fluidos, barra de fluido ou slot de balde.
- Input na esquerda; seta ao centro; saída à direita.
- Válvula não ocupa a região de receita. Na UI atual aprovada, fica na aba externa de válvulas.
- Aba de energia (raio), aba de itens (baú quadrado) e aba de válvulas (ícone da válvula). Não há aba de fluidos.
- Abas externas podem subir para preencher os espaços: energia, itens, válvulas.
- Aba de itens abre os seis lados e o controle de auto-ejeção, se o comportamento atual existir e for sincronizado.
- Aba de energia abre seis faces, mas só oferece desligado/entrada por ser consumidor.
- Aba de válvulas deve refletir slots existentes no código atual. A proposta visual global usa dois slots; a cópia do Macerador inspecionada contém apenas um. Não inventar o segundo slot sem verificar branch e escopo da implementação funcional.
- Estado “sem energia” e estado de processamento vêm do estado real sincronizado. O slot de entrada vazio pode mostrar a silhueta de um item aceito, sem indicar que apenas um dos dois materiais é válido; preferir ciclo discreto de ícones ou tooltip com ambos.

## Organização relativa proposta

Seguir as coordenadas canônicas do documento principal `Especificacao-UI-NovaDyne.md`, encaixando os elementos reais do Macerador. Inputs ficam antes da seta e outputs após a seta. Não reutilizar as coordenadas antigas do menu (45,22 e 117,22) literalmente depois de mudar o tamanho do painel; essas coordenadas são relativas ao layout legado.

O output tem moldura de coleta; não aceita input manual, shift-click ou capability externa. Slot auxiliar de válvula preserva filtros. O inventário do jogador permanece no mesmo padrão de grade e alinhamento do restante das máquinas.

## Status para o jogador

Mostrar um indicador discreto, com tooltip, para processamento e bloqueios. A prioridade deve refletir condições do Macerador: desligada/redstone, saída cheia, sem receita válida, sem energia, processando/ocioso. Não mostrar estados de fluido ou tanque nesta máquina.

Wafer falho pode produzir dois itens diferentes aleatoriamente. O tooltip do input descreve ambos os resultados; a UI não promete um output específico antes da receita terminar. Saída cheia bloqueia a operação para os dois resultados possíveis.

## Conferência pendente no repo atual

- Confirmar as duas receitas e o sorteio do wafer falho.
- Confirmar se limites de entrada/output foram implementados no nível do BlockEntity/capability.
- Confirmar consumo e pausa de FE, incluindo o que ocorre com progresso se faltar energia.
- Confirmar estado atual do slot de válvula e se algum segundo slot foi adicionado na branch de trabalho.
- Confirmar auto-output e sincronização dos lados energia/itens.
- Validar as posições reais de `Slot` contra sprites após integração.

Nenhum arquivo de gameplay foi alterado durante este mapeamento.
