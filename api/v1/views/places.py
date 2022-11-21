#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from api.v1 import app
from flask import jsonify, render_template, abort, \
                    redirect, url_for, request, Response, \
                    make_response
from models import storage
import json


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    single_city = storage.get("City", city_id)
    if single_city is None:
        abort(404)
    else:
        places = single_city.places
    dict_places = []
    for place in places:
        dict_places.append(place.to_dict())
    return jsonify(dict_places)


@app_views.route("/places/<place_id>", methods=['GET'])
def get_place(place_id):
    single_place = storage.get("Place", place_id)
    if single_place is None:
        abort(404)
    else:
        return jsonify(single_place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    single_place = storage.get("Place", place_id)
    if single_place is None:
        abort(404)
    else:
        storage.delete(single_place)
        storage.save()
        return {}, 200


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def create_place(city_id):
    single_city = storage.get("City", city_id)
    if single_city is None:
        abort(404)
    try:
        place = request.get_json()
        json.dumps(place)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    if "user_id" not in place.keys():
        resp = make_response(jsonify("Missing user_id"), 400)
        return resp
    else:
        single_user = storage.get("User", place['user_id'])
        if single_user is None:
            abort(404)
    from models.place import Place
    if "name" not in place.keys():
        resp = make_response(jsonify("Missing name"), 400)
        return resp
    place['city_id'] = city_id
    place_obj = Place(**place)
    storage.new(place_obj)
    storage.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def update_place(place_id):
    try:
        place = request.get_json()
        json.dumps(place)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    from models.place import Place
    single_place = storage.get("Place", place_id)
    if single_place is None:
        abort(404)
    for key, value in place.items():
        if key is "id" or key is "created_at" or key is "updated_at" \
          or key is "user_id" or key is "city_id":
            pass
        else:
            setattr(single_place, key, value)
    storage.save()
    updated_place = storage.get("Place", place_id)
    return jsonify(updated_place.to_dict()), 200
