# Backlog do Projeto

## Objetivo do backlog

Este backlog reúne as funcionalidades, melhorias e tarefas planejadas para a evolução do sistema Gestão RCC.

O projeto já possui uma base inicial desenvolvida anteriormente, mas será continuado nesta disciplina com foco em organização, melhoria técnica, documentação, versionamento e preparação da versão 1.0.

---

# Backlog geral do produto

## 1. Gestão de pacientes

### Já iniciado

- [x] Criar estrutura inicial do projeto Flask.
- [x] Criar rota de listagem de pacientes.
- [x] Criar tela de cadastro de paciente.
- [x] Criar tela de edição de paciente.
- [x] Criar tela de detalhes do paciente.
- [x] Criar integração inicial com API Oracle ORDS.

### Planejado para a versão 1.0

- [ ] Revisar os campos obrigatórios do cadastro.
- [ ] Melhorar validação dos formulários.
- [ ] Padronizar mensagens de sucesso e erro.
- [ ] Melhorar organização visual da listagem.
- [ ] Adicionar busca simples por nome ou CPF.
- [ ] Revisar fluxo de exclusão de paciente.

### Futuro

- [ ] Criar filtros avançados.
- [ ] Criar histórico de alterações do paciente.
- [ ] Criar exportação de dados.

---

## 2. Serviços prestados

### Já iniciado

- [x] Criar estrutura inicial para cadastro de serviços.
- [x] Criar vínculo entre serviço e paciente.
- [x] Exibir serviços na tela de detalhes do paciente.

### Planejado para a versão 1.0

- [ ] Melhorar o formulário de cadastro de serviço.
- [ ] Exibir histórico de serviços de forma mais organizada.
- [ ] Permitir edição de serviços registrados.
- [ ] Permitir exclusão controlada de serviços.

### Futuro

- [ ] Criar categorias de serviços.
- [ ] Criar relatórios de serviços prestados por período.

---

## 3. Controle de cesta básica

### Já iniciado

- [x] Criar lógica inicial de teste com dados mockados.
- [x] Identificar pacientes com entrega atrasada no modo de teste.

### Planejado para a versão 1.0

- [ ] Integrar o controle de cesta com os dados reais.
- [ ] Registrar data da última entrega.
- [ ] Registrar frequência de entrega.
- [ ] Exibir pacientes com cesta atrasada.
- [ ] Criar botão para marcar cesta como entregue.
- [ ] Atualizar automaticamente a próxima previsão de entrega.

### Futuro

- [ ] Criar histórico completo de entregas.
- [ ] Gerar relatório de cestas entregues.
- [ ] Criar alerta visual para pacientes prioritários.

---

## 4. Autenticação e segurança

### Já iniciado

- [x] Criar tela inicial de login.
- [x] Criar proteção básica de rotas.
- [x] Criar usuário mockado para teste.

### Planejado para a versão 1.0

- [ ] Remover usuário mockado.
- [ ] Integrar login com base de dados ou API.
- [ ] Criar controle básico de sessão.
- [ ] Proteger todas as rotas internas.
- [ ] Revisar arquivos sensíveis do repositório.
- [ ] Garantir que `.env` não seja enviado ao GitHub.

### Futuro

- [ ] Criar níveis de permissão.
- [ ] Criar cadastro de usuários administradores.
- [ ] Criar recuperação de senha.

---

## 5. Interface e experiência do usuário

### Já iniciado

- [x] Criar templates HTML iniciais.
- [x] Criar arquivo CSS inicial.
- [x] Criar navegação básica entre telas.

### Planejado para a versão 1.0

- [ ] Padronizar layout das páginas.
- [ ] Melhorar responsividade.
- [ ] Criar menu de navegação mais claro.
- [ ] Melhorar organização das informações dos pacientes.
- [ ] Criar tela inicial ou dashboard simples.

### Futuro

- [ ] Criar dashboard com indicadores.
- [ ] Criar gráficos de acompanhamento.
- [ ] Melhorar acessibilidade visual.

---

## 6. Documentação e organização do projeto

### Planejado para o primeiro bimestre

- [x] Criar estrutura de documentação.
- [x] Atualizar README.
- [x] Criar visão do projeto.
- [ ] Criar backlog.
- [ ] Criar roadmap.
- [ ] Criar documentação de separação entre desenvolvimento e produção.
- [ ] Criar documentação de organização da equipe.
- [ ] Criar Kanban.
- [ ] Criar Gantt.
- [ ] Registrar evidências de Git/GitHub.
- [ ] Fotografar Kanban físico.
- [ ] Fotografar Gantt físico.

### Planejado para os próximos bimestres

- [ ] Atualizar documentação conforme o projeto evoluir.
- [ ] Registrar decisões técnicas importantes.
- [ ] Documentar como executar o projeto localmente.
- [ ] Documentar versão 1.0.

---

# Priorização

## Alta prioridade

- Organização do repositório.
- Documentação obrigatória da avaliação.
- Evidências de Git/GitHub.
- Revisão da segurança do `.env`.
- Cadastro e listagem de pacientes.
- Controle básico de cesta básica.

## Média prioridade

- Melhorias na interface.
- Busca de pacientes.
- Histórico de serviços.
- Testes manuais.

## Baixa prioridade

- Dashboard completo.
- Relatórios avançados.
- Integrações externas.
- Aplicativo mobile.

---

# Escopo da versão 1.0

A versão 1.0 deverá conter:

- cadastro de pacientes;
- listagem de pacientes;
- edição de pacientes;
- tela de detalhes do paciente;
- registro de serviços;
- controle básico de cesta básica;
- login funcional;
- interface organizada;
- documentação atualizada;
- repositório limpo e versionado.

---

# Fora do escopo da avaliação final

Os itens abaixo poderão ser estudados futuramente, mas não fazem parte da avaliação final da disciplina:

- aplicativo mobile;
- integração com WhatsApp;
- sistema financeiro;
- dashboard avançado;
- relatórios complexos;
- automações externas.