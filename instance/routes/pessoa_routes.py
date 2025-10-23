# -*- coding: utf-8 -*-
"""
Blueprint para as rotas da aplicação, consumindo a API do Oracle (ORDS).

Este módulo define todas as rotas e a lógica de visualização, atuando como
o controlador que faz a ponte entre os templates (front-end) e
a API RESTful (back-end).
"""

import requests
import json # Importado para os prints de debug
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime # Importado para data do serviço

# --- Configuração do Blueprint ---
# Mantemos 'pessoa_bp' para consistência com os templates e url_for
pessoa_bp = Blueprint(
    'pessoa_bp',
    __name__,
    template_folder='../templates'
)

# --- Função Auxiliar ---
def get_api_url():
    """Busca a URL base da API (ex: .../ords/bulldog/) a partir da config."""
    return current_app.config['API_BASE_URL']

# ============================================================================
# ROTAS PARA A ENTIDADE 'PESSOA' (CRUD VIA API)
# ============================================================================

@pessoa_bp.route('/')
def listar():
    """Exibe a lista de todas as pessoas cadastradas, buscando da API."""
    pessoas = [] # Inicializa com lista vazia
    try:
        api_url = f"{get_api_url()}pessoas/"
        print(f"--- [DEBUG] GET para: {api_url} ---") # Debug URL GET
        # Adicionado timeout
        response = requests.get(api_url, timeout=15) # Aumentado um pouco o timeout para GET
        print(f"--- [DEBUG] GET Status Code: {response.status_code} ---") # Debug Status
        response.raise_for_status() # Lança erro para 4xx/5xx
        data = response.json()
        pessoas = data.get('items', [])
        print(f"--- [DEBUG] GET Recebido {len(pessoas)} itens ---") # Debug Itens
    except requests.exceptions.Timeout:
        print("\n--- [DEBUG] Erro: Timeout na requisição GET (listar) ---\n")
        flash("Erro ao listar pacientes: A conexão demorou muito (Timeout).", 'danger')
    except requests.exceptions.RequestException as e:
        print(f"\n--- [DEBUG] Erro capturado na requisição GET (listar): {e} ---\n")
        flash(f"Erro ao conectar com a API do Oracle: {e}", "danger")

    return render_template('listar.html', pessoas=pessoas, titulo="Lista de Pacientes")


@pessoa_bp.route('/novo', methods=['GET', 'POST'])
def novo():
    """Cria um novo registro de Pessoa via API."""
    response = None # Inicializa response fora do try
    if request.method == 'POST':
        try:
            api_url = f"{get_api_url()}pessoas/"

            # Monta o payload com os nomes corretos das colunas (minúsculas)
            novo_dado = {
                "ds_nome": request.form.get('ds_nome') or None,
                "num_cpf": request.form.get('num_cpf') or None,
                "dt_nascimento": request.form.get('dt_nascimento') or None,
                "num_telefone": request.form.get('num_telefone') or None,
                "char_endereco": request.form.get('char_endereco') or None,
                "char_diagnostico": request.form.get('char_diagnostico') or None,
                "char_tratamento": request.form.get('char_tratamento') or None,
                "char_medicamento": request.form.get('char_medicamento') or None,
                "char_alergia": request.form.get('char_alergia') or None,
                "char_observacoes": request.form.get('char_observacoes') or None
                # Campo BLOB removido por enquanto
            }

            print("\n--- [DEBUG] Enviando Payload ---")
            print(json.dumps(novo_dado, indent=2))

            print("--- [DEBUG] PRESTES A EXECUTAR requests.post ---")
            # Executa o POST com timeout
            response = requests.post(api_url, json=novo_dado, timeout=10)
            print("--- [DEBUG] requests.post EXECUTADO ---")

            print(f"--- [DEBUG] API Respondeu Status: {response.status_code} ---")

            # Tenta imprimir a resposta da API
            try:
                print("--- [DEBUG] Resposta API (JSON) ---")
                print(json.dumps(response.json(), indent=2))
            except requests.exceptions.JSONDecodeError:
                print("--- [DEBUG] Resposta API (Texto) ---")
                print(response.text)
            print("--- [DEBUG] Fim da Resposta API ---\n")

            # Verifica se o status code NÃO é 201 (Created)
            if response.status_code != 201:
                response.raise_for_status() # Força cair no except

            # Se chegou aqui, o status é 201 - Sucesso!
            flash('Pessoa cadastrada com sucesso!', 'success')
            return redirect(url_for('pessoa_bp.listar'))

        except requests.exceptions.Timeout:
            print("\n--- [DEBUG] Erro: Timeout na requisição POST ---\n")
            flash("Erro ao cadastrar via API: A conexão demorou muito para responder (Timeout).", 'danger')

        except requests.exceptions.RequestException as e:
            print(f"\n--- [DEBUG] Erro capturado na requisição POST: {e} ---\n")
            # Monta mensagem de erro detalhada
            error_message = f"Erro ao cadastrar via API: {e}"
            if response is not None:
                error_message += f" (Status: {response.status_code})"
                try:
                    error_details = response.json()
                    error_message += f" Detalhes: {json.dumps(error_details)}"
                except requests.exceptions.JSONDecodeError:
                     error_message += f" Resposta: {response.text}"
            flash(error_message, 'danger')

    # Se for GET ou se o POST falhar e cair no except
    return render_template('novo.html', titulo="Novo Paciente")


@pessoa_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Atualiza um registro de Pessoa existente via API."""
    api_url_item = f"{get_api_url()}pessoas/{id}"
    response = None # Inicializa response
    pessoa = None # Inicializa pessoa

    if request.method == 'POST':
        try:
            # Monta payload com colunas corretas e data_obito
            dados_atualizados = {
                "ds_nome": request.form.get('ds_nome'),
                "num_cpf": request.form.get('num_cpf'),
                "dt_nascimento": request.form.get('dt_nascimento') or None,
                "num_telefone": request.form.get('num_telefone') or None,
                "char_endereco": request.form.get('char_endereco') or None,
                "char_diagnostico": request.form.get('char_diagnostico') or None,
                "char_tratamento": request.form.get('char_tratamento') or None,
                "char_medicamento": request.form.get('char_medicamento') or None,
                "char_alergia": request.form.get('char_alergia') or None,
                "char_observacoes": request.form.get('char_observacoes') or None,
                "data_obito": request.form.get('data_obito') or None # Campo data_obito
                # BLOB removido
            }

            print("\n--- [DEBUG] Enviando Payload (PUT) ---")
            print(json.dumps(dados_atualizados, indent=2))
            print("--- [DEBUG] PRESTES A EXECUTAR requests.put ---")

            # Executa PUT com timeout
            response = requests.put(api_url_item, json=dados_atualizados, timeout=10)
            print("--- [DEBUG] requests.put EXECUTADO ---")
            print(f"--- [DEBUG] API Respondeu Status (PUT): {response.status_code} ---")
            # ORDS geralmente retorna 200 OK para PUT bem-sucedido
            response.raise_for_status() # Erro se não for 2xx

            flash('Pessoa atualizada com sucesso!', 'success')
            return redirect(url_for('pessoa_bp.listar'))

        except requests.exceptions.Timeout:
            print("\n--- [DEBUG] Erro: Timeout na requisição PUT ---\n")
            flash("Erro ao atualizar via API: A conexão demorou muito (Timeout).", 'danger')
        except requests.exceptions.RequestException as e:
            print(f"\n--- [DEBUG] Erro capturado na requisição PUT: {e} ---\n")
            # (Lógica de mensagem de erro para PUT...)
            flash(f"Erro ao atualizar via API: {e}", 'danger')
         # Se deu erro no POST, precisamos buscar os dados da pessoa novamente para re-renderizar o form.
         # Buscaremos no bloco GET abaixo.

    # Código GET para buscar a pessoa (também precisa de timeout)
    # Executa sempre que for GET ou após falha no POST
    if pessoa is None: # Tenta buscar se ainda não temos os dados
        try:
            print(f"--- [DEBUG] GET (Editar) para: {api_url_item} ---")
            response = requests.get(api_url_item, timeout=10)
            print(f"--- [DEBUG] GET Status Code (Editar): {response.status_code} ---")
            response.raise_for_status()
            pessoa = response.json()
        except requests.exceptions.Timeout:
             print("\n--- [DEBUG] Erro: Timeout na requisição GET (editar) ---\n")
             flash("Erro ao buscar dados da pessoa: A conexão demorou muito (Timeout).", 'danger')
             return redirect(url_for('pessoa_bp.listar'))
        except requests.exceptions.RequestException as e:
            print(f"\n--- [DEBUG] Erro capturado na requisição GET (editar): {e} ---\n")
            flash(f"Erro ao buscar dados da pessoa na API: {e}", 'danger')
            # Verifica se o erro foi 404 (Não encontrado)
            if response is not None and response.status_code == 404:
                 flash(f"Erro: Paciente com ID {id} não encontrado.", 'danger')
            return redirect(url_for('pessoa_bp.listar'))

    # Se 'pessoa' foi carregado com sucesso (no GET ou após falha no POST)
    if pessoa:
        return render_template('editar.html', pessoa=pessoa, titulo="Editar Paciente")
    else:
        # Se por algum motivo 'pessoa' ainda for None (erro no GET inicial)
        return redirect(url_for('pessoa_bp.listar'))


@pessoa_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """Deleta um registro de Pessoa via API."""
    try:
        api_url_item = f"{get_api_url()}pessoas/{id}"
        print(f"--- [DEBUG] DELETE para: {api_url_item} ---")
        # Adicionado timeout
        response = requests.delete(api_url_item, timeout=10)
        print(f"--- [DEBUG] DELETE Status Code: {response.status_code} ---")
        # ORDS retorna 200 OK ou 204 No Content para DELETE bem-sucedido
        response.raise_for_status() # Erro se não for 2xx
        flash('Pessoa removida com sucesso!', 'success')
    except requests.exceptions.Timeout:
        print("\n--- [DEBUG] Erro: Timeout na requisição DELETE ---\n")
        flash("Erro ao remover via API: A conexão demorou muito (Timeout).", 'danger')
    except requests.exceptions.RequestException as e:
        print(f"\n--- [DEBUG] Erro capturado na requisição DELETE: {e} ---\n")
        flash(f"Erro ao remover via API: {e}", 'danger')
    return redirect(url_for('pessoa_bp.listar'))


# ============================================================================
# ROTAS PARA A ENTIDADE 'SERVIÇO' (VINCULADA A 'PESSOA')
# ============================================================================

@pessoa_bp.route('/pessoa/<int:id>/')
def detalhes(id):
    """Exibe a página de detalhes de uma pessoa e seu histórico de serviços."""
    pessoa = None
    servicos = []
    try:
        # 1. Busca os dados da pessoa
        api_url_pessoa = f"{get_api_url()}pessoas/{id}"
        print(f"--- [DEBUG] GET (Detalhes/Pessoa) para: {api_url_pessoa} ---")
        response_pessoa = requests.get(api_url_pessoa, timeout=10)
        print(f"--- [DEBUG] GET Status Code (Detalhes/Pessoa): {response_pessoa.status_code} ---")
        response_pessoa.raise_for_status()
        pessoa = response_pessoa.json()

        # 2. Busca os serviços associados usando a coluna correta 'sq_idpaciente'
        api_url_servicos = f"{get_api_url()}servicos/?q={{\"sq_idpaciente\":{id}}}"
        print(f"--- [DEBUG] GET (Detalhes/Serviços) para: {api_url_servicos} ---")
        response_servicos = requests.get(api_url_servicos, timeout=10)
        print(f"--- [DEBUG] GET Status Code (Detalhes/Serviços): {response_servicos.status_code} ---")
        response_servicos.raise_for_status()
        servicos_data = response_servicos.json()
        servicos = servicos_data.get('items', [])
        print(f"--- [DEBUG] GET Recebido {len(servicos)} serviços ---")

    except requests.exceptions.Timeout:
        print("\n--- [DEBUG] Erro: Timeout na requisição GET (detalhes) ---\n")
        flash("Erro ao carregar dados: A conexão demorou muito (Timeout).", 'danger')
        if pessoa:
             return render_template('detalhes.html', pessoa=pessoa, servicos=[], titulo=f"Detalhes de {pessoa.get('ds_nome')} (Erro ao carregar serviços)")
        else:
            return redirect(url_for('pessoa_bp.listar'))
    except requests.exceptions.RequestException as e:
        print(f"\n--- [DEBUG] Erro capturado na requisição GET (detalhes): {e} ---\n")
        flash(f"Erro ao carregar dados da API: {e}", 'danger')
        if response_pessoa is not None and response_pessoa.status_code == 404:
             flash(f"Erro: Paciente com ID {id} não encontrado.", 'danger')
        return redirect(url_for('pessoa_bp.listar'))

    return render_template('detalhes.html', pessoa=pessoa, servicos=servicos, titulo=f"Detalhes de {pessoa.get('ds_nome')}")


@pessoa_bp.route('/pessoa/<int:id>/servicos/novo', methods=['GET', 'POST'])
def novo_servico(id):
    """Adiciona um novo registro de serviço para uma pessoa específica."""
    pessoa = None
    # Busca dados da pessoa para exibir no formulário
    try:
        api_url_pessoa = f"{get_api_url()}pessoas/{id}"
        print(f"--- [DEBUG] GET (Novo Serviço/Pessoa) para: {api_url_pessoa} ---")
        response_pessoa = requests.get(api_url_pessoa, timeout=10)
        print(f"--- [DEBUG] GET Status Code (Novo Serviço/Pessoa): {response_pessoa.status_code} ---")
        response_pessoa.raise_for_status()
        pessoa = response_pessoa.json()
    except requests.exceptions.Timeout:
         print("\n--- [DEBUG] Erro: Timeout na requisição GET (novo_servico/pessoa) ---\n")
         flash("Erro ao carregar dados da pessoa: A conexão demorou muito (Timeout).", "danger")
         return redirect(url_for('pessoa_bp.listar'))
    except requests.exceptions.RequestException as e:
        print(f"\n--- [DEBUG] Erro capturado na requisição GET (novo_servico/pessoa): {e} ---\n")
        flash(f"Erro ao carregar dados da pessoa: {e}", "danger")
        if response_pessoa is not None and response_pessoa.status_code == 404:
             flash(f"Erro: Paciente com ID {id} não encontrado.", 'danger')
        return redirect(url_for('pessoa_bp.listar'))

    # Se a pessoa não foi encontrada, redireciona
    if not pessoa:
        return redirect(url_for('pessoa_bp.listar'))

    # Lógica do POST
    if request.method == 'POST':
        response = None # Inicializa response
        try:
            api_url = f"{get_api_url()}servicos/"

            # Monta payload com colunas corretas da tabela SERVICOS
            novo_servico_dado = {
                "ds_nome": request.form.get('ds_nome') or None, # Nome do serviço
                "char_descricao": request.form.get('char_descricao') or None, # Descrição
                "dt_dataservico": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), # Data atual
                "sq_idpaciente": id # Chave estrangeira para o paciente
            }

            print("\n--- [DEBUG] Enviando Payload (Serviço) ---")
            print(json.dumps(novo_servico_dado, indent=2))
            print("--- [DEBUG] PRESTES A EXECUTAR requests.post (Serviço) ---")

            # Executa POST com timeout
            response = requests.post(api_url, json=novo_servico_dado, timeout=10)
            print("--- [DEBUG] requests.post EXECUTADO (Serviço) ---")
            print(f"--- [DEBUG] API Respondeu Status (Serviço): {response.status_code} ---")

            try:
                print("--- [DEBUG] Resposta API (JSON/Serviço) ---")
                print(json.dumps(response.json(), indent=2))
            except requests.exceptions.JSONDecodeError:
                print("--- [DEBUG] Resposta API (Texto/Serviço) ---")
                print(response.text)
            print("--- [DEBUG] Fim da Resposta API (Serviço) ---\n")

            if response.status_code != 201:
                 response.raise_for_status()

            flash('Novo serviço registrado com sucesso!', 'success')
            return redirect(url_for('pessoa_bp.detalhes', id=id))

        except requests.exceptions.Timeout:
             print("\n--- [DEBUG] Erro: Timeout na requisição POST (Serviço) ---\n")
             flash("Erro ao registrar serviço: A conexão demorou muito (Timeout).", 'danger')
        except requests.exceptions.RequestException as e:
            print(f"\n--- [DEBUG] Erro capturado na requisição POST (Serviço): {e} ---\n")
            # (Lógica de mensagem de erro para POST Serviço...)
            flash(f"Erro ao registrar serviço: {e}", 'danger')

    # Re-renderiza o formulário se GET ou se POST falhou
    return render_template('novo_servico.html', pessoa=pessoa, titulo="Registrar Novo Serviço")