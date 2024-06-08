import os
from flask import Blueprint, jsonify, send_file
import folium

icon_blueprint = Blueprint('icons', __name__)


def get_icon_path_from_id(id):
    if id == 1:
        return 'icons/coffee-cup.png'
    elif id == 2:
        return 'icons/beer.png'


def get_folium_icon_from_id(id):
    return folium.features.CustomIcon(
        get_icon_path_from_id(id),
        icon_size=(30, 30)
    )


@icon_blueprint.route('/<int:id>', methods=['GET'])
def get_icon(id):
    icon_path = get_icon_path_from_id(id)

    if os.path.exists(icon_path):
        return send_file(icon_path)
    else:
        return jsonify({'error': 'Icon not found'}), 404
