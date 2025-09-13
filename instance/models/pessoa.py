from app import db

class Pessoa(db.Model):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    diagnostico = db.Column(db.String(500), nullable=True)
    tratamentos = db.Column(db.String(500), nullable=True)
    medicamentos = db.Column(db.String(500), nullable=True)
    alergias = db.Column(db.String(500), nullable=True)
    historico_medico = db.Column(db.String(1000), nullable=True)
    observacoes = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"<Pessoa {self.nome} - CPF: {self.cpf}>"
    