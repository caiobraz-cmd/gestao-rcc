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
    default_url = 'https://oracleapex.com/ords/gestaorcc/rcc/'
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
    token = getpass('Token Bearer do ORDS, se exigido (Enter se não houver): ').strip()
    if any(c in token + url for c in '\r\n\'"'):
        raise SystemExit('Valor inválido para configuração.')
    content = (f"API_BASE_URL='{url.rstrip('/')}/'\nAPI_TOKEN='{token}'\n"
               f"SECRET_KEY='{secrets.token_hex(32)}'\nADMIN_USERNAME='{username}'\n"
               f"ADMIN_PASSWORD_HASH='{generate_password_hash(password)}'\n"
               'FLASK_ENV=development\nORDS_CESTAS_HABILITADAS=false\nORDS_SERVICOS_HABILITADOS=false\n')
    with destination.open('x', encoding='utf-8') as stream:
        stream.write(content)
    print('Configuração salva em .env. No Windows, abra INICIAR.cmd. A senha não foi salva em texto puro.')


if __name__ == '__main__':
    main()
