import csv
import io
import unittest
from datetime import date
from unittest.mock import patch
from app import create_app, ords
from app.routes.relatorios_routes import resumo

class ReportTests(unittest.TestCase):
    def setUp(self):
        self.app=create_app({'TESTING':True,'SECRET_KEY':'test-'*10,
            'API_BASE_URL':'https://example.invalid/rcc-v2/','ADMIN_USERNAME':'gestor',
            'ADMIN_PASSWORD_HASH':'not-used','API_TOKEN':'teste'})
        self.client=self.app.test_client()
        with self.client.session_transaction() as s:
            s.update(usuario_id='admin',usuario_nome='gestor',perfil='admin')
        self.people=[{'status':'ATIVO'},{'status':'INATIVO'},{'status':'OUTRO'}]
        self.rows=[
            {'operacao':'entrega','referencia':1,'quando':'2026-01-01 00:00:00'},
            {'operacao':'entrega','referencia':1,'quando':'2026-01-01 00:00:00'},
            {'operacao':'servico','referencia':1,'quando':'2026-01-31 23:59:59'},
            {'operacao':'entrega','referencia':2,'quando':'2026-02-01'},
            {'operacao':'alteracao','referencia':None,'quando':'2026-01-02'}]

    @patch('app.ords.collection')
    def test_inclusive_dates_no_duplicate_or_patient_change_count(self, collection):
        collection.side_effect=[self.people,self.rows]
        with self.app.app_context():
            r=resumo(date(2026,1,1),date(2026,1,31))
        self.assertEqual((r['cestas'],r['servicos'],r['total'],r['outros']),(1,1,3,1))
        self.assertEqual(len(r['dias']),2)

    @patch('app.ords.collection')
    def test_csv_and_invalid_period_and_outage(self, collection):
        collection.side_effect=[self.people,self.rows]
        r=self.client.get('/relatorios/?inicio=2026-01-01&fim=2026-01-31&formato=csv')
        self.assertEqual(r.status_code,200)
        table=list(csv.reader(io.StringIO(r.data.decode('utf-8-sig')),delimiter=';'))
        self.assertEqual(table[1],['Cestas entregues','2026-01-01','2026-01-31','1'])
        self.assertIn('attachment',r.headers['Content-Disposition'])
        self.assertIn('no-store',r.headers['Cache-Control'])
        collection.reset_mock()
        self.assertEqual(self.client.get('/relatorios/?inicio=2026-01-31&fim=2026-01-01').status_code,422)
        collection.assert_not_called()
        collection.side_effect=ords.APIError('offline')
        self.assertEqual(self.client.get('/relatorios/').status_code,503)

    @patch('app.contas.lookup',return_value={'login':'ana','ativo':1,'versao':1})
    @patch('app.ords.collection')
    def test_operator_cannot_view_or_export(self, collection, lookup):
        with self.client.session_transaction() as s:
            s.update(usuario_id='ana',usuario_nome='ana',perfil='operador',versao=1)
        for path in ('/relatorios/','/relatorios/?formato=csv'):
            self.assertEqual(self.client.get(path).status_code,403)
        collection.assert_not_called()

    @patch('app.ords.collection')
    def test_incomplete_data_fails_instead_of_partial_total(self, collection):
        collection.side_effect=[self.people,[{'operacao':'entrega','referencia':1,'quando':None}]]
        self.assertEqual(self.client.get('/relatorios/').status_code,503)
