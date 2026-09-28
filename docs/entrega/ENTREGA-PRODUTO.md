# Conferência da entrega — Produto funcionando para o cliente

**Versão candidata:** 0.5.0-rc1. **Ativação e homologação:** 27/09/2026.

## Diagnóstico do material enviado anteriormente

O ZIP original contém a mesma implementação de rotas e configuração encontrada na versão 0.3: listagem fictícia, cadastro dependente de URL não configurada e cesta sem gravação. O print `ErroAoCadastrarAPI.PNG` mostra `Nonepessoas`, indicando ausência da URL base. Isso é falha de configuração, não demonstração de rejeição correta de dados inválidos.

O ZIP também inclui `.git`, ambientes virtuais e cache; esses arquivos não substituem instruções de instalação. Os PDFs de roadmap, backlog e changelog ajudam a explicar escopo e histórico, mas não comprovam execução dos fluxos. Os três prints antigos mostram listagem fictícia, erro de cadastro e saída para login; não mostram uma operação persistida no Oracle nem uma demonstração confirmada pelo cliente.

## Atendimento dos requisitos

| Requisito | Material preparado / situação |
|---|---|
| 1. Código-fonte completo | Fontes Flask, templates, CSS, configuração de exemplo, testes, estrutura lógica das tabelas e exportação da API ORDS em `database/`. |
| 2. Produto executável ou acessível | Execução local com `INICIAR.cmd`; operador e OAuth já configurados neste computador. Outra instalação exige credenciais próprias. |
| 3. README com objetivo, tecnologias e execução | README reescrito com instalação, configuração de operador, URL base e diagnóstico. |
| 4. Recursos entregues | Login, listagem, busca, cadastro completo, consulta, edição, óbito, inativação, agenda e histórico de cestas. Serviços permanecem pendentes. |
| 5. Evidências dos principais fluxos | 28 testes locais, 23 verificações reais e operação no navegador; veja `docs/evidences/v05-oracle/README.md`. |
| 6. Problemas e limitações | `LIMITACOES.md`, incluindo dependências remotas e operação. |
| 7. Demonstração ao cliente | Roteiro pronto; apresentação e confirmação ainda não realizadas nesta revisão. |

## Correções implementadas no código

- Configuração obrigatória da URL e dos segredos; mensagem clara ao iniciar sem configuração.
- Remoção da listagem fictícia do fluxo normal e adequação dos nomes do JSON ao Oracle observado.
- Login sem senha padrão, sessão temporária, rotas protegidas e verificação de token nos formulários.
- Validação de CPF, nascimento, situação e limites dos campos; preservação do formulário após erro.
- Busca por nome ou CPF e leitura das páginas da coleção.
- Falhas da API tratadas sem expor respostas brutas, dados clínicos ou rastros de execução.
- Versão identificada nas telas e em `/ping`.
- Bloqueio de recursos remotos não homologados para não exibir sucesso fictício.

## Resultado da integração 0.5

Campos clínicos e histórico instalados no Oracle. O novo módulo recusou acesso anônimo; o cliente autorizado realizou cadastro,
edição, limpeza de campo, entrega e inativação por óbito. Duas entregas concorrentes geraram uma única linha, com respostas 201/409.
Nova instância confirmou os dados após nova autenticação. O navegador também registrou uma entrega com próxima data calculada.
Essas evidências técnicas não substituem a demonstração ao cliente, ainda pendente.

## Histórico da integração 0.4

O usuário confirmou que os dados são fictícios e autorizou testes. A primeira tentativa falhou na conexão (timeout/403). Uma comparação posterior obteve JSON 200 pelo cliente HTTPX. A aplicação passou a usar esse cliente, com HTTP/2 habilitado e certificados verificados. Em 27/09/2026, `tools/homologar_ords.py` concluiu 11 verificações com o Oracle real, incluindo cadastro, edição, inativação e leitura após nova sessão. O registro de teste ID 21 permanece inativo. O relatório aprovado é `oracle-real-20260927T050620.json`; a tentativa anterior foi preservada como histórico.

## Critérios para liberar a entrega como funcionando

- [x] API real responde à aplicação.
- [x] Um paciente identificado como TESTE é criado e encontrado em nova consulta.
- [x] Sua edição persiste após recarregar e iniciar nova sessão.
- [x] CPF inválido é rejeitado pela aplicação antes de enviar ao Oracle (teste automatizado e captura real de interface).
- [x] Situação inativa persiste.
- [x] Screenshots correspondem à versão identificada e usam apenas dados fictícios.
- [ ] Cliente ou usuário final acompanha o roteiro e registra o que foi atendido e o que fica para depois.

Não marcar esses itens a partir de testes simulados. O estado desta checklist deve ser atualizado somente após cada verificação efetiva.
