from datetime import datetime
from operator import or_
from typing import List

from flask import jsonify, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, and_

from ..models.Supplier import Supplier
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

    return render_template('place_order.html', order=order, products=products)


@app.route('/patch_order/<order_id>', methods=['POST'])
@login_required
def patch_order(order_id: str):
    if (order := db.session.query(Order).get(int(order_id))) is None:
        return f'Order with {order_id} id not found.'
    elif order.consumer_id != current_user.id:
        return f'Invalid user.'

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


@app.route('/update_order_status', methods=['GET'])
@login_required
def update_status():
    orders: List[Order] = db.session.query(Order).filter(Order.status == 'ordered').all()
    counter = 0

    for order in orders:
        supplier = _get_nearest_supplier(order)
        if supplier is not None:
            Order.query.filter_by(id=int(order.id)).update({
                'supplier_id': supplier.id,
                'status': 'in_progress',
            })
            counter += 1
    db.session.commit()
    return f'{counter} orders updated'


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


def _get_nearest_supplier(order: Order) -> Supplier:
    supplier = (db.session
                .query(Supplier)
                .select_from(Supplier)
                .outerjoin(Order, Supplier.id == Order.supplier_id)
                .filter(and_(or_(Order.status == 'in_progress', Order.status == None),
                             func.sqrt(
                                 func.pow(Supplier.lat - order.lat, 2) + func.pow(Supplier.lon - order.lon, 2)) < 0.05))
                .group_by(Supplier.id, Supplier.lat, Supplier.lon)
                .having(func.count(Order.id) <= 5)
                .order_by(func.sqrt(func.pow(Supplier.lat - order.lat, 2) + func.pow(Supplier.lon - order.lon, 2)))
                .first())
    return supplier
