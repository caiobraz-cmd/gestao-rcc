# -*- coding: utf-8 -*-
"""
Define o modelo de dados para a tabela 'pessoas'.

Este módulo contém a classe Pessoa, que mapeia a tabela 'pessoas' no banco de
dados. Esta tabela é a entidade central do sistema, armazenando os dados
cadastrais e médicos dos indivíduos atendidos.
"""

from app import db
# Importar 'Servico' é uma boa prática para garantir que o Python conheça
# o modelo antes de estabelecer o relacionamento.
from .servico import Servico

class Pessoa(db.Model):
    """Modelo SQLAlchemy para a entidade Pessoa."""
    
    # O __tablename__ define o nome exato da tabela no banco de dados.
    __tablename__ = 'pessoas'

    # ---MAPEAMENTO DAS COLUNAS---

    #: Identificador único (chave primária) para cada pessoa.
    id = db.Column(db.Integer, primary_key=True)
    
    #: Nome completo da pessoa.
    nome = db.Column(db.String(100), nullable=False)
    
    #: CPF (Cadastro de Pessoa Física), deve ser único para cada pessoa.
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    
    #: Idade da pessoa em anos.
    idade = db.Column(db.Integer, nullable=False)
    
    #: Telefone de contato (opcional).
    telefone = db.Column(db.String(15), nullable=True)
    
    #: Endereço residencial (opcional).
    endereco = db.Column(db.String(200), nullable=True)
    
    #: Descrição do diagnóstico médico (opcional).
    diagnostico = db.Column(db.String(500), nullable=True)
    
    #: Tratamentos médicos realizados ou em curso (opcional).
    tratamentos = db.Column(db.String(500), nullable=True)
    
    #: Medicamentos de uso contínuo (opcional).
    medicamentos = db.Column(db.String(500), nullable=True)
    
    #: Registro de alergias conhecidas (opcional).
    alergias = db.Column(db.String(500), nullable=True)
    
    #: Resumo do histórico médico relevante (opcional).
    historico_medico = db.Column(db.String(1000), nullable=True)
    
    #: Campo livre para observações gerais (opcional).
    observacoes = db.Column(db.String(1000), nullable=True)

    # ---RELACIONAMENTOS---

    #: Define a relação "Um-para-Muitos" com o modelo Servico.
    #: Isso cria um atributo 'servicos' em cada objeto Pessoa, que conterá
    #: uma lista de todos os serviços associados a essa pessoa.
    #: - backref='pessoa': cria um atributo 'pessoa' em cada objeto Servico.
    #: - lazy=True: os serviços só são carregados do banco quando acessados.
    #: - cascade: se uma pessoa for deletada, todos os seus serviços
    #:   associados também serão deletados automaticamente.
    servicos = db.relationship('Servico', backref='pessoa', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        """
        Retorna uma representação em string do objeto, útil para depuração.
        """
        return f"<Pessoa id={self.id} nome='{self.nome}'>"