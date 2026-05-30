# Workflow Funcional da Equipe

## Objetivo

Este documento descreve o fluxo de trabalho utilizado pela equipe do projeto Gestão RCC durante a Sprint 1.

O objetivo é comprovar um processo real de desenvolvimento, integrando gestão de tarefas, versionamento, Pull Requests, revisão, merge, documentação e registro de evidências.

## Modelo adotado

A equipe adotou uma adaptação simples do GitHub Flow.

Esse modelo foi escolhido porque o projeto possui uma equipe pequena e precisa de um fluxo direto, rastreável e fácil de aplicar dentro dos prazos semanais da disciplina.

## Fluxo utilizado

```txt
Issue → Branch → Commit → Push → Pull Request → Revisão → Merge → Evidência → Documentação
```

## Etapas do processo

### 1. Criação da issue

Toda tarefa da sprint deve começar com uma issue no GitHub.

A issue deve conter:

- título claro;
- descrição da tarefa;
- responsável;
- labels;
- relação com a sprint;
- entregas esperadas.

Na Sprint 1, foram criadas issues para workflow, ambiente, POPs, sprint e evidências.

### 2. Criação da branch

Cada tarefa deve ser feita em uma branch separada a partir da `main`.

Padrão utilizado:

```txt
sprint-XX/nome-da-tarefa
fix/nome-da-correcao
docs/nome-da-documentacao
```

Exemplos utilizados na Sprint 1:

```txt
sprint-01/workflow-ambiente
sprint-01/sprint-pops-evidencias
fix/sprint-01-documentacao-caio
```

### 3. Alteração dos arquivos

Cada integrante realiza suas alterações na própria branch.

As alterações devem estar relacionadas à issue correspondente.

### 4. Commit

Os commits devem ter mensagens claras.

Padrões utilizados:

```txt
docs: alteração de documentação
fix: correção
feat: nova funcionalidade
chore: organização ou manutenção
```

Exemplos:

```txt
docs: adiciona workflow e ambiente da sprint 1
docs: registra sprint 1 pops e evidencias
docs: completa documentacao tecnica da sprint 1
```

### 5. Push

Após o commit, a branch é enviada para o GitHub:

```bash
git push -u origin nome-da-branch
```

### 6. Pull Request

O responsável abre um Pull Request para integrar a branch à `main`.

O Pull Request deve conter:

- resumo do que foi feito;
- issues relacionadas;
- arquivos alterados;
- evidências, quando houver;
- solicitação de revisão para outro integrante.

### 7. Revisão

Outro integrante revisa o Pull Request antes do merge.

A revisão verifica:

- se os arquivos esperados foram criados;
- se a documentação está clara;
- se o PR está relacionado às issues corretas;
- se não há arquivos sensíveis;
- se a alteração pode ser integrada à `main`.

### 8. Merge

Após a revisão, o Pull Request é integrado à branch `main`.

A branch `main` representa o estado organizado e estável do projeto.

### 9. Registro de evidências

As evidências da sprint devem ser salvas em:

```txt
docs/evidences/sprint-01/
```

As evidências podem incluir:

- prints das issues;
- prints das branches;
- prints dos commits;
- prints dos Pull Requests;
- prints das revisões;
- prints dos merges;
- prints do ambiente executando;
- links para issues e PRs.

## Workflow aplicado na Sprint 1

Durante a Sprint 1, a equipe executou o seguinte fluxo:

1. Criação das issues da sprint.
2. Criação das branches de trabalho.
3. Criação dos arquivos de documentação.
4. Commits das alterações.
5. Abertura de Pull Requests.
6. Revisão cruzada entre Caio e Osvaldo.
7. Merge das alterações na `main`.
8. Organização das evidências.
9. Atualização da documentação do projeto.

## Rastreabilidade

| Item | Local de registro |
|---|---|
| Tarefa | GitHub Issues |
| Desenvolvimento | Branch |
| Alteração | Commit |
| Revisão | Pull Request |
| Aprovação | Review no GitHub |
| Entrega | Merge na main |
| Evidência | docs/evidences/sprint-01 |
| Processo | docs/workflow.md |

## Critérios de sucesso

O workflow é considerado aplicado corretamente quando:

- cada tarefa possui uma issue;
- cada alteração é feita em branch própria;
- os commits possuem mensagens compreensíveis;
- cada entrega passa por Pull Request;
- outro integrante revisa o PR;
- o merge é feito após revisão;
- as evidências são registradas;
- a documentação é atualizada.