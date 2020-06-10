from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()
db.init_app(app)

migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run()
