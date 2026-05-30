# Ambiente de Desenvolvimento

## Objetivo

Este documento descreve o ambiente de desenvolvimento utilizado no projeto Gestão RCC e apresenta as instruções necessárias para executar o sistema localmente.

O objetivo é permitir que outro integrante consiga clonar o repositório, instalar as dependências e validar o funcionamento da aplicação.

## Ambiente utilizado

```txt
Sistema operacional: Windows 10/11
Terminal: PowerShell
Editor/IDE: Visual Studio Code
Controle de versão: Git
Repositório remoto: GitHub
```

## Linguagem e framework

```txt
Linguagem: Python
Framework: Flask
Template engine: Jinja2
```

## Dependências

As dependências do projeto estão registradas no arquivo `requirements.txt`.

Dependências atuais:

```txt
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
Werkzeug==3.0.1
```

## Clonar o repositório

```bash
git clone https://github.com/caiobraz-cmd/gestao-rcc.git
cd gestao-rcc
```

## Criar ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Instalar dependências

Com o ambiente virtual ativado:

```powershell
pip install -r requirements.txt
```

## Configurar variáveis de ambiente

O projeto utiliza variáveis de ambiente para evitar que dados sensíveis fiquem no código.

Criar um arquivo `.env` com base no `.env.example`:

```env
API_BASE_URL=
SECRET_KEY=
FLASK_ENV=development
ITEMS_PER_PAGE=20
```

O arquivo `.env` não deve ser enviado ao GitHub.

## Executar o projeto

```powershell
python run.py
```

O servidor deverá iniciar em:

```txt
http://localhost:5000
```

## Testar funcionamento

Acessar no navegador:

```txt
http://localhost:5000/ping
```

Resultado esperado:

```txt
Pong! O servidor Flask está no ar.
```

## Comandos de validação

Para registrar evidências do ambiente, executar:

```bash
python --version
pip --version
git --version
```

## Evidências esperadas

As evidências devem ser salvas em:

```txt
docs/evidences/sprint-01/
```

Evidências recomendadas:

```txt
python-version.png
pip-version.png
git-version.png
pip-install.png
projeto-executando.png
rota-ping-funcionando.png
```

## Critérios de sucesso

O ambiente é considerado validado quando:

- o repositório foi clonado;
- o ambiente virtual foi criado;
- as dependências foram instaladas;
- o arquivo `.env` foi configurado localmente;
- o comando `python run.py` iniciou o servidor;
- a rota `/ping` respondeu corretamente;
- as evidências foram registradas.