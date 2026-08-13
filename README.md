# Gestão RCC

Sistema web para apoio à gestão de pacientes, serviços e benefícios da Rede de Combate ao Câncer.

## Integrantes

- Caio Braz
- Osvaldo Mazoni Neto

## Objetivo do projeto

O objetivo do Gestão RCC é dar continuidade a um sistema iniciado anteriormente, organizando sua documentação, fluxo de trabalho, versionamento e evolução até uma versão 1.0 funcional.

O sistema busca auxiliar a Rede de Combate ao Câncer no cadastro de pacientes, acompanhamento de informações importantes, registro de serviços prestados e controle de benefícios, como entrega de cestas básicas.

## Contexto da disciplina

Nesta disciplina, a equipe deve simular uma experiência real de mercado, aplicando gestão de projetos, versionamento, documentação de processos e execução de sprints semanais.

A Sprint 1 tem como foco comprovar que a equipe possui um fluxo funcional de trabalho, com issues, branches, commits, Pull Requests, revisões, documentação e evidências reais de execução.

## Tecnologias utilizadas

- Python
- Flask
- Jinja2
- HTML
- CSS
- Bootstrap
- Oracle ORDS / API REST
- Git
- GitHub
- Markdown

## Estado atual do projeto

O projeto já possui uma base inicial em Flask, contendo:

- estrutura principal da aplicação;
- rotas para pacientes;
- telas HTML com templates Jinja2;
- arquivos estáticos;
- autenticação inicial;
- integração planejada com API Oracle ORDS;
- lógica inicial de controle de cestas em modo de teste.

## Entrega — Sprint 1

A Sprint 1 foi planejada para estruturar e comprovar o fluxo de trabalho da equipe.

### Documentação da Sprint 1

- [Workflow funcional da equipe](docs/workflow.md)
- [Ambiente de desenvolvimento](docs/development-environment.md)
- [Referências bibliográficas](docs/references.md)

### POPs

- [POP — Desenvolvedor: criar branch](docs/pops/desenvolvedor-criar-branch.md)
- [POP — Desenvolvedor: abrir Pull Request](docs/pops/desenvolvedor-abrir-pull-request.md)
- [POP — Documentador: atualizar documentação](docs/pops/documentador-atualizar-documentacao.md)
- [POP — Documentador: registrar evidências](docs/pops/documentador-registrar-evidencias.md)

### Sprint

- [Índice de Sprints](docs/sprints/README.md)
- [Sprints históricas reconstruídas](docs/sprints/historico/README.md)
- [Template de Sprint](docs/sprints/sprint-template.md)
- [Registro da Sprint 1](docs/sprints/sprint-01.md)

### Evidências

- [Evidências de versionamento](docs/evidences/version-control/README.md)

## Estrutura do repositório

```txt
gestao-rcc/
├── app/                         # Código principal da aplicação Flask
├── templates/                   # Templates HTML/Jinja2
├── static/                      # Arquivos CSS e estáticos
├── docs/                        # Documentação do projeto
│   ├── planning/                # Planejamento geral
│   ├── workflow/                # Documentos do primeiro bimestre
│   ├── pops/                    # Procedimentos Operacionais Padrão
│   ├── sprints/                 # Template e registros de sprint
│   └── evidences/               # Evidências da execução
├── src/                         # Referência estrutural exigida
├── config.py                    # Configurações da aplicação
├── run.py                       # Execução local
├── requirements.txt             # Dependências Python
├── .env.example                 # Exemplo de variáveis de ambiente
└── README.md
```

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/caiobraz-cmd/gestao-rcc.git
cd gestao-rcc
```

### 2. Criar ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Criar um arquivo `.env` com base no `.env.example`:

```env
API_BASE_URL=
SECRET_KEY=
FLASK_ENV=development
ITEMS_PER_PAGE=20
```

O arquivo `.env` não deve ser enviado ao GitHub.

### 5. Executar o projeto

```powershell
python run.py
```

A aplicação ficará disponível em:

```txt
http://localhost:5000
```

### 6. Testar o servidor

Acessar:

```txt
http://localhost:5000/ping
```

Resultado esperado:

```txt
Pong! O servidor Flask está no ar.
```

## Workflow da equipe

A equipe utiliza uma adaptação simples do GitHub Flow:

1. Criar uma issue para cada tarefa.
2. Criar uma branch a partir da `main`.
3. Fazer as alterações necessárias.
4. Realizar commits com mensagens compreensíveis.
5. Abrir Pull Request.
6. Solicitar revisão de outro integrante.
7. Fazer merge após revisão.
8. Registrar evidências.

## Divisão de papéis

### Caio Braz

Função: Desenvolvedor / responsável técnico.

Responsabilidades:

- documentação do workflow;
- documentação do ambiente de desenvolvimento;
- criação dos POPs da função Desenvolvedor;
- validação da execução local do sistema;
- abertura e revisão de Pull Requests.

### Osvaldo Mazoni Neto

Função: Documentador / apoio de processos.

Responsabilidades:

- criação dos POPs da função Documentador;
- registro da Sprint 1;
- organização das evidências;
- apoio na documentação do processo;
- revisão de Pull Requests.

## Planejamento do projeto

- [Visão do Projeto](docs/planning/project-vision.md)
- [Backlog](docs/planning/backlog.md)
- [Roadmap](docs/planning/roadmap.md)
- [Changelog](CHANGELOG.md)
- [Sprints](docs/sprints/README.md)

## Versão atual

Versão acadêmica atual: `0.3`

A versão `1.0` deverá ser preparada até o final do terceiro bimestre.

## Segurança

- O arquivo `.env` não deve ser versionado.
- Dados sensíveis devem ser armazenados em variáveis de ambiente.
- A branch `main` deve representar uma versão estável.
- Alterações devem ser feitas por branch e Pull Request.

## Licença

Projeto acadêmico desenvolvido para fins educacionais.
