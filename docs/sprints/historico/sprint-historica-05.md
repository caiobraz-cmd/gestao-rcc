# Sprint Historica 05 - Interface e Autenticacao Inicial

**Nota de rastreabilidade:** Este registro foi reconstruido retrospectivamente em 2026 a partir do historico Git, codigo-fonte e documentacao disponivel. A Sprint foi efetivamente representada pelo trabalho realizado no periodo, mas nao possuia documentacao formal de Sprint na epoca.

## 1. Alinhamento e Planejamento

* **Nome da Sprint**: Sprint Historica 05 - Interface e autenticacao inicial
* **Periodo**: Evidencias Git entre 19/04/2026 e 21/04/2026. Nao ha registro formal de inicio e fim da Sprint.
* **Objetivo da Sprint**: Melhorar a interface do sistema e implementar autenticacao inicial em modo de desenvolvimento, com login, sessao, logout e protecao parcial de rotas.

## 2. Backlog da Sprint

| Item | Tarefa | Responsavel provavel/documentado | Resultado |
| --- | --- | --- | --- |
| 1 | Atualizar visual das telas principais | Nesto310, conforme autoria Git do commit `2f60ab7` | CSS e templates principais reformulados |
| 2 | Criar tela de login e Blueprint de autenticacao | Nesto310, conforme autoria Git do commit `a0f4d06` | `auth_routes.py` e `login.html` adicionados |
| 3 | Implementar sessao, logout, hash de senha e usuario mockado | Nesto310, conforme autoria Git dos commits `a0f4d06` e `4b4b574` | Autenticacao inicial disponivel para desenvolvimento |
| 4 | Aplicar `login_required` em parte das rotas | Nesto310, conforme autoria Git do commit `a0f4d06` | Protecao parcial implementada |

## 3. Governanca e criterios

* **Criterio de pronto**: Existencia de tela de login, controle de sessao e protecao inicial para acesso a partes internas do sistema.
* **Riscos**: Nao ha registro historico formal de riscos. Tecnicamente, o usuario mockado e a protecao parcial nao representam autenticacao definitiva para producao.
* **Impedimentos conhecidos**: Nao determinados pelo historico disponivel.
* **Artefatos produzidos**: `app/routes/auth_routes.py`, `templates/login.html`, ajustes em `app/__init__.py`, `templates/base.html` e `static/style.css`.

## 4. Fechamento

### Sprint Review

O incremento disponivel foi uma interface mais organizada e uma autenticacao inicial com login, sessao, logout, hash de senha e usuario mockado para desenvolvimento.

### Observacoes retrospectivas

O codigo atual confirma que a protecao de rotas ainda nao e completa. Portanto, este registro trata a autenticacao como etapa inicial, nao como solucao final de seguranca da versao 1.0.
