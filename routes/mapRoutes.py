import os
import uuid
from flask import Blueprint, send_file, request
import folium
from models.venue import Venue
from routes.iconRoute import get_folium_icon_from_id

map_blueprint = Blueprint('maps', __name__)


@map_blueprint.route('/', methods=['GET'])
def map_of_all_venues():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    venues = Venue.query.paginate(page=page, per_page=per_page)
    map = folium.Map(location=[38.4237, 27.1428], zoom_start=13)

    for venue in venues:
        folium.Marker(
            [venue.lat, venue.long],
            popup=f'| {venue.name} |\n\n{venue.description}',
            tooltip=venue.name,
            icon=get_folium_icon_from_id(venue.iconNum)
        ).add_to(map)

    map_filename = f"maps/{uuid.uuid4()}.html"
    map.save(map_filename)

    try:
        response = send_file(map_filename, mimetype='text/html')
        return response
    finally:
        if os.path.exists(map_filename):
            os.remove(map_filename)


@map_blueprint.route('/download', methods=['GET'])
def download_map_of_all_venues():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    venues = Venue.query.paginate(page=page, per_page=per_page)
    map = folium.Map(location=[38.4237, 27.1428], zoom_start=13)

    for venue in venues:
        folium.Marker(
            [venue.lat, venue.long],
            popup=venue.description,
            tooltip=venue.name,
            icon=get_folium_icon_from_id(venue.iconNum)
        ).add_to(map)

    map_filename = f"maps/{uuid.uuid4()}.html"
    map.save(map_filename)

    try:
        response = send_file(map_filename, mimetype='text/html', as_attachment=True)
        return response
    finally:
        if os.path.exists(map_filename):
            os.remove(map_filename)
