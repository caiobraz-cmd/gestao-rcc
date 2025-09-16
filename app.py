import os
from flask import Flask, redirect, url_for
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

    with app.app_context():
        from instance.routes.pessoa_routes import pessoa_bp
        app.register_blueprint(pessoa_bp)

    @app.route("/")
    def home():
       return redirect(url_for('pessoa_bp.listar'))

    return app
