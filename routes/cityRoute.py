from flask import jsonify, request, Blueprint
from config import db
from models.city import City

city_blueprint = Blueprint('cities', __name__)


# Create City
@city_blueprint.route('/', methods=['POST'])
def create_city():
    data = request.get_json()
    new_city = City(
        name=data['name'],
        lat=data['lat'],
        long=data['long'],
        diameter=data.get('diameter')
    )
    db.session.add(new_city)
    db.session.commit()
    return jsonify({'message': 'City created successfully'}), 201


# Read all Cities
@city_blueprint.route('/', methods=['GET'])
def get_cities():
    cities = City.query.all()
    result = []
    for city in cities:
        city_data = {
            'id': city.id,
            'name': city.name,
            'lat': city.lat,
            'long': city.long,
            'diameter': city.diameter
        }
        result.append(city_data)
    return jsonify(result), 200


# Read single City
@city_blueprint.route('/<int:id>', methods=['GET'])
def get_city(id):
    city = City.query.get_or_404(id)
    city_data = {
        'id': city.id,
        'name': city.name,
        'lat': city.lat,
        'long': city.long,
        'diameter': city.diameter
    }
    return jsonify(city_data), 200


# Update City
@city_blueprint.route('/<int:id>', methods=['PUT'])
def update_city(id):
    data = request.get_json()
    city = City.query.get_or_404(id)
    city.name = data['name']
    city.lat = data['lat']
    city.long = data['long']
    city.diameter = data.get('diameter')
    db.session.commit()
    return jsonify({'message': 'City updated successfully'}), 200


# Delete City
@city_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_city(id):
    city = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    return jsonify({'message': 'City deleted successfully'}), 200


