#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from api.v1 import app
from flask import jsonify, render_template, abort, \
                    redirect, url_for, request, Response, \
                    make_response
from models import storage
import json


@app_views.route("/amenities")
def amenities():
    all_amenities = storage.all("Amenity")
    dict_all_amenities = []
    for key, value in all_amenities.items():
        dict_all_amenities.append(value.to_dict())
    return jsonify(dict_all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_state(amenity_id):
    single_amenity = storage.get("Amenity", amenity_id)
    if single_amenity is None:
        abort(404)
    else:
        return jsonify(single_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_state(amenity_id):
    single_amenity = storage.get("Amenity", amenity_id)
    if single_amenity is None:
        abort(404)
    else:
        storage.delete(single_amenity)
        storage.save()
        return {}, 200


@app_views.route("/amenities", methods=['POST'])
def create_state():
    try:
        amenity = request.get_json()
        json.dumps(amenity)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
    from models.amenity import Amenity
    if "name" not in amenity.keys():
        resp = make_response(jsonify("Missing name"), 400)
        return resp
    amenity_obj = Amenity(**amenity)
    storage.new(amenity_obj)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_state(amenity_id):
    try:
        amenity = request.get_json()
        json.dumps(amenity)
    except Exception:
        resp = make_response(jsonify("Missing name"), 400)
        return resp
    from models.amenity import Amenity
    single_amenity = storage.get("Amentiy", amenity_id)
    if single_amenity is None:
        abort(404)
    for key, value in amenity.items():
        if key is "id" or key is "created_at" or key is "updated_at":
            pass
        else:
            setattr(single_amenity, key, value)
    storage.save()
    updated_amenity = storage.get("Amenity", amenity_id)
    return jsonify(updated_amenity.to_dict()), 200
