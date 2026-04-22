# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__, template_folder='../../templates')

# --- NOSSO BANCO DE DADOS FICTÍCIO ---
# Aqui simulamos o que viria da API Oracle. 
# Veja como a senha "senha123" foi transformada em um Hash seguro.
MOCK_DATABASE = {
    "admin": {
        "id": 1,
        "nome": "Administrador",
        "senha_hash": generate_password_hash("senha123")
    }
}

# --- DECORADOR PARA PROTEGER AS ROTAS ---
def login_required(f):
    """
    Coloque @login_required acima de qualquer rota que precise de proteção.
    Ele verifica se existe um usuário na sessão atual.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar o sistema.', 'warning')
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROTAS ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, manda para a página inicial
    if 'usuario_id' in session:
        return redirect(url_for('pessoa_bp.listar'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario_db = MOCK_DATABASE.get(username)

        # APRENDIZADO DE CRIPTOGRAFIA:
        # check_password_hash pega a senha que o cara digitou, criptografa, 
        # e compara com o hash que está salvo.
        if usuario_db and check_password_hash(usuario_db['senha_hash'], password):
            # Login com sucesso! Guardamos os dados na sessão (Cookies)
            session['usuario_id'] = usuario_db['id']
            session['usuario_nome'] = usuario_db['nome']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('pessoa_bp.listar'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html', titulo="Login")

@auth_bp.route('/logout')
def logout():
    # Remove os dados da sessão
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth_bp.login'))