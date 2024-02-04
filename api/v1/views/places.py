#!/usr/bin/python3
"""
This file contains the Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """List places by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create new place instance"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in request.json or 'name' not in request.json:
        return make_response(jsonify({"error": "Missing user_id or name"}), 400)

    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)

    place_data = request.json
    place_data['city_id'] = city_id
    new_place = Place(**place_data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update place by ID"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search places by criteria"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = storage.all(Place).values()

    if states:
        places = [place for place in places if place.city.state_id in states]

    if cities:
        places = [place for place in places if place.city_id in cities]

    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places if amenities_set.issubset(set(am.id for am in place.amenities))]

    result_places = [place.to_dict() for place in places]
    for place in result_places:
        place.pop('amenities', None)

    return jsonify(result_places)
