"""Testes locais com API simulada; não equivalem à homologação no Oracle."""
import unittest
from unittest.mock import patch
import httpx
from werkzeug.security import generate_password_hash
from app import create_app
from app.ords import APIError


class ProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = {'TESTING': True, 'SECRET_KEY': 'test-' * 10,
                      'API_BASE_URL': 'https://example.invalid/ords/test/rcc/',
                      'ADMIN_USERNAME': 'operador', 'ADMIN_PASSWORD_HASH': generate_password_hash('senha-de-teste'),
                      'ORDS_CESTAS_HABILITADAS': False, 'ORDS_DADOS_MEDICOS_HABILITADOS': False,
                      'ORDS_SERVICOS_HABILITADOS': False, 'API_TOKEN': '', 'ORDS_CLIENT_ID': '', 'ORDS_CLIENT_SECRET': ''}

    def setUp(self):
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.person = {'seq_id': 123, 'ds_nome': 'Paciente fictício', 'num_cpf': '52998224725',
                       'dt_nascimento': '1990-01-01', 'status': 'ATIVO', 'num_frequencia_cesta': 30, 'dt_ultima_cesta': '2026-01-01'}

    def token(self):
        with self.client.session_transaction() as session:
            session['_csrf_token'] = 'test-token'
        return 'test-token'

    def login(self):
        return self.client.post('/auth/login', data={'username': 'operador', 'password': 'senha-de-teste', 'csrf_token': self.token()})

    def form(self, **values):
        return {'ds_nome': 'Paciente fictício', 'num_cpf': '529.982.247-25', 'dt_nascimento': '1990-01-01',
                'csrf_token': self.token(), **values}

    def test_login_invalid_valid_and_logout(self):
        self.assertEqual(self.client.get('/auth/login').status_code, 200)
        self.assertEqual(self.client.post('/auth/login', data={'username': 'operador', 'password': 'errada', 'csrf_token': self.token()}).status_code, 401)
        self.assertEqual(self.login().status_code, 302)
        self.assertEqual(self.client.post('/auth/logout', data={'csrf_token': self.token()}).status_code, 302)
        self.assertIn('/auth/login', self.client.get('/').location)

    @patch('app.ords.call')
    def test_all_internal_routes_require_login(self, call):
        for path in ['/', '/novo', '/editar/123', '/pessoa/123/', '/pessoa/123/servicos/novo']:
            with self.subTest(path=path):
                self.assertIn('/auth/login', self.client.get(path).location)
        for path in ['/novo', '/editar/123', '/deletar/123', '/pessoa/123/servicos/novo', '/renovar_cesta/123']:
            self.assertIn('/auth/login', self.client.post(path, data={'csrf_token': self.token()}).location)
        call.assert_not_called()

    @patch('app.ords.call')
    def test_csrf_blocks_post(self, call):
        self.login()
        for invalid_token in ['errado', 'inválido']:
            self.assertEqual(self.client.post('/novo', data=self.form(csrf_token=invalid_token)).status_code, 400)
        call.assert_not_called()

    @patch('app.ords.collection', return_value=[])
    @patch('app.ords.call')
    def test_create_valid_and_reject_invalid(self, call, collection):
        self.login()
        bad = self.client.post('/novo', data=self.form(num_cpf='11111111111'))
        self.assertEqual(bad.status_code, 422)
        self.assertIn('CPF válido', bad.get_data(as_text=True))
        self.assertIn('Paciente fictício', bad.get_data(as_text=True))
        call.assert_not_called()
        collection.side_effect = [[], [self.person]]
        self.assertEqual(self.client.post('/novo', data=self.form()).status_code, 302)
        self.assertEqual(call.call_args.kwargs['payload']['num_cpf'], '52998224725')

    @patch('app.ords.call')
    @patch('app.ords.collection')
    def test_duplicate_not_sent(self, collection, call):
        self.login()
        collection.return_value = [self.person]
        self.assertEqual(self.client.post('/novo', data=self.form()).status_code, 422)
        call.assert_not_called()

    @patch('app.ords.collection', return_value=[])
    @patch('app.ords.call')
    def test_create_does_not_claim_success_when_readback_fails(self, call, collection):
        self.login()
        response = self.client.post('/novo', data=self.form())
        self.assertEqual(response.status_code, 503)
        self.assertIn('leitura de confirmação falhou', response.get_data(as_text=True))

    @patch('app.ords.collection', return_value=[])
    @patch('app.ords.call')
    def test_edit_does_not_claim_success_when_oracle_ignores_change(self, call, collection):
        self.login()
        call.return_value = dict(self.person)
        response = self.client.post('/editar/123', data=self.form(status='INATIVO'))
        self.assertEqual(response.status_code, 503)
        self.assertIn('confirmar todos os dados', response.get_data(as_text=True))

    @patch('app.ords.collection')
    @patch('app.ords.call')
    def test_edit_details_and_service(self, call, collection):
        self.app.config['ORDS_SERVICOS_HABILITADOS'] = True
        self.login()
        call.return_value = dict(self.person)
        collection.return_value = []
        self.assertEqual(self.client.get('/editar/123').status_code, 200)
        self.assertEqual(self.client.post('/editar/123', data=self.form()).status_code, 302)
        self.assertEqual(self.client.get('/pessoa/123/').status_code, 200)
        self.assertEqual(self.client.post('/pessoa/123/servicos/novo', data={'ds_nome': 'a', 'csrf_token': self.token()}).status_code, 422)
        result = self.client.post('/pessoa/123/servicos/novo', data={'ds_nome': 'Atendimento teste', 'csrf_token': self.token()})
        self.assertEqual(result.status_code, 302)
        self.assertEqual(call.call_args.kwargs['payload']['sq_idpaciente'], 123)

    @patch('app.ords.collection')
    @patch('app.ords.call')
    def test_delete_preserves_service_history(self, call, collection):
        self.app.config['ORDS_SERVICOS_HABILITADOS'] = True
        self.login()
        call.return_value = dict(self.person)
        collection.return_value = [{'sq_idpaciente': 123}]
        self.client.post('/deletar/123', data={'csrf_token': self.token()})
        self.assertFalse(any(c.args[0] == 'DELETE' for c in call.call_args_list))
        collection.return_value = []
        self.client.post('/deletar/123', data={'csrf_token': self.token()})
        self.assertEqual(call.call_args.args, ('DELETE', 'pessoas/123'))

    @patch('app.ords.collection', return_value=[])
    @patch('app.ords.call')
    def test_basket_never_claims_success_without_persistence(self, call, collection):
        self.login()
        self.assertEqual(self.client.post('/renovar_cesta/123', data={'csrf_token': self.token()}).status_code, 409)
        call.assert_not_called()
        self.app.config['ORDS_CESTAS_HABILITADAS'] = True
        call.return_value = dict(self.person)
        response = self.client.post('/renovar_cesta/123', data={'csrf_token': self.token()})
        self.assertEqual(response.status_code, 503)
        self.assertIn('não foi persistida', response.get_data(as_text=True))

    @patch('app.ords.httpx.Client.request', side_effect=httpx.ReadTimeout('timeout'))
    def test_api_failure_is_handled_without_traceback(self, request):
        self.app.config['ORDS_SERVICOS_HABILITADOS'] = True
        self.login()
        for path in ['/', '/pessoa/123/', '/pessoa/123/servicos/novo']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 503)
            self.assertNotIn('Traceback', response.get_data(as_text=True))

    def test_configuration_and_version(self):
        with self.assertRaises(RuntimeError):
            create_app({**self.config, 'API_BASE_URL': ''})
        with self.assertRaises(RuntimeError):
            create_app({**self.config, 'SECRET_KEY': 'short'})
        self.assertEqual(self.client.get('/ping').json['version'], '0.5.0-rc1')

    @patch('app.ords.httpx.Client.request')
    def test_real_schema_field_mapping(self, request):
        from app import ords
        request.return_value.status_code = 200
        request.return_value.json.return_value = {'items': [{'id': 1, 'nome': 'TESTE', 'cpf': '52998224725'}]}
        with self.app.app_context():
            self.assertEqual(ords.collection('pessoas/')[0]['seq_id'], 1)
            ords.call('POST', 'pessoas/', payload={'ds_nome': 'TESTE', 'num_cpf': '52998224725', 'status': 'ATIVO'})
            self.assertEqual(request.call_args.kwargs['json'], {'nome': 'TESTE', 'cpf': '52998224725', 'status': 'ATIVO'})

    @patch('app.ords.httpx.Client.request')
    def test_pagination_reads_all_pages(self, request):
        from app import ords
        request.return_value.status_code = 200
        request.return_value.json.side_effect = [{'items': [{'id': 1}], 'hasMore': True}, {'items': [{'id': 2}], 'hasMore': False}]
        with self.app.app_context():
            self.assertEqual([p['seq_id'] for p in ords.collection('pessoas/')], [1, 2])
        self.assertEqual(request.call_args.kwargs['params']['offset'], 1)

    @patch('app.ords.call')
    def test_unavailable_service_does_not_call_api(self, call):
        self.login()
        self.app.config['ORDS_SERVICOS_HABILITADOS'] = False
        self.assertEqual(self.client.get('/pessoa/123/servicos/novo').status_code, 409)
        call.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
