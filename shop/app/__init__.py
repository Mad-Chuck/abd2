from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("app.config.Config")
app.config['SECRET_KEY'] = 'secret-shop'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import *

# flask login
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return Consumer.get(user_id)

from .controller import *

@app.route('/', methods=['GET'])
def get_healthcheck():
    return 'shop is up.'
