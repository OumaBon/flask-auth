from flask import jsonify, request
from app.service.service import UserService
from flask_jwt_extended import jwt_required
from . import api 


user_service = UserService()


@api.route("/users", methods=["POST"])
def new_user():
    data = request.get_json()
    user, error, status_code = user_service.create_user(data)
    if error:
        return jsonify(error), status_code
    return jsonify(user), status_code


@api.route("/users", methods=["GET"])
@jwt_required()
def users():
    users,error,status_code = user_service.get_users()
    if error:
        return jsonify(error), status_code
    return jsonify(users), status_code


@api.route("/users/<int:id>", methods=["GET"])
def user(id):
    user,error, status_code = user_service.get_user(id)
    if error:
        return jsonify(error), status_code
    return jsonify(user), status_code


@api.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user,error, status_code = user_service.update_user(id, data)
    if error:
        return jsonify(error), status_code
    return jsonify(user), status_code



@api.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user,error,status_code = user_service.delete_user(id)
    if error:
        return jsonify(error), status_code
    return jsonify(user), status_code