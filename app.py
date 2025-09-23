# -*- coding: utf-8 -*-
"""
Ponto de Entrada e Fábrica da Aplicação Flask.

Este módulo utiliza o padrão "Application Factory" para criar e configurar a
instância principal da aplicação Flask. Esta abordagem permite uma maior
flexibilidade para criar múltiplas instâncias da aplicação com diferentes
configurações, o que é ideal para testes e escalabilidade.

Funções:
    create_app(): Constrói e retorna a instância configurada da aplicação.
"""

import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig

# --- Instância da Extensão SQLAlchemy ---

# A instância de SQLAlchemy é criada globalmente, mas inicializada
# dentro da fábrica da aplicação para vinculá-la a uma instância específica.
db = SQLAlchemy()

def create_app():
    """
    Cria, configura e retorna a instância da aplicação Flask.

    Esta função é a "fábrica" que constrói a aplicação, realizando os
    seguintes passos:
    1. Cria a instância do Flask.
    2. Carrega as configurações apropriadas (Desenvolvimento ou Produção).
    3. Inicializa as extensões, como o SQLAlchemy.
    4. Registra os Blueprints que contêm as rotas.
    5. Define rotas principais, se houver.
    
    Returns:
        Flask: A instância da aplicação configurada e pronta para ser executada.
    """
    # 1. Criação da Instância da Aplicação
    #    'instance_relative_config=True' permite carregar arquivos da pasta 'instance'.
    app = Flask(__name__, instance_relative_config=True)

    # 2. Carregamento das Configurações
    #    Determina qual classe de configuração usar com base na variável de
    #    ambiente FLASK_ENV. O padrão é 'development'.
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 3. Inicialização de Extensões
    #    Vincula a instância do SQLAlchemy à aplicação Flask.
    db.init_app(app)

    # 4. Registro de Blueprints
    #    O 'app_context' é necessário para que as importações que dependem
    #    do 'app' funcionem corretamente.
    with app.app_context():
        # Importa o Blueprint que contém as rotas de 'pessoas'.
        from instance.routes.pessoa_routes import pessoa_bp
        
        # Registra o Blueprint, tornando todas as suas rotas acessíveis.
        app.register_blueprint(pessoa_bp)

    # 5. Definição de Rotas Globais
    @app.route("/")
    def home():
        """
        Rota principal (homepage) da aplicação.
        
        Redireciona o usuário diretamente para a página de listagem de pessoas,
        que é a funcionalidade central do sistema.
        """
        return redirect(url_for('pessoa_bp.listar'))

    # Retorna a instância da aplicação pronta.
    return app