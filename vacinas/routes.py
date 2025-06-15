from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Vacina, Paciente
from datetime import datetime

vacinas_bp = Blueprint('vacinas', __name__, url_prefix='/vacinas')

@vacinas_bp.route('/')
def listar_vacinas():
    vacinas = Vacina.query.all()
    return render_template('vacinas/listar.html', vacinas=vacinas)

@vacinas_bp.route('/novo', methods=['GET', 'POST'])
def nova_vacina():
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        tipo = request.form['tipo'].strip()
        fabricante = request.form['fabricante'].strip()

        if not tipo or not fabricante:
            flash('Preencha todos os campos.', 'error')
        else:
            try:
                vacina = Vacina(tipo=tipo, fabricante=fabricante)
                db.session.add(vacina)
                db.session.commit()
                return redirect(url_for('vacinas.listar_vacinas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar vacina: {str(e)}', 'error')

    return render_template('vacinas/novo.html', pacientes=pacientes)

@vacinas_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_vacina(id):
    vacina = Vacina.query.get_or_404(id)
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        vacina.tipo = request.form['tipo'].strip()
        vacina.fabricante = request.form['fabricante'].strip()

        if not vacina.tipo or not vacina.fabricante:
            flash('Preencha todos os campos.', 'error')
        else:
            try:
                db.session.commit()
                return redirect(url_for('vacinas.listar_vacinas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao editar vacina: {str(e)}', 'error')

    return render_template('vacinas/editar.html', vacina=vacina, pacientes=pacientes)

@vacinas_bp.route('/<int:id>/excluir', methods=['POST'])
def excluir_vacina(id):
    vacina = Vacina.query.get_or_404(id)
    try:
        db.session.delete(vacina)
        db.session.commit()
        flash('Vacina excluída com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir vacina: {str(e)}', 'error')
    return redirect(url_for('vacinas.listar_vacinas'))
