# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:senha@localhost/vacinadb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave_secreta_segura'
