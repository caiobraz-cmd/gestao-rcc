"""
Ponto de Entrada Principal da Aplicação.

Este arquivo é usado para iniciar o servidor Flask em modo de desenvolvimento.
Em produção, use um servidor WSGI como Gunicorn ou uWSGI.
"""

from app import create_app

# Cria a instância da aplicação usando a Application Factory
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=True)
