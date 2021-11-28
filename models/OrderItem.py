from app import db


class OrderItem(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete="CASCADE"))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"))
    count = db.Column(db.Integer, nullable=False)
    worth = db.Column(db.Float, nullable=False)
