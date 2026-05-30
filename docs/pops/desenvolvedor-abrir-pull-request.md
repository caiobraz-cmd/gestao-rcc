# POP — Abrir Pull Request

## Título

Procedimento Operacional Padrão para abertura de Pull Request.

## Objetivo

Padronizar a abertura de Pull Requests no projeto Gestão RCC, garantindo revisão antes da integração das alterações à branch principal.

## Responsável

Desenvolvedor / responsável técnico.

No projeto Gestão RCC, essa função é exercida por Caio Braz.

## Quando usar

Este POP deve ser utilizado quando uma branch possui alterações prontas para revisão.

Exemplos:

- documentação preenchida;
- correção concluída;
- funcionalidade implementada;
- evidências organizadas;
- ajuste técnico realizado.

## Pré-requisitos

Antes de abrir o Pull Request, o responsável deve garantir que:

- existe uma issue relacionada;
- a branch foi criada corretamente;
- os arquivos foram alterados;
- os commits foram realizados;
- o push foi feito para o GitHub;
- não há arquivos sensíveis no commit.

## Passo a passo

### 1. Verificar status local

```bash
git status
```

O ideal é que não existam alterações pendentes.

### 2. Enviar branch para o GitHub

```bash
git push -u origin nome-da-branch
```

### 3. Acessar o repositório

```txt
https://github.com/caiobraz-cmd/gestao-rcc
```

### 4. Criar Pull Request

Clicar em:

```txt
Compare & pull request
```

Ou acessar:

```txt
Pull requests → New pull request
```

Selecionar:

```txt
base: main
compare: nome-da-branch
```

### 5. Preencher título

Exemplo:

```txt
docs: completa documentacao tecnica da sprint 1
```

### 6. Preencher descrição

Modelo:

```md
## Resumo

Este PR completa a documentação técnica da Sprint 1.

## Arquivos alterados

- README.md
- docs/workflow.md
- docs/development-environment.md
- docs/pops/desenvolvedor-criar-branch.md
- docs/pops/desenvolvedor-abrir-pull-request.md

## Issues relacionadas

Refs #1
Refs #3
Closes #4

## Evidências

- Workflow documentado
- Ambiente de desenvolvimento documentado
- POPs da função Desenvolvedor preenchidos
- README atualizado
```

### 7. Solicitar revisão

O outro integrante deve revisar o Pull Request antes do merge.

No projeto:

```txt
Caio revisa PRs do Osvaldo.
Osvaldo revisa PRs do Caio.
```

### 8. Corrigir, se necessário

Se o revisor solicitar ajustes:

```bash
git add .
git commit -m "fix: ajusta documentacao conforme revisao"
git push
```

### 9. Fazer merge

Após revisão, o Pull Request pode ser integrado à `main`.

### 10. Registrar evidências

Salvar prints ou links em:

```txt
docs/evidences/sprint-01/
```

## Evidências esperadas

- print do PR aberto;
- print da descrição do PR;
- print dos arquivos alterados;
- print da revisão;
- print do merge;
- link do Pull Request;
- link das issues relacionadas.

## Critérios de sucesso

O procedimento é concluído com sucesso quando:

- o PR foi aberto para a `main`;
- a descrição está clara;
- as issues corretas foram relacionadas;
- outro integrante revisou;
- o PR foi aprovado ou comentado;
- o merge foi realizado;
- as evidências foram registradas.

## Referências utilizadas

- GitHub Docs — Pull Requests.
- GitHub Docs — Reviewing proposed changes.
- Documentação interna do projeto Gestão RCC.