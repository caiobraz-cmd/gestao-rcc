import os 
from urllib.parse import quote_plus


basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

if os.environ.get("FLASK_ENV") != "production":
    try: 

        from dotenv import load_dotenv
        load_dotenv()
    except Exception: 
        pass

class BaseConfig: 
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-seret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(instance_path, 'banco.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.environ.get("DB_POOL_SIZE", 5)),
        "max_overflow": int(os.environ.get("DB_MAX_OVERFLOW", 10)),
        "pool_timeout": int(os.environ.get("DB_POOL_TIMEOUT", 30)),
        "pool_recycle": int(os.environ.get("DB_POOL_RECYCLE", 1800)),

    }
    
    DEBUG = False
    TESTING = False
    ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 20))

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "False").lower() in ("1", "true", "yes")

class TestingConfig(BaseConfig): 
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
class ProductionConfig(BaseConfig):
    DEBUG = False

    @classmethod
    def check_env(cls):
        if not os.environ.get("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL não está definida em ProductionConfig")

