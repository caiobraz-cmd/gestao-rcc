# Gestão de contas — verificação em 06/11/2026

Revisão local sobre 0.6.0-rc1, ainda não publicada. As contas de operadores usam a tabela RCC_CONTA_OPERADOR no Oracle; a conta administrativa inicial permanece na configuração privada.

## Verificações reais

- Cadastro de operador fictício e rejeição de login duplicado.
- Acesso do operador aos pacientes; painel administrativo oculto e acesso direto recusado com 403, inclusive tentativa de gravação.
- Redefinição de senha, desativação e reativação pelo administrador.
- Rotas de contas e credenciais recusam acesso anônimo com 401.
- Troca de senha pelo próprio operador: senha atual incorreta rejeitada; senha nova persistida e aceita em novo login; senha antiga rejeitada.
- Uma segunda sessão, aberta antes da troca, perdeu acesso à rota protegida na próxima requisição.
- A conta fictícia ficou desativada ao final.

Executado com os formulários Flask (test_client) e ORDS real. O painel administrativo também foi conferido no navegador, conforme painel.png. A suíte local passou nos 34 testes. Isso não equivale a auditoria completa de segurança, teste de carga nem validação desta revisão no Render.

## Revisão de 07/11/2026

Foram adicionados testes para limites de tentativas concorrentes, expiração da janela, limite de memória, bloqueio anterior à consulta Oracle e confirmação de persistência das alterações administrativas. A suíte de 37 testes passou; em seguida, os oito testes de administração passaram com duas novas verificações de persistência, totalizando 39 testes distintos na revisão. Uma alteração da conta fictícia já desativada também foi confirmada por releitura no Oracle real. Nenhuma conta real foi modificada.
