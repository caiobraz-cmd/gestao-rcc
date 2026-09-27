# Problemas conhecidos — 0.4.0-rc1

1. **Dependência de internet e do serviço Oracle:** a falha inicial de conexão foi resolvida no ambiente testado após adoção do HTTPX. Cadastro, edição e inativação passaram em 27/09/2026. A causa exata da diferença entre clientes não foi isolada; não se garante disponibilidade permanente do serviço externo. Falhas futuras continuam sendo tratadas sem afirmar gravação não confirmada.
2. **Serviços ainda não publicados:** a tabela existe, porém falta endpoint no módulo examinado. O recurso fica desativado até a configuração e validação remotas.
3. **Cestas e dados médicos não suportados pelo schema atual:** faltam campos e contrato de persistência. Não existe histórico de entregas nesta versão habilitada.
4. **Exclusão preserva histórico:** sem acesso validado aos serviços, a aplicação oferece inativação em vez de exclusão. Quando serviços forem habilitados, a exclusão só será tentada para pacientes sem serviços vinculados, além das regras do banco.
5. **Um operador por instalação:** login configurável com hash, mas sem cadastro de múltiplos usuários, perfis ou recuperação de senha. Não é implantação pronta para uso público.
6. **API precisa de autorização própria:** a proteção das telas não protege o acesso direto ao Oracle. A configuração de privilégios deve ser validada antes do uso com dados reais. O estado “Authorization Required for Metadata Access” do painel refere-se a metadados, não comprova segurança dos endpoints de dados.
7. **Duplicidade e concorrência:** a aplicação verifica CPF duplicado antes de gravar e foi confirmada chave UNIQUE em CPF no banco. A normalização dos dados legados e o tratamento específico de conflito concorrente nos handlers ainda merecem revisão; atualmente o handler retorna erro genérico.
8. **Escala:** a busca e a checagem de duplicidade percorrem a coleção paginada, com limite de 10.000 registros por consulta. Para bases maiores, implementar filtros no servidor.
9. **Dependências e operação:** revisar versões e vulnerabilidades antes de produção, definir backup e restauração, monitoramento e proteção contra tentativas repetidas de login. Não foi feita auditoria completa de segurança.
10. **Demonstração ao cliente ainda depende de participação humana:** um teste automatizado ou screenshot técnico não substitui apresentação e confirmação do usuário final.

Os PDFs e prints enviados anteriormente descrevem a versão 0.3. Não devem ser reutilizados como comprovação de funcionamento da 0.4.0-rc1 sem identificação de que são registros anteriores.

O histórico, a comparação de clientes e a correção estão em [CONEXAO-ORACLE.md](CONEXAO-ORACLE.md). O 403 anterior não é mais o estado da última homologação.
