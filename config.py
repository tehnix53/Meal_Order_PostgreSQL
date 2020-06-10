db_path = "postgresql://postgres:postgres@127.0.0.1:5432/test6"


class Config:
    DEBUG = True
    SECRET_KEY = "randomstring"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False


''''
app.secret_key = "randomstring"
app.config["SQLALCHEMY_DATABASE_URI"] = \
    ("postgresql://postgres:postgres@127.0.0.1:5432/test6")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''''