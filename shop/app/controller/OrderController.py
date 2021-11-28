from datetime import datetime
from typing import List

from flask import jsonify, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from ..models.Product import Product
from ..models.Order import Order
from .. import app, db


@app.route('/orders_history', methods=['GET'])
@login_required
def orders_history():
    orders = (db.session
              .query(Order)
              .filter(Order.consumer_id == current_user.id)
              .all())

    return render_template('orders_history.html', orders=orders)


@app.route('/place_order', methods=['GET'])
@login_required
def place_order_form():
    order = _get_created_order()
    products = _get_products()

    # todo: add template with buttons:
    #   Add product -> POST /add_order_item
    #   Delete product -> GET /delete_order_item/<order_item_id>
    #   Place order -> POST /patch_order/<order_id>
    #
    # return jsonify({
    #     'id': order.id,
    #     'name': order.status,
    #     'products number': len(products)
    # })

    return render_template('place_order.html', order=order, products=products)


@app.route('/patch_order/<order_id>', methods=['POST'])
def patch_order(order_id: str):
    if db.session.query(Order).get(int(order_id)) is None:
        return f'Order with {order_id} id not found.'

    try:
        Order.query.filter_by(id=int(order_id)).update({
            'date_ordered': datetime.now(),
            'lat': float(request.form.get('lat')),
            'lon': float(request.form.get('lon')),
            'status': request.form.get('status'), # todo: add method for status update
        })
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        raise exc
    return redirect(url_for('orders_history'))


def _get_created_order() -> Order:
    """Search for users created order in database or create new if not exist"""

    order = (db.session
             .query(Order)
             .filter(Order.status == 'created' and Order.consumer_id == current_user.id)
             .first())

    if order is None:
        order = Order(consumer_id=current_user.id, status='created')
        db.session.add(order)
        db.session.commit()
    return order


def _get_products() -> List[Product]:
    return db.session.query(Product).all()
