from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    vacinas = db.relationship('Vacina', backref='paciente', lazy=True)

class Vacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    fabricante = db.Column(db.String(50), nullable=False)
    data_dose = db.Column(db.Date, nullable=False)
    lote = db.Column(db.String(30))
    local_aplicacao = db.Column(db.String(100), nullable=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
