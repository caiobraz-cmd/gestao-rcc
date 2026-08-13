# Sprint Historica 06 - Controle Inicial de Cesta Basica

**Nota de rastreabilidade:** Este registro foi reconstruido retrospectivamente em 2026 a partir do historico Git, codigo-fonte e documentacao disponivel. A Sprint foi efetivamente representada pelo trabalho realizado no periodo, mas nao possuia documentacao formal de Sprint na epoca.

## 1. Alinhamento e Planejamento

* **Nome da Sprint**: Sprint Historica 06 - Controle inicial de cesta basica
* **Periodo**: Evidencia Git em 26/04/2026. Nao ha registro formal de inicio e fim da Sprint.
* **Objetivo da Sprint**: Criar um algoritmo inicial, em modo mock, para identificar pacientes com cesta basica atrasada e validar visualmente o fluxo de registro de entrega.

## 2. Backlog da Sprint

| Item | Tarefa | Responsavel provavel/documentado | Resultado |
| --- | --- | --- | --- |
| 1 | Criar dados mockados para testar controle de cesta basica | Nesto310, conforme autoria Git do commit `4371ccf` | Lista local de pacientes ficticios adicionada |
| 2 | Calcular atraso com base em ultima cesta e frequencia | Nesto310, conforme autoria Git do commit `4371ccf` | Pacientes atrasados identificados na listagem |
| 3 | Exibir alerta visual de cestas atrasadas | Nesto310, conforme autoria Git do commit `4371ccf` | Caixa de atrasos adicionada em `templates/listar.html` |
| 4 | Criar rota temporaria para registrar visualmente entrega | Nesto310, conforme autoria Git do commit `4371ccf` | Botao/rota `renovar_cesta` em modo teste |

## 3. Governanca e criterios

* **Criterio de pronto**: Fluxo de teste capaz de listar atrasos e simular visualmente uma entrega sem persistencia real.
* **Riscos**: Nao ha registro historico formal de riscos. Tecnicamente, o recurso usa dados mockados e nao grava entrega real via Oracle ORDS.
* **Impedimentos conhecidos**: Persistencia real da entrega nao implementada no codigo atual.
* **Artefatos produzidos**: Dados mockados em `pessoa_routes.py`, calculo de atraso, secao visual em `listar.html` e rota temporaria `renovar_cesta`.

## 4. Fechamento

### Sprint Review

O incremento disponivel foi o controle inicial de cesta basica em modo de teste, permitindo visualizar pacientes atrasados e acionar uma entrega simulada.

### Observacoes retrospectivas

Este registro nao trata o controle de cesta como definitivo. A integracao real com Oracle ORDS, a persistencia da entrega e a atualizacao automatica da proxima previsao continuam como pendencias para evolucao da versao 1.0.
