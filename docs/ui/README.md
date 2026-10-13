# NovaDyne — referência de UI

Este diretório contém a entrega de referência de 13/10/2026. Leia primeiro `Especificacao-UI-NovaDyne.md`, o contrato consolidado. `Checkpoint-UI-Abas-NovaDyne.md` conserva decisões e histórico; `Perfil-UI-Macerador.md` detalha a adaptação do Macerador.

Os arquivos estão descompactados para leitura direta por agentes. `Kit-UI-NovaDyne.zip` preserva o pacote original completo. A prévia `Referencia-UI-NovaDyne.html`, os tokens e a captura são referências; não constituem implementação no Minecraft.

## Estado desta entrega

- Somente documentação e referências visuais foram adicionadas ao Git.
- ZIP verificado sem erros; JSON de tokens validado; documentos conferidos contra as versões atuais fornecidas.
- Nenhuma execução nova de Gradle, Minecraft ou GameTests.
- O relatório de validação incluído descreve verificações históricas da prévia HTML, não testes do mod.
- Medidas normalizadas ainda exigem validação no jogo.

## Integração com o trabalho local

Entrega publicada em branch separada `docs/ui-reference`, baseada em `73c240c0`, para preservar a branch de implementação e suas alterações locais. O commit local de configuração de lados informado pelo usuário é `bb780e0`; ele não estava na branch remota no momento desta entrega.

Traga somente o commit desta entrega para a branch de trabalho com fetch e cherry-pick, conferindo antes o estado local. Não use reset, force-push ou descarte de alterações. O conteúdo não altera `docs/STATUS.md`, wiki, configuração do OpenCode ou código de gameplay.
