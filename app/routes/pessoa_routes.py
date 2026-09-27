"""Fluxos de pacientes e serviços usando somente Oracle ORDS."""
from datetime import date, datetime, timedelta, timezone
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from app import ords
from app.routes.auth_routes import login_required
from app.validation import PATIENT_FIELDS, patient

pessoa_bp = Blueprint('pessoa_bp', __name__)

def baskets_enabled():
    return current_app.config['ORDS_CESTAS_HABILITADAS']

def item(identifier):
    data = ords.call('GET', f'pessoas/{identifier}')
    if 'items' in data:
        rows = data['items']
        if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
            raise ords.APIError('Paciente não encontrado ou resposta da API inválida.', 404)
        data = rows[0]
    if str(data.get('seq_id')) != str(identifier):
        raise ords.APIError('A API não retornou o paciente solicitado.')
    for field in ('dt_nascimento', 'data_obito', 'dt_ultima_cesta'):
        if data.get(field):
            data[field] = str(data[field])[:10]
    return data

def api_error(error):
    flash(str(error), 'danger')
    return render_template('erro.html', titulo='Operação não concluída', mensagem=str(error)), (404 if error.status == 404 else 503)

def duplicate(cpf, exclude=None):
    # Verificação defensiva em toda a coleção: API customizada pode ignorar q.
    for row in ords.collection('pessoas/'):
        value = ''.join(c for c in str(row.get('num_cpf') or '') if c.isdigit())
        if value == cpf and str(row.get('seq_id')) != str(exclude):
            return True
    return False


def verify_saved(saved, expected):
    """HTTP 2xx sozinho não comprova que o handler gravou os campos."""
    for key, value in expected.items():
        actual = saved.get(key)
        if key == 'dt_nascimento' and actual:
            actual = str(actual)[:10]
        if key == 'num_cpf':
            actual = ''.join(c for c in str(actual or '') if c.isdigit())
        if str(actual or '') != str(value or ''):
            raise ords.APIError('Não foi possível confirmar todos os dados salvos. Consulte o cadastro antes de repetir a operação.')

@pessoa_bp.route('/')
@login_required
def listar():
    try:
        people = ords.collection('pessoas/')
    except ords.APIError as error:
        return api_error(error)
    query = request.args.get('q', '').strip()
    if query:
        digits = ''.join(c for c in query if c.isdigit())
        people = [p for p in people if query.casefold() in str(p.get('ds_nome', '')).casefold()
                  or (digits and digits in ''.join(c for c in str(p.get('num_cpf', '')) if c.isdigit()))]
    late = []
    if baskets_enabled():
        for person in people:
            try:
                frequency = int(person.get('num_frequencia_cesta') or 0)
                if frequency > 0 and person.get('dt_ultima_cesta') and not person.get('data_obito'):
                    due = date.fromisoformat(str(person['dt_ultima_cesta'])[:10]) + timedelta(days=frequency)
                    person['proxima_cesta'] = due.isoformat()
                    if due < date.today():
                        person['dias_atraso'] = (date.today() - due).days
                        late.append(person)
            except (ValueError, TypeError, OverflowError):
                flash('Um cadastro possui dados de cesta inválidos. Revise a frequência e a data.', 'warning')
    return render_template('listar.html', pessoas=people, pacientes_atrasados=late, titulo='Pacientes', busca=query)

@pessoa_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    status = 200
    if request.method == 'POST':
        data, errors = patient(request.form, baskets_enabled())
        if not errors:
            try:
                if duplicate(data['num_cpf']):
                    errors.append('Já existe um paciente com este CPF.')
                else:
                    ords.call('POST', 'pessoas/', payload=data)
                    saved = [row for row in ords.collection('pessoas/')
                             if ''.join(c for c in str(row.get('num_cpf') or '') if c.isdigit()) == data['num_cpf']]
                    if len(saved) != 1 or not saved[0].get('seq_id'):
                        raise ords.APIError('O Oracle recebeu o cadastro, mas a leitura de confirmação falhou. Consulte a listagem antes de repetir.')
                    verify_saved(saved[0], data)
                    flash('Paciente cadastrado e confirmado no Oracle.', 'success')
                    return redirect(url_for('pessoa_bp.detalhes', id=saved[0]['seq_id']))
            except ords.APIError as error:
                flash(str(error), 'danger')
                status = 503
        if errors:
            for error in errors:
                flash(error, 'danger')
            status = 422
    return render_template('novo.html', titulo='Novo Paciente', valores=request.form), status

@pessoa_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    try:
        person = item(id)
    except ords.APIError as error:
        return api_error(error)
    status = 200
    if request.method == 'POST':
        data, errors = patient(request.form, baskets_enabled(), editing=True)
        if not errors:
            try:
                if duplicate(data['num_cpf'], exclude=id):
                    errors.append('Já existe outro paciente com este CPF.')
                else:
                    if baskets_enabled():
                        data['dt_ultima_cesta'] = person.get('dt_ultima_cesta')
                    ords.call('PUT', f'pessoas/{id}', payload=data)
                    verify_saved(item(id), data)
                    flash('Paciente atualizado e confirmado no Oracle.', 'success')
                    return redirect(url_for('pessoa_bp.detalhes', id=id))
            except ords.APIError as error:
                flash(str(error), 'danger')
                status = 503
        if errors:
            for error in errors:
                flash(error, 'danger')
            status = 422
        person.update({key: request.form.get(key, '') for key in PATIENT_FIELDS + ('status',)})
        person['num_frequencia_cesta'] = request.form.get('frequencia_cesta', '')
    return render_template('editar.html', pessoa=person, titulo='Editar Paciente'), status

@pessoa_bp.route('/deletar/<int:id>', methods=['POST'])
@login_required
def deletar(id):
    try:
        item(id)
        if not current_app.config['ORDS_SERVICOS_HABILITADOS']:
            flash('Exclusão indisponível até validar o histórico de serviços. Use a situação Inativo para preservar o cadastro.', 'warning')
            return redirect(url_for('pessoa_bp.editar', id=id))
        services = ords.collection('servicos/', {'pessoa_id': id})
        if any(str(s.get('sq_idpaciente')) == str(id) for s in services):
            flash('Não é possível excluir um paciente com serviços registrados. Preserve seu histórico.', 'warning')
            return redirect(url_for('pessoa_bp.detalhes', id=id))
        ords.call('DELETE', f'pessoas/{id}')
        flash('Paciente removido com sucesso.', 'success')
        return redirect(url_for('pessoa_bp.listar'))
    except ords.APIError as error:
        return api_error(error)

@pessoa_bp.route('/pessoa/<int:id>/')
@login_required
def detalhes(id):
    try:
        person = item(id)
        services = ords.collection('servicos/', {'pessoa_id': id}) if current_app.config['ORDS_SERVICOS_HABILITADOS'] else []
        services = [s for s in services if str(s.get('sq_idpaciente')) == str(id)]
    except ords.APIError as error:
        return api_error(error)
    return render_template('detalhes.html', pessoa=person, servicos=services, titulo='Detalhes do paciente')

@pessoa_bp.route('/pessoa/<int:id>/servicos/novo', methods=['GET', 'POST'])
@login_required
def novo_servico(id):
    if not current_app.config['ORDS_SERVICOS_HABILITADOS']:
        return render_template('erro.html', titulo='Serviços ainda não habilitados',
                               mensagem='O registro de serviços aguarda a configuração da API Oracle.'), 409
    try:
        person = item(id)
    except ords.APIError as error:
        return api_error(error)
    status = 200
    if request.method == 'POST':
        name = request.form.get('ds_nome', '').strip()
        description = request.form.get('char_descricao', '').strip()
        if not 3 <= len(name) or len(name.encode('utf-8')) > 100 or len(description.encode('utf-8')) > 255:
            flash('Informe um serviço de pelo menos 3 caracteres, até 100 bytes, e descrição de até 255 bytes.', 'danger')
            status = 422
        else:
            try:
                ords.call('POST', 'servicos/', payload={'ds_nome': name, 'char_descricao': description or None,
                          'dt_dataservico': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'sq_idpaciente': id})
                flash('Serviço registrado. Confira o histórico do paciente.', 'success')
                return redirect(url_for('pessoa_bp.detalhes', id=id))
            except ords.APIError as error:
                flash(str(error), 'danger')
                status = 503
    return render_template('novo_servico.html', pessoa=person, titulo='Registrar Serviço'), status

@pessoa_bp.route('/renovar_cesta/<int:id>', methods=['POST'])
@login_required
def renovar_cesta(id):
    if not baskets_enabled():
        return render_template('erro.html', titulo='Recurso ainda não habilitado',
                               mensagem='O registro de cestas aguarda validação da integração com o Oracle.'), 409
    try:
        person = item(id)
        frequency = person.get('num_frequencia_cesta')
        if person.get('data_obito') or not frequency or not 1 <= int(frequency) <= 365:
            flash('Revise a situação do paciente e a frequência da cesta antes de registrar entrega.', 'warning')
            return redirect(url_for('pessoa_bp.detalhes', id=id))
        today = date.today().isoformat()
        if person.get('dt_ultima_cesta') == today:
            flash('A entrega de hoje já foi registrada.', 'info')
            return redirect(url_for('pessoa_bp.detalhes', id=id))
        payload = {key: person.get(key) for key in PATIENT_FIELDS + ('data_obito', 'num_frequencia_cesta')}
        payload['dt_ultima_cesta'] = today
        ords.call('PUT', f'pessoas/{id}', payload=payload)
        if item(id).get('dt_ultima_cesta') != today:
            raise ords.APIError('A API respondeu, mas a data da cesta não foi persistida. Avise o responsável.')
        flash('Entrega da cesta registrada e confirmada no Oracle.', 'success')
        return redirect(url_for('pessoa_bp.detalhes', id=id))
    except (ValueError, TypeError):
        flash('A frequência cadastrada é inválida.', 'danger')
        return redirect(url_for('pessoa_bp.detalhes', id=id))
    except ords.APIError as error:
        return api_error(error)
