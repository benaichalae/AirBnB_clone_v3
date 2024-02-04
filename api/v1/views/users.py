#!/usr/bin/python3
"""
This file contains the User module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Get all users"""
    users_list = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user instance"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in request.json or 'password' not in request.json:
        return make_response(jsonify({"error": "Missing email or password"}), 400)

    user_data = request.json
    new_user = User(**user_data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update user by ID"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in request.json.items():
        if key not in ['id', 'email', 'created_at', 'updated']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict())
