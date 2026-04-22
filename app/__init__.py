"""
Ponto de Entrada e Fábrica da Aplicação Flask.

Este módulo utiliza o padrão "Application Factory" para criar e configurar a
instância principal da aplicação Flask.
"""

import os
from flask import Flask


def create_app():
    """Cria, configura e retorna a instância da aplicação Flask."""
    
    # Define os caminhos absolutos para templates e static
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(basedir, 'templates')
    static_dir = os.path.join(basedir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)

    # Carrega a configuração (DevelopmentConfig ou ProductionConfig)
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Registro de Blueprints
    with app.app_context():
        # Blueprint de Autenticação (NOVO)
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        # Importa e registra o blueprint de pessoas
        from app.routes.pessoa_routes import pessoa_bp
        app.register_blueprint(pessoa_bp, url_prefix='/')
        
    # Rota de teste
    @app.route("/ping")
    def ping():
        return "Pong! O servidor Flask está no ar."

    return app
