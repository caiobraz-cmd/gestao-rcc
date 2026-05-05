# Separação entre Desenvolvimento e Produção

## Objetivo

Este documento explica como a equipe pretende separar o ambiente de desenvolvimento do ambiente de produção no projeto Gestão RCC.

Essa separação é importante para evitar que arquivos de teste, rascunhos, documentos internos ou dados sensíveis sejam enviados junto com a versão final do sistema.

---

# Ambiente de desenvolvimento

O ambiente de desenvolvimento é utilizado pelos integrantes da equipe para criar, testar e ajustar funcionalidades antes de enviá-las para a versão principal do projeto.

Nesse ambiente, podem existir arquivos que não devem ir para produção, como configurações locais, dados de teste, ambientes virtuais e documentos internos.

## Arquivos e recursos de desenvolvimento

Exemplos de arquivos usados apenas no desenvolvimento:

- `.env`
- `venv/`
- `__pycache__/`
- arquivos de log
- arquivos temporários
- dados mockados
- prints e evidências da disciplina
- documentos internos de planejamento
- testes locais
- rascunhos de funcionalidades

No projeto atual, ainda existem partes em modo de teste, como dados mockados para simular pacientes e controle de cesta básica. Esses recursos ajudam no desenvolvimento, mas devem ser revisados antes da versão final.

---

# Ambiente de produção

O ambiente de produção representa a versão que será usada de forma estável.

A produção deve conter apenas os arquivos necessários para executar o sistema com segurança e organização.

## Arquivos e recursos que devem ir para produção

- código-fonte da aplicação Flask;
- templates HTML;
- arquivos CSS e estáticos necessários;
- `requirements.txt`;
- `README.md`;
- documentação essencial;
- configurações lidas por variáveis de ambiente;
- arquivos necessários para execução do sistema.

## Arquivos que não devem ir para produção

- `.env` com dados reais;
- ambiente virtual `venv/`;
- arquivos de cache;
- logs locais;
- rascunhos;
- prints da avaliação;
- dados sensíveis;
- senhas, chaves secretas ou URLs privadas escritas diretamente no código.

---

# Controle de arquivos sensíveis

A equipe utilizará o arquivo `.gitignore` para impedir que arquivos sensíveis ou desnecessários sejam enviados ao GitHub.

O arquivo `.env` deverá ser mantido apenas no computador dos desenvolvedores ou no ambiente de hospedagem, nunca no repositório público.

Para orientar outros desenvolvedores, poderá ser criado um arquivo `.env.example`, contendo apenas os nomes das variáveis necessárias, sem valores reais.

Exemplo:

```env
API_BASE_URL=
SECRET_KEY=
FLASK_ENV=development
ITEMS_PER_PAGE=20