import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    @app.route("/")
    def home():
        return "Sistema de Gestão de pessoas - Rede de Combate ao Câncer (RCC)"
    
    return app

    if __name__ == "__main__":
        app = create_app()

        debug_mode = os.environ.get("FLASK_ENV", "development") != "production"
        app.run(debug=debug_mode)
        
