# Usar o NovaDyne com OpenCode no Windows

## 1. Instalar ferramentas (uma vez)

Abra PowerShell e execute um comando por vez:

```powershell
winget install --id Git.Git -e
winget install --id OpenJS.NodeJS.LTS -e
```

Feche e abra o terminal novamente:

```powershell
npm.cmd install -g opencode-ai
opencode --version
```

Sem winget, instale [Git](https://git-scm.com/downloads/win) e
[Node.js LTS](https://nodejs.org/) pelos sites oficiais. NPM evita o erro de
politica de execucao de npm.ps1 ao usar npm.cmd.

Este guia usa Windows nativo para evitar instalar outro ambiente no PC de 4 GB.
OpenCode recomenda WSL para maior compatibilidade; se houver erro, confirme a
versao e a mensagem antes de instalar WSL. Java/Gradle nao sao necessarios para
usar a IA; a compilacao do mod exige Java 25.

## 2. Baixar o projeto

Se ainda nao tem o repositorio:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\Projetos"
cd "$env:USERPROFILE\Projetos"
git clone https://github.com/nicotfpn/Novadyne-MOD.git
cd Novadyne-MOD
```

Se ja tem, abra o terminal na pasta existente e confira `git status`.
Com a arvore limpa e na main, atualize com `git pull --ff-only`.
Se houver alteracoes locais ou outra branch, preserve o trabalho antes de atualizar.
Nao precisa baixar o ZIP de configuracao nem executar /init.

## 3. Abrir

Dê dois cliques em `ABRIR-NOVADYNE.cmd`, na raiz do repositorio, ou execute:

```powershell
opencode
```

O launcher usa sua propria pasta; funciona mesmo se mover o repositorio.
Dentro do OpenCode, use `/models` e confira **Big Pickle** (`opencode/big-pickle`).
A configuracao usa esse modelo tambem nas tarefas auxiliares.

Se nao estiver disponivel ou pedir conexao, use `/connect` e escolha OpenCode Zen.
A disponibilidade gratuita e temporaria e nao significa cota ilimitada. Se o fluxo
exigir cartao ou compra, pare antes de concluir: esse setup pretende ser gratuito.
Nao compartilhe chaves. O provedor informa que dados do Big Pickle podem ser usados
para melhorar o modelo no periodo gratuito.

Para trocar o modelo no arquivo `opencode.json`, ajuste `model` e `small_model`.
Outro provedor tambem exige ajustar `enabled_providers` e autenticar nele.
A configuracao nao instala plugins nem verifica automaticamente precos futuros.

## 4. Conferir a configuracao

Primeiro pedido:

> Leia AGENTS.md e docs/STATUS.md. Nao altere arquivos ainda. Confirme branch,
> commit e mudancas locais. Verifique que novadyne-review esta disponivel.
> Resuma os limites do meu PC e a proxima tarefa sugerida.

O agente principal se chama `novadyne`. O revisor `novadyne-review` trabalha depois
 da implementacao, sem editar. As regras pedem uma revisao para mudancas relevantes,
 mas a chamada depende de o modelo seguir as instrucoes; nao e um pipeline obrigatorio.

## 5. Primeiro trabalho sugerido

> Corrija somente os filtros dos slots e o shift-clique das quatro maquinas,
> especialmente o Processor. Preserve a insercao interna dos resultados, valves,
> IDs e dados dos mundos. Use novadyne-review depois da implementacao. Prepare
> testes de regressao sem executar builds pesados neste PC. Atualize STATUS e
> entregue as mudancas. Nao faca commit, push, PR ou merge sem minha aprovacao.

## 6. Contexto, RAM e aprovacoes

- Instrucoes permanentes em `AGENTS.md`; checkpoint curto em `docs/STATUS.md`.
- Compactacao automatica ligada. Ela pode perder detalhes; o codigo e o checkpoint
  continuam sendo a referencia, nao uma promessa de memoria perfeita ou uso infinito.
- LSP e formatadores automaticos desligados. Feche navegador, IDE e Minecraft.
- Principal limitado a 60 passos; revisor a 25. Se parar por limite, diga `continue`.
- Edicao local autorizada por pedidos de implementacao. Comandos de terminal pedem
  aprovacao, exceto poucas leituras Git exatas. Revise e aprove uma vez os comandos.
- As permissoes nao sao um sandbox; instrucoes nao impedem toda acao incorreta.
- Build/GameTests no GitHub Actions exigem envio aprovado. Um diff local nao dispara CI.
- Clonar repo publico nao requer login. Push pode pedir autenticacao pelo navegador;
  o login GitHub do ChatGPT nao e transferido para o OpenCode.
- Outro dia, abra o launcher. Use `/sessions` se sua versao oferecer esse comando,
  ou a lista de sessoes no menu. Novas sessoes na mesma pasta leem as mesmas regras.

## Validacao deste setup

Configuracao validada contra o schema oficial em 09/10/2026, caminhos de prompts
conferidos e diff sem erros de espaco. IDs de modelos validados como strings; isso
nao confirma disponibilidade do provedor. O launcher nao foi executado em Windows.
Nao houve mudanca na logica do mod nem novo teste de cliente/Java nesta entrega.

## Fontes oficiais

- [Instalacao](https://docs.opencode.ai/docs/)
- [Configuracao](https://docs.opencode.ai/docs/config/)
- [Permissoes](https://docs.opencode.ai/docs/permissions/)
- [Agentes](https://opencode.ai/docs/agents/)
- [Modelos e precos](https://docs.opencode.ai/docs/zen/)
