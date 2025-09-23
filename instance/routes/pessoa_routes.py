# -*- coding: utf-8 -*-
"""
Blueprint para as rotas relacionadas à entidade Pessoa e seus Serviços.

Este módulo define todas as rotas e a lógica de visualização para as operações
de CRUD da entidade Pessoa, bem como as rotas para gerenciar os serviços
associados a cada pessoa.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from instance.models.pessoa import Pessoa
from instance.models.servico import Servico 

# --- Configuração do Blueprint ---

# O Blueprint permite organizar as rotas de forma modular.
# O url_prefix='/pessoas' é definido no momento do registro em app.py,
# o que significa que todas as URLs aqui são relativas a /pessoas.
pessoa_bp = Blueprint(
    'pessoa_bp',
    __name__,
    template_folder='../templates'
)

# ============================================================================
# ROTAS PARA A ENTIDADE 'PESSOA' (CRUD)
# ============================================================================

@pessoa_bp.route('/')
def listar():
    """Exibe a lista de todas as pessoas cadastradas, ordenadas por nome."""
    pessoas = Pessoa.query.order_by(Pessoa.nome).all()
    return render_template('listar.html', pessoas=pessoas)


@pessoa_bp.route('/novo', methods=['GET', 'POST'])
def novo():
    """Cria um novo registro de Pessoa no banco de dados."""
    if request.method == 'POST':
        # (Lógica de criação de pessoa...)
        nova_pessoa = Pessoa(
            nome=request.form.get('nome'),
            cpf=request.form.get('cpf'),
            idade=request.form.get('idade'),
            # ... etc.
        )
        db.session.add(nova_pessoa)
        db.session.commit()
        flash('Pessoa cadastrada com sucesso!', 'success')
        return redirect(url_for('pessoa_bp.listar'))
    
    return render_template('novo.html')


@pessoa_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Atualiza um registro de Pessoa existente."""
    pessoa = Pessoa.query.get_or_404(id)
    if request.method == 'POST':
        # (Lógica de edição de pessoa...)
        pessoa.nome = request.form.get('nome')
        # ... etc.
        db.session.commit()
        flash('Dados da pessoa atualizados com sucesso!', 'success')
        return redirect(url_for('pessoa_bp.listar'))

    return render_template('editar.html', pessoa=pessoa)


@pessoa_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """Deleta um registro de Pessoa do banco de dados."""
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    flash('Pessoa removida com sucesso!', 'success')
    return redirect(url_for('pessoa_bp.listar'))

# ============================================================================
# ROTAS PARA A ENTIDADE 'SERVIÇO' (VINCULADA A 'PESSOA')
# ============================================================================

@pessoa_bp.route('/<int:id>/')
def detalhes(id):
    """
    Exibe a página de detalhes de uma pessoa e seu histórico de serviços.
    URL: /pessoas/1/
    """
    pessoa = Pessoa.query.get_or_404(id)
    return render_template('detalhes.html', pessoa=pessoa)


@pessoa_bp.route('/<int:id>/servicos/novo', methods=['GET', 'POST'])
def novo_servico(id):
    """
    Adiciona um novo registro de serviço para uma pessoa específica.
    URL: /pessoas/1/servicos/novo
    """
    pessoa = Pessoa.query.get_or_404(id)
    if request.method == 'POST':
        nome_servico = request.form.get('nome')
        desc_servico = request.form.get('descricao')

        if not nome_servico or not desc_servico:
            flash('O nome e a descrição do serviço são obrigatórios.', 'warning')
        else:
            novo_servico = Servico(
                nome=nome_servico,
                descricao=desc_servico,
                pessoa=pessoa  # Associa o serviço à pessoa
            )
            db.session.add(novo_servico)
            db.session.commit()
            flash('Novo serviço registrado com sucesso!', 'success')
            return redirect(url_for('pessoa_bp.detalhes', id=id))
    
    # Se a requisição for GET, ou se a validação do POST falhar,
    # renderiza o formulário de novo serviço.
    return render_template('novo_servico.html', pessoa=pessoa)