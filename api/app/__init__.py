
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

from . import model_api


