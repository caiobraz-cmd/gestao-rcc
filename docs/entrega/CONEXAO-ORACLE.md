# Conexão Oracle — correção validada em 27/09/2026

## Estado atual

A aplicação foi alterada de Requests para HTTPX 0.28.1, com suporte a HTTP/2 habilitado. A consulta voltou a responder 200 com JSON e o teste completo de cadastro, edição, inativação e leitura após nova sessão passou usando o Oracle real.

O relatório aprovado é `docs/evidences/produto/oracle-real-20260927T050620.json` (11 etapas, concluido: true, registro de teste ID 21). A consulta atual também está registrada em `diagnostico-httpx-aprovado.json`.

## Comparação que orientou a correção

| Cliente observado | Resultado |
|---|---|
| Requests no ambiente inicial | Timeout ou 403 com HTML fw_error_www e Server AkamaiNetStorage |
| Navegador do usuário | JSON disponível, inclusive após atualização |
| PowerShell com HTTP/2 e identificação Gestão RCC | 200, application/json, protocolo 2.0 |
| HTTPX no ambiente isolado, HTTP/1.1 | 200 com JSON |
| HTTPX no ambiente isolado, HTTP/2 | 200 com JSON |
| Fluxos Flask usando HTTPX | Leitura e gravação confirmadas no Oracle |

O HTTPX funcionou com os dois protocolos. Portanto, não foi demonstrado que a falha era exclusivamente HTTP/1.1, nem que uma regra específica do firewall era a causa. A troca de cliente e o ambiente atualizado resolveram o problema nas verificações executadas. A hipótese anterior de exigir liberação manual do Oracle foi superada por esses resultados; não houve mudança de permissões.

## Aplicação da correção

Abra `INICIAR.cmd`, que utiliza o ambiente isolado e instala `requirements.txt`, ou siga os comandos do README. Executar o Python global sem instalar as novas dependências pode resultar em erro de módulo ausente. Não reutilize o ZIP anterior como se já contivesse esta revisão: use o pacote reconstruído.

Certificados HTTPS continuam sendo verificados, não são copiadas sessões do navegador, não foi alterada a autenticação do Oracle e o User-Agent identifica Gestão RCC. O banco remoto foi mantido.

## Se a falha voltar

Execute o diagnóstico do README, preserve status, tipo de resposta e protocolo e confira se está usando o ambiente isolado. Em caso de timeout durante gravação, consulte a lista antes de repetir. Se a recusa persistir mesmo no ambiente validado, o responsável pelo serviço poderá investigar a resposta e o número do incidente, sem receber credenciais ou dados de pacientes.

Referência técnica: [suporte oficial a HTTP/2 no HTTPX](https://www.python-httpx.org/http2/). A documentação explica como habilitar o suporte e conferir o protocolo negociado; ela não garante disponibilidade de um serviço externo.
