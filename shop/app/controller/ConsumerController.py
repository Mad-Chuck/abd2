import hashlib
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from .. import app, db
from ..models.Consumer import Consumer


def code_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/consumer/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/consumer/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = code_password(request.form.get('password'))

    user = Consumer.query.filter_by(email=email, password=password).first()
    if user is None:
        flash('Login failed')
    else:
        login_user(user)
        flash('Login successful')
    return render_template('login.html')

@app.route('/consumer/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
