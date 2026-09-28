# Contrato Oracle verificado em 26/09/2026

Inspeção autenticada e somente de leitura no workspace GESTAORCC, schema WKSP_GESTAORCC. Módulo `gestao_rcc`, prefixo `/rcc/`. Nenhuma senha ou identificador de sessão do painel é necessário para compreender este documento.

## Pacientes

Endpoints observados: `pessoas/` (GET e POST), `pessoas/:id` (GET, PUT e DELETE). O `:id` é substituído pelo identificador numérico, nunca enviado literalmente.

| Interface/código Flask | Nome no JSON Oracle | Limite da tabela observado |
|---|---|---|
| seq_id | id | NUMBER, obrigatório |
| ds_nome | nome | VARCHAR2(150), obrigatório |
| num_cpf | cpf | VARCHAR2(14) |
| dt_nascimento | data_nascimento | DATE; JSON YYYY-MM-DD |
| num_telefone | telefone | VARCHAR2(20) |
| char_endereco | endereco | VARCHAR2(255) |
| status | status | VARCHAR2(20) |

Há também `data_cadastro` TIMESTAMP na tabela. Os handlers examinados usam os nomes da coluna Oracle, não os nomes antigos da interface. `app/ords.py` faz a tradução nas duas direções. Campos não existentes não devem ser apresentados como gravados.

O GET da coleção retorna `items`; o GET individual é Collection Query Item. O POST observado retorna 201; o PUT retorna 200. O tratamento de exceções de gravação no banco retorna 400 genérico. O PUT examinado não verifica `SQL%ROWCOUNT`, portanto sucesso HTTP não basta para confirmar uma atualização: a aplicação deve consultar novamente.

## Atualização 0.5 — contrato instalado em 27/09/2026

O contrato acima descreve a API antiga `/rcc/`, mantida para compatibilidade. A instalação atual usa `/rcc-v2/`, protegida pelo papel `gestao_rcc_v2_operador`.

- GET/POST `pessoas/` e GET/PUT `pessoas/:id`: cadastro básico, cinco campos clínicos, `data_obito`, `num_frequencia_cesta` e `dt_ultima_cesta` calculada pelo histórico.
- PUT recebe `atualizar_clinico` e `atualizar_cestas` para atualizar explicitamente os grupos opcionais. A aplicação usa esses indicadores conforme as flags configuradas.
- GET `cestas/:id/`: histórico do paciente. POST no mesmo caminho registra a entrega de hoje; o banco valida situação e intervalo sob bloqueio da linha do paciente.
- A tabela ENTREGA_CESTA tem unicidade por paciente/data. Não há exclusão, edição do histórico ou serviços nesse módulo.
- Uma nova gravação só é apresentada como sucesso após consulta de confirmação.

Definições reproduzíveis: `database/005-cadastro-cestas.sql` e `database/005-ords-v2.sql`. A ausência de token foi testada e retorna 401; concorrência retornou 201/409 com uma única linha gravada.

## Serviços e cestas na versão anterior 0.4

A tabela SERVICO_PRESTADO existe, com `id`, `pessoa_id`, `tipo_servico` (100), `descricao` (255) e `data_servico` (DATE). Não foi encontrado template `servicos/` no módulo examinado. A integração de serviços foi mantida no código, mas fica desabilitada até que o endpoint seja disponibilizado e validado.

Não foram observadas colunas de frequência ou última entrega na tabela PESSOA. Cestas e campos médicos não compõem o contrato atualmente publicado. O botão antigo de entrega só mostrava uma mensagem, sem persistência; a versão candidata não apresenta esse comportamento como funcionamento real.

## Reprodução em outra instalação

É necessário acesso a um módulo Oracle que implemente o contrato acima, além de credenciais de API quando exigidas. A pasta `database/` contém a exportação original do módulo e uma estrutura lógica portável das duas tabelas utilizadas. Não contém dados nem o banco hospedado. O responsável precisa revisar o destino e as permissões e testar a restauração em um schema vazio; isso não foi executado nesta revisão.

A leitura de DBMS_METADATA confirmou UNIQUE em CPF e a chave estrangeira `FK_SERVICO_PESSOA` com `ON DELETE CASCADE`. Por isso, a exclusão direta pela API pode apagar os serviços do paciente. O escopo habilitado da aplicação usa inativação.
