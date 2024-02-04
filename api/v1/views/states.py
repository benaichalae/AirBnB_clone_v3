#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Get all state objects"""
    states_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new instance"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    state_data = request.json
    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update state by ID"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict())
