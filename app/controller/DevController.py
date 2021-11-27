"""For develop purpose only"""

from app import app, db


@app.route('/recreate-db', methods=['PATCH'])
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return 'Database recreated.'


@app.route('/drop-db', methods=['DELETE'])
def drop_db():
    db.drop_all()
    db.session.commit()
    return 'Database deleted.'
