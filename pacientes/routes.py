from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Paciente
from datetime import datetime
import re

pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')

def validar_cpf(cpf):
    return bool(re.fullmatch(r'\d{11}', cpf))

@pacientes_bp.route('/')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@pacientes_bp.route('/novo', methods=['GET', 'POST'])
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
                return redirect(url_for('pacientes.listar_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar paciente: {str(e)}', 'error')

    return render_template('pacientes/novo.html')

@pacientes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
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
                return redirect(url_for('pacientes.listar_pacientes'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao editar paciente: {str(e)}', 'error')

    return render_template('pacientes/editar.html', paciente=paciente)

@pacientes_bp.route('/<int:id>/excluir', methods=['POST'])
def excluir_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    try:
        db.session.delete(paciente)
        db.session.commit()
        flash('Paciente excluído com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir paciente: {str(e)}', 'error')
    return redirect(url_for('pacientes.listar_pacientes'))
