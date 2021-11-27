# from flask import jsonify, request, render_template
#
# from app import app, db
# from app.model.City import City
#
#
# @app.route('/cities', methods=['GET'])
# def get_cities():
#     cities: list[City] = City.query.all()
#     return render_template('city_view.html', cities=cities)
#
#
# @app.route('/cities', methods=['POST'])
# def add_city():
#     req_json = request.get_json()
#     try:
#         city = City(name=req_json['name'], population=req_json['population'])
#         db.session.add(city)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e
#     return 'City added to database.'
#
#
# @app.route('/cities/<city_id>', methods=['GET'])
# def get_city(city_id: str):
#     if (city := db.session.query(City).get(city_id)) is None:
#         return f'City with {city_id} id not found.'
#     else:
#         return jsonify({
#             'id': city.id,
#             'name': city.name,
#             'population': city.population
#         })
#
#
# @app.route('/cities/<city_id>', methods=['DELETE'])
# def delete_city(city_id: str):
#     if db.session.query(City).get(city_id) is None:
#         return f'City with {city_id} id not found.'
#     try:
#         City.query.filter_by(id=int(city_id)).delete()
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e
#     return f'City with {city_id} id deleted from database.'
#
#
# @app.route('/cities/<city_id>/<population>', methods=['PATCH'])
# def update_city_population(city_id: str, population: str):
#     if db.session.query(City).get(city_id) is None:
#         return f'City with {city_id} id not found.'
#     try:
#         City.query.filter_by(id=int(city_id)).update({City.population: int(population)})
#         db.session.commit()
#     except Exception as exc:
#         db.session.rollback()
#         raise exc
#     return f'City with {city_id} id has new population value: {population}.'
