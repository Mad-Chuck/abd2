from flask import jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from ..models.Order import Order
from .. import app, db


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
