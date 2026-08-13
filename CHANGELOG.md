# Changelog

Todas as alteracoes relevantes realizadas no Sistema de Gestao RCC sao registradas neste documento.

**Nota de rastreabilidade:** Este CHANGELOG foi criado retrospectivamente em 2026 a partir do historico Git, codigo-fonte, documentacao e registros de Sprint disponiveis. Os registros anteriores a criacao deste arquivo representam mudancas reais identificadas no projeto, mesmo quando nao existia um CHANGELOG formal na epoca.

## Estado atual - versao academica 0.3

### Adicionado

- Aplicacao Python/Flask organizada com Application Factory, Blueprints, templates Jinja2 e arquivos estaticos.
- Rotas de pacientes para listagem, cadastro, edicao, exclusao e detalhes.
- Cadastro de servicos vinculados a pacientes.
- Historico basico de servicos exibido na tela de detalhes do paciente.
- Integracao preparada com Oracle ORDS/API REST usando `requests` e `API_BASE_URL`.
- Tratamento basico de erros e timeout nas chamadas para a API.
- Tela de login, logout, sessao, hash de senha com Werkzeug e usuario mockado para desenvolvimento.
- Decorador `login_required` aplicado parcialmente em rotas internas.
- Controle inicial de cesta basica em modo mock, com calculo de atraso e rota visual temporaria de entrega.

### Alterado

- Backend reorganizado para a estrutura atual em `app/`, `templates/`, `static/` e `run.py`.
- Persistencia anterior foi substituida por consumo de API Oracle ORDS/API REST.
- Interface visual evoluiu com CSS proprio, navegacao, formularios e telas de listagem/detalhes.

### Documentacao

- README organizado com contexto do projeto, execucao local, tecnologias, equipe e links principais.
- Documentos de planejamento criados em `docs/planning/`.
- Workflow, POPs, Kanban, Gantt e evidencias de versionamento organizados em `docs/`.
- Sprint 01 de 2026 registrada como primeira Sprint formal da retomada.
- Sprints historicas reconstruidas em `docs/sprints/historico/`.
- Indice de Sprints criado em `docs/sprints/README.md`.
- Links documentais de Sprint e evidencias fisicas corrigidos.
- Backlog e roadmap reorganizados para separar possibilidades futuras de itens efetivamente comprometidos.
- Este CHANGELOG foi criado para registrar somente mudancas ja realizadas.

## Historico reconstruido

### Setembro de 2025 - Fundacao do projeto

Evidencias Git: commits `746b051` e `a89cac6`, em 13/09/2025.

- Criacao inicial do repositorio do projeto RCC.
- Inclusao de configuracao inicial em `config.py`.
- Inclusao de dependencias em `requirements.txt`.
- Criacao e ajuste inicial de `.gitignore`.

### Setembro de 2025 - Gestao de pacientes

Evidencias Git: commits `84c300b`, `681e133`, `53219c9`, `ea8cebb`, `1fa7410`, `d6cfb02` e `26045a6`, entre 13/09/2025 e 15/09/2025.

- Criacao de arquivos iniciais de rotas e modelos para pacientes.
- Inclusao de templates HTML para base, listagem, cadastro e edicao.
- Adicao de CSS inicial.
- Ajustes iniciais em formularios, listagem e estilo.
- Correcoes relacionadas a estilo e configuracao/banco da epoca.

### Setembro de 2025 - Servicos e historico do paciente

Evidencia Git: commit `33c1bc0`, em 22/09/2025.

- Adicao de estrutura inicial para servicos.
- Preparacao de rotas e modelo para historico de servicos vinculados a pacientes.
- Comentarios tecnicos adicionados ao backend da epoca.

### Outubro de 2025 - Oracle ORDS e reorganizacao da aplicacao

Evidencias Git: commits `ffb6407`, `9e5f053`, `cac4a9a` e `c339a3c`, entre 23/10/2025 e 27/10/2025.

- Migracao do backend para consumo de Oracle ORDS/API REST usando `requests`.
- Ajustes em `config.py` e `requirements.txt`.
- Reorganizacao da aplicacao para a estrutura atual com `app/__init__.py`, `app/routes/`, `app/models/`, `templates/`, `static/` e `run.py`.
- Consolidacao de rotas atuais de pacientes e servicos.
- Inclusao de tela de detalhes do paciente e formulario de novo servico na estrutura atual.
- Correcoes pontuais apos a reorganizacao.

### Abril de 2026 - Interface, autenticacao e cesta basica

Evidencias Git: commits `2f60ab7`, `a0f4d06`, `4b4b574` e `4371ccf`, entre 19/04/2026 e 26/04/2026.

- Reformulacao visual de paginas principais e CSS.
- Criacao de tela de login.
- Criacao de Blueprint de autenticacao.
- Implementacao inicial de sessao, logout, hash de senha e usuario mockado.
- Inclusao de `login_required` em parte das rotas internas.
- Criacao de dados mockados para teste do controle de cesta basica.
- Calculo de atraso com base na data da ultima cesta e frequencia.
- Exibicao de pacientes com cesta atrasada.
- Criacao de botao/rota visual temporaria para marcar entrega em modo teste.

Observacao: a autenticacao ainda nao e definitiva, pois usa usuario mockado e protecao parcial de rotas. O controle de cesta basica tambem ainda nao possui persistencia definitiva das entregas via Oracle ORDS/API REST.

### Maio de 2026 - Retomada e organizacao do projeto

Evidencias Git: commits `ec4f094`, `28895c3`, `64a7519`, `984ea4a`, `d3a48ef`, `ccdbc06`, `26bb2a8`, `f96a9f0`, `4eb43df`, `0ced885`, `2b15394` e merges relacionados, entre 04/05/2026 e 29/05/2026.

- Criacao da estrutura de documentacao da avaliacao do primeiro bimestre.
- Atualizacao da visao inicial do projeto.
- Criacao de backlog e roadmap iniciais.
- Documentacao de separacao entre desenvolvimento e producao.
- Documentacao de organizacao da equipe e artefatos de acompanhamento.
- Organizacao de evidencias de versionamento.
- Inclusao de workflow, ambiente de desenvolvimento, POPs e referencias.
- Registro formal da Sprint 01 de 2026.
- Renomeacao dos arquivos de Sprint para `sprint-template.md` e `sprint-01.md`.

### Agosto de 2026 - Organizacao documental

Evidencia: alteracoes realizadas no working tree em 13/08/2026.

- Reconstrucao retrospectiva das seis Sprints historicas em `docs/sprints/historico/`.
- Criacao do indice de Sprints em `docs/sprints/README.md`.
- Correcao de links no README para os caminhos reais de Sprint.
- Correcao das referencias de evidencias fisicas de `.jpg` para `.jpeg`.
- Reorganizacao do backlog para representar possibilidades amplas de evolucao do produto.
- Reorganizacao do roadmap para conter apenas itens comprometidos ate a versao 1.0.
- Criacao deste CHANGELOG.
