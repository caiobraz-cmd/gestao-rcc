# Gestão RCC

Sistema web de apoio à Rede de Combate ao Câncer, desenvolvido por Caio Braz e Osvaldo Mazoni Neto.

**Versão candidata 0.5.0-rc1 — cadastro completo e cestas, ativados em 27/09/2026.** Migração instalada no Oracle, API protegida com OAuth, campos clínicos e histórico persistidos. Passaram 28 testes locais e 23 verificações com Oracle real, incluindo duas entregas simultâneas com apenas uma aceita. A entrega pelo navegador também foi confirmada. Consulte [Evidências reais da 0.5](docs/evidences/v05-oracle/README.md) e [Instalação da atualização](docs/entrega/PROXIMA-VERSAO.md).

A entrega anterior **0.4.0-rc1**, com cadastro básico testado no Oracle, permanece no ZIP de entrega original. Seus relatórios e capturas estão em [Evidências da 0.4](docs/evidences/produto/README.md); não comprovam a integração da 0.5. A apresentação ao cliente continua pendente em [Entrega do produto](docs/entrega/ENTREGA-PRODUTO.md).

## Objetivo e escopo

Organizar o cadastro de pacientes e sua consulta. A integração usa Oracle ORDS, sem banco local substituto. Foram implementados login de operador configurável, consulta, busca, cadastro, edição e mudança de situação ativo/inativo. Cadastro, edição e inativação foram confirmados por novas leituras da API, inclusive após uma nova sessão.

Diagnóstico, tratamentos, medicamentos, alergias, observações, óbito e cestas estão habilitados nesta instalação. A próxima entrega usa a frequência definida no cadastro, e cada entrega fica no histórico. Serviços continuam pendentes. Em outra instalação, é necessário configurar as credenciais próprias do cliente Oracle; elas não acompanham o ZIP nem o GitHub. Veja [Limitações](docs/entrega/LIMITACOES.md).

## Tecnologias e arquitetura

- Python, Flask 3.0.0, Jinja2, HTML e CSS.
- HTTPX 0.28.1 com suporte a HTTP/2 para comunicação com Oracle ORDS por HTTPS.
- python-dotenv para configuração local; Werkzeug para hash de senha.
- unittest para testes automatizados, sem dependência adicional.
- Navegador → Flask → Oracle ORDS → banco Oracle.

A interface usa ícones e fontes de serviços externos; acesso à internet é necessário para a API. Não se deve enviar dados reais de pacientes em evidências.

## Execução no Windows

Pré-requisitos: Python 3.11 ou superior, acesso à API ORDS e terminal na pasta do projeto. A execução dos testes desta revisão foi validada no Python 3.14.4; outras versões precisam de validação no ambiente de destino.

**Atalho no Windows:** abra `INICIAR.cmd`. Ele prepara o ambiente, instala as dependências, pede sua configuração na primeira execução e inicia o sistema. A URL do Oracle já é sugerida pelo configurador; pressione Enter para mantê-la. Crie seu próprio usuário e senha e acesse `http://127.0.0.1:5000`. Mantenha a janela aberta enquanto usar o sistema. O passo a passo manual está abaixo.

1. Baixe e extraia o código. Abra o PowerShell na pasta que contém este README.
2. Prepare o ambiente e instale as versões registradas:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

3. Configure a instalação:

~~~powershell
.\.venv\Scripts\python.exe configurar.py
~~~

O programa pergunta a URL base da API, o usuário da aplicação e uma senha de pelo menos 12 caracteres. A senha é armazenada como hash. Para `/rcc-v2/`, configure também o ID e o segredo do cliente Oracle autorizado. O login do painel APEX é diferente do login do Gestão RCC e não é solicitado pelo aplicativo. Nesta instalação, o acesso local já foi criado: veja `instance/ACESSO-LOCAL.txt` (arquivo privado, fora da entrega).

A URL base deve terminar no módulo, por exemplo `https://oracleapex.com/ords/gestaorcc/rcc/`, **sem** acrescentar `pessoas/` ou `:id`. O `.env.example` lista as variáveis, sem credenciais. O configurador não sobrescreve um `.env` existente.

4. Inicie:

~~~powershell
.\.venv\Scripts\python.exe run.py
~~~

5. Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000), entre com o operador criado e siga o [roteiro de demonstração](docs/entrega/ROTEIRO-DEMONSTRACAO.md).

Para encerrar, pressione Ctrl+C no terminal. O processo local escuta somente neste computador e não usa debug.

## Linux ou macOS

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python configurar.py
.venv/bin/python run.py
~~~

## Verificações

~~~powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools/verificar_ords.py --url https://oracleapex.com/ords/gestaorcc/rcc/pessoas/
~~~

Os testes automatizados simulam respostas HTTP: validam a aplicação, mas não comprovam que a API remota esteja disponível. O diagnóstico faz somente leituras e informa status e nomes de campos, sem imprimir pacientes. O endereço `/ping` identifica a versão e o processo Flask; não testa o Oracle.

## Configuração e limites operacionais

- `API_BASE_URL`: endereço base do módulo ORDS.
- `API_TOKEN`: token Bearer se a API exigir autenticação; não é a senha do APEX.
- `ORDS_CLIENT_ID` e `ORDS_CLIENT_SECRET`: credenciais do cliente OAuth da API. Com elas, deixe `API_TOKEN` vazio; a renovação é automática e o token fica somente em memória.
- `SECRET_KEY`: segredo aleatório de pelo menos 32 caracteres, gerado pelo configurador.
- `ADMIN_USERNAME` e `ADMIN_PASSWORD_HASH`: operador desta instalação. Não há senha padrão.
- `ORDS_SERVICOS_HABILITADOS=false`: só alterar após disponibilizar e testar o contrato de serviços.
- `ORDS_CESTAS_HABILITADAS=true` e `ORDS_DADOS_MEDICOS_HABILITADOS=true`: habilitados na instalação homologada com `/rcc-v2/`; em outra base, aplicar e validar a migração antes.
- `FLASK_ENV=development`: seleção própria desta aplicação. Para produção, a configuração exige HTTPS e cookie seguro.

A sessão expira após 30 minutos. Os formulários são protegidos contra envio sem token de sessão. A API deve ter sua própria autorização: o login Flask não impede acesso direto a um endpoint Oracle público.

Não usar `run.py` como servidor público. Publicação exige servidor WSGI, HTTPS, proteção da API, gestão de usuários e revisão operacional. Esta entrega prevê execução local demonstrável.

## Contrato do banco

Consulte [Contrato Oracle verificado](docs/entrega/CONTRATO-ORACLE.md). A URL de um painel APEX com parâmetro de sessão não é a URL da API e não deve ser incluída nos arquivos distribuídos.

A pasta [database](database/README.md) inclui a definição exportada do módulo e a estrutura das tabelas, sem dados. Não importar sobre o banco existente.

Somente em base fictícia autorizada, o seguinte teste percorre os fluxos Flask usando o Oracle real. Ele cria um registro identificado como TESTE, edita e deixa esse registro inativo; não exclui dados:

~~~powershell
.\.venv\Scripts\python.exe tools/homologar_ords.py --url https://oracleapex.com/ords/gestaorcc/rcc/ --confirmar-dados-ficticios
~~~

O relatório é salvo em `docs/evidences/produto/`. A execução de 27/09/2026 concluiu todas as 11 verificações com o Oracle real; o registro fictício ID 21 ficou inativo. A falha inicial de conexão foi preservada como histórico. A troca para HTTPX foi validada; não foi necessário alterar permissões, autenticação Oracle ou banco. Consulte [Diagnóstico e correção](docs/entrega/CONEXAO-ORACLE.md).

## Documentação da entrega

- [Conferência dos sete requisitos](docs/entrega/ENTREGA-PRODUTO.md)
- [Problemas conhecidos e limitações](docs/entrega/LIMITACOES.md)
- [Roteiro para o cliente](docs/entrega/ROTEIRO-DEMONSTRACAO.md)
- [Evidências e resultados](docs/evidences/produto/README.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](docs/planning/roadmap.md) e [backlog](docs/planning/backlog.md)
- [Workflow da equipe](docs/workflow.md) e [sprints](docs/sprints/README.md)

Não distribua `.env`, ambientes virtuais, cache, histórico `.git` ou bancos locais contendo dados. O pacote deve conter fontes, dependências, instruções e evidências da versão correspondente.
