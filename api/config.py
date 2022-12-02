
import os,sys
from flask_appbuilder.security.manager import AUTH_DB

AUTH_TYPE = AUTH_DB

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:testpass@postgres:5432/chembl_31_TDC'

FAB_API_SWAGGER_UI=True

SECRET_KEY = 'PzMxttbFyw8NI9ek5PCqmBWiIDn7JxoK'

CSRF_ENABLED = True