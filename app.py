
"""
Ponto de Entrada e Fábrica da Aplicação Flask.

Este módulo utiliza o padrão "Application Factory" para criar e configurar a
instância principal da aplicação Flask.
"""

import os
from flask import Flask, redirect, url_for
from config import DevelopmentConfig, ProductionConfig


def create_app():
    """Cria, configura e retorna a instância da aplicação Flask."""
    
    app = Flask(__name__, instance_relative_config=True)

    # Carrega a configuração (DevelopmentConfig ou ProductionConfig)
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)


    # Registro de Blueprints
    with app.app_context():
        # Importamos o blueprint 
        from instance.routes.pessoa_routes import pessoa_bp
        
        # Registra o blueprint na URL raiz '/'
        app.register_blueprint(pessoa_bp, url_prefix='/')

    # Rota de teste
    @app.route("/ping")
    def home():
        return "Pong! O servidor Flask está no ar."

    return app