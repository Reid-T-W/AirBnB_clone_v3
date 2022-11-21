#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from api.v1 import app
from flask import jsonify, render_template, abort, \
                    redirect, url_for, request, Response, \
                    make_response
from models import storage
import json


@app_views.route("/users")
def users():
    all_users = storage.all("User")
    dict_all_users = []
    for key, value in all_users.items():
        dict_all_users.append(value.to_dict())
    return jsonify(dict_all_users)


@app_views.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    single_user = storage.get("User", user_id)
    if single_user is None:
        abort(404)
    else:
        return jsonify(single_user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    single_user = storage.get("User", user_id)
    if single_user is None:
        abort(404)
    else:
        storage.delete(single_user)
        storage.save()
        return {}, 200


@app_views.route("/users", methods=['POST'])
def create_user():
    try:
        user = request.get_json()
        json.dumps(user)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
    from models.user import User
    if "email" not in user.keys():
        resp = make_response(jsonify("Missing email"), 400)
        return resp
    if "password" not in user.keys():
        resp = make_response(jsonify("Missing password"), 400)
        return resp
    user_obj = User(**user)
    storage.new(user_obj)
    storage.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    try:
        user = request.get_json()
        json.dumps(user)
    except Exception:
        resp = make_response(jsonify("Not a JSON"), 400)
        return resp
    from models.user import User
    single_user = storage.get("User", user_id)
    if single_user is None:
        abort(404)
    for key, value in user.items():
        if key is "id" or key is "created_at" or key is "updated_at" \
          or key is "email":
            pass
        else:
            setattr(single_user, key, value)
    storage.save()
    updated_user = storage.get("User", user_id)
    return jsonify(updated_user.to_dict()), 200
