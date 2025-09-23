# -*- coding: utf-8 -*-
"""
Define o modelo de dados para a tabela 'servicos'.

Este módulo contém a classe Servico, que mapeia a tabela 'servicos' no banco de
dados. A tabela é responsável por registrar todos os atendimentos/serviços
prestados a uma pessoa cadastrada no sistema.
"""

from app import db
from datetime import datetime

class Servico(db.Model):
    """Modelo SQLAlchemy para a entidade Servico."""
    
    # O __tablename__ define o nome exato da tabela no banco de dados.
    __tablename__ = 'servicos'

    # ---MAPEAMENTO DAS COLUNAS---

    #: Identificador único (chave primária) para cada serviço registrado.
    id = db.Column(db.Integer, primary_key=True)
    
    #: Nome ou título do serviço para fácil categorização (ex: "Cesta Básica").
    nome = db.Column(db.String(100), nullable=False)

    #: Descrição detalhada do serviço prestado.
    descricao = db.Column(db.String(255), nullable=False)

    #: Data e hora em que o serviço foi registrado. O valor padrão é o momento atual.
    data_servico = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # ---RELACIONAMENTOS---

    #: Chave estrangeira que estabelece o vínculo com a tabela 'pessoas'.
    #: Este campo armazena o 'id' da pessoa que recebeu o serviço, garantindo
    #: que cada registro de serviço esteja associado a uma única pessoa.
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)

    def __repr__(self):
        """
        Retorna uma representação em string do objeto, útil para depuração.
        """
        return f"<Servico id={self.id} nome='{self.nome}'>"