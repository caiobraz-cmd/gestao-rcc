from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import contas, ords
from app.routes.auth_routes import admin_required

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.get('/rastreabilidade')
@admin_required
def rastreabilidade():
    tipos = {'cadastro':'Cadastro de paciente','alteracao':'Alteração de paciente',
             'entrega':'Entrega de cesta','servico':'Registro de serviço'}
    tipo = request.args.get('tipo','')
    if tipo not in tipos:
        tipo = ''
    busca = request.args.get('q','').strip()[:120]
    try:
        pagina = min(100000, max(1,int(request.args.get('pagina','1'))))
    except ValueError:
        pagina = 1
    try:
        contas.validate_api()
        data = ords.call('GET','registros-operacoes/',params={
            'tipo':tipo or None,'busca':busca or None,'limit':25,'offset':(pagina-1)*25})
        if not isinstance(data.get('items'),list):
            raise ords.APIError('Lista inválida.')
    except ords.APIError:
        return render_template('erro.html',titulo='Registros indisponíveis',
            mensagem='Não foi possível consultar a rastreabilidade no Oracle.'),503
    return render_template('rastreabilidade.html',titulo='Rastreabilidade',tipos=tipos,tipo=tipo,
        busca=busca,pagina=pagina,mais=bool(data.get('hasMore')),registros=data['items'])

@admin_bp.get('/registros-servicos')
@admin_required
def registros_servicos():
    query = request.args.get('q', '').strip()[:120]
    try:
        page = max(1, int(request.args.get('pagina', '1')))
    except ValueError:
        page = 1
    try:
        contas.validate_api()
        data = ords.call('GET', 'registros-servicos/', params={'busca':query or None, 'limit':25, 'offset':(page-1)*25})
        if not isinstance(data.get('items'), list):
            raise ords.APIError('Lista inválida.')
    except ords.APIError:
        return render_template('erro.html', titulo='Registros indisponíveis',
            mensagem='Não foi possível consultar os registros de serviços no Oracle.'), 503
    return render_template('registros_servicos.html', titulo='Registros de serviços',
                           registros=data['items'], busca=query, pagina=page, mais=bool(data.get('hasMore')))

def panel(error=None, status=200):
    try:
        rows = contas.accounts()
    except ords.APIError:
        return render_template('erro.html', titulo='Contas indisponíveis',
            mensagem='Não foi possível carregar as contas. Verifique a integração do painel com o Oracle.'), 503
    if error:
        flash(error, 'danger')
    return render_template('admin.html', titulo='Administração', contas=rows), status

@admin_bp.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    if request.method == 'GET':
        return panel()
    login = request.form.get('login','').strip().lower()
    nome = request.form.get('nome','').strip()
    senha = request.form.get('senha','')
    if not contas.LOGIN.fullmatch(login) or login == current_app.config['ADMIN_USERNAME'].lower():
        return panel('Escolha outro login: use de 3 a 40 letras sem acento, números, ponto, hífen ou sublinhado.', 422)
    if not 2 <= len(nome) or len(nome.encode()) > 120 or not 12 <= len(senha) <= 128:
        return panel('Informe um nome válido (até 120 bytes) e uma senha de 12 a 128 caracteres.', 422)
    try:
        contas.validate_api()
        ords.call('POST', 'contas/', payload={'login':login,'nome':nome,'senha_hash':generate_password_hash(senha)})
        saved = contas.lookup(login, credentials=True)
        if not saved or saved['ativo'] != 1 or not check_password_hash(saved['senha_hash'], senha):
            raise ords.APIError('Cadastro não confirmado.')
    except ords.APIError as exc:
        if exc.status == 409:
            return panel('Esse login já está em uso.', 409)
        return panel('Não foi possível confirmar o cadastro. Confira a lista antes de tentar novamente.', 503)
    flash('Conta criada. A pessoa já pode entrar pelo navegador.', 'success')
    return redirect(url_for('admin_bp.index'))

@admin_bp.post('/<login>/acesso')
@admin_required
def acesso(login):
    acao = request.form.get('acao')
    if (not contas.LOGIN.fullmatch(login) or login == current_app.config['ADMIN_USERNAME'].lower()
            or acao not in ('ativar','desativar','senha')):
        return panel('Operação inválida.', 422)
    payload = {'acao': acao}
    if acao == 'senha':
        senha = request.form.get('senha','')
        if not 12 <= len(senha) <= 128:
            return panel('A nova senha deve ter de 12 a 128 caracteres.', 422)
        payload['senha_hash'] = generate_password_hash(senha)
    try:
        contas.validate_api()
        before = contas.lookup(login)
        if not before:
            return panel('Conta não encontrada.', 404)
        ords.call('PUT', f'contas/{login}/', payload=payload)
        saved = contas.lookup(login, credentials=acao == 'senha')
        if not saved or saved['versao'] <= before['versao']:
            raise ords.APIError('Alteração não confirmada.')
        if acao == 'senha':
            if not check_password_hash(saved['senha_hash'], senha):
                raise ords.APIError('Senha não confirmada.')
        elif saved['ativo'] != (1 if acao == 'ativar' else 0):
            raise ords.APIError('Situação não confirmada.')
    except ords.APIError:
        return panel('Não foi possível confirmar a alteração. Confira a conta antes de repetir.', 503)
    flash('Acesso atualizado para ' + login + '.', 'success')
    return redirect(url_for('admin_bp.index'))
