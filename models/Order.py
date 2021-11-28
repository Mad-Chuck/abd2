from sqlalchemy.orm import relationship

from .. import db


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id', ondelete="CASCADE"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', ondelete="CASCADE"), nullable=True)
    date_ordered = db.Column(db.DateTime, nullable=False)
    date_delivered = db.Column(db.DateTime)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum("created", "ordered", "in_progress", "delivered", name="order_status"), nullable=False)
    order_item = relationship("OrderItem", lazy="select")
