#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from api.v1 import app
from flask import jsonify, render_template, abort, \
                    redirect, url_for, request, Response, \
                    make_response
from models import storage
import json


@app_views.route("/places/<place_id>/reviews")
def reviews(place_id):
    single_place = storage.get("Place", place_id)
    if single_place is None:
        abort(404)
    else:
        reviews = single_place.reviews
    dict_reviews = []
    for review in reviews:
        dict_reviews.append(review.to_dict())
    return jsonify(dict_reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review(review_id):
    single_review = storage.get("Review", review_id)
    if single_review is None:
        abort(404)
    else:
        return jsonify(single_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    single_review = storage.get("Review", review_id)
    if single_review is None:
        abort(404)
    else:
        storage.delete(single_review)
        storage.save()
        return {}, 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def create_review(place_id):
    single_place = storage.get("Place", place_id)
    if single_place is None:
        abort(404)
    try:
        review = request.get_json()
        json.dumps(review)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    from models.review import Review
    if "text" not in review.keys():
        resp = make_response(jsonify("Missing text"), 400)
        return resp
    if "user_id" not in review.keys():
        resp = make_response(jsonify("Missing user_id"), 400)
        return resp
    else:
        single_user = storage.get("User", review['user_id'])
        if single_user is None:
            abort(404)
    review['place_id'] = place_id
    review_obj = Review(**review)
    storage.new(review_obj)
    storage.save()
    return jsonify(review_obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def update_review(review_id):
    try:
        review = request.get_json()
        json.dumps(review)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    from models.review import Review
    single_review = storage.get("Review", review_id)
    if single_review is None:
        abort(404)
    for key, value in review.items():
        if key is "id" or key is "created_at" or key is "updated_at" \
          or key is "user_id" or key is "place_id":
            pass
        else:
            setattr(single_review, key, value)
    storage.save()
    updated_review = storage.get("Review", review_id)
    return jsonify(updated_review.to_dict()), 200
