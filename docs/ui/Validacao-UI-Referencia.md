# Verificação do pacote de UI

13/10/2026. Verificações executadas em Chromium headless sobre a prévia HTML:

- 36 slots do jogador, exatamente 27 inventário + 9 hotbar.
- Seis controles de faces por recurso.
- Dois slots de válvula.
- Alternância entre energia/itens/válvulas.
- Ejeção de itens visível no painel de itens.
- Faces ocultas ao abrir válvulas.
- Drawer fechado ao clicar novamente na aba ativa.
- Barra de FE em 0%, 50% e 100%: 0, 26 e 52 pixels lógicos de preenchimento.
- Demonstração local modifica os valores e pode ser parada.
- Captura visual revisada; texto longo de ajuda foi abreviado para não exceder o painel.

Não executado: Gradle, compilação Java, Minecraft, servidor dedicado, verificação de fluid sprites nativos, migração de segundo slot, teste de interação de slots reais de Minecraft, escalas de GUI do jogo. O HTML não prova esses comportamentos.

As medidas canônicas são especificação proposta, normalizada para slots reais. As animações usam dados simulados locais; a implementação real deve ler snapshots do servidor. A água do HTML usa um padrão simples, não o sprite animado nativo. Consultar a especificação para a solução de produção.
