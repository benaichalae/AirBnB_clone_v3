#!/usr/bin/python3
"""
This file contains the Review module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Get reviews from a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review instance"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in request.json or 'text' not in request.json:
        return make_response(jsonify({"error": "Missing user_id or text"}), 400)

    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)

    review_data = request.json
    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    new_review.save()

    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update review by id"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated']:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(review.to_dict()))
