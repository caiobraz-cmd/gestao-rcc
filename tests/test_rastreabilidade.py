import unittest
from unittest.mock import patch
from flask import Flask
from app.rastreabilidade import autoria, confirmar
from app.ords import APIError

class TraceTests(unittest.TestCase):
    def test_confirmation_checks_person_actor_and_operation(self):
        app=Flask(__name__)
        with app.app_context(), patch('app.ords.call') as call:
            meta={'registro':'a'*32,'autor':'ana','perfil':'operador'}
            valid={**meta,'pessoa_id':7,'operacao':'cadastro'}
            call.return_value=valid
            confirmar(meta,7,'cadastro')
            for change in ({'pessoa_id':8},{'autor':'outro'},{'perfil':'admin'},
                           {'operacao':'entrega'},{'registro':'b'*32}):
                call.return_value={**valid,**change}
                with self.assertRaises(APIError):
                    confirmar(meta,7,'cadastro')

    def test_author_is_from_session_not_form(self):
        app=Flask(__name__)
        app.secret_key='teste'
        app.config['API_BASE_URL']='https://example.invalid/rcc-v2/'
        with app.test_request_context('/',method='POST',data={'autor':'forjado','perfil':'admin'}):
            from flask import session
            session.update(usuario_nome='ana',perfil='operador')
            self.assertEqual(autoria()['autor'],'ana')
            self.assertEqual(autoria()['perfil'],'operador')
