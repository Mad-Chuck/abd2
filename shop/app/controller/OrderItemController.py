from datetime import datetime
from typing import List

from flask import jsonify, request, flash, url_for, redirect
from flask_login import login_required, current_user

from ..models.Product import Product
from ..models.OrderItem import OrderItem
from .. import app, db


@app.route('/add_order_item', methods=['POST'])
@login_required
def add_order_item():
    order_id = request.form.get('order_id')
    product_id = request.form.get('product_id')
    count = request.form.get('count')
    worth = request.form.get('worth')

    try:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            count=count,
            worth=worth
        )
        db.session.add(order_item)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        raise exc
    flash('Item added to order')
    return redirect(url_for('place_order_form'))


@app.route('/delete_order_item/<item_id>', methods=['POST'])
@login_required
def delete_order_item(item_id: str):
    if db.session.query(OrderItem).get(int(item_id)) is None:
        return f'OrderItem with {item_id} id not found.'
    try:
        OrderItem.query.filter_by(id=int(item_id)).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    flash('Item deleted from order')
    return redirect(url_for('place_order_form'))
