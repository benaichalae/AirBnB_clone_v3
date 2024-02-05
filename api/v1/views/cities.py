#!/usr/bin/python3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
"""
This file contains the City module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Get cities for state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create new city instance"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    city_data = request.json
    new_city = City(**city_data)
    new_city.state_id = state.id
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update city by ID"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
