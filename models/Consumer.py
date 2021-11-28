from sqlalchemy.orm import relationship
from flask_login import UserMixin

from .. import db


class Consumer(db.Model, UserMixin):
    __tablename__ = "consumer"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    order = relationship("Order")