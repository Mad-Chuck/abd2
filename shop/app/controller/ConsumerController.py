import flask
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .. import app, db


@app.route('/consumer/login', methods=['GET'])
def login_form():
    return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')

    user = Consumer.query.filter_by(email=email).first()
    #login_user(user)

    flash('Logged in successfully.')
    return render_template('login.html')


@app.route('/consumer/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
