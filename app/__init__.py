"""Fábrica da aplicação e proteção dos formulários."""
import os
import secrets
from pathlib import Path
from urllib.parse import urlsplit
from flask import Flask, render_template, request, session

def create_app(test_config=None):
    from config import DevelopmentConfig, ProductionConfig
    root = Path(__file__).resolve().parent.parent
    app = Flask(__name__, template_folder=str(root / 'templates'), static_folder=str(root / 'static'))
    app.config.from_object(ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else DevelopmentConfig)
    if test_config:
        app.config.update(test_config)
    missing = [key for key in ('SECRET_KEY', 'API_BASE_URL', 'ADMIN_USERNAME', 'ADMIN_PASSWORD_HASH') if not app.config.get(key)]
    if missing:
        raise RuntimeError('Configure ' + ', '.join(missing) + '. Execute python configurar.py; consulte o README.')
    address = urlsplit(app.config['API_BASE_URL'])
    if address.scheme not in ('http', 'https') or not address.hostname or address.query or address.fragment or address.username:
        raise RuntimeError('API_BASE_URL deve ser a URL base HTTP(S) do ORDS, sem usuário, consulta ou fragmento.')
    app.config['API_BASE_URL'] = app.config['API_BASE_URL'].rstrip('/') + '/'
    if len(app.config['SECRET_KEY']) < 32:
        raise RuntimeError('SECRET_KEY deve ter pelo menos 32 caracteres aleatórios.')
    if app.config['SESSION_COOKIE_SECURE'] and address.scheme != 'https':
        raise RuntimeError('Produção requer API_BASE_URL com HTTPS.')

    def csrf_token():
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_urlsafe(32)
        return session['_csrf_token']
    app.jinja_env.globals['csrf_token'] = csrf_token

    @app.before_request
    def protect_forms():
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            expected = session.get('_csrf_token', '')
            supplied = request.form.get('csrf_token', '')
            if not expected or not secrets.compare_digest(expected.encode('utf-8'), supplied.encode('utf-8')):
                return render_template('erro.html', titulo='Formulário expirado',
                    mensagem='O formulário expirou ou é inválido. Volte à página e tente novamente.'), 400

    from app.routes.auth_routes import auth_bp
    from app.routes.pessoa_routes import pessoa_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(pessoa_bp)

    @app.route('/ping')
    def ping():
        return {'status': 'ok', 'version': app.config['APP_VERSION']}

    @app.after_request
    def response_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        if request.endpoint != 'static':
            response.headers['Cache-Control'] = 'no-store'
        return response
    return app
