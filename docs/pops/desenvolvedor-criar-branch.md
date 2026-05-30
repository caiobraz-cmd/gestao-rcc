# POP — Criar Branch de Trabalho

## Título

Procedimento Operacional Padrão para criação de branch de trabalho.

## Objetivo

Padronizar a criação de branches no projeto Gestão RCC, garantindo que cada tarefa seja desenvolvida de forma isolada e relacionada a uma issue.

## Responsável

Desenvolvedor / responsável técnico.

No projeto Gestão RCC, essa função é exercida por Caio Braz.

## Quando usar

Este POP deve ser utilizado sempre que uma nova tarefa for iniciada, incluindo:

- documentação;
- correção;
- funcionalidade;
- organização de evidências;
- melhoria técnica.

## Pré-requisitos

Antes de criar a branch, o desenvolvedor deve garantir que:

- o Git está instalado;
- o repositório está clonado;
- existe uma issue relacionada;
- a branch `main` está atualizada;
- o escopo da tarefa está definido.

## Padrão de nomes

```txt
sprint-XX/nome-da-tarefa
fix/nome-da-correcao
docs/nome-da-documentacao
feature/nome-da-funcionalidade
```

Exemplos:

```txt
sprint-01/workflow-ambiente
sprint-01/sprint-pops-evidencias
fix/sprint-01-documentacao-caio
```

## Passo a passo

### 1. Acessar a pasta do projeto

```bash
cd gestao-rcc
```

### 2. Ir para a branch principal

```bash
git switch main
```

Ou:

```bash
git checkout main
```

### 3. Atualizar a branch principal

```bash
git pull origin main
```

### 4. Criar a branch da tarefa

```bash
git checkout -b nome-da-branch
```

Exemplo:

```bash
git checkout -b fix/sprint-01-documentacao-caio
```

### 5. Confirmar a branch atual

```bash
git branch
```

### 6. Fazer as alterações da tarefa

Editar ou criar os arquivos necessários.

### 7. Verificar alterações

```bash
git status
```

### 8. Adicionar arquivos

```bash
git add .
```

### 9. Criar commit

```bash
git commit -m "docs: descreve alteracao realizada"
```

### 10. Enviar branch para o GitHub

```bash
git push -u origin nome-da-branch
```

## Evidências esperadas

- print da issue;
- print da branch criada;
- print do `git status`;
- print do commit;
- print do push;
- link da branch;
- link do Pull Request.

As evidências devem ser salvas em:

```txt
docs/evidences/sprint-01/
```

## Critérios de sucesso

O procedimento é concluído com sucesso quando:

- a branch foi criada a partir da `main`;
- o nome segue o padrão da equipe;
- a alteração está relacionada a uma issue;
- o commit foi realizado;
- a branch foi enviada ao GitHub;
- a branch está pronta para Pull Request.

## Referências utilizadas

- GitHub Docs — GitHub Flow.
- GitHub Docs — Branches.
- Documentação interna do projeto Gestão RCC.