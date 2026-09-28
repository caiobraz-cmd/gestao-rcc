# Problemas conhecidos — 0.5.0-rc1

1. **Execução local:** servidor de desenvolvimento Flask; não é publicação pronta para produção.
2. **Internet e Oracle:** necessários para todos os cadastros e entregas. Após falha de conexão, consultar o registro antes de repetir uma gravação.
3. **Serviços:** sem endpoints na API nova, permanecem desativados.
4. **Um operador por instalação:** sem múltiplos perfis ou recuperação de senha. O histórico identifica data e frequência, não o operador humano.
5. **Cestas:** sem estoque, entrega antecipada/retroativa ou correção de histórico pela interface. A equipe define quem recebe e a frequência.
6. **API antiga:** /rcc-v2/ exige OAuth e recusou acesso anônimo. O módulo legado /rcc/ continua com acesso público aos dados básicos. Revisar sua proteção antes de usar dados reais; a base atual foi declarada fictícia pelo responsável.
7. **CPF legado:** a edição exige CPF válido; cadastros antigos não foram corrigidos automaticamente.
8. **Escala:** busca percorre a coleção com limite de 10.000 registros. Bases maiores exigem filtros no servidor.
9. **Operação:** revisar dependências, tentativas de login, monitoramento e backup/restauração antes de produção. A cópia BKP_PESSOA_20260927_V05 preserva dados anteriores, mas não substitui uma política de backup.
10. **Testes:** 28 locais e 23 verificações reais aprovados. Datas-limite e atraso foram testados localmente; concorrência real usou duas requisições. Não equivale a teste de carga ou auditoria completa.
11. **Aceite:** apresentação e confirmação pelo cliente continuam pendentes.

Capturas v05-local são prévias simuladas; v05-oracle mostra integração real. Relatórios da 0.4 permanecem históricos.
