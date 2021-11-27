from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.model import *
from app.controller.CityController import *

app = Flask(__name__)
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET'])
def get_healthcheck():
    return 'service is up.'


"""
from app import db

db.drop_all()
db.create_all()
db.session.commit()
"""
