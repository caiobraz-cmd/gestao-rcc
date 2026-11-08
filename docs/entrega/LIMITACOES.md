# Problemas conhecidos — revisão local em 07/11/2026

1. **Execução local:** servidor de desenvolvimento Flask; não é publicação pronta para produção.
2. **Internet e Oracle:** necessários para todos os cadastros e entregas. Após falha de conexão, consultar o registro antes de repetir uma gravação.
3. **Serviços:** exigem a atualização 006 e a flag habilitada. O fluxo contempla cadastro e consulta, sem edição ou exclusão do histórico.
4. **Acessos:** a revisão local oferece um administrador por instalação e contas individuais de operador no Oracle. O operador pode trocar sua senha; o administrador pode redefini-la. Não há recuperação pública por e-mail. As entregas novas identificam a conta responsável; as antigas não recebem autoria retroativa.
5. **Cestas:** sem estoque, entrega antecipada/retroativa ou correção de histórico pela interface. A equipe define quem recebe e a frequência.
6. **API antiga:** /rcc-v2/ exige OAuth e recusou acesso anônimo. O módulo legado /rcc/ continua com acesso público aos dados básicos. Revisar sua proteção antes de usar dados reais; a base atual foi declarada fictícia pelo responsável.
7. **CPF legado:** a edição exige CPF válido; cadastros antigos não foram corrigidos automaticamente.
8. **Escala:** busca percorre a coleção com limite de 10.000 registros. Bases maiores exigem filtros no servidor.
9. **Operação:** revisar dependências, monitoramento e backup/restauração antes de produção. Há limite de tentativas em memória por processo; reinícios zeram os contadores. Múltiplos workers/servidores exigem armazenamento compartilhado. A aplicação usa o endereço remoto da conexão e não confia em X-Forwarded-For; atrás de proxy, usuários podem compartilhar esse limite. A cópia BKP_PESSOA_20260927_V05 preserva dados anteriores, mas não substitui uma política de backup.
10. **Testes:** 28 locais e 23 verificações reais aprovados. Datas-limite e atraso foram testados localmente; concorrência real usou duas requisições. Não equivale a teste de carga ou auditoria completa.
11. **Aceite:** apresentação e confirmação pelo cliente continuam pendentes.

Capturas v05-local são prévias simuladas; v05-oracle mostra integração real. Relatórios da 0.4 permanecem históricos.
