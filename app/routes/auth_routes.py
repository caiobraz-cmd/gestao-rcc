"""Login da equipe e autorização das áreas internas."""
from functools import wraps
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import contas, ords
from app.access_limits import check_attempts

auth_bp = Blueprint('auth_bp', __name__)

def is_admin():
    return (session.get('perfil') == 'admin' and session.get('usuario_id') == 'admin'
            and session.get('usuario_nome') == current_app.config['ADMIN_USERNAME'])

def unavailable():
    return render_template('erro.html', titulo='Acesso indisponível',
                           mensagem='Não foi possível verificar as contas no Oracle. Tente novamente.'), 503

def limited(seconds):
    return render_template('erro.html', titulo='Aguarde para tentar novamente',
        mensagem='Muitas tentativas em pouco tempo. Aguarde alguns minutos antes de tentar novamente.'), 429, {'Retry-After': str(seconds)}

def login_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if is_admin():
            return function(*args, **kwargs)
        if session.get('perfil') == 'operador':
            try:
                row = contas.lookup(session.get('usuario_nome', ''))
            except ords.APIError:
                return unavailable()
            if (row and row['ativo'] == 1 and row['versao'] == session.get('versao')
                    and row['login'] == session.get('usuario_id')):
                return function(*args, **kwargs)
        session.clear()
        flash('Entre para acessar o sistema.', 'warning')
        return redirect(url_for('auth_bp.login'))
    return decorated

def admin_required(function):
    @login_required
    @wraps(function)
    def decorated(*args, **kwargs):
        if not is_admin():
            return render_template('erro.html', titulo='Acesso restrito',
                                   mensagem='Esta área é exclusiva do administrador.'), 403
        return function(*args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        if len(username) > 128:
            username = '__login_invalido__'
        delay = check_attempts('login', username)
        if delay:
            return limited(delay)
        password = request.form.get('password', '')
        admin = current_app.config['ADMIN_USERNAME']
        row = None
        if username != admin.lower() and contas.LOGIN.fullmatch(username):
            try:
                row = contas.lookup(username, credentials=True)
            except ords.APIError:
                return unavailable()
        # A conta ausente também passa por uma verificação de hash.
        good = check_password_hash(row['senha_hash'] if row else current_app.config['ADMIN_PASSWORD_HASH'], password)
        bootstrap = username == admin.lower()
        if good and (bootstrap or (row and row['ativo'] == 1)):
            session.clear()
            session.permanent = True
            session.update(usuario_id='admin' if bootstrap else username, usuario_nome=admin if bootstrap else username,
                           perfil='admin' if bootstrap else 'operador', versao=0 if bootstrap else row['versao'])
            return redirect(url_for('pessoa_bp.listar'))
        flash('Usuário ou senha inválidos.', 'danger')
        return render_template('login.html', titulo='Acesso ao Sistema'), 401
    return render_template('login.html', titulo='Acesso ao Sistema')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/senha', methods=['GET', 'POST'])
@login_required
def senha():
    if is_admin():
        return render_template('erro.html', titulo='Conta administrativa',
            mensagem='Esta opção atende às contas de operadores. A conta administrativa desta instalação é gerenciada pelo responsável técnico.'), 403
    status = 200
    if request.method == 'POST':
        delay = check_attempts('senha', session['usuario_nome'])
        if delay:
            return limited(delay)
        atual = request.form.get('senha_atual', '')
        nova = request.form.get('nova_senha', '')
        confirma = request.form.get('confirmacao', '')
        if not 12 <= len(nova) <= 128 or nova != confirma or nova == atual:
            flash('Use uma nova senha de 12 a 128 caracteres, diferente da atual, e repita-a na confirmação.', 'danger')
            status = 422
        else:
            login_name = session['usuario_nome']
            try:
                row = contas.lookup(login_name, credentials=True)
                if not row or row['ativo'] != 1 or row['versao'] != session['versao']:
                    session.clear()
                    return redirect(url_for('auth_bp.login'))
                if not check_password_hash(row['senha_hash'], atual):
                    flash('A senha atual está incorreta.', 'danger')
                    status = 422
                else:
                    ords.call('PUT', f'contas/{login_name}/', payload={
                        'acao': 'senha', 'senha_hash': generate_password_hash(nova)})
                    saved = contas.lookup(login_name, credentials=True)
                    if not saved or saved['versao'] <= row['versao'] or not check_password_hash(saved['senha_hash'], nova):
                        raise ords.APIError('Não foi possível confirmar a alteração.')
                    session.clear()
                    flash('Senha atualizada. Entre novamente com a nova senha.', 'success')
                    return redirect(url_for('auth_bp.login'))
            except ords.APIError:
                flash('Não foi possível confirmar a troca. Tente entrar com a nova senha antes de repetir a operação.', 'danger')
                status = 503
    return render_template('minha_senha.html', titulo='Minha senha'), status
