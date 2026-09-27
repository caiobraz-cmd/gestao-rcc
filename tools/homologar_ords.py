"""Valida o fluxo Flask com Oracle real; cria um registro fictício e o deixa INATIVO."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from werkzeug.security import generate_password_hash
from app import create_app, ords


def fictional_cpf():
    digits = [secrets.randbelow(10) for _ in range(9)]
    for length in (9, 10):
        digits.append((sum(digits[i] * (length + 1 - i) for i in range(length)) * 10 % 11) % 10)
    return ''.join(map(str, digits))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True, help='URL base do módulo, sem pessoas/')
    parser.add_argument('--confirmar-dados-ficticios', action='store_true')
    args = parser.parse_args()
    if not args.confirmar_dados_ficticios:
        parser.error('Use somente em base de teste autorizada e informe --confirmar-dados-ficticios.')
    password = secrets.token_urlsafe(24)
    app = create_app({'TESTING': True, 'SECRET_KEY': secrets.token_hex(32),
                      'ADMIN_USERNAME': 'verificacao-temporaria', 'ADMIN_PASSWORD_HASH': generate_password_hash(password),
                      'API_BASE_URL': args.url, 'SESSION_COOKIE_SECURE': False,
                      'ORDS_SERVICOS_HABILITADOS': False, 'ORDS_CESTAS_HABILITADAS': False})
    client = app.test_client()
    report = {'versao': app.config['APP_VERSION'], 'inicio_utc': datetime.now(timezone.utc).isoformat(),
              'tipo': 'Fluxos Flask com chamadas reais ao Oracle ORDS, sem simulação', 'etapas': [], 'concluido': False}
    identifier = None

    def check(name, condition):
        report['etapas'].append({'etapa': name, 'resultado': 'OK' if condition else 'FALHOU'})
        print(f'{name}: {"OK" if condition else "FALHOU"}', flush=True)
        if not condition:
            raise RuntimeError('Validação interrompida: ' + name)

    def csrf():
        client.get('/auth/login')
        with client.session_transaction() as session:
            return session['_csrf_token']

    def login():
        return client.post('/auth/login', data={'username': 'verificacao-temporaria', 'password': password, 'csrf_token': csrf()})

    try:
        check('Login do operador', login().status_code == 302)
        check('Listagem real', client.get('/').status_code == 200)
        marker = 'TESTE ENTREGA ' + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S') + ' ' + secrets.token_hex(2)
        data = {'ds_nome': marker, 'num_cpf': fictional_cpf(), 'dt_nascimento': '1990-01-01',
                'num_telefone': '', 'char_endereco': 'Endereco ficticio para teste', 'status': 'ATIVO', 'csrf_token': csrf()}
        with app.app_context():
            before = len(ords.collection('pessoas/'))
        invalid = client.post('/novo', data={**data, 'num_cpf': '11111111111'})
        with app.app_context():
            after = len(ords.collection('pessoas/'))
        check('CPF inválido rejeitado sem novo registro', invalid.status_code == 422 and before == after)
        result = client.post('/novo', data=data)
        check('Cadastro confirmado por nova consulta', result.status_code == 302 and '/pessoa/' in result.location)
        identifier = int(result.location.strip('/').split('/')[-1])
        report['registro_teste_id'] = identifier
        report['registro_teste_nome'] = marker
        check('Detalhes do registro real', client.get(result.location).status_code == 200)
        data['char_endereco'] = 'Endereco ficticio alterado no teste'
        check('Edição confirmada por nova consulta', client.post(f'/editar/{identifier}', data=data).status_code == 302)
        data['status'] = 'INATIVO'
        check('Inativação confirmada por nova consulta', client.post(f'/editar/{identifier}', data=data).status_code == 302)
        check('Saída do sistema', client.post('/auth/logout', data={'csrf_token': csrf()}).status_code == 302)
        check('Proteção após saída', client.get('/').status_code == 302)
        check('Nova sessão', login().status_code == 302)
        with app.app_context():
            from app.routes.pessoa_routes import item, verify_saved
            saved = item(identifier)
            verify_saved(saved, {k: v for k, v in data.items() if k != 'csrf_token'})
        check('Persistência após nova sessão', True)
        report['concluido'] = True
    except (RuntimeError, ords.APIError) as error:
        report['erro'] = str(error)
        print(str(error))
        print('Consulte a listagem antes de repetir; uma gravação pode ter sido recebida pelo Oracle.')
    finally:
        report['fim_utc'] = datetime.now(timezone.utc).isoformat()
        report['observacao'] = 'Não comprova apresentação ao cliente. Registro criado permanece identificado como TESTE; não há exclusão automática.'
        folder = ROOT / 'docs' / 'evidences' / 'produto'
        folder.mkdir(parents=True, exist_ok=True)
        output = folder / ('oracle-real-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.json')
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print('Relatório: ' + str(output))
    return 0 if report['concluido'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
