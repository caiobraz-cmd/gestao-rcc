"""
Modelo de Dados - Pessoa.

Este módulo define a estrutura de dados para a entidade Pessoa.
Nota: Como estamos consumindo uma API REST (Oracle ORDS), este modelo
serve apenas como referência da estrutura de dados, não como ORM.
"""


class Pessoa:
    """
    Classe que representa uma Pessoa no sistema.
    
    Atributos mapeiam os campos da API do Oracle ORDS.
    """
    
    def __init__(self, **kwargs):
        """
        Inicializa uma instância de Pessoa.
        
        Args:
            **kwargs: Dicionário com os campos da pessoa
        """
        self.id = kwargs.get('id')
        self.ds_nome = kwargs.get('ds_nome')
        self.num_cpf = kwargs.get('num_cpf')
        self.dt_nascimento = kwargs.get('dt_nascimento')
        self.num_telefone = kwargs.get('num_telefone')
        self.char_endereco = kwargs.get('char_endereco')
        self.char_diagnostico = kwargs.get('char_diagnostico')
        self.char_tratamento = kwargs.get('char_tratamento')
        self.char_medicamento = kwargs.get('char_medicamento')
        self.char_alergia = kwargs.get('char_alergia')
        self.char_observacoes = kwargs.get('char_observacoes')
        self.data_obito = kwargs.get('data_obito')

    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            'id': self.id,
            'ds_nome': self.ds_nome,
            'num_cpf': self.num_cpf,
            'dt_nascimento': self.dt_nascimento,
            'num_telefone': self.num_telefone,
            'char_endereco': self.char_endereco,
            'char_diagnostico': self.char_diagnostico,
            'char_tratamento': self.char_tratamento,
            'char_medicamento': self.char_medicamento,
            'char_alergia': self.char_alergia,
            'char_observacoes': self.char_observacoes,
            'data_obito': self.data_obito
        }

    def __repr__(self):
        return f"<Pessoa {self.ds_nome} - CPF: {self.num_cpf}>"
