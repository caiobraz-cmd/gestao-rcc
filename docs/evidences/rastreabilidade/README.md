# Rastreabilidade de serviços — 07/11/2026

Instalada em GESTAORCC pelos scripts 008 (serviços) e 009 (pacientes e cestas). Revisão local ainda não publicada.

## Resultado

- Botão Buscar azul alinhado ao campo; busca por TESTE conferida no navegador.
- Tela Administração → Registros de serviços com busca no servidor, paginação de 25 itens e link para o paciente.
- 40 testes locais aprovados, incluindo bloqueio de operador na consulta administrativa, filtro/paginação e rejeição de autor forjado no formulário.
- Homologação real criou serviços fictícios 21 e 22 para o paciente de teste 41. O registro 21 veio do formulário Flask; o Oracle confirmou autoria da sessão, perfil, data e vínculo.
- GET da consulta sem credenciais retornou 401.
- Repetição da chave de rastreabilidade retornou 409. A contagem dos serviços permaneceu igual, comprovando que a falha na segunda gravação desfez também o serviço.
- A consulta e os registros anteriores foram conferidos no navegador. Registros antigos têm autoria não identificada.

## Limites

A implementação registra criação de serviços, cadastro/alteração de pacientes e entrega de cestas. A autoria é declarada pelo backend autenticado com OAuth; credenciais desse cliente devem permanecer privadas. A interface não permite editar ou excluir os registros, mas isso não torna o banco inviolável para seus administradores. Não foram copiados CPF, diagnóstico ou descrição clínica para a tabela de rastreabilidade. A consulta mostra o nome atual do paciente, sem versões anteriores dos campos.

Clientes antigos que não enviam autoria permanecem compatíveis e geram registros sem identificação. Não reexecute os scripts 006 após instalar 008, pois isso restauraria o handler antigo.

## Ampliação para pacientes e cestas

- Tabela RCC_REGISTRO_OPERACAO e endpoints instalados incrementalmente. Os três handlers anteriores foram preservados em arquivo privado antes da substituição; módulo, permissões e GETs existentes não foram recriados.
- Paciente fictício 61 criado pelo formulário Flask, editado e contemplado com uma cesta. A criação, edição, entrega e inativação final foram confirmadas na consulta do Oracle e na interface administrativa.
- Colisão forçada na chave de auditoria durante uma entrega retornou 409 e não deixou cesta gravada. Colisão durante edição retornou 409 e preservou o nome anterior do paciente.
- Consulta sem token retornou 401. Os 43 testes locais passaram, incluindo bloqueio de operador, filtros e confirmação de pessoa, autoria, perfil e tipo da operação.
- A tela unificada tem busca por paciente ou responsável e filtro por operação, com 25 itens por página. Cestas antigas aparecem sem autoria e podem ter apenas a data; alterações anteriores à ativação não são inventadas.
- Não reaplicar 005 sobre 009: isso restauraria handlers sem rastreabilidade. A instalação no Render não faz parte desta revisão.
