from flask import jsonify
from . import api 
from app import jwt 


@jwt.expired_token_loader
def expired_token_callback(jtw_header, jwt_payload):
    return jsonify({"error": "Token has Expired"}), 401 


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid Token"}), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"error": "Authorization token mising"}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has been Revocked"}), 401


@api.errorhandler
def not_found(error):
    return jsonify({"error":"Not Found"}),404




