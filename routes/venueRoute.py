import os
import random
import uuid
from flask import request, Blueprint, jsonify, send_file
from sqlalchemy import text

from config import db
from models.city import City
from models.venue import Venue
import pandas as pd

venue_blueprint = Blueprint('venues', __name__)


@venue_blueprint.route('/', methods=['POST'])
def create_venue():
    data = request.get_json()
    new_venue = Venue(
        name=data['name'],
        lat=data['lat'],
        long=data['long'],
        description=data.get('description'),
        type=data['type'],
        iconNum=data.get('iconNum', 1)
    )
    db.session.add(new_venue)
    db.session.commit()
    return jsonify({'message': 'Venue created successfully'}), 201


@venue_blueprint.route('/', methods=['GET'])
def get_venues():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    venues = Venue.query.paginate(page=page, per_page=per_page)
    result = []
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'name': venue.name,
            'lat': venue.lat,
            'long': venue.long,
            'description': venue.description,
            'type': venue.type,
            'iconNum': venue.iconNum
        }
        result.append(venue_data)
    return jsonify(result), 200


@venue_blueprint.route('/<int:id>', methods=['GET'])
def get_venue(id):
    venue = Venue.query.get_or_404(id)
    venue_data = {
        'id': venue.id,
        'name': venue.name,
        'lat': venue.lat,
        'long': venue.long,
        'description': venue.description,
        'type': venue.type,
        'iconNum': venue.iconNum
    }
    return jsonify(venue_data), 200


@venue_blueprint.route('/venues/<int:id>', methods=['PUT'])
def update_venue(id):
    data = request.get_json()
    venue = Venue.query.get_or_404(id)
    venue.name = data['name']
    venue.lat = data['lat']
    venue.long = data['long']
    venue.description = data.get('description')
    venue.type = data['type']
    venue.iconNum = data.get('iconNum', 1)
    db.session.commit()
    return jsonify({'message': 'Venue updated successfully'}), 200


@venue_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_venue(id):
    venue = Venue.query.get_or_404(id)
    db.session.delete(venue)
    db.session.commit()
    return jsonify({'message': 'Venue deleted successfully'}), 200


@venue_blueprint.route('/download', methods=['GET'])
def download_all_venues():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    venues = Venue.query.paginate(page=page, per_page=per_page)
    venue_data = [
        {
            'id': venue.id,
            'name': venue.name,
            'lat': venue.lat,
            'long': venue.long,
            'description': venue.description,
            'type': venue.type,
            'iconNum': venue.iconNum
        }
        for venue in venues
    ]

    df = pd.DataFrame(venue_data)
    filename = f"csv-files/{uuid.uuid4()}.csv"
    df.to_csv(filename, index=False)

    try:
        return send_file(filename, mimetype='text/csv', as_attachment=True)
    finally:
        if os.path.exists(filename):
            os.remove(filename)


@venue_blueprint.route('/from-city/<int:city_id>', methods=['GET'])
def get_venues_of_a_city(city_id):
    city = City.query.get_or_404(city_id)
    city_center_lat = city.lat
    city_center_long = city.long
    city_radius_km = city.diameter / 2

    query = text("""
        SELECT *,
        (6371 * acos(cos(radians(:lat)) * cos(radians(lat)) * cos(radians(long) - radians(:long)) + sin(radians(:lat)) * sin(radians(lat)))) AS distance
        FROM venue
        WHERE (6371 * acos(cos(radians(:lat)) * cos(radians(lat)) * cos(radians(long) - radians(:long)) + sin(radians(:lat)) * sin(radians(lat)))) <= :radius
    """)

    parameters = {'lat': city_center_lat, 'long': city_center_long, 'radius': city_radius_km}
    venues = db.session.execute(query, parameters).fetchall()

    result = []
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'name': venue.name,
            'cityName': city.name,
            'lat': venue.lat,
            'long': venue.long,
            'description': venue.description,
            'type': venue.type,
            'iconNum': venue.iconNum
        }
        result.append(venue_data)

    return jsonify(result), 200


@venue_blueprint.route('/random-from-city/<int:city_id>', methods=['GET'])
def get_random_venue_from_a_city(city_id):
    city = City.query.get_or_404(city_id)
    city_center_lat = city.lat
    city_center_long = city.long
    city_radius_km = city.diameter / 2

    query = text("""
        SELECT *,
        (6371 * acos(cos(radians(:lat)) * cos(radians(lat)) * cos(radians(long) - radians(:long)) + sin(radians(:lat)) * sin(radians(lat)))) AS distance
        FROM venue
        WHERE (6371 * acos(cos(radians(:lat)) * cos(radians(lat)) * cos(radians(long) - radians(:long)) + sin(radians(:lat)) * sin(radians(lat)))) <= :radius
    """)

    parameters = {'lat': city_center_lat, 'long': city_center_long, 'radius': city_radius_km}
    venues = db.session.execute(query, parameters).fetchall()

    if not venues:
        return jsonify({'message': 'No venues found within the specified radius.'}), 404

    random_venue = random.choice(venues)

    venue_data = {
        'id': random_venue.id,
        'name': random_venue.name,
        'cityName': city.name,
        'lat': random_venue.lat,
        'long': random_venue.long,
        'description': random_venue.description,
        'type': random_venue.type,
        'iconNum': random_venue.iconNum,
    }

    return jsonify(venue_data), 200