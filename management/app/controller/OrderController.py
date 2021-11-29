from datetime import datetime
from operator import and_, or_
from typing import List

from flask import jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, extract

from ..models.OrderItem import OrderItem
from ..models.Supplier import Supplier
from ..models.Product import Product
from ..models.Order import Order
from .. import app, db


@app.route('/time_it', methods=['GET'])
def time_it():
    order = (db.session.query(Order).filter(Order.id == 2).first())

    start1 = datetime.now()
    _get_nearest_supplier(order)
    time_delta1 = datetime.now() - start1
    start2 = datetime.now()
    _get_inflation_price()
    time_delta2 = datetime.now() - start2

    return f'time1: {time_delta1}, time2: {time_delta2}'


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


@app.route('/orders_history', methods=['GET'])
@login_required
def orders_history_form():
    orders = (db.session
              .query(Order)
              .filter(Order.status == 'in_progress' and Order.supplier_id == current_user.id)
              .all())
    return render_template('orders_history.html', orders=orders)


@app.route('/order_delivered/<order_id>', methods=['POST'])
@login_required
def orders_history(order_id: str):
    if (order := db.session.query(Order).get(int(order_id))) is None:
        return f'Order with {order_id} id not found.'
    elif order.consumer_id != current_user.id:
        return f'Invalid user.'

    try:
        Order.query.filter_by(id=int(order_id)).update({
            'status': 'delivered',
        })
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        raise exc
    flash('Order delivered.')
    return redirect(url_for('orders_history_form'))


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


def _get_inflation_price():
    product: Product = (db.session
                        .query(Product)
                        .select_from(Product)
                        .join(OrderItem, Product.id == OrderItem.product_id)
                        .join(Order, Order.id == OrderItem.id)
                        .filter(extract('year', Order.date_ordered) == 2001)
                        .group_by(Product.id, Product.name, Product.price)
                        .order_by(func.sum(OrderItem.count).desc())
                        .first())
    product.price = int(106.8 * product.price) / 100
    db.session.commit()
