# Backlog do Projeto

## Objetivo do backlog

Este backlog reune as funcionalidades, melhorias, ideias e possibilidades de evolucao do Sistema de Gestao RCC.

Estar no backlog nao significa compromisso de implementacao. O backlog representa tudo que pode fazer sentido para o produto em algum momento. Os itens escolhidos para execucao ate o final do bimestre sao registrados separadamente no `roadmap.md`.

## Leitura dos status

- **Implementado**: ja existe no codigo, documentacao ou estrutura atual.
- **Em evolucao**: existe parcialmente, mas ainda precisa de revisao ou finalizacao.
- **Planejado**: item que faz sentido para o produto e pode ser priorizado.
- **Ideias futuras**: possibilidades sem compromisso atual.
- **Fora do escopo atual**: ideias de longo prazo, fora da entrega principal da versao 1.0.

---

# 1. Gestao de pacientes

## Implementado

- [x] Estrutura inicial do projeto Flask.
- [x] Rota de listagem de pacientes.
- [x] Tela de cadastro de paciente.
- [x] Tela de edicao de paciente.
- [x] Tela de detalhes do paciente.
- [x] Exclusao de paciente via rota POST.
- [x] Integracao inicial com Oracle ORDS/API REST.
- [x] Tratamento basico de erros e timeout nas chamadas para a API.

## Em evolucao

- [ ] Revisar CRUD de pacientes.
- [ ] Revisar campos obrigatorios do cadastro.
- [ ] Melhorar validacao dos formularios.
- [ ] Padronizar mensagens de sucesso e erro.
- [ ] Revisar fluxo de exclusao de paciente.
- [ ] Melhorar organizacao visual da listagem.

## Planejado

- [ ] Busca por nome.
- [ ] Busca por CPF.
- [ ] Prevencao de cadastros duplicados.
- [ ] Identificacao de pacientes ativos e inativos.

## Ideias futuras

- [ ] Filtros avancados.
- [ ] Historico de alteracoes do paciente.
- [ ] Auditoria de alteracoes.
- [ ] Exportacao de pacientes.
- [ ] Campos configuraveis.

---

# 2. Servicos prestados

## Implementado

- [x] Estrutura inicial para cadastro de servicos.
- [x] Vinculo entre servico e paciente.
- [x] Exibicao de servicos na tela de detalhes do paciente.
- [x] Cadastro basico de servico via Oracle ORDS/API REST.

## Em evolucao

- [ ] Revisar cadastro de servicos.
- [ ] Melhorar formulario de cadastro de servico.
- [ ] Melhorar historico exibido no paciente.
- [ ] Validar vinculo paciente-servico.

## Planejado

- [ ] Edicao de servicos.
- [ ] Exclusao controlada de servicos.
- [ ] Categorias de atendimento.
- [ ] Filtros de servicos por periodo.
- [ ] Quantidade de atendimentos por paciente.

## Ideias futuras

- [ ] Historico avancado de servicos.
- [ ] Relatorios de servicos.
- [ ] Indicadores de atendimento por periodo.

---

# 3. Beneficios e cesta basica

## Implementado

- [x] Logica inicial de teste com dados mockados.
- [x] Data da ultima cesta em dados mockados.
- [x] Frequencia de entrega em dados mockados.
- [x] Identificacao de pacientes com entrega atrasada no modo de teste.
- [x] Calculo de dias de atraso.
- [x] Botao e rota visual temporaria para marcar entrega em modo mock.

## Em evolucao

- [ ] Integrar o controle de cesta basica aos dados reais via Oracle ORDS/API REST.
- [ ] Persistir entrega real da cesta via Oracle ORDS/API REST.
- [ ] Registrar ultima entrega com dados reais.
- [ ] Registrar frequencia de entrega com dados reais.
- [ ] Calcular proxima entrega com dados reais.
- [ ] Identificar atrasos utilizando dados reais.

## Planejado

- [ ] Historico completo de cestas.
- [ ] Proxima entrega automatica.
- [ ] Alertas de atraso.
- [ ] Pacientes prioritarios.
- [ ] Relatorios de cestas.

## Ideias futuras

- [ ] Outros tipos de beneficios.
- [ ] Controle de medicamentos.
- [ ] Controle de auxilios.
- [ ] Controle de estoque de itens assistenciais.

---

# 4. Usuarios e seguranca

## Implementado

- [x] Tela inicial de login.
- [x] Sessao em modo mock.
- [x] Logout.
- [x] Hash de senha com Werkzeug.
- [x] Usuario mockado para teste.
- [x] Decorador `login_required`.
- [x] Protecao parcial de rotas internas.

## Em evolucao

- [ ] Substituir autenticacao mockada por solucao definitiva.
- [ ] Integrar usuario com base de dados ou API, conforme arquitetura adotada.
- [ ] Revisar e fortalecer controle de sessao.
- [ ] Proteger todas as rotas internas com `login_required`.
- [ ] Revisar tratamento de dados sensiveis.
- [ ] Criar `.env.example` seguro, sem credenciais reais.
- [ ] Garantir que `.env` nao seja enviado ao GitHub.

## Planejado

- [ ] Usuarios reais.
- [ ] Niveis de acesso.
- [ ] Perfil administrador.
- [ ] Perfil funcionario.
- [ ] Perfil voluntario.
- [ ] Expiracao de sessao.
- [ ] Registro de acoes realizadas por usuario.
- [ ] Permissoes por funcao.

## Ideias futuras

- [ ] Recuperacao de senha.
- [ ] Auditoria de login.
- [ ] Cadastro de usuarios administradores.
- [ ] Controle avancado de usuarios.

---

# 5. Dashboard e indicadores

## Implementado

Nao ha dashboard consolidado implementado no estado atual.

## Planejado

- [ ] Dashboard inicial simples.
- [ ] Total de pacientes.
- [ ] Pacientes ativos.
- [ ] Atendimentos realizados.
- [ ] Pacientes com cesta atrasada.
- [ ] Cestas entregues.

## Ideias futuras

- [ ] Servicos por periodo.
- [ ] Indicadores gerenciais.
- [ ] Graficos.
- [ ] Dashboard avancado.

---

# 6. Relatorios

## Planejado

- [ ] Relatorio de pacientes.
- [ ] Relatorio de servicos.
- [ ] Relatorio de beneficios.
- [ ] Relatorios por periodo.

## Ideias futuras

- [ ] Exportacao para PDF.
- [ ] Exportacao para Excel.
- [ ] Relatorios complexos.

---

# 7. Interface, usabilidade e acessibilidade

## Implementado

- [x] Templates HTML/Jinja2 iniciais.
- [x] CSS inicial.
- [x] Navegacao basica entre telas.
- [x] Formularios principais.
- [x] Listagem e telas de detalhes.
- [x] Melhorias visuais registradas no historico Git.

## Em evolucao

- [ ] Padronizar telas.
- [ ] Melhorar navegacao.
- [ ] Melhorar responsividade.
- [ ] Revisar UX das principais operacoes.
- [ ] Melhorar organizacao das informacoes dos pacientes.

## Planejado

- [ ] Interface mais simples para usuarios com pouca familiaridade tecnologica.
- [ ] Melhorias de contraste.
- [ ] Navegacao por teclado.

## Ideias futuras

- [ ] Acessibilidade visual avancada.
- [ ] Redesign completo da experiencia.

---

# 8. Qualidade tecnica

## Implementado

- [x] Execucao local documentada no README.
- [x] Rota `/ping` para teste basico do servidor.

## Em evolucao

- [ ] Executar testes manuais dos principais fluxos.
- [ ] Registrar problemas encontrados.
- [ ] Corrigir falhas criticas.
- [ ] Preparar versao estavel.
- [ ] Tratamento centralizado de erros.
- [ ] Validacao de formularios.

## Planejado

- [ ] PyTest.
- [ ] Testes unitarios.
- [ ] Testes de integracao.
- [ ] Logging estruturado.
- [ ] Documentacao de API.

## Ideias futuras

- [ ] GitHub Actions.
- [ ] CI.
- [ ] Cobertura de testes.
- [ ] Monitoramento de erros.

---

# 9. Documentacao e organizacao do projeto

## Implementado

- [x] Estrutura de documentacao em `docs/`.
- [x] README organizado.
- [x] Visao do projeto.
- [x] Backlog.
- [x] Roadmap.
- [x] Workflow.
- [x] Documentacao de ambiente de desenvolvimento.
- [x] Documentacao de separacao entre desenvolvimento e producao.
- [x] Documentacao de organizacao da equipe.
- [x] POPs do Desenvolvedor.
- [x] POPs do Documentador.
- [x] Kanban.
- [x] Gantt.
- [x] Evidencias de Git/GitHub.
- [x] Kanban fisico fotografado.
- [x] Gantt fisico fotografado.
- [x] Registro formal da Sprint 01 de 2026.
- [x] Reconstrucao retrospectiva das Sprints historicas.
- [x] Indice de Sprints.
- [x] CHANGELOG.

## Em evolucao

- [ ] Manter backlog atualizado.
- [ ] Manter roadmap atualizado.
- [ ] Manter CHANGELOG atualizado.
- [ ] Registrar Sprints.
- [ ] Atualizar README conforme a evolucao.
- [ ] Registrar evidencias necessarias.

## Planejado

- [ ] Documentar versao 1.0.
- [ ] Registrar decisoes tecnicas importantes.
- [ ] Revisar instrucoes de execucao local apos ajustes finais.

---

# 10. Fora do escopo atual e longo prazo

Os itens abaixo podem ser estudados futuramente, mas nao fazem parte do compromisso atual da versao 1.0.

- [ ] Aplicativo mobile.
- [ ] Integracao com WhatsApp.
- [ ] Notificacoes.
- [ ] Lembretes automaticos.
- [ ] Integracao com outros sistemas.
- [ ] Modulo de doacoes.
- [ ] Modulo financeiro.
- [ ] Controle de estoque completo.
- [ ] Gestao de voluntarios.
- [ ] Automacoes externas complexas.
