"""Diagnóstico somente de leitura, sem imprimir dados de pacientes."""
import argparse
import re
import json
import httpx


def check(url):
    try:
        with httpx.Client(http2=True, timeout=httpx.Timeout(10, connect=5), follow_redirects=False) as client:
            response = client.get(url, headers={'Accept': 'application/json', 'User-Agent': 'GestaoRCC/0.4.0-rc1'})
        result = {'endereco': url, 'http': response.status_code, 'tipo': response.headers.get('Content-Type')}
        result['protocolo'] = response.http_version
        result['servidor'] = response.headers.get('Server')
        result['autenticacao_exigida'] = response.headers.get('WWW-Authenticate')
        if response.status_code >= 400 and 'text/html' in response.headers.get('Content-Type', ''):
            title = re.search(r'<title[^>]*>(.*?)</title>', response.text, flags=re.I | re.S)
            result['titulo_erro'] = re.sub(r'\s+', ' ', title.group(1)).strip()[:200] if title else None
        if 'json' in response.headers.get('Content-Type', ''):
            data = response.json()
            if isinstance(data, dict) and isinstance(data.get('items'), list):
                result['quantidade_na_pagina'] = len(data['items'])
                result['campos'] = list(data['items'][0]) if data['items'] else []
        return result
    except (httpx.HTTPError, ValueError) as error:
        return {'endereco': url, 'falha': type(error).__name__}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='URL da coleção de pacientes')
    parser.add_argument('--json', action='store_true', help='Imprimir resultado JSON para evidência')
    args = parser.parse_args()
    result = check(args.url)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
