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
from .controller import *

from .models.Consumer import Consumer

# flask login
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    #return db.session.query(Consumer).get(int(user_id))
    #return db.session.query(Consumer).query.get(int(user_id))
    return Consumer.query.get(int(user_id))

@app.route('/', methods=['GET'])
def get_healthcheck():
    return 'shop is up.'
