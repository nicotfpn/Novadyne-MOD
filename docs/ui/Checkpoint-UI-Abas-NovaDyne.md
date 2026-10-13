# NovaDyne — checkpoint de UI, abas e válvulas

## Referência completa atual — entrega de 13/10/2026

Para implementar e padronizar outras máquinas, ler `Especificacao-UI-NovaDyne.md` e o pacote `Kit-UI-NovaDyne.zip`. A especificação é o contrato consolidado mais completo; este checkpoint conserva histórico e decisões.

O kit contém a especificação, `Referencia-UI-NovaDyne.html` autocontido, `UI-NovaDyne-tokens.json`, captura `UI-NovaDyne-Referencia.png`, este checkpoint e relatório `Validacao-UI-Referencia.md`.

Referência atual de cores: vermelho entrada, azul saída, roxo ambos e branco desligado. A nova captura usa essas cores e a geometria normalizada proposta de 176×166 pixels lógicos, com envelope externo 296×166. Essa normalização ainda precisa ser validada em jogo e não altera a direção visual aprovada.

A prévia inclui controles fora da máquina para demonstrar FE, água e progresso; esses sliders NÃO são controles a adicionar ao mod. Demonstração local sem servidor, com 50 ms de suavização curta e snapshots simulados. No mod, valores exatos vêm do servidor/menu; fluido deve usar sprite/tint nativos.

Medidas, fontes, cliques externos, slots ocultos, estados, textos, modos suportados, migração do segundo slot e checklist constam na especificação. Custos/combinações de válvulas 2×/4× continuam não decididos. Nenhuma implementação no mod, compilação ou teste Minecraft foi feito.

## Perfil por máquina — Macerador (primeiro)

Lido na cópia de referência: entrada argila → pó cerâmico; wafer de silício falho → resultado aleatório (camada de cobre ou wafer base); saída; válvula existente; energia apenas; sem tanque nem balde. Tem 10.000 FE de capacidade, 20 FE/tick parametrizados e 120 ticks base. A saída precisa estar vazia ao processar o wafer falho.

UI: input à esquerda, seta, saída à direita; barra FE; sem aba/indicadores de fluido; abas energia, itens e válvulas. Não codificado. O perfil e pontos que exigem conferir na branch atual estão em `Perfil-UI-Macerador.md` e seção 20 da especificação. Cópia consultada pode divergir do trabalho de lados não enviado pelo usuário.

## Visão futura — veículos, armas e Lua

O usuário quer expandir o NovaDyne para armas e veículos e, no futuro, exploração espacial chegando à Lua de forma natural, com sensação de viagem contínua e sem tela de carregamento, na direção de No Man's Sky. Isso é visão de longo prazo, não requisito para a UI/máquinas atuais nem autorização para começar conteúdo agora.

Consequência para arquitetura visual: reutilizar tokens e componentes pequenos (fonte Minecraft, slots, botões, barras, ícones e tooltips), mas criar famílias de layout diferentes. Máquinas usam tela de processamento; veículos precisam de painel/controles; armas precisam de interface própria; foguete/nave precisa de telemetria e estado de viagem. Não forçar sidebar e inventário de máquina em toda tela.

Escadinha de produto sugerida, ainda não aprovada como roadmap definitivo: 1) fechar máquinas e identidade visual; 2) definir materiais/energia/combustível e receitas de construção de veículo; 3) veículo terrestre simples e testável; 4) armas como sistema modular com limites e feedback claro; 5) foguete, combustível, lançamento e telemetria; 6) viagem terrestre-espacial e chegada à Lua com streaming/transição contínua. A percepção sem loading é objetivo de UX; a arquitetura técnica que a viabiliza deve ser prototipada antes de prometer seamless real. Pode exigir uma solução própria de mundo/dimensões e tem risco e escopo bem maiores que conteúdo normal de mod.

Atualizado em 13/10/2026, horário de Brasília. Este documento registra o planejamento visual feito com o usuário e permite continuar em outra conversa. Não é um relatório de implementação no mod.

## Estado atual

Estamos desenhando a Litografia como piloto visual. Foram criadas prévias HTML e capturas reais do navegador. Nenhuma mudança deste trabalho visual foi aplicada ao código Java, texturas ou menus do mod. Minecraft não foi executado; não há validação visual em jogo.

A primeira imagem gerada por IA foi descartada como referência técnica. O usuário quer capturas reais de layouts, sem ImageGen para inventar a interface.

Última captura disponível: `litografia-ui-refinada.png`, em `/novadyne/litografia-ui-refinada.png`. Incorpora balde junto à barra de água e válvula em uma quarta aba externa. A captura mostra a aba de válvulas aberta, com dois slots vazios e silhuetas.

## Direção visual decidida com o usuário

- Interface nativa do Minecraft Java/NeoForge, com aparência coerente com o jogo.
- Mekanism como referência de organização, interação e fluidez; não copiar sua identidade visual nem suas texturas.
- Fonte nativa do Minecraft na implementação. A última prévia usa uma fonte construída a partir dos caracteres bitmap de Minecraft para aproximar a aparência; essa fonte de prévia não precisa entrar no mod.
- Botões quadrados, com textura cinza discreta, borda e estados visíveis. Evitar o aspecto liso que o usuário descreveu como “Bedrock”.
- Layout limpo, sem textos explicativos permanentes sobre os slots e barras.
- Manter apenas título da máquina e identificação do inventário como na prévia. O usuário pediu retirar rótulos como “Água”, “FE”, “Balde / Água”, “Material / Entrada” e “Resultado / Saída” de dentro da máquina.
- Explicações e valores devem ser apresentados por tooltip, sem poluir a tela.
- Ícones de slot vazio devem representar o item: silhueta de balde para o slot do balde; silhueta da válvula para o slot da válvula. A indicação desaparece quando o slot contém um item.
- Não usar triângulos ou outros símbolos genéricos para representar itens.
- Reutilizar um padrão visual entre máquinas, depois de aprovar o piloto.

## Layout mais recente a desenhar

1. Centro da máquina: entrada de material → seta de progresso → saída.
2. Barras de água e energia JUNTAS no lado direito da tela principal.
3. Dentro desse par: água à esquerda, FE à direita. A fala anterior sobre “trocar os lados” se referia à ordem das duas barras, não a colocar uma barra em cada extremidade da máquina.
4. Slot do balde próximo da barra de água. Já representado na nova prévia.
5. Retirar o slot da válvula da região principal e colocá-lo em uma aba externa própria de válvulas, conforme direção proposta na última troca. Já representada na nova prévia, com slot vazio, silhueta e estado “Nenhuma instalada”.
6. Inventário do jogador: 9 colunas × 3 linhas e hotbar separada de 9 slots. Não criar linhas extras nem duplicar slots ao reconstruir o HTML.

## Abas externas de configuração

Os controles ficam fora do painel principal, no canto superior direito. São quadradinhos em uma coluna, não botões largos com nomes dentro da máquina.

| Ordem | Ícone | Recurso | Identificação visual |
|---|---|---|---|
| 1 | Raio | Energia | Acento amarelo |
| 2 | Balde | Fluidos | Acento azul |
| 3 | Baú quadrado | Itens | Acento de baú; tooltip identifica |
| 4, proposta atual | Válvula | Válvulas/upgrades | Silhueta do item real do mod |

Clicar no quadradinho de energia, fluido ou itens abre um painel externo com os seis lados daquele recurso. Clicar em outro troca o recurso exibido. A prévia permite clicar novamente no ativo para fechar. Esse comportamento de fechamento foi adotado na prévia, ainda não validado em jogo.

O painel aberto não ocupa espaço do inventário nem sobrepõe slots e barras. Recursos não suportados por uma máquina não devem aparecer. A aba de válvulas terá conteúdo próprio, não a grade de seis lados.

### Painel dos seis lados

- Faces relativas: frente, trás, esquerda, direita, cima e baixo.
- Disposição em cruz/cubo, como nas prévias.
- Siglas provisórias: F frente, T trás, E esquerda, D direita, C cima, B baixo.
- Tooltip identifica recurso, face e modo; não depender exclusivamente de cores ou siglas.
- Cores atualizadas pelo usuário às 00:56: branco desligado, VERMELHO entrada, AZUL saída, ROXO entrada/saída. Substitui o esquema anterior azul entrada/laranja saída.
- Cada recurso mantém configuração independente.
- Selecionar uma aba não modifica configurações por si só.
- Auto-output pertence aos itens. Mostrar seu controle apenas no painel de itens; não confundir com saída de energia ou fluido.
- Consumidores de FE oferecem somente desligado/entrada. Litografia aceita fluido como entrada; não oferecer saída de água se o armazenamento não a suporta.

## Slots reais conferidos nesta conversa

Foi inspecionada uma cópia local de referência em `audit-novadyne`. Não presumir que seja o checkout atual do usuário: antes de implementar, ler o repositório e seu estado corrente.

| Índice | Função na Litografia | Posição encontrada no menu de referência |
|---|---|---|
| 0 | Entrada de material | x=54, y=22 |
| 1 | Balde de água | x=54, y=58 |
| 2 | Válvula | x=145, y=57 |
| 3 | Saída, bloqueada para inserção | x=118, y=40 |

Fontes consultadas: `LitografiaMenu.java`, `LitografiaScreen.java`, `LitografiaBlockEntity.java` e textura `valve_tier_1.png`. O slot da válvula existe de verdade; a dúvida anterior sobre ele era decorrente de uma proposta visual ainda não conferida.

A máquina de referência possui quatro slots, tanque de 4.000 de água, uso de 1.000 de água por wafer na operação correspondente e armazenamento de 20.000 FE. Estes valores são observações da cópia inspecionada, não decisões novas de balanceamento.

A prévia muda a organização visual dos slots. Implementar isso exige alinhar as posições reais do Menu às posições desenhadas na Screen. Um PNG/HTML não altera inventário ou regras por conta própria.

## Válvulas: ideias em planejamento

O usuário propôs válvulas de 2× e uma que faça quatro wafers em vez de um. Ainda não foi implementado nem fechado o balanceamento.

Direção atual: aba externa própria, mostrando DOIS slots de válvula, seus efeitos e custos. O usuário pediu dois slots após aprovar o layout. A proposta anterior de um único slot foi substituída. A alternativa de colocar a válvula na aba de energia foi discutida; a aba própria foi recomendada por permitir efeitos além de FE.

| Ideia | Comportamento proposto | Pendências |
|---|---|---|
| Velocidade 2× | Metade do tempo de processamento | Definir aumento de FE/tick e custo total por receita |
| Lote 4× | Processar até quatro receitas simultaneamente | Conferir receitas, resultados variáveis, consumo e espaço na saída |
| Eficiência | Reduzir FE por receita | Ideia adicional sugerida, sem confirmação do usuário |

Para Lote 4×, a proposta é quatro entradas virarem quatro resultados com os custos de quatro receitas, não multiplicar um item de graça. Se houver material para dois, processar dois foi sugerido. Confirmar essa semântica com o usuário antes de implementar, pois ele ainda não respondeu especificamente à proposta de custos.

Cuidados propostos: validar insumos, água, FE e espaço de saída antes de iniciar; não permitir perda/duplicação; definir o lote no início; trocar/remover a válvula durante um processamento não pode alterar retroativamente o lote. Verificar o comportamento e as tiers das válvulas existentes antes de criar uma segunda progressão concorrente.

## Relação com o trabalho funcional de lados

O usuário está conduzindo em outra sessão/OpenCode uma tarefa para adicionar lados independentes de energia e fluidos nas máquinas. O último relato recebido dizia que o núcleo tinha sido implementado e ainda faltavam Menu/Screen, traduções, GameTests, revisão e checkpoint. Não assumir que isso permanece pendente ou que já terminou: pedir/ler a entrega atual antes de integrar a nova direção visual.

Máquinas do escopo anterior: Macerador, Prensa de Wafers, Processador e Litografia. Não ampliar automaticamente para geradores, baterias ou novos blocos.

Limites do trabalho anterior: preservar alterações locais; não executar Gradle/Minecraft localmente; não alterar configuração do OpenCode, wiki, gerador ou hashes; não fazer commit/push/merge; não implementar o transmissor de FE nesta entrega. Essas restrições não são autorização para modificar o repositório nesta conversa: até aqui o trabalho autorizado foi a proposta visual e sua documentação.

A próxima tarefa funcional registrada anteriormente é um transmissor local de FE por área configurável, respeitando lados e sem carregar chunks. Não misturar essa implementação com a exploração visual de abas/válvulas.

## Validação e próximos passos

Feito nesta conversa:

- Capturas reais de prévias HTML, sem ImageGen nas versões atuais.
- Refinamento de fonte, botões, silhuetas e controles externos.
- Inspeção dos quatro slots reais na cópia de referência.
- Verificação no navegador de abrir/fechar painéis, selecionar recurso e mudar uma face.

Pendente:

1. Obter feedback do usuário sobre a nova prévia e ajustar se necessário.
2. Definir a apresentação da válvula instalada e de seus efeitos, sem antecipar balanceamento.
3. Fechar o comportamento das válvulas com o usuário e conferir as existentes.
4. Receber/inspecionar a entrega funcional atual do sistema de lados.
5. Integrar o piloto ao mod somente quando solicitado, respeitando regras do repo.
6. Validar em jogo escalas de GUI, janelas pequenas, tooltips, áreas clicáveis, posições reais de slots, estados dos botões e sincronização de servidor.

Não declarar “sem bugs visuais” ou “testado no Minecraft” por captura HTML ou análise estática.

## Como retomar em outra conversa

“Leia Checkpoint-UI-Abas-NovaDyne.md e use a última captura como referência parcial. Continue a proposta visual da Litografia: barras juntas à direita, água à esquerda de FE; balde junto à água; válvula numa quarta aba externa própria; três abas de lados em quadradinhos com raio, balde e baú. Use fonte Minecraft, botões texturizados e silhuetas de slot vazio; não coloque rótulos nos slots/barras. Antes de codar no mod, confira o estado atual do repo e a entrega de lados. As válvulas 2×/lote 4× ainda estão em planejamento. Não gere a GUI por IA; entregue captura real do layout.”

## Manutenção deste checkpoint

Atualizar este mesmo documento após decisões relevantes. Registrar mudanças, decisões confirmadas, propostas pendentes, última captura e o que foi realmente implementado/testado. Não substituir propostas por fatos nem presumir que as prévias foram integradas ao mod.

## Nova decisão de cores — 13/10/2026, 00:56

Usuário definiu as cores dos botões de configuração das faces, para energia, fluidos e itens: vermelho INPUT/entrada, azul OUTPUT/saída, roxo BOTH/entrada e saída. Desligado mantém branco. Atualizar botões, legenda e tooltips de forma consistente. Isso não muda os modos suportados por cada máquina: consumidores de FE e fluido de entrada continuam apenas desligado/entrada. A última captura ainda usa o esquema anterior; ajustar na próxima prévia. Os acentos dos ícones que identificam recursos (raio, balde, baú) são independentes dessas cores de modo.

## Atualização — nova UI solicitada às 00:32

Criada captura `litografia-nova-ui.png`: entrada/seta/saída no centro, balde junto ao par água/FE à direita, válvula removida da região principal e colocada em sua própria aba externa. Quatro botões quadrados: raio, balde, baú, válvula. A prévia inicia com a aba de válvulas aberta.

Verificações executadas no navegador: alternar para energia; esconder conteúdo de válvulas ao trocar recurso; alternar para fluido e bloquear uma face; disponibilizar ejeção apenas em itens; reabrir válvulas; fechar ao clicar novamente na aba ativa. Nenhuma implementação Java ou teste Minecraft foi feito. Efeitos 2×/lote 4× continuam em planejamento.

## Decisão confirmada — 13/10/2026, 00:50

O usuário aprovou o layout atual: “assim já tá muito bom”. Manter a direção visual e evitar novo redesenho sem necessidade.

- Fluidos: aba, barra e controles de líquido aparecem somente em máquinas com suporte real a fluido. Slot com silhueta de balde aparece somente quando a máquina também aceita abastecimento por balde. Ter tanque não implica necessariamente aceitar baldes.
- Máquinas sem fluido não exibem aba de fluidos, barra de água ou slot de balde vazio/desativado.
- Válvulas: usuário pediu DUAS válvulas. A aba deve ter dois slots, substituindo a proposta anterior de slot único. A prévia refinada já mostra dois slots.
- Ainda pendente: regras de combinação, repetição de tipo, empilhamento de bônus e balanceamento. Não presumir que duas válvulas de velocidade multiplicam ou somam efeitos.
- Sugestão a discutir: permitir combinar uma de velocidade com uma de lote, sem duplicar o mesmo tipo inicialmente. Não é decisão confirmada.
- A Litografia existente tem apenas um slot real de válvula na cópia inspecionada. O segundo slot exige mudança funcional no inventário/menu, persistência e regras; a aprovação visual não prova que ele existe no mod.

## Refinamento solicitado — 13/10/2026, 00:52

Usuário autorizou aplicar à prévia os refinamentos sugeridos. Nova captura: `litografia-ui-refinada.png`.

- Entrada: indicação visual derivada da textura real de wafer sujo, com baixa opacidade. É indicação de slot vazio, não um item fornecido gratuitamente. A Litografia também aceita circuitos empilhados; tooltip deve explicar materiais aceitos. Avaliar com o usuário se a textura do wafer é suficientemente clara.
- Saída: borda dupla neutra e detalhe de bandeja na base, sem texto permanente.
- Seta de progresso: forma pixelada com preenchimento amarelo ilustrativo. Não há receita real rodando nesta prévia; conectar ao progresso do servidor somente na implementação.
- Indicador discreto junto ao título: estado ilustrativo amarelo e tooltip. Definir estados processando, sem material, sem energia, sem água e saída cheia com prioridade consistente ao implementar.
- Balde alinhado junto às barras; água à esquerda de FE.
- Aba de válvulas: dois slots lado a lado, com silhuetas. Efeitos e custos de válvulas instaladas ainda não desenhados nem definidos funcionalmente.
- Mantidos controles externos em quatro quadradinhos e ausência de rótulos permanentes em slots/barras.

Checks de navegador executados: alternância dos painéis, troca de face de fluido, disponibilidade da ejeção em itens, abertura de válvulas e fechamento da aba ativa. Minecraft/Gradle não executados; mod não alterado.

## Nova direção de mundo — nações, fortalezas e Lua

Ideia proposta pelo usuário em 13/10/2026: o mundo pode conter estruturas que funcionem como fortalezas de nações fictícias, com níveis diferentes de desenvolvimento. Nações mais simples podem ter fortalezas modestas e defesa com lanças; as mais avançadas podem ter instalações militares e torres de mísseis, usando armas que fazem parte da progressão do NovaDyne.

A exploração espacial pode se conectar a essas nações: uma nação avançada teria uma base de foguetes e uma base correspondente na Lua. A ideia é que, ao partir daquela base, o foguete chegue à base lunar daquela mesma nação. Isso cria continuidade entre mundo, tecnologia, armas e espaço, em vez de a Lua parecer um destino desconectado.

É direção de longo prazo e conceito em aberto, não conteúdo aprovado para implementação agora. Ainda não foram decididos nomes/identidades das nações, geração das estruturas, hostilidade, alianças, acesso às bases ou regras de viagem. Manter as nações ficcionais e dar identidade própria sem associar automaticamente “pobre/atrasada” a povos ou culturas reais.


## Refinamento da ideia de nações — identidade, atitude e escudos

Em 13/10/2026, o usuário acrescentou que cada nação pode receber uma cor e um nome aleatórios, e variar entre passiva e hostil. Nações de tecnologia mais alta podem proteger suas fortalezas com forcefields. Atravessá-los exigiria uma tecnologia que o jogador conquista, talvez laser; a mecânica exata permanece aberta.

Ideias para explorar depois:
- Gerar nome e cor por mundo, mas salvar o resultado para a nação manter a mesma identidade em todas as visitas. A cor deve aparecer junto de nome/símbolo para não ser o único identificador.
- A atitude pode orientar se a fortaleza ignora, adverte ou ataca o jogador. Escalar de aviso para combate daria leitura clara antes de uma torre de mísseis disparar.
- O forcefield pode depender de uma fonte de energia ou de emissores. Possíveis soluções: laser que sobrecarrega um emissor, ferramenta que desativa nós em sequência, ou invadir a rede elétrica da fortaleza. São opções para discutir, não regras decididas.
- Tecnologia de escudo deve refletir o nível da nação; evitar que todas as fortalezas avançadas usem a mesma defesa ou que o laser seja uma chave universal sem custo/risco.

Não definido: lista de cores/nomes, distribuição de atitudes, relacionamento entre nações, comportamento exato das defesas, custo/risco para abrir o escudo e se haverá diplomacia. Isso continua sendo planejamento de longo prazo, sem implementação autorizada nesta etapa.



## Ideia de arma orbital — canhão laser de satélite

Em 13/10/2026, o usuário propôs um satélite que dispara um laser orbital extremamente poderoso, capaz de desintegrar tudo no ponto atingido. É uma possível arma de fim de jogo e pode inspirar uma tecnologia para superar os forcefields das fortalezas avançadas. Manter a escala épica e destrutiva da ideia; não converter automaticamente em arma comum ou equilibrada para uso frequente.

Caminhos de gameplay a explorar, ainda não decididos: o laser pode destruir um emissor de escudo ou sobrecarregar o forcefield; exigir satélite em órbita, energia/tempo de recarga e marcação precisa do alvo; e ter limites claros de uso e impacto no terreno. Não está definido se pertence ao jogador, a uma nação ou a ambos, nem se o raio atravessa blocos, alcance, custo, recarga, proteção contra ele ou efeitos no mundo.


## Dispositivo portátil Controller — interface contextual

Em 13/10/2026, o usuário propôs um dispositivo portátil chamado Controller, com aparência e interface de console de mão/PSP inspirado em um aparelho da série Loki. O jogador usaria o Controller em armas ou outros sistemas compatíveis para abrir configurações. Primeiro caso imaginado: usar o Controller no satélite/canhão orbital abre um mapa para escolher onde o laser vai mirar.

Ideia de fluxo para o satélite: Controller → mapa tático → selecionar ponto de impacto → visualizar área/alcance do disparo → confirmar mira. Considerar uma etapa explícita de confirmação/aborto porque o efeito pode ser enorme. Depois, a mesma peça pode abrir controles contextuais de armas e veículos, mantendo componentes e estética NovaDyne sem forçar a UI industrial das máquinas.

Em aberto: se o Controller é item, bloco, ou ambos; quais sistemas aceitam interação; como o mapa obtém/revela terreno; alcance e precisão; acesso remoto vs. proximidade; permissões/ownership; bateria/energia; e etapas necessárias para autorizar o disparo. Conceito futuro, não implementação aprovada.


## Ideias aprovadas para continuar explorando — 13/10/2026

O usuário gostou destas quatro ideias para a expansão de nações, Controller e Lua:

1. **Mapa tático no Controller:** mostrar território conhecido, identidade da nação, alcance das torres e informações/áreas de força do forcefield. Regiões desconhecidas podem ser reveladas por exploração ou escaneamento.
2. **Infiltração com abordagens alternativas:** o canhão orbital é a opção destrutiva; outras rotas podem incluir invadir sistemas, sabotar emissores do forcefield ou evitar detecção. A mecânica concreta ainda precisa ser desenhada.
3. **Relações reativas:** ações do jogador podem mudar a atitude de uma nação — por exemplo, uma nação passiva pode tornar-se hostil após ataque/roubo; uma nação hostil pode mudar de atitude após troca ou missão. Diplomacia ainda não foi definida.
4. **Bases lunares especializadas:** bases de nações diferentes podem focar em combustível, armas, pesquisa ou veículos, levando a identidade da facção para o espaço.

A ideia de avisos/etapas de mira antes das torres de mísseis atacarem foi sugerida e não foi selecionada pelo usuário; não incluir como requisito atual. As quatro ideias acima continuam sendo direção de design para o futuro, sem implementação imediata.



## Expansão selecionada — exploração, projetos e infraestrutura

Em 13/10/2026, o usuário aprovou as sete propostas abaixo como parte da visão futura do NovaDyne:

1. **Destroços de tecnologia:** veículos abatidos, satélites caídos e bases abandonadas podem oferecer peças recuperáveis e projetos que o jogador aprende a fabricar.
2. **Projetos exclusivos das nações:** especializações tecnológicas (escudos, veículos, armamentos orbitais, entre outras) incentivam explorar e negociar com nações diferentes.
3. **Veículos modulares:** peças como motor, bateria, blindagem, armazenamento e armamento podem ser trocadas. O Controller mostra componentes instalados e configura funções compatíveis.
4. **Rover lunar:** veículo para explorar a Lua, transportar minérios e retornar à base, com possíveis módulos de mineração e pesquisa.
5. **Base espacial própria:** o jogador pode construir infraestrutura por módulos, começando por energia/armazenamento e expandindo para laboratório, hangar e plataforma de lançamento.
6. **Rede de satélites:** satélites de reconhecimento revelam informações no mapa; satélites de comunicação ampliam o alcance do Controller; o laser orbital integra essa família.
7. **Reivindicação de fortalezas:** conquistar uma instalação ou recuperar uma base abandonada e transformá-la em base própria, aproveitando máquinas e defesas.

Loop de progressão selecionado: explorar → encontrar/recuperar tecnologia e projetos → fabricar nas máquinas → montar equipamentos e infraestrutura → explorar locais mais avançados. Projetos, receitas, custos, desbloqueios, geração de estruturas, ownership e regras de conquista ainda precisam de especificação; a seleção aprova a direção de design.

