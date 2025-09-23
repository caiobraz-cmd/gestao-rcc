# -*- coding: utf-8 -*-
"""
Arquivo de Configuração da Aplicação Flask.

Este módulo centraliza todas as configurações, separando-as por ambientes
(Desenvolvimento, Teste, Produção) e garantindo a portabilidade do projeto
através da criação dinâmica de caminhos.
"""

import os 
from urllib.parse import quote_plus

# --- Configuração de Caminhos Dinâmicos ---

# 'basedir' calcula o caminho absoluto para o diretório raiz do projeto.
# Isso garante que a aplicação encontre seus arquivos, não importa de onde
# o script de execução seja chamado.
basedir = os.path.abspath(os.path.dirname(__file__))

# Define o caminho para a pasta 'instance' e a cria se não existir.
# A pasta 'instance' é ideal para arquivos que não devem ser versionados,
# como o banco de dados de desenvolvimento local.
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# --- Carregamento de Variáveis de Ambiente (.env) ---

# Em ambientes de não-produção, tenta carregar variáveis de um arquivo .env
# para facilitar o desenvolvimento local.
if os.environ.get("FLASK_ENV") != "production":
    try: 
        from dotenv import load_dotenv
        load_dotenv()
    except Exception: 
        pass

# --- Classes de Configuração ---

class BaseConfig: 
    """Configurações base que se aplicam a todos os ambientes."""

    #: Chave secreta para segurança de sessões e cookies.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    #: URI de conexão com o banco de dados. Prioriza a variável de ambiente
    #: DATABASE_URL, caso contrário, usa um banco SQLite local na pasta 'instance'.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(instance_path, 'banco.db')

    #: Desativa o rastreamento de modificações do SQLAlchemy para otimização.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #: Opções de otimização para o pool de conexões do SQLAlchemy.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.environ.get("DB_POOL_SIZE", 5)),
        "max_overflow": int(os.environ.get("DB_MAX_OVERFLOW", 10)),
        "pool_timeout": int(os.environ.get("DB_POOL_TIMEOUT", 30)),
        "pool_recycle": int(os.environ.get("DB_POOL_RECYCLE", 1800)),
    }
    
    #: Configurações padrão para DEBUG e TESTING.
    DEBUG = False
    TESTING = False
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 20))


class DevelopmentConfig(BaseConfig):
    """Configurações para o ambiente de desenvolvimento."""
    DEBUG = True
    #: Se ativado, o SQLAlchemy imprime todas as queries SQL executadas.
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "False").lower() in ("1", "true", "yes")


class TestingConfig(BaseConfig): 
    """Configurações para o ambiente de testes automatizados."""
    TESTING = True
    #: Usa um banco de dados em memória para testes rápidos e isolados.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Configurações para o ambiente de produção."""
    DEBUG = False

    @classmethod
    def check_env(cls):
        """Verifica se variáveis críticas estão definidas em produção."""
        if not os.environ.get("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL não está definida em ProductionConfig")