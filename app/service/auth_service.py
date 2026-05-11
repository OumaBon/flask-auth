from flask_jwt_extended import (create_access_token, create_refresh_token,get_jwt, get_jti)
from . service import user_schema

from datetime import datetime 
from app.models.model import User
from app import db
from app.service.redis_service import redis_token_service


class AuthService:
    def login(self,username_or_email, password):
        try:
            user=User.query.filter((User.username==username_or_email) |
                                   (User.email == username_or_email)).first()
            if not user or not user.verify_password(password):
                return None, {"error": "Invalid Credentials"}, 401
            
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_schema.dump(user)} , None, 200

        except Exception as err:
            db.session.rollback()
            return None, {"error": str(err)},500
        
        
    def logout(self, access_token_jti, expires_in_seconds):
        success = redis_token_service.add_to_blacklist(
            access_token_jti, expires_in_seconds
        )
        if success:
            return {"message": "Logout out Successfully"}, None, 200
        return None, {"error": "Logout Failed"}, 500
    
    
    def logout_all_devices(self, user_id):
        success = redis_token_service.revoke_all_user_tokens(user_id)
        if success:
            return None, {"Message": "All Devices Loggout Successfully"}, 200
        return None, {"error": "Logout Failed"}, 500
            
        
            






auth = AuthService()