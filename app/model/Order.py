from flask_sqlalchemy import sqlalchemy

from app import db


class OrderStatus(sqlalchemy.types.Enum):
    ordered = "Ordered"
    progress = "In progress"
    delivered = "Delivered"


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    # consumer_id = db.Column(db.Integer)
    # supplier_id = db.Column(db.Integer)
    date_ordered = db.Column(db.DateTime, nullable=False)
    date_delivered = db.Column(db.DateTime)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False)
