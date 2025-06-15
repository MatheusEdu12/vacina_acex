from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PacienteVacina(db.Model):
    __tablename__ = 'paciente_vacina'
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), primary_key=True)
    vacina_id = db.Column(db.Integer, db.ForeignKey('vacina.id'), primary_key=True)
    data_dose = db.Column(db.Date, nullable=False)
    lote = db.Column(db.String(30))
    local_aplicacao = db.Column(db.String(100))

    paciente = db.relationship('Paciente', back_populates='vacinas_assoc')
    vacina = db.relationship('Vacina', back_populates='pacientes_assoc')

class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    vacinas_assoc = db.relationship('PacienteVacina', back_populates='paciente')
    vacinas = db.relationship('Vacina', secondary='paciente_vacina', back_populates='pacientes')

class Vacina(db.Model):
    __tablename__ = 'vacina'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    fabricante = db.Column(db.String(50), nullable=False)

    pacientes_assoc = db.relationship('PacienteVacina', back_populates='vacina')
    pacientes = db.relationship('Paciente', secondary='paciente_vacina', back_populates='vacinas')

