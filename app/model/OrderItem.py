from app import db


class OrderItem(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True)
    # order_id = db.Column(db.String(127))
    # product_id = db.Column(db.String(127))
    count = db.Column(db.Integer, nullable=False)
    worth = db.Column(db.Float, nullable=False)
