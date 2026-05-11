from app import jwt
from app.service.redis_service import redis_token_service
from flask import request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt
from datetime import datetime 
from . import api 
from app.service.auth_service import auth


@jwt.token_in_blocklist_loader
def check_if_token_is_revocked(jwt_header, jwt_payload):
    jti = jwt_payload.get('jti')
    if not jti:
        return False 
    return redis_token_service.is_blacklisted(jti)


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username') or data.get('email')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Login Credentials Required"}), 400
    
    result, error , status_code = auth.login(username,password)
    if error:
        return jsonify(error), status_code
    return jsonify(result), status_code


@api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt_data = get_jwt()
    jti = jwt_data.get('jti')
    exp = jwt_data.get('exp')
    expires_in = max(0, exp - int(datetime.utcnow().timestamp()))
    
    result, error, status_code = auth.logout(jti, expires_in)
    if error:
        return jsonify(error), status_code
    return jsonify(result), status_code
    

@api.route("/logout_all", methods=["POST"])
@jwt_required()
def logout_all_devices():
    user_id = get_jwt_identity()
    success, error, status_code = auth.logout_all_devices(user_id)
    if error:
        return jsonify(error),status_code
    return jsonify(success),status_code
       



@api.route("/reset_password", methods=["POST"])
def reset_password():
    pass 


@api.route("/forget_password", methods=["POST"])
def forget_password():
    pass 




