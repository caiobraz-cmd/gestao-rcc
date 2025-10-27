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
basedir = os.path.abspath(os.path.dirname(__file__))

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

    #: URL base da API do Oracle (ORDS) de onde os dados serão consumidos.
    #: Lida a partir da variável de ambiente API_BASE_URL.
    API_BASE_URL = os.environ.get("API_BASE_URL")
    
    #: Configurações padrão para DEBUG e TESTING.
    DEBUG = False
    TESTING = False
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 20))


class DevelopmentConfig(BaseConfig):
    """Configurações para o ambiente de desenvolvimento."""
    DEBUG = True


class TestingConfig(BaseConfig): 
    """Configurações para o ambiente de testes automatizados."""
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Configurações para o ambiente de produção."""
    DEBUG = False

    @classmethod
    def check_env(cls):
        """Verifica se variáveis críticas estão definidas em produção."""
        if not os.environ.get("API_BASE_URL"):
            raise RuntimeError("API_BASE_URL não está definida em ProductionConfig")
