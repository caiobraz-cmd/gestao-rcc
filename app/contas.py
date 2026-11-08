"""Contas de operadores; o administrador inicial continua na configuração privada."""
import re
from flask import current_app
from app import ords

LOGIN = re.compile(r'[a-z0-9][a-z0-9._-]{2,39}', re.ASCII)

def validate_api():
    cfg = current_app.config
    if not (cfg['API_BASE_URL'].startswith('https://') and cfg['API_BASE_URL'].endswith('/rcc-v2/')
            and (cfg.get('API_TOKEN') or (cfg.get('ORDS_CLIENT_ID') and cfg.get('ORDS_CLIENT_SECRET')))):
        raise ords.APIError('A gestão de contas exige o módulo Oracle protegido.')

def lookup(login, *, credentials=False):
    validate_api()
    if not LOGIN.fullmatch(login):
        return None
    rows = ords.collection(('conta-login/' if credentials else 'contas/') + login + '/')
    if not rows:
        return None
    if len(rows) != 1 or rows[0].get('login') != login:
        raise ords.APIError('O Oracle retornou uma conta inesperada.')
    return rows[0]

def accounts():
    validate_api()
    return ords.collection('contas/')
