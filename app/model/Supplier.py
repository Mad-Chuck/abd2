from sqlalchemy.orm import relationship

from app import db


class Supplier(db.Model):
    __tablename__ = "supplier"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    order = relationship("Order")
