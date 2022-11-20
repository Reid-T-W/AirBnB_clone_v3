#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from flask import jsonify, render_template, abort, \
                    redirect, url_for, request, Response, \
                    make_response
from models import storage
import json


@app_views.route("/states")
def states():
    all_states = storage.all("State")
    dict_all_states = []
    for key, value in all_states.items():
        dict_all_states.append(value.to_dict())
    return jsonify(dict_all_states)


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state(state_id):
    single_state = storage.get("State", state_id)
    if single_state is None:
        abort(404)
    else:
        return jsonify(single_state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    single_state = storage.get("State", state_id)
    if single_state is None:
        abort(404)
    else:
        storage.delete(single_state)
        storage.save()
        return {}, 200


@app_views.route("/states", methods=['POST'])
def create_state():
    try:
        state = request.get_json()
        json.dumps(state)
    except Exception:
        resp = make_response("Not a JSON\n", 400)
        return resp
    from models.state import State
    if "name" not in state.keys():
        resp = make_response("Missing name\n", 400)
        return resp
    state_obj = State(**state)
    storage.new(state_obj)
    storage.save()
    return jsonify(state_obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def update_state(state_id):
    try:
        state = request.get_json()
        json.dumps(state)
    except Exception:
        resp = make_response("Missing name\n", 400)
        return resp
    from models.state import State
    single_state = storage.get("State", state_id)
    if single_state is None:
        abort(404)
    for key, value in state.items():
        if key is "id" or key is "created_at" or key is "updated_at":
            pass
        else:
            setattr(single_state, key, value)
    storage.save()
    updated_state = storage.get("State", state_id)
    return jsonify(updated_state.to_dict()), 200
