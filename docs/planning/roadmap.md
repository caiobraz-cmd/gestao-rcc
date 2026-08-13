# Roadmap do Projeto

## Objetivo do roadmap

Este roadmap registra somente os itens que a equipe decidiu executar ate o final do terceiro bimestre para preparar a versao `1.0` funcional, organizada, testada e documentada do Sistema de Gestao RCC.

O roadmap e um subconjunto do backlog. Ideias futuras, possibilidades de longo prazo e itens sem compromisso atual permanecem apenas em `docs/planning/backlog.md`.

## Contexto de rastreabilidade

O desenvolvimento anterior foi reconstruido retrospectivamente em `docs/sprints/historico/`, a partir do codigo-fonte, documentacao disponivel e historico Git. Esses registros historicos explicam o estado herdado do sistema, mas nao substituem evidencias formais de Issues, Pull Requests ou reunioes.

---

# Estado herdado antes da execucao atual

O sistema ja possui uma base inicial com:

- aplicacao Flask organizada com Application Factory e Blueprints;
- templates Jinja2 e arquivos estaticos;
- CRUD de pacientes via Oracle ORDS/API REST;
- cadastro e consulta basica de servicos vinculados a pacientes;
- tela de detalhes do paciente com historico de servicos;
- autenticacao inicial em modo mock, com sessao e protecao parcial de rotas;
- controle inicial de cesta basica em modo mock, sem persistencia real da entrega;
- documentacao inicial de planejamento, workflow, POPs, Sprints e evidencias.

---

# Execucao comprometida ate a versao 1.0

## 1. Autenticacao e seguranca

- [ ] Substituir autenticacao mockada por solucao definitiva.
- [ ] Integrar usuario com base/API, conforme arquitetura adotada.
- [ ] Proteger todas as rotas internas.
- [ ] Revisar sessao.
- [ ] Revisar tratamento de dados sensiveis.
- [ ] Criar `.env.example` seguro, sem credenciais reais.

## 2. Gestao de pacientes

- [ ] Revisar CRUD de pacientes.
- [ ] Melhorar validacao dos formularios.
- [ ] Adicionar busca por nome ou CPF.
- [ ] Revisar fluxo de exclusao.
- [ ] Padronizar mensagens de erro e sucesso.

## 3. Servicos

- [ ] Revisar cadastro de servicos.
- [ ] Melhorar historico exibido no paciente.
- [ ] Validar vinculo paciente-servico.

## 4. Cesta basica

- [ ] Substituir comportamento exclusivamente mock por integracao real.
- [ ] Persistir entrega da cesta.
- [ ] Registrar ultima entrega.
- [ ] Registrar frequencia.
- [ ] Calcular proxima entrega.
- [ ] Identificar atrasos utilizando dados reais.

## 5. Interface e usabilidade

- [ ] Padronizar telas.
- [ ] Melhorar navegacao.
- [ ] Melhorar responsividade.
- [ ] Revisar UX das principais operacoes.

## 6. Qualidade

- [ ] Executar testes manuais dos principais fluxos.
- [ ] Registrar problemas encontrados.
- [ ] Corrigir falhas criticas.
- [ ] Preparar versao estavel.

## 7. Documentacao

- [ ] Manter backlog atualizado.
- [ ] Manter roadmap atualizado.
- [ ] Manter CHANGELOG atualizado.
- [ ] Registrar Sprints.
- [ ] Atualizar README.
- [ ] Registrar evidencias necessarias.

---

# Criterios para considerar a versao 1.0 pronta

- O sistema executa localmente sem erros criticos.
- As rotas internas estao protegidas conforme o fluxo de autenticacao definido.
- O fluxo de pacientes funciona para cadastro, listagem, edicao, detalhes e exclusao revisada.
- O fluxo de servicos funciona de forma basica e vinculada ao paciente correto.
- O controle de cesta basica usa dados reais para entrega, frequencia, proxima previsao e atraso.
- As mensagens de sucesso e erro estao padronizadas nos principais fluxos.
- As principais telas estao organizadas e utilizaveis.
- A documentacao essencial esta atualizada.
- O README orienta a execucao local e aponta para backlog, roadmap, changelog e Sprints.

---

# Itens deliberadamente fora deste roadmap

Os itens abaixo permanecem no backlog, mas nao fazem parte do compromisso atual ate a versao 1.0:

- aplicativo mobile;
- integracao com WhatsApp;
- modulo financeiro;
- gestao de voluntarios;
- dashboard avancado;
- relatorios complexos;
- automacoes externas;
- estoque completo;
- notificacoes avancadas.

---

# Fluxo documental adotado

```text
IDEIA
|
v
BACKLOG
|
v
DECISAO DE IMPLEMENTAR
|
v
ROADMAP / SPRINT
|
v
DESENVOLVIMENTO
|
v
CONCLUIDO
|
v
CHANGELOG
```
