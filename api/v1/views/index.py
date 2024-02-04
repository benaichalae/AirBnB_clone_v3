#!/usr/bin/python3
"""Routing File"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@ app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})


@ app_views.route('/stats', strict_slashes=False)
def count():
    """Retrieves the number of each object by type."""
    objects_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(objects_count)
