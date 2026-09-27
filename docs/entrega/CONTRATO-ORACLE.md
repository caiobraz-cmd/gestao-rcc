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

## Serviços e cestas

A tabela SERVICO_PRESTADO existe, com `id`, `pessoa_id`, `tipo_servico` (100), `descricao` (255) e `data_servico` (DATE). Não foi encontrado template `servicos/` no módulo examinado. A integração de serviços foi mantida no código, mas fica desabilitada até que o endpoint seja disponibilizado e validado.

Não foram observadas colunas de frequência ou última entrega na tabela PESSOA. Cestas e campos médicos não compõem o contrato atualmente publicado. O botão antigo de entrega só mostrava uma mensagem, sem persistência; a versão candidata não apresenta esse comportamento como funcionamento real.

## Reprodução em outra instalação

É necessário acesso a um módulo Oracle que implemente o contrato acima, além de credenciais de API quando exigidas. A pasta `database/` contém a exportação original do módulo e uma estrutura lógica portável das duas tabelas utilizadas. Não contém dados nem o banco hospedado. O responsável precisa revisar o destino e as permissões e testar a restauração em um schema vazio; isso não foi executado nesta revisão.

A leitura de DBMS_METADATA confirmou UNIQUE em CPF e a chave estrangeira `FK_SERVICO_PESSOA` com `ON DELETE CASCADE`. Por isso, a exclusão direta pela API pode apagar os serviços do paciente. O escopo habilitado da aplicação usa inativação.
