from sqlalchemy.orm import relationship

from .. import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    order_item = relationship("OrderItem")
