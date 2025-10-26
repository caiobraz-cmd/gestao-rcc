# Sistema de Gestão RCC

Sistema de gestão de pacientes da Rede de Combate ao Câncer, desenvolvido com Flask e integração com API Oracle ORDS.

## 📋 Descrição

Sistema web para gerenciamento de informações de pacientes, incluindo:
- Cadastro completo de pacientes
- Histórico médico e tratamentos
- Registro de serviços prestados
- Integração com banco de dados Oracle via API REST (ORDS)

## 🏗️ Arquitetura do Projeto

```
gestao-rcc/
│
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py              # Application Factory (create_app)
│   ├── models/                  # Modelos de dados
│   │   ├── __init__.py
│   │   └── pessoa.py           # Modelo Pessoa
│   └── routes/                  # Blueprints e rotas
│       ├── __init__.py
│       └── pessoa_routes.py    # Rotas CRUD de Pessoas
│
├── templates/                   # Templates Jinja2
│   ├── base.html               # Template base
│   ├── listar.html             # Lista de pacientes
│   ├── novo.html               # Cadastro de paciente
│   ├── editar.html             # Edição de paciente
│   ├── detalhes.html           # Detalhes e serviços
│   └── novo_servico.html       # Cadastro de serviço
│
├── static/                      # Arquivos estáticos
│   └── style.css               # Estilos CSS
│
├── BKP/                         # Backup da versão anterior
│
├── config.py                    # Configurações da aplicação
├── run.py                       # Ponto de entrada (development)
├── requirements.txt             # Dependências Python
├── .env                         # Variáveis de ambiente (não versionar)
├── .gitignore                   # Arquivos ignorados pelo Git
└── README.md                    # Este arquivo

```

## 🚀 Tecnologias Utilizadas

- **Flask 3.0.0** - Framework web
- **Python 3.8+** - Linguagem de programação
- **Oracle ORDS** - API REST para banco de dados Oracle
- **Requests** - Cliente HTTP para consumo de API
- **Jinja2** - Engine de templates
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd gestao-rcc
```

### 2. Crie um ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Edite o arquivo `.env` com suas configurações:

```env
API_BASE_URL="https://seu-servidor-ords.com/ords/schema/"
SECRET_KEY="sua-chave-secreta-aqui"
FLASK_ENV="development"
ITEMS_PER_PAGE=20
```

## ▶️ Executando o Projeto

### Modo Desenvolvimento

```powershell
python run.py
```

O servidor estará disponível em: `http://localhost:5000`

### Modo Produção

Para produção, use um servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 🧪 Testando a API

Você pode testar a conexão com a API acessando:

```
http://localhost:5000/ping
```

Deve retornar: `Pong! O servidor Flask está no ar.`

## 📚 Estrutura de Rotas

### Pessoas (Pacientes)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Lista todas as pessoas |
| GET | `/novo` | Exibe formulário de cadastro |
| POST | `/novo` | Cria nova pessoa |
| GET | `/editar/<id>` | Exibe formulário de edição |
| POST | `/editar/<id>` | Atualiza pessoa |
| POST | `/deletar/<id>` | Remove pessoa |
| GET | `/pessoa/<id>/` | Detalhes e histórico |

### Serviços

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/pessoa/<id>/servicos/novo` | Formulário novo serviço |
| POST | `/pessoa/<id>/servicos/novo` | Cria novo serviço |

## 🗃️ Estrutura da API (Oracle ORDS)

### Tabela PESSOAS

```sql
- seq_id (PK)
- ds_nome
- num_cpf
- dt_nascimento
- num_telefone
- char_endereco
- char_diagnostico
- char_tratamento
- char_medicamento
- char_alergia
- char_observacoes
- data_obito
```

### Tabela SERVICOS

```sql
- seq_id (PK)
- ds_nome
- char_descricao
- dt_dataservico
- sq_idpaciente (FK)
```

## 🔒 Segurança

- Nunca commite o arquivo `.env` no Git
- Use variáveis de ambiente para dados sensíveis
- Em produção, use uma `SECRET_KEY` forte e única
- Configure HTTPS em produção

## 🐛 Tratamento de Erros

O sistema implementa tratamento robusto de erros:
- Timeout em requisições (10-15s)
- Validação de status HTTP
- Mensagens flash informativas
- Logs de debug detalhados

## 📝 Padrões de Código

O projeto segue:
- **Application Factory Pattern** - Criação modular da aplicação
- **Blueprints** - Organização de rotas
- **PEP 8** - Estilo de código Python
- **Docstrings** - Documentação de funções

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é privado e pertence à Rede de Combate ao Câncer.

## 👥 Autores

- Desenvolvedor Principal - Gestão RCC Team

## 📞 Suporte

Para suporte, entre em contato através do email: suporte@rcc.org.br

---

**Rede de Combate ao Câncer** © 2025
