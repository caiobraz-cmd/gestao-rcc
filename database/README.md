# Fontes da dependência Oracle

- `ords-exportado.sql`: exportação original do módulo `gestao_rcc`, realizada pelo painel Oracle APEX em 26/09/2026. Contém os handlers de pacientes existentes; não contém registros nem credenciais.
- `schema.sql`: estrutura lógica das tabelas PESSOA e SERVICO_PRESTADO, obtida por leitura de DBMS_METADATA. Foram retirados nomes de schema, tablespace e opções de armazenamento para facilitar a revisão. Não inclui outras tabelas do workspace que não são utilizadas pelo escopo atual.

## Uso normal

Para usar a API existente, configure o Flask conforme o README principal. **Não execute estes scripts no workspace existente.** A exportação redefine o módulo e configura sua publicação; ela não é uma migração incremental.

## Reprodução em outro ambiente

Um responsável Oracle deve criar um schema vazio, revisar os tamanhos/semântica dos campos e executar `schema.sql`; depois revisar o alias, a publicação e a autorização antes de importar `ords-exportado.sql`. A exportação preserva a configuração observada e não deve ser aplicada em um ambiente com dados reais sem essa revisão. A reprodução em um segundo schema não foi executada nesta entrega.

Há chave UNIQUE em CPF e chave estrangeira de serviço para paciente. O banco observado usa `ON DELETE CASCADE`, portanto excluir um paciente diretamente na API pode apagar seu histórico de serviços. A aplicação mantém exclusão desabilitada no escopo atual e oferece inativação.

Os handlers PUT e DELETE atuais retornam 200 sem verificar quantidade de linhas afetadas. A aplicação confirma a edição por nova leitura. A API não tem endpoint de serviços nem campos para cestas/dados médicos no módulo exportado.
