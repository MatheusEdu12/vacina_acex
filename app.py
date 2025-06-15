from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Paciente, Vacina
from datetime import datetime
import re
import click

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.cli.command("create-tables")
def create_tables():
    """Cria as tabelas no banco de dados."""
    with app.app_context():
        db.create_all()
    click.echo("Tabelas criadas com sucesso!")

# Função simples para validar CPF (só checar tamanho e dígitos aqui)
def validar_cpf(cpf):
    return bool(re.fullmatch(r'\d{11}', cpf))

@app.route('/')
def index():
    vacinas = Vacina.query.all()
    return render_template('index.html', vacinas=vacinas)

# ----------------- CRUD Paciente -----------------

@app.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@app.route('/pacientes/novo', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        cpf = request.form['cpf'].strip()
        nascimento = request.form['nascimento']
        endereco = request.form['endereco'].strip()
        telefone = request.form['telefone'].strip()

        if not nome or not cpf or not nascimento or not endereco or not telefone:
            flash('Preencha todos os campos.', 'error')
        elif not validar_cpf(cpf):
            flash('CPF inválido. Deve conter 11 dígitos numéricos.', 'error')
        else:
            try:
                nascimento_date = datetime.strptime(nascimento, '%Y-%m-%d')
                paciente = Paciente(nome=nome, cpf=cpf, nascimento=nascimento_date,
                                    endereco=endereco, telefone=telefone)
                db.session.add(paciente)
                db.session.commit()
                return redirect(url_for('listar_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar paciente: {str(e)}', 'error')

    return render_template('pacientes/novo.html')

@app.route('/pacientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    if request.method == 'POST':
        paciente.nome = request.form['nome'].strip()
        cpf = request.form['cpf'].strip()
        paciente.endereco = request.form['endereco'].strip()
        paciente.telefone = request.form['telefone'].strip()

        nascimento = request.form['nascimento']

        if not paciente.nome or not cpf or not nascimento or not paciente.endereco or not paciente.telefone:
            flash('Preencha todos os campos.', 'error')
        elif not validar_cpf(cpf):
            flash('CPF inválido. Deve conter 11 dígitos numéricos.', 'error')
        else:
            try:
                paciente.cpf = cpf
                paciente.nascimento = datetime.strptime(nascimento, '%Y-%m-%d')
                db.session.commit()
                return redirect(url_for('listar_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao editar paciente: {str(e)}', 'error')

    return render_template('pacientes/editar.html', paciente=paciente)

@app.route('/pacientes/<int:id>/excluir', methods=['POST'])
def excluir_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    try:
        db.session.delete(paciente)
        db.session.commit()
        flash('Paciente excluído com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir paciente: {str(e)}', 'error')
    return redirect(url_for('listar_pacientes'))

# ----------------- CRUD Vacina -----------------

@app.route('/vacinas')
def listar_vacinas():
    vacinas = Vacina.query.join(Paciente).all()
    return render_template('vacinas/listar.html', vacinas=vacinas)

@app.route('/vacinas/novo', methods=['GET', 'POST'])
def nova_vacina():
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        tipo = request.form['tipo'].strip()
        fabricante = request.form['fabricante'].strip()
        data_dose = request.form['data_dose']
        lote = request.form['lote'].strip()
        local_aplicacao = request.form['local_aplicacao'].strip()
        paciente_id = request.form.get('paciente_id')

        if not tipo or not fabricante or not data_dose or not lote or not local_aplicacao or not paciente_id:
            flash('Preencha todos os campos.', 'error')
        else:
            try:
                data_dose_date = datetime.strptime(data_dose, '%Y-%m-%d')
                vacina = Vacina(tipo=tipo, fabricante=fabricante, data_dose=data_dose_date,
                                lote=lote, local_aplicacao=local_aplicacao,
                                paciente_id=int(paciente_id))
                db.session.add(vacina)
                db.session.commit()
                return redirect(url_for('listar_vacinas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar vacina: {str(e)}', 'error')

    return render_template('vacinas/novo.html', pacientes=pacientes)

@app.route('/vacinas/<int:id>/editar', methods=['GET', 'POST'])
def editar_vacina(id):
    vacina = Vacina.query.get_or_404(id)
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        vacina.tipo = request.form['tipo'].strip()
        vacina.fabricante = request.form['fabricante'].strip()
        data_dose = request.form['data_dose']
        vacina.lote = request.form['lote'].strip()
        vacina.local_aplicacao = request.form['local_aplicacao'].strip()
        paciente_id = request.form.get('paciente_id')

        if not vacina.tipo or not vacina.fabricante or not data_dose or not vacina.lote or not vacina.local_aplicacao or not paciente_id:
            flash('Preencha todos os campos.', 'error')
        else:
            try:
                vacina.data_dose = datetime.strptime(data_dose, '%Y-%m-%d')
                vacina.paciente_id = int(paciente_id)
                db.session.commit()
                return redirect(url_for('listar_vacinas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao editar vacina: {str(e)}', 'error')

    return render_template('vacinas/editar.html', vacina=vacina, pacientes=pacientes)

@app.route('/vacinas/<int:id>/excluir', methods=['POST'])
def excluir_vacina(id):
    vacina = Vacina.query.get_or_404(id)
    try:
        db.session.delete(vacina)
        db.session.commit()
        flash('Vacina excluída com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir vacina: {str(e)}', 'error')
    return redirect(url_for('listar_vacinas'))
