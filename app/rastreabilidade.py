from uuid import uuid4
from flask import current_app, session
from app import ords

def autoria():
    # Compatibilidade com instalações básicas antigas, fora do módulo v2.
    if not current_app.config['API_BASE_URL'].endswith('/rcc-v2/'):
        return {}
    return {'registro': uuid4().hex, 'autor':session['usuario_nome'], 'perfil':session['perfil']}

def confirmar(meta, pessoa_id, operacao):
    if not meta:
        return
    data = ords.call('GET', f"registros-operacoes/{meta['registro']}/")
    if (data.get('registro') != meta['registro'] or str(data.get('pessoa_id')) != str(pessoa_id)
        or data.get('autor') != meta['autor'] or data.get('perfil') != meta['perfil']
        or data.get('operacao') != operacao):
        raise ords.APIError('Não foi possível confirmar a rastreabilidade. Consulte o histórico antes de repetir.')
