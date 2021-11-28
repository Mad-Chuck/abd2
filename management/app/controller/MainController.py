from flask import render_template

from .. import app, db


@app.route('/', methods=['GET'])
def main():
    return render_template('base.html')
