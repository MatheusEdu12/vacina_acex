from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Paciente, Vacina, PacienteVacina
from datetime import datetime

registros_bp = Blueprint('registros', __name__)

@registros_bp.route('/', methods=['GET', 'POST'])
def index():
    pacientes = Paciente.query.all()
    vacinas = Vacina.query.all()
    registros = PacienteVacina.query.all()

    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        vacina_id = request.form.get('vacina_id')
        data_dose = request.form.get('data_dose')
        lote = request.form.get('lote')
        local_aplicacao = request.form.get('local_aplicacao')

        if not paciente_id or not vacina_id or not data_dose:
            flash("Preencha paciente, vacina e data da dose", "error")
        else:
            try:
                data_dose_date = datetime.strptime(data_dose, '%Y-%m-%d')
                registro = PacienteVacina(
                    paciente_id=int(paciente_id),
                    vacina_id=int(vacina_id),
                    data_dose=data_dose_date,
                    lote=lote,
                    local_aplicacao=local_aplicacao
                )
                db.session.add(registro)
                db.session.commit()
                flash("Registro criado com sucesso", "success")
                return redirect(url_for('registros.index'))
            except Exception as e:
                db.session.rollback()
                flash(f"Erro ao salvar registro: {str(e)}", "error")

    return render_template('index.html', pacientes=pacientes, vacinas=vacinas, registros=registros)
