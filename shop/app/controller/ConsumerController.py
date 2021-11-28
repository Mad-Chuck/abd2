from flask import render_template

from app import app, db


@app.route('/consumer/login', methods=['GET'])
def login():
    return render_template('login.html')\

@app.route('/consumer/logout', methods=['GET'])
def logout():
    return render_template('logout.html')