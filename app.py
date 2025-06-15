from flask import Flask
from config import Config
from models import db
import click

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Comando para criar tabelas
@app.cli.command("create-tables")
def create_tables():
    with app.app_context():
        db.create_all()
    click.echo("Tabelas criadas com sucesso!")

# Importar e registrar blueprints
from pacientes.routes import pacientes_bp
from vacinas.routes import vacinas_bp
from registros.routes import registros_bp

app.register_blueprint(pacientes_bp)
app.register_blueprint(vacinas_bp)
app.register_blueprint(registros_bp)

if __name__ == '__main__':
    app.run(debug=True)
