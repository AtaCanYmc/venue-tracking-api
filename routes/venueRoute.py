import csv
from io import BytesIO, StringIO
from flask import request, Blueprint, jsonify, send_file
from config import db
from models.venue import Venue

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
    venues = Venue.query.all()
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
    venues = Venue.query.all()
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

    si = StringIO()
    cw = csv.DictWriter(si, fieldnames=venue_data[0].keys())
    cw.writeheader()
    cw.writerows(venue_data)

    output = BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)

    return send_file(output, mimetype='text/csv', as_attachment=True)



