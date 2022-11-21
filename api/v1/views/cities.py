#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from api.v1 import app
from flask import jsonify, render_template, abort, \
                    redirect, url_for, request, Response, \
                    make_response
from models import storage
import json


@app_views.route("/states/<state_id>/cities")
def cities(state_id):
    single_state = storage.get("State", state_id)
    if single_state is None:
        abort(404)
    else:
        cities = single_state.cities
    dict_cities = []
    for city in cities:
        dict_cities.append(city.to_dict())
    return jsonify(dict_cities)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    single_city = storage.get("City", city_id)
    if single_city is None:
        abort(404)
    else:
        return jsonify(single_city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    single_city = storage.get("City", city_id)
    if single_city is None:
        abort(404)
    else:
        storage.delete(single_city)
        storage.save()
        return {}, 200


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def create_city(state_id):
    single_state = storage.get("State", state_id)
    if single_state is None:
        abort(404)
    try:
        city = request.get_json()
        json.dumps(city)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    from models.city import City
    if "name" not in city.keys():
        resp = make_response(jsonify("Missing name"), 400)
        return resp
    city['state_id'] = state_id
    city_obj = City(**city)
    storage.new(city_obj)
    storage.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    try:
        city = request.get_json()
        json.dumps(city)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    from models.city import City
    single_city = storage.get("City", city_id)
    if single_city is None:
        abort(404)
    for key, value in city.items():
        if key is "id" or key is "created_at" or key is "updated_at" \
          or key is "state_id":
            pass
        else:
            setattr(single_city, key, value)
    storage.save()
    updated_city = storage.get("City", city_id)
    return jsonify(updated_city.to_dict()), 200
