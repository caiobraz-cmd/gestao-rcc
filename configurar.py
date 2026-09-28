"""Configuração interativa local. Não envia credenciais pela rede."""
from getpass import getpass
from pathlib import Path
import secrets
from urllib.parse import urlsplit
from werkzeug.security import generate_password_hash


def main():
    destination = Path(__file__).resolve().parent / '.env'
    if destination.exists():
        raise SystemExit('O .env já existe. Edite-o localmente; nenhuma configuração foi sobrescrita.')
    default_url = 'https://oracleapex.com/ords/gestaorcc/rcc-v2/'
    url = input(f'URL base do Oracle ORDS [Enter para {default_url}]: ').strip() or default_url
    parts = urlsplit(url)
    if parts.scheme != 'https' or not parts.hostname or parts.query or parts.fragment or parts.username:
        raise SystemExit('Informe uma URL HTTPS base válida, sem usuário ou parâmetros.')
    username = input('Nome do operador para acessar o Gestão RCC: ').strip()
    if not username or any(c in username for c in '\r\n\'"#= '):
        raise SystemExit('Use um nome de usuário sem espaços, aspas ou símbolos de configuração.')
    password = getpass('Crie uma senha de pelo menos 12 caracteres: ')
    if len(password) < 12 or password != getpass('Repita a senha: '):
        raise SystemExit('Senha curta ou confirmação diferente. Nenhum arquivo foi criado.')
    extended = parts.path.rstrip('/').endswith('/rcc-v2')
    client_id = input('ID do cliente OAuth autorizado no Oracle: ').strip() if extended else ''
    client_secret = getpass('Segredo do cliente OAuth (digitação oculta): ').strip() if extended else ''
    token = '' if extended else getpass('Token Bearer do ORDS, se exigido (Enter se não houver): ').strip()
    if extended and (not client_id or not client_secret):
        raise SystemExit('Solicite as credenciais da API ao responsável pelo Oracle. Nenhum arquivo foi criado.')
    if any(c in token + url + client_id + client_secret for c in '\r\n\'"'):
        raise SystemExit('Valor inválido para configuração.')
    content = (f"API_BASE_URL='{url.rstrip('/')}/'\nAPI_TOKEN='{token}'\n"
               f"ORDS_CLIENT_ID='{client_id}'\nORDS_CLIENT_SECRET='{client_secret}'\n"
               f"SECRET_KEY='{secrets.token_hex(32)}'\nADMIN_USERNAME='{username}'\n"
               f"ADMIN_PASSWORD_HASH='{generate_password_hash(password)}'\n"
               'FLASK_ENV=development\nORDS_SERVICOS_HABILITADOS=false\n'
               f'ORDS_CESTAS_HABILITADAS={str(extended).lower()}\nORDS_DADOS_MEDICOS_HABILITADOS={str(extended).lower()}\n')
    with destination.open('x', encoding='utf-8') as stream:
        stream.write(content)
    print('Configuração salva em .env. No Windows, abra INICIAR.cmd. A senha não foi salva em texto puro.')


if __name__ == '__main__':
    main()
