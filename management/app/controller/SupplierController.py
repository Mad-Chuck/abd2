import hashlib
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from .. import app, db
from ..models.Supplier import Supplier


def code_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/supplier/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/supplier/login', methods=['POST'])
def login():
    id = request.form.get('id')
    password = code_password(request.form.get('password'))

    user = Supplier.query.filter_by(id=id, password=password).first()
    if user is None:
        flash('Log in failed')
    else:
        login_user(user)
        flash('Logged in successfully')
    return redirect(url_for('login_form'))


@app.route('/supplier/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('login'))
