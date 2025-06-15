class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/vacinadb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'chave_simples'
