"""Homologação real da 0.5. Cria um cadastro TESTE, conserva histórico e o inativa."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import httpx
from werkzeug.security import generate_password_hash
from app import create_app, ords
from app.cestas import agenda, hoje
from app.routes.pessoa_routes import item
from tools.homologar_ords import fictional_cpf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirmar-dados-ficticios', action='store_true')
    args = parser.parse_args()
    if not args.confirmar_dados_ficticios:
        parser.error('Confirme a base de testes com --confirmar-dados-ficticios.')
    password = secrets.token_urlsafe(24)
    config = {'TESTING': True, 'SECRET_KEY': secrets.token_hex(32), 'ADMIN_USERNAME': 'homologacao',
              'ADMIN_PASSWORD_HASH': generate_password_hash(password), 'SESSION_COOKIE_SECURE': False,
              'ORDS_DADOS_MEDICOS_HABILITADOS': True, 'ORDS_CESTAS_HABILITADAS': True,
              'ORDS_SERVICOS_HABILITADOS': False}
    app = create_app(config)
    if not app.config['API_BASE_URL'].endswith('/rcc-v2/'):
        raise SystemExit('Configure a API /rcc-v2/ no .env antes de homologar.')
    client = app.test_client()
    report = {'versao': app.config['APP_VERSION'], 'inicio_utc': datetime.now(timezone.utc).isoformat(),
              'tipo': 'Flask e API Oracle reais, sem simulacao', 'etapas': [], 'concluido': False}
    identifier = None

    def check(name, condition):
        report['etapas'].append({'etapa': name, 'resultado': 'OK' if condition else 'FALHOU'})
        print(name + ': ' + ('OK' if condition else 'FALHOU'), flush=True)
        if not condition:
            raise RuntimeError('Verificacao interrompida: ' + name)

    def csrf():
        client.get('/auth/login')
        with client.session_transaction() as session:
            return session['_csrf_token']

    def remote_delivery():
        with app.app_context():
            try:
                ords.call('POST', f'cestas/{identifier}/', payload={'data_entrega': hoje().isoformat()})
                return 201
            except ords.APIError as error:
                return error.status

    try:
        with httpx.Client(http2=True, timeout=25, follow_redirects=False,
                          headers={'User-Agent': 'GestaoRCC/' + app.config['APP_VERSION']}) as public:
            for method, path in [('GET', 'pessoas/'), ('POST', 'pessoas/'), ('POST', 'cestas/1/')]:
                response = public.request(method, app.config['API_BASE_URL'] + path)
                check('API sem token recusa ' + method + ' ' + path, response.status_code in (401, 403))
        check('Login do operador', client.post('/auth/login', data={'username': 'homologacao',
              'password': password, 'csrf_token': csrf()}).status_code == 302)
        check('Listagem autenticada', client.get('/').status_code == 200)
        data = {'ds_nome': 'TESTE CESTAS ' + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S'),
                'num_cpf': fictional_cpf(), 'dt_nascimento': '1990-01-01', 'status': 'ATIVO',
                'num_telefone': '', 'char_endereco': 'Endereco ficticio', 'frequencia_cesta': '7',
                'data_obito': '', 'char_diagnostico': 'Diagnostico ficticio de homologacao',
                'char_tratamento': 'Tratamento ficticio', 'char_medicamento': 'Medicamento ficticio',
                'char_alergia': 'Alergia ficticia', 'char_observacoes': 'Somente teste autorizado', 'csrf_token': csrf()}
        with app.app_context():
            before = len(ords.collection('pessoas/'))
        for changes in [{'frequencia_cesta': '366'}, {'data_obito': '1980-01-01'}, {'char_alergia': 'a' * 2001}]:
            check('Formulario invalido rejeitado: ' + next(iter(changes)),
                  client.post('/novo', data={**data, **changes}).status_code == 422)
        with app.app_context():
            check('Invalidos nao criaram cadastros', len(ords.collection('pessoas/')) == before)
        response = client.post('/novo', data=data)
        check('Cadastro completo confirmado', response.status_code == 302 and '/pessoa/' in (response.location or ''))
        identifier = int(response.location.strip('/').split('/')[-1])
        report['registro_teste_id'] = identifier
        check('Detalhes com campos clinicos', data['char_diagnostico'] in client.get(response.location).get_data(as_text=True))
        with app.app_context():
            check('Primeira entrega pendente', agenda(item(identifier))['situacao'] == 'Primeira entrega pendente')
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: remote_delivery(), range(2)))
        report['http_entregas_concorrentes'] = results
        check('Duas entregas concorrentes: uma aceita, outra recusada', sorted(results) == [201, 409])
        with app.app_context():
            history = ords.collection(f'cestas/{identifier}/')
            check('Apenas uma entrega persistida no historico', len(history) == 1 and history[0]['data_entrega'] == hoje().isoformat())
            check('Ultima entrega calculada pelo historico', item(identifier)['dt_ultima_cesta'] == hoje().isoformat())
        response = client.post(f'/renovar_cesta/{identifier}', data={'csrf_token': csrf()})
        check('Repeticao pela interface bloqueada', response.status_code == 302)
        data.update({'char_diagnostico': 'Diagnostico ficticio alterado', 'char_alergia': '', 'frequencia_cesta': '15'})
        check('Edicao e limpeza de campo confirmadas', client.post(f'/editar/{identifier}', data=data).status_code == 302)
        with app.app_context():
            saved = item(identifier)
            history = ords.collection(f'cestas/{identifier}/')
            check('Edicao preservou historico e frequencia da entrega', len(history) == 1 and history[0]['frequencia_dias'] == 7 and saved['num_frequencia_cesta'] == 15)
        data['data_obito'] = hoje().isoformat()
        check('Obito registrado e cadastro inativado', client.post(f'/editar/{identifier}', data=data).status_code == 302)
        check('Oracle impede entrega para inativo', remote_delivery() == 409)
        fresh = create_app(config)
        with fresh.app_context():
            saved = item(identifier)
            check('Persistencia em nova instancia autenticada', saved['status'] == 'INATIVO' and saved['data_obito'] == hoje().isoformat()
                  and saved['char_diagnostico'] == data['char_diagnostico'] and not saved.get('char_alergia'))
        check('Logout', client.post('/auth/logout', data={'csrf_token': csrf()}).status_code == 302)
        check('Rotas protegidas apos logout', client.get('/').status_code == 302)
        report['concluido'] = True
    except (RuntimeError, ords.APIError, httpx.HTTPError) as error:
        report['erro'] = str(error) if not isinstance(error, httpx.HTTPError) else type(error).__name__
        print(report['erro'], flush=True)
    finally:
        report['fim_utc'] = datetime.now(timezone.utc).isoformat()
        report['observacao'] = 'Dados ficticios; sem exclusao. Nao comprova demonstracao ou aceite do cliente.'
        folder = ROOT / 'docs/evidences/v05-oracle'
        folder.mkdir(parents=True, exist_ok=True)
        output = folder / ('homologacao-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.json')
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print('Relatorio: ' + str(output), flush=True)
    return 0 if report['concluido'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
