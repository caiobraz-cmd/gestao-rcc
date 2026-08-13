# Sprint Historica 03 - Servicos e Historico do Paciente

**Nota de rastreabilidade:** Este registro foi reconstruido retrospectivamente em 2026 a partir do historico Git, codigo-fonte e documentacao disponivel. A Sprint foi efetivamente representada pelo trabalho realizado no periodo, mas nao possuia documentacao formal de Sprint na epoca.

## 1. Alinhamento e Planejamento

* **Nome da Sprint**: Sprint Historica 03 - Servicos e historico do paciente
* **Periodo**: Evidencia Git em 22/09/2025. Nao ha registro formal de inicio e fim da Sprint.
* **Objetivo da Sprint**: Adicionar a estrutura inicial para registrar servicos vinculados a pacientes e consultar historico associado.

## 2. Backlog da Sprint

| Item | Tarefa | Responsavel provavel/documentado | Resultado |
| --- | --- | --- | --- |
| 1 | Criar estrutura inicial de servico | Caio Braz, conforme autoria Git do commit `33c1bc0` | Modelo inicial de servico adicionado na estrutura da epoca |
| 2 | Incluir rotas para detalhes do paciente e servicos associados | Caio Braz, conforme autoria Git do commit `33c1bc0` | Rotas de detalhes e novo servico aparecem no historico |
| 3 | Preparar exibicao de historico relacionado ao paciente | Caio Braz, conforme autoria Git do commit `33c1bc0` | Base para historico de servicos vinculados ao paciente |

## 3. Governanca e criterios

* **Criterio de pronto**: Paciente com pagina de detalhes e possibilidade inicial de associar servicos.
* **Riscos**: Nao ha registro historico formal de riscos. A implementacao ainda dependia da forma de persistencia vigente na epoca e foi adaptada posteriormente.
* **Impedimentos conhecidos**: Nao determinados pelo historico disponivel.
* **Artefatos produzidos**: Modelo/estrutura de servico, alteracoes em rotas de paciente e preparacao de historico.

## 4. Fechamento

### Sprint Review

O incremento disponivel foi a ampliacao do cadastro de pacientes para incluir detalhes e historico de servicos, aproximando o sistema do acompanhamento de atendimentos prestados pela Rede de Combate ao Cancer.

### Observacoes retrospectivas

O codigo atual mantem a funcionalidade de servicos via API REST, mas a evidencia historica mostra que a primeira estrutura foi criada antes da migracao para Oracle ORDS.
