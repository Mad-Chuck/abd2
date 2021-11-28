from datetime import datetime
from typing import List

from flask import jsonify, request
from flask_login import login_required, current_user

from ..models.Product import Product
from ..models.OrderItem import OrderItem
from .. import app, db


@app.route('/add_order_item', methods=['POST'])
@login_required
def add_order_item():
    try:
        order_item_json = request.get_json()
        order_item = OrderItem(
            order_id=order_item_json['order_id'],
            product_id=order_item_json['product_id'],
            count=order_item_json['count'],
            worth=order_item_json['worth'],
        )
        db.session.add(order_item)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        raise exc
    return f'Order Item {order_item.id} id created.'


@app.route('/delete_order_item/<item_id>', methods=['POST'])
@login_required
def add_order_item(item_id: str):
    if db.session.query(OrderItem).get(int(item_id)) is None:
        return f'OrderItem with {item_id} id not found.'
    try:
        OrderItem.query.filter_by(id=int(item_id)).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return f'Item with {item_id} id deleted from database.'
