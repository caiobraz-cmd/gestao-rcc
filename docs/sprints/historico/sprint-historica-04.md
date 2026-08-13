# Sprint Historica 04 - Migracao para Oracle ORDS e Reorganizacao da Aplicacao

**Nota de rastreabilidade:** Este registro foi reconstruido retrospectivamente em 2026 a partir do historico Git, codigo-fonte e documentacao disponivel. A Sprint foi efetivamente representada pelo trabalho realizado no periodo, mas nao possuia documentacao formal de Sprint na epoca.

## 1. Alinhamento e Planejamento

* **Nome da Sprint**: Sprint Historica 04 - Migracao para Oracle ORDS e reorganizacao da aplicacao
* **Periodo**: Evidencias Git entre 23/10/2025 e 27/10/2025. Nao ha registro formal de inicio e fim da Sprint.
* **Objetivo da Sprint**: Migrar o backend para consumo de API Oracle ORDS via REST e reorganizar a aplicacao para a estrutura atual baseada em `app/`, Blueprints, templates e arquivos estaticos fora de `instance/`.

## 2. Backlog da Sprint

| Item | Tarefa | Responsavel provavel/documentado | Resultado |
| --- | --- | --- | --- |
| 1 | Migrar configuracao e dependencias para consumo de Oracle ORDS/API REST | Caio Braz, conforme autoria Git do commit `ffb6407` | Backend ajustado para uso de `requests` e `API_BASE_URL` |
| 2 | Reorganizar a aplicacao para Application Factory e estrutura atual | Nesto310, conforme autoria Git do commit `9e5f053` | `app/__init__.py`, `run.py`, Blueprints, templates e static consolidados |
| 3 | Recriar rotas de pacientes e servicos no padrao da aplicacao reorganizada | Nesto310, conforme autoria Git do commit `9e5f053` | CRUD de pacientes e servicos passaram a existir na estrutura atual |
| 4 | Realizar ajustes posteriores de configuracao e rotas | Nesto310, conforme autoria Git dos commits `cac4a9a` e `c339a3c` | Correcoes pontuais apos reorganizacao |

## 3. Governanca e criterios

* **Criterio de pronto**: Aplicacao executavel pela estrutura atual, com rotas registradas por Blueprint e comunicacao preparada com Oracle ORDS.
* **Riscos**: Nao ha registro historico formal de riscos. Tecnicamente, a migracao poderia gerar divergencias entre caminhos antigos e novos, alem de dependencia de configuracao via variaveis de ambiente.
* **Impedimentos conhecidos**: Nao determinados pelo historico disponivel.
* **Artefatos produzidos**: `app/__init__.py`, `app/routes/pessoa_routes.py`, `app/models/pessoa.py`, `run.py`, templates atuais, CSS e ajustes em `config.py`.

## 4. Fechamento

### Sprint Review

O incremento disponivel foi uma aplicacao reorganizada, com estrutura Flask mais modular e backend preparado para consultar e alterar dados por Oracle ORDS/API REST.

### Observacoes retrospectivas

Esta etapa parece ser a principal ponte entre a versao inicial com persistencia local/ORM e a arquitetura atual orientada a API REST. O registro nao afirma decisao formal de arquitetura, apenas documenta a evolucao observavel nos commits.
