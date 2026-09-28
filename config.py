"""Configuração por ambiente, sem credenciais embutidas."""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env', override=False)

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_BASE_URL = os.environ.get('API_BASE_URL', '').strip()
    API_TOKEN = os.environ.get('API_TOKEN', '').strip()
    ORDS_CLIENT_ID = os.environ.get('ORDS_CLIENT_ID', '').strip()
    ORDS_CLIENT_SECRET = os.environ.get('ORDS_CLIENT_SECRET', '').strip()
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', '').strip()
    ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', '').strip()
    APP_VERSION = '0.5.0-rc1'
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    ORDS_CESTAS_HABILITADAS = os.environ.get('ORDS_CESTAS_HABILITADAS', 'false').lower() == 'true'
    ORDS_SERVICOS_HABILITADOS = os.environ.get('ORDS_SERVICOS_HABILITADOS', 'false').lower() == 'true'
    ORDS_DADOS_MEDICOS_HABILITADOS = os.environ.get('ORDS_DADOS_MEDICOS_HABILITADOS', 'false').lower() == 'true'

class DevelopmentConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    SESSION_COOKIE_SECURE = True
