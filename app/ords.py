"""Cliente ORDS sem exposição de respostas brutas ou dados sensíveis."""
import httpx
from time import monotonic
from threading import Lock
from urllib.parse import urljoin
from flask import current_app

_token_lock = Lock()


def access_token():
    """Mantém tokens curtos em memória e os renova com o cliente autorizado."""
    if current_app.config.get('API_TOKEN'):
        return current_app.config['API_TOKEN']
    identifier = current_app.config.get('ORDS_CLIENT_ID')
    secret = current_app.config.get('ORDS_CLIENT_SECRET')
    if not identifier or not secret:
        return None
    with _token_lock:
        cached = current_app.extensions.get('ords_token', {})
        if cached.get('until', 0) > monotonic():
            return cached['value']
        endpoint = urljoin(current_app.config['API_BASE_URL'], '../oauth/token')
        if not endpoint.startswith('https://'):
            raise APIError('A autenticação Oracle exige HTTPS.')
        try:
            with httpx.Client(http2=True, timeout=httpx.Timeout(20, connect=5), follow_redirects=False) as client:
                response = client.post(endpoint, auth=(identifier, secret),
                    data={'grant_type': 'client_credentials'}, headers={'Accept': 'application/json',
                    'User-Agent': 'GestaoRCC/' + current_app.config['APP_VERSION']})
            if response.status_code != 200:
                raise APIError('Não foi possível autenticar a aplicação no Oracle. Confira as credenciais ORDS.')
            data = response.json()
            value = data.get('access_token')
            lifetime = int(data.get('expires_in', 0))
            if not isinstance(value, str) or not value or lifetime <= 0 or str(data.get('token_type', '')).lower() != 'bearer':
                raise ValueError
        except (httpx.HTTPError, ValueError, TypeError, AttributeError):
            raise APIError('O Oracle não forneceu um token válido. Verifique a conexão e a configuração.') from None
        current_app.extensions['ords_token'] = {'value': value, 'until': monotonic() + max(0, lifetime - 30)}
        return value

PATIENT_MAP = {'seq_id': 'id', 'ds_nome': 'nome', 'num_cpf': 'cpf', 'dt_nascimento': 'data_nascimento',
               'num_telefone': 'telefone', 'char_endereco': 'endereco', 'status': 'status'}
SERVICE_MAP = {'seq_id': 'id', 'sq_idpaciente': 'pessoa_id', 'ds_nome': 'tipo_servico',
               'char_descricao': 'descricao', 'dt_dataservico': 'data_servico'}


def translate_record(data, mapping):
    return {**data, **{local: data[remote] for local, remote in mapping.items() if remote in data}}


class APIError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


def call(method, path, *, payload=None, params=None):
    mapping = PATIENT_MAP if path.startswith('pessoas') else SERVICE_MAP if path.startswith('servicos') else {}
    if payload is not None:
        payload = {mapping.get(key, key): value for key, value in payload.items()}
        if path.startswith('pessoas') and (current_app.config['ORDS_DADOS_MEDICOS_HABILITADOS'] or current_app.config['ORDS_CESTAS_HABILITADAS']):
            payload['atualizar_clinico'] = int(current_app.config['ORDS_DADOS_MEDICOS_HABILITADOS'])
            payload['atualizar_cestas'] = int(current_app.config['ORDS_CESTAS_HABILITADAS'])
    headers = {'Accept': 'application/json', 'User-Agent': 'GestaoRCC/' + current_app.config['APP_VERSION']}
    token = access_token()
    if token:
        headers['Authorization'] = 'Bearer ' + token
    try:
        with httpx.Client(http2=True, timeout=httpx.Timeout(20, connect=5), follow_redirects=False) as client:
            response = client.request(method, current_app.config['API_BASE_URL'] + path.lstrip('/'),
                                      json=payload, params=params, headers=headers)
    except httpx.TimeoutException:
        raise APIError('O Oracle demorou a responder. Consulte os registros antes de repetir uma gravação.') from None
    except httpx.HTTPError:
        raise APIError('Não foi possível conectar ao Oracle. Verifique a conexão e tente novamente.') from None
    if not 200 <= response.status_code < 300:
        if response.status_code == 401:
            current_app.extensions.pop('ords_token', None)
        messages = {401: 'O acesso à API não foi autorizado. Verifique a configuração com o responsável.',
                    403: 'A API não permitiu esta operação.', 404: 'Registro ou endereço da API não encontrado.',
                    409: 'A operação conflita com um registro existente. Verifique os dados.'}
        raise APIError(messages.get(response.status_code, 'O Oracle não confirmou a operação. Nenhum sucesso foi registrado.'), response.status_code)
    if method != 'GET':
        return None
    try:
        data = response.json()
    except ValueError:
        raise APIError('A API retornou uma resposta inválida. Avise o responsável pelo sistema.') from None
    if not isinstance(data, dict):
        raise APIError('A API retornou um formato inesperado.')
    if isinstance(data.get('items'), list):
        data['items'] = [translate_record(row, mapping) if isinstance(row, dict) else row for row in data['items']]
    else:
        data = translate_record(data, mapping)
    return data


def collection(path, params=None):
    items = []
    offset = 0
    for _ in range(100):
        data = call('GET', path, params={**(params or {}), 'limit': 100, 'offset': offset})
        page = data.get('items')
        if not isinstance(page, list) or any(not isinstance(item, dict) for item in page):
            raise APIError('A API não retornou a lista esperada.')
        items.extend(page)
        if not data.get('hasMore'):
            return items
        if not page:
            raise APIError('A paginação da API está inconsistente.')
        offset += len(page)
    raise APIError('A consulta excedeu o limite desta versão. Solicite uma consulta mais específica.')
