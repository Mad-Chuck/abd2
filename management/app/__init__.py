from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("app.config.Config")
app.config['SECRET_KEY'] = 'secret-management'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import *
from .controller import *

from .models.Supplier import Supplier

# flask login
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return Supplier.query.get(int(user_id))
