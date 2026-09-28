"""Regras de calendário e fluxos da versão 0.5; Oracle simulado explicitamente."""
from datetime import date, timedelta
import unittest
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from app import create_app
from app.cestas import agenda, hoje
from app.validation import patient


class AgendaTests(unittest.TestCase):
    def test_first_delivery_disabled_and_suspended(self):
        person = {'status': 'ATIVO', 'num_frequencia_cesta': 7}
        self.assertTrue(agenda(person)['pode_entregar'])
        for changes in [{'status': 'INATIVO'}, {'data_obito': '2026-01-01'},
                        {'num_frequencia_cesta': None}, {'num_frequencia_cesta': 0},
                        {'num_frequencia_cesta': 'inválida'}, {'num_frequencia_cesta': 7.5}]:
            self.assertFalse(agenda({**person, **changes})['pode_entregar'])

    def test_due_today_late_and_month_boundary(self):
        person = {'status': 'ATIVO', 'num_frequencia_cesta': 7, 'dt_ultima_cesta': '2024-02-23'}
        self.assertEqual(agenda(person, date(2024, 2, 29))['situacao'], 'Agendada')
        self.assertEqual(agenda(person, date(2024, 3, 1))['situacao'], 'Entrega prevista hoje')
        late = agenda(person, date(2024, 3, 4))
        self.assertEqual(late['atraso'], 3)
        self.assertTrue(late['pode_entregar'])
        self.assertFalse(agenda(person, date(2024, 2, 23))['pode_entregar'])
        self.assertEqual(agenda(person, date(2024, 2, 22))['situacao'], 'Revisar cadastro')

    def test_medical_death_and_limits(self):
        form = {'ds_nome': 'Teste fictício', 'num_cpf': '52998224725', 'dt_nascimento': '1990-01-01',
                'char_diagnostico': 'Texto de teste', 'data_obito': '2020-01-01', 'frequencia_cesta': '15'}
        data, errors = patient(form, baskets=True, medical=True)
        self.assertEqual(errors, [])
        self.assertEqual(data['status'], 'INATIVO')
        self.assertEqual(data['char_diagnostico'], 'Texto de teste')
        self.assertNotIn('char_diagnostico', patient(form)[0])
        for changes in [{'data_obito': '1980-01-01'}, {'data_obito': '2999-01-01'},
                        {'char_diagnostico': 'á' * 1001}, {'frequencia_cesta': '366'}]:
            self.assertTrue(patient({**form, **changes}, baskets=True, medical=True)[1])


class ExtendedFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.password_hash = generate_password_hash('senha-teste')

    def setUp(self):
        self.config = {'TESTING': True, 'SECRET_KEY': 'teste-' * 10,
                       'API_BASE_URL': 'https://example.invalid/rcc-v2/',
                       'ADMIN_USERNAME': 'operador', 'ADMIN_PASSWORD_HASH': self.password_hash,
                       'ORDS_CESTAS_HABILITADAS': True, 'ORDS_DADOS_MEDICOS_HABILITADOS': True,
                       'ORDS_SERVICOS_HABILITADOS': False, 'API_TOKEN': '', 'ORDS_CLIENT_ID': '', 'ORDS_CLIENT_SECRET': ''}
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        with self.client.session_transaction() as session:
            session['usuario_id'] = 1
            session['_csrf_token'] = 'teste'
        self.person = {'seq_id': 1, 'ds_nome': 'TESTE', 'num_cpf': '52998224725',
                       'dt_nascimento': '1990-01-01', 'status': 'ATIVO', 'num_frequencia_cesta': 7}

    def test_features_require_protected_endpoint(self):
        with self.assertRaisesRegex(RuntimeError, 'API protegida'):
            create_app({**self.config, 'TESTING': False})
        with self.assertRaisesRegex(RuntimeError, 'API protegida'):
            create_app({**self.config, 'TESTING': False, 'API_TOKEN': 'fake', 'API_BASE_URL': 'https://example.invalid/rcc/'})

    @patch('app.ords.collection')
    @patch('app.ords.call')
    def test_full_fields_render_and_readback_prevents_false_success(self, call, collection):
        call.return_value = dict(self.person)
        collection.return_value = []
        for path in ['/novo', '/editar/1']:
            html = self.client.get(path).get_data(as_text=True)
            self.assertIn('name="char_diagnostico"', html)
            self.assertIn('name="frequencia_cesta"', html)
        response = self.client.post('/editar/1', data={**self.person, 'char_diagnostico': 'Texto de teste',
                                                      'frequencia_cesta': 7, 'csrf_token': 'teste'})
        self.assertEqual(response.status_code, 503)
        self.assertIn('Texto de teste', response.get_data(as_text=True))
        sent = [c.kwargs['payload'] for c in call.call_args_list if c.args[0] == 'PUT'][0]
        self.assertEqual(sent['char_diagnostico'], 'Texto de teste')
        self.assertNotIn('dt_ultima_cesta', sent)

    @patch('app.ords.collection')
    @patch('app.ords.call')
    def test_delivery_verified_in_history_and_patient(self, call, collection):
        today = hoje().isoformat()
        call.side_effect = [dict(self.person), None, {**self.person, 'dt_ultima_cesta': today}]
        collection.return_value = [{'id': 15, 'pessoa_id': 1, 'data_entrega': today, 'frequencia_dias': 7}]
        response = self.client.post('/renovar_cesta/1', data={'csrf_token': 'teste'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(call.call_args_list[1].args, ('POST', 'cestas/1/'))
        self.assertEqual(call.call_args_list[1].kwargs['payload'], {'data_entrega': today})
        with self.client.session_transaction() as session:
            self.assertTrue(any('confirmada' in message for _, message in session['_flashes']))

    @patch('app.ords.collection', return_value=[])
    @patch('app.ords.call')
    def test_early_duplicate_and_inactive_do_not_write(self, call, collection):
        for changes in [{'dt_ultima_cesta': hoje().isoformat()}, {'status': 'INATIVO'},
                        {'data_obito': '2020-01-01'}, {'dt_ultima_cesta': (hoje() - timedelta(days=1)).isoformat()}]:
            call.reset_mock()
            call.return_value = {**self.person, **changes}
            self.assertEqual(self.client.post('/renovar_cesta/1', data={'csrf_token': 'teste'}).status_code, 302)
            self.assertFalse(any(c.args[0] != 'GET' for c in call.call_args_list))

    @patch('app.ords.collection')
    @patch('app.ords.call')
    def test_history_other_patient_is_not_confirmation(self, call, collection):
        call.return_value = dict(self.person)
        collection.return_value = [{'id': 15, 'pessoa_id': 2, 'data_entrega': hoje().isoformat()}]
        self.assertEqual(self.client.post('/renovar_cesta/1', data={'csrf_token': 'teste'}).status_code, 503)

    @patch('app.ords.collection')
    @patch('app.ords.call')
    def test_list_details_and_preserve_history(self, call, collection):
        call.return_value = dict(self.person)
        collection.return_value = [dict(self.person)]
        self.assertIn('Primeira entrega pendente', self.client.get('/').get_data(as_text=True))
        collection.return_value = [{'id': 4, 'pessoa_id': 1, 'data_entrega': '2026-01-01', 'frequencia_dias': 7}]
        self.assertIn('2026-01-01', self.client.get('/pessoa/1/').get_data(as_text=True))
        self.app.config['ORDS_SERVICOS_HABILITADOS'] = True
        self.client.post('/deletar/1', data={'csrf_token': 'teste'})
        self.assertFalse(any(c.args[0] == 'DELETE' for c in call.call_args_list))


if __name__ == '__main__':
    unittest.main()
