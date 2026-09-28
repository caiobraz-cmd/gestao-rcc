"""Autenticação sem dependência de uma credencial Oracle real."""
import unittest
from unittest.mock import patch
from app import create_app, ords


class OAuthTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'teste-' * 10,
            'ADMIN_USERNAME': 'teste', 'ADMIN_PASSWORD_HASH': 'apenas-teste',
            'API_BASE_URL': 'https://example.invalid/ords/test/rcc-v2/', 'API_TOKEN': '',
            'ORDS_CLIENT_ID': 'cliente-ficticio', 'ORDS_CLIENT_SECRET': 'segredo-ficticio'})

    @patch('app.ords.httpx.Client.post')
    def test_token_cached_and_renewed_before_expiry(self, post):
        post.return_value.status_code = 200
        post.return_value.json.return_value = {'access_token': 'token-ficticio', 'expires_in': 3600, 'token_type': 'bearer'}
        with self.app.app_context():
            self.assertEqual(ords.access_token(), 'token-ficticio')
            self.assertEqual(ords.access_token(), 'token-ficticio')
            self.assertEqual(post.call_count, 1)
            self.app.extensions['ords_token']['until'] = 0
            ords.access_token()
            self.assertEqual(post.call_count, 2)
        self.assertEqual(post.call_args.args[0], 'https://example.invalid/ords/test/oauth/token')

    @patch('app.ords.httpx.Client.post')
    def test_auth_failure_does_not_expose_secret(self, post):
        post.return_value.status_code = 401
        with self.app.app_context(), self.assertRaises(ords.APIError) as raised:
            ords.access_token()
        self.assertNotIn('segredo-ficticio', str(raised.exception))
        self.assertNotIn('ords_token', self.app.extensions)

    @patch('app.ords.httpx.Client.post')
    def test_malformed_token_not_cached(self, post):
        post.return_value.status_code = 200
        post.return_value.json.return_value = {'access_token': 'fake', 'expires_in': 0, 'token_type': 'bearer'}
        with self.app.app_context(), self.assertRaises(ords.APIError):
            ords.access_token()
        self.assertNotIn('ords_token', self.app.extensions)

    @patch('app.ords.httpx.Client.request')
    def test_401_clears_cache_without_replaying_write(self, request):
        self.app.extensions['ords_token'] = {'value': 'fake', 'until': float('inf')}
        request.return_value.status_code = 401
        with self.app.app_context(), self.assertRaises(ords.APIError):
            ords.call('POST', 'cestas/123/', payload={'data_entrega': '2026-09-27'})
        self.assertNotIn('ords_token', self.app.extensions)
        self.assertEqual(request.call_count, 1)
