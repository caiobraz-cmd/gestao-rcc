# Evidências reais — atualização 0.5

Integração verificada em 27/09/2026 no Oracle ORDS GESTAORCC, usando somente dados fictícios autorizados.

- `homologacao-20260927T142512.json`: 23 verificações reais aprovadas antes da promoção de 0.5.0-dev para 0.5.0-rc1. Registro TESTE ID 41 ficou inativo, com uma entrega. Duas requisições simultâneas retornaram 201/409 e gravaram uma única linha.
- `01-entrega-confirmada.png`: entrega do TESTE ID 42 pela interface, confirmada no Oracle em 27/09/2026; próxima entrega 04/10/2026.
- `02-formulario-completo.png`: campos clínicos e frequência carregados do Oracle, com identificação 0.5.0-rc1.
- `03-edicao-historico-preservado.png`: edição com acentos confirmada no Oracle; o ID 42 foi inativado e seu histórico preservado. Os cadastros de homologação 41 e 42 ficaram inativos.
- 28 testes locais aprovados, incluindo renovação de tokens, regras de agenda e falhas de persistência.

O módulo `gestao_rcc_v2` foi publicado com privilégio e papel próprios. Consultas e gravações sem token foram recusadas.
Os dados anteriores foram copiados para `BKP_PESSOA_20260927_V05` antes da migração; não foram excluídos.
Credenciais e acesso local estão fora do repositório e do pacote. A pasta `v05-local` contém prévias simuladas, anteriores à ativação.
Esta evidência não comprova apresentação ou aceite do cliente.
