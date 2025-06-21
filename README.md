# 💉 Vacina ACEX

Aplicação web feita com Flask para gerenciamento de pacientes e vacinas, desenvolvida no contexto do projeto de extensão da ACEX (Ação Curricular de Extensão).

---

## ⚙️ Tecnologias utilizadas

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- MySQL (com PyMySQL)
- Bootstrap (via templates HTML)
- MySQL Workbench (opcional, para gerenciar o banco)

---

## 📦 Requisitos

- Python instalado ([baixar aqui](https://www.python.org/downloads/))
- MySQL Server local funcionando (ex: via XAMPP, MySQL Workbench, etc.)
- Git (para clonar o projeto)

---

## 🚀 Como executar a aplicação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd vacina_acex
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  (Linux/macOS)
```
### 3. Instale as dependências

```bash
pip install -r requirements.txt
```
Caso não tenha o arquivo requirements.txt, crie com:
```bash
pip freeze > requirements.txt
```

### 4. Configure o banco de dados MySQL
#### 4.1 Crie o banco vacinadb no MySQL
Você pode usar o MySQL Workbench:
```sql
CREATE DATABASE vacinadb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
#### 4.2 (Opcional) Criar um usuário para uso da aplicação
```sql
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON vacinadb.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
```
#### 4.3 Atualize a string de conexão no config.py
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:123456@localhost/vacinadb'
```

#### 5. Crie as tabelas no banco
```bash
flask create-tables
```
### 6. Rode a aplicação
```bash
python app.py
```
Acesse em http://127.0.0.1:5000

## 📁 Estrutura do projeto
```csharp
vacina_acex/
│
├── app.py                  # Arquivo principal da aplicação
├── config.py               # Configurações do Flask e banco de dados
├── models.py               # Modelos (ORM SQLAlchemy)
├── pacientes/              # Blueprint de pacientes
├── vacinas/                # Blueprint de vacinas
├── registros/              # Blueprint de registros de vacinação
├── templates/              # Templates HTML (Jinja2)
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
└── requirements.txt        # Lista de dependências
```

## 🧪 Teste rápido
1. Acesse http://127.0.0.1:5000
2. Cadastre pacientes, vacinas e registre aplicações

## 📝 Licença
Este projeto é livre para uso acadêmico e educacional.
