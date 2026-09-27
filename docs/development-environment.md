# Ambiente de desenvolvimento

As instruções atuais estão no [README principal](../README.md#execução-no-windows): criar ambiente virtual, instalar requirements.txt, executar configurar.py e iniciar run.py.

A versão 0.4.0-rc1 exige URL base Oracle, segredo de sessão e operador com senha em hash. Não há senha padrão. O configurador não sobrescreve um .env existente.

A integração real passou em 27/09/2026 após troca do cliente para HTTPX com suporte a HTTP/2. Use o ambiente isolado `.venv` e as dependências atuais. No Windows, `INICIAR.cmd` prepara e inicia o projeto. O painel APEX é separado da aplicação Flask; consulte também [limitações](entrega/LIMITACOES.md).

Validação local no Windows: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`. A API é simulada nesses testes. Para avaliar a integração real, use o procedimento específico no README, apenas com dados fictícios autorizados.

Modelos em app/models/ são referências históricas e não são um ORM nem um banco substituto. O contrato efetivo está em app/ords.py e docs/entrega/CONTRATO-ORACLE.md.
