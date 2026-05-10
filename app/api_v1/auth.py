from app import jwt
from flask import request, jsonify
from . import api 

from app.service.service import UserService


auth = UserService()


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
def logout():
    pass 

@api.route("/reset_password", methods=["POST"])
def reset_password():
    pass 




