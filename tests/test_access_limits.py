import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from app.access_limits import AttemptLimiter
from app import create_app
from werkzeug.security import generate_password_hash


class LimitTests(unittest.TestCase):
    def test_parallel_requests_and_expiration(self):
        now = [100]
        limiter = AttemptLimiter(clock=lambda: now[0])
        with ThreadPoolExecutor(max_workers=12) as pool:
            replies = list(pool.map(lambda _: limiter.consume([('account', 5)]), range(15)))
        self.assertEqual(replies.count(0), 5)
        self.assertEqual(replies.count(300), 10)
        now[0] = 400
        self.assertEqual(limiter.consume([('account', 5)]), 0)

    def test_capacity_does_not_evict_existing_limits(self):
        limiter = AttemptLimiter(capacity=2, clock=lambda: 0)
        self.assertEqual(limiter.consume([('a', 1), ('b', 1)]), 0)
        self.assertEqual(limiter.consume([('c', 1)]), 300)
        self.assertEqual(limiter.consume([('a', 1)]), 300)
        self.assertEqual(len(limiter.entries), 2)

    def test_login_limit_precedes_oracle_and_ignores_proxy_header(self):
        app = create_app({'TESTING':True,'SECRET_KEY':'test-'*10,
            'API_BASE_URL':'https://example.invalid/rcc-v2/', 'API_TOKEN':'teste',
            'ADMIN_USERNAME':'gestor','ADMIN_PASSWORD_HASH':generate_password_hash('senha-qualquer')})
        client = app.test_client()
        with client.session_transaction() as session:
            session['_csrf_token'] = 't'
        with patch('app.contas.lookup', return_value=None) as lookup:
            for n in range(5):
                r = client.post('/auth/login', data={'username':'INEXISTENTE','password':'x','csrf_token':'t'},
                                headers={'X-Forwarded-For':str(n)})
                self.assertEqual(r.status_code,401)
            r = client.post('/auth/login', data={'username':'inexistente','password':'x','csrf_token':'t'})
            self.assertEqual(r.status_code,429)
            self.assertTrue(1 <= int(r.headers['Retry-After']) <= 300)
            self.assertEqual(lookup.call_count,5)
            self.assertNotIn('inexistente',r.get_data(as_text=True))
