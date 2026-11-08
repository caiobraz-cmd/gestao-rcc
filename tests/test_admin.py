"""Regressões de autorização do painel, sem dados nem rede."""
import unittest
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from app import create_app
from app import ords

class AdminTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_hash = generate_password_hash('senha-de-administrador')

    def setUp(self):
        self.app = create_app({'TESTING':True,'SECRET_KEY':'tests-'*8,'API_BASE_URL':'https://example.invalid/rcc-v2/',
            'ADMIN_USERNAME':'gestor','ADMIN_PASSWORD_HASH':self.admin_hash,'API_TOKEN':'teste'})
        self.client = self.app.test_client()

    def session(self, **fields):
        with self.client.session_transaction() as s:
            s.update(_csrf_token='teste', **fields)

    @patch('app.ords.call')
    @patch('app.contas.lookup')
    def test_operator_cannot_access_or_mutate_accounts(self, lookup, call):
        lookup.return_value={'login':'maria','versao':1,'ativo':1}
        self.session(usuario_id='maria',usuario_nome='maria',perfil='operador',versao=1)
        self.assertEqual(self.client.get('/admin/').status_code,403)
        self.assertEqual(self.client.get('/admin/registros-servicos').status_code,403)
        self.assertEqual(self.client.get('/admin/rastreabilidade').status_code,403)
        for path in ('/admin/','/admin/maria/acesso'):
            self.assertEqual(self.client.post(path,data={'csrf_token':'teste','acao':'ativar'}).status_code,403)
        call.assert_not_called()
        lookup.return_value['versao']=2
        self.assertEqual(self.client.get('/novo').status_code,302)
        with self.client.session_transaction() as s:
            self.assertNotIn('usuario_id',s)

    @patch('app.ords.call')
    @patch('app.contas.accounts',return_value=[])
    def test_admin_rejects_duplicate_identity_and_csrf(self, accounts, call):
        self.session(usuario_id='admin',usuario_nome='gestor',perfil='admin')
        form={'login':'GESTOR','nome':'Nome Teste','senha':'senha-operador-longa'}
        self.assertEqual(self.client.post('/admin/',data=form).status_code,400)
        self.assertEqual(self.client.post('/admin/',data={**form,'csrf_token':'teste'}).status_code,422)
        call.assert_not_called()

    @patch('app.contas.lookup',side_effect=ords.APIError('offline'))
    def test_operator_fails_closed_during_outage(self, lookup):
        self.session(usuario_id='maria',usuario_nome='maria',perfil='operador',versao=1)
        self.assertEqual(self.client.get('/novo').status_code,503)

    def test_old_session_is_not_promoted(self):
        self.session(usuario_id=1,usuario_nome='gestor')
        self.assertEqual(self.client.get('/admin/').status_code,302)

    @patch('app.ords.call')
    def test_operations_filter_and_page(self, call):
        self.session(usuario_id='admin',usuario_nome='gestor',perfil='admin')
        call.return_value={'items':[],'hasMore':True}
        r=self.client.get('/admin/rastreabilidade?tipo=entrega&q=teste&pagina=2')
        self.assertEqual(r.status_code,200)
        call.assert_called_with('GET','registros-operacoes/',params={
            'tipo':'entrega','busca':'teste','limit':25,'offset':25})
        self.assertIn('Próxima',r.get_data(as_text=True))

    @patch('app.ords.call')
    def test_audit_page_filter_pagination_and_legacy(self, call):
        self.session(usuario_id='admin',usuario_nome='gestor',perfil='admin')
        call.return_value = {'items':[{'servico_id':1,'pessoa_id':42,'paciente':'TESTE',
                             'servico':'Consulta','quando':'2026-11-07','autor':None}], 'hasMore':True}
        r=self.client.get('/admin/registros-servicos?q=Consulta&pagina=2')
        self.assertEqual(r.status_code,200)
        call.assert_called_with('GET','registros-servicos/',params={'busca':'Consulta','limit':25,'offset':25})
        self.assertIn('Não identificado',r.get_data(as_text=True))
        self.assertIn('Próxima',r.get_data(as_text=True))
        call.side_effect=ords.APIError('offline')
        self.assertEqual(self.client.get('/admin/registros-servicos').status_code,503)

    @patch('app.contas.accounts',return_value=[])
    @patch('app.contas.lookup',return_value=None)
    @patch('app.ords.call')
    def test_create_does_not_claim_success_without_persistence(self, call, lookup, accounts):
        self.session(usuario_id='admin',usuario_nome='gestor',perfil='admin')
        response = self.client.post('/admin/',data={'csrf_token':'teste','nome':'Equipe Teste',
            'login':'nova.conta','senha':'senha-comprida-de-teste'})
        self.assertEqual(response.status_code,503)
        self.assertNotIn('Conta criada.',response.get_data(as_text=True))

    @patch('app.contas.accounts',return_value=[])
    @patch('app.contas.lookup')
    @patch('app.ords.call')
    def test_update_does_not_claim_success_without_version_change(self, call, lookup, accounts):
        lookup.return_value = {'login':'maria','ativo':1,'versao':1}
        self.session(usuario_id='admin',usuario_nome='gestor',perfil='admin')
        response = self.client.post('/admin/maria/acesso',data={'csrf_token':'teste','acao':'desativar'})
        self.assertEqual(response.status_code,503)
        self.assertNotIn('Acesso atualizado',response.get_data(as_text=True))

    @patch('app.ords.call')
    @patch('app.contas.lookup')
    def test_self_password_requires_current_password_and_own_identity(self, lookup, call):
        row = {'login':'maria','ativo':1,'versao':1,'senha_hash':self.admin_hash}
        lookup.return_value = row
        self.session(usuario_id='maria',usuario_nome='maria',perfil='operador',versao=1)
        data = {'csrf_token':'teste','senha_atual':'incorreta',
                'nova_senha':'nova-senha-operadora','confirmacao':'nova-senha-operadora','login':'outra'}
        self.assertEqual(self.client.post('/auth/senha',data=data).status_code,422)
        call.assert_not_called()
        data['senha_atual']='senha-de-administrador'
        lookup.side_effect = [row,row,{**row,'versao':2,'senha_hash':generate_password_hash(data['nova_senha'])}]
        self.assertEqual(self.client.post('/auth/senha',data=data).status_code,302)
        self.assertEqual(call.call_args.args,('PUT','contas/maria/'))
        self.assertNotIn(data['nova_senha'],str(call.call_args.kwargs))
        with self.client.session_transaction() as s:
            self.assertNotIn('usuario_id',s)

    @patch('app.ords.call')
    @patch('app.contas.lookup')
    def test_self_password_validates_confirmation_and_csrf(self, lookup, call):
        lookup.return_value = {'login':'maria','ativo':1,'versao':1}
        self.session(usuario_id='maria',usuario_nome='maria',perfil='operador',versao=1)
        data = {'senha_atual':'atual','nova_senha':'nova-senha-operadora','confirmacao':'diferente'}
        self.assertEqual(self.client.post('/auth/senha',data=data).status_code,400)
        self.assertEqual(self.client.post('/auth/senha',data={**data,'csrf_token':'teste'}).status_code,422)
        call.assert_not_called()
