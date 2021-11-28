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
        flash('Log in failed')
    else:
        login_user(user)
        flash('Logged in successfully')
    return redirect(url_for('login_form'))


@app.route('/consumer/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('login'))


@app.route('/consumer/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')


@app.route('/consumer/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    password_coded = code_password(password)
    password_confirm = request.form.get('password_confirm')

    if password != password_confirm:
        flash('Passwords do not match')
        return redirect(url_for('signup'))

    user = Consumer.query.filter_by(email=email).first()
    if not (user is None):
        flash('User already exists')
        return redirect(url_for('signup'))

    user = Consumer(email=email, password=password_coded, phone=phone)
    db.session.add(user)
    db.session.commit()

    flash("Signed up successfully. You can now log in")
    return redirect(url_for('login_form'))