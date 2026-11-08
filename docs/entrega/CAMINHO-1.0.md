# Próximos passos para a 1.0

Revisão em 07/11/2026. Esta lista descreve o estado local, não a publicação no Render.

## Já disponível

- Pacientes, campos clínicos, cestas e serviços integrados ao Oracle.
- Painel exclusivo do administrador para cadastrar, suspender, reativar e redefinir senhas de operadores.
- Troca de senha pelo operador, com validação da senha atual e revogação das sessões antigas.
- Verificação de persistência antes de confirmar sucesso na gestão de contas.
- Dependências Flask, Werkzeug e python-dotenv atualizadas após auditoria; nenhum alerta conhecido nas 19 dependências resolvidas na consulta de 07/11/2026. [Relatório](../evidences/seguranca/README.md).
- Limite local de 5 tentativas por login e 30 por origem em uma janela de 5 minutos, aplicado separadamente ao login e à troca de senha. Tentativas corretas também contam; não reinicia a janela a cada bloqueio.

## Prioridades restantes

1. **Rastreabilidade entregue nesta revisão:** cadastro/alteração de pacientes, entrega de cestas e criação de serviços registram autoria na mesma transação. O administrador consulta o histórico unificado; validar com o cliente se é necessário identificar também os nomes dos campos alterados, sem duplicar valores clínicos.
2. **Recuperação:** definir e testar backup/restauração em uma base separada. As cópias históricas existentes não são uma política de recuperação.
3. **Acessos e publicação:** revisar o módulo legado público, a recuperação da conta administrativa inicial e um limitador compartilhado quando houver vários processos ou servidores. Verificar dependências e realizar revisão de segurança antes do uso com dados reais.
4. **Validação pelo usuário:** percorrer os fluxos com o cliente, especialmente em celular, registrar aceite e corrigir os problemas encontrados.
5. **Release:** consolidar documentação e versão, preparar pacote sem credenciais e publicar somente após os critérios anteriores.

O Render permanece fora desta etapa por decisão do responsável. Recursos como estoque completo, WhatsApp e relatórios avançados podem esperar até o fluxo básico ser validado.
