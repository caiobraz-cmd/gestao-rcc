"""Autenticação de operador configurado localmente, sem senha padrão."""
from functools import wraps
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

def login_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if not session.get('usuario_id'):
            flash('Por favor, faça login para acessar o sistema.', 'warning')
            return redirect(url_for('auth_bp.login'))
        return function(*args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('usuario_id'):
        return redirect(url_for('pessoa_bp.listar'))
    if request.method == 'POST':
        password_ok = check_password_hash(current_app.config['ADMIN_PASSWORD_HASH'], request.form.get('password', ''))
        if password_ok and request.form.get('username', '').strip() == current_app.config['ADMIN_USERNAME']:
            session.clear()
            session.permanent = True
            session['usuario_id'] = 1
            session['usuario_nome'] = current_app.config['ADMIN_USERNAME']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('pessoa_bp.listar'))
        flash('Usuário ou senha inválidos.', 'danger')
        return render_template('login.html', titulo='Acesso ao Sistema'), 401
    return render_template('login.html', titulo='Acesso ao Sistema')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth_bp.login'))
