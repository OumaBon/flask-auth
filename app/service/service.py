from app.schema.schema import UserSchema
from app.models.model import User
from app import db 
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (create_access_token,create_refresh_token,get_jwt, get_jwt_identity)


class UserService:
    def __init__(self):
       self.users_schema= UserSchema(many=True)
       self.user_schema = UserSchema()


    def create_user(self, data):
        try:
            user = self.user_schema.load(data, session=db.session)
            db.session.add(user)
            db.session.commit()
            return self.user_schema.dump(user), None,201
        
        except ValidationError as err:
            db.session.rollback()
            return err.messages, 400
        
        except IntegrityError as err:
            db.session.rollback()
            if "username" in str(err):
                return None, {"username": ["username Already Exists"]}, 409
            elif "email" in str(err):
                return None, {"email": ["Email Already Exists"]}, 409
            return None, {"error": "Database Unvailable"}, 409
        
        except Exception as err:
            db.session.rollback()
            return None, {"error": str(err)},500
    

    def get_user(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return None, {"error": "Not Found"}, 404
            return self.user_schema.dump(user),None, 200
        
        except Exception as err:
            return None, {"error": str(err)}, 500
        
     


    def get_users(self):
        users = User.query.all()
        return self.users_schema.dump(users), None,200
    

    def update_user(self, user_id, data):
        try:
            user = User.query.get(user_id)
            if not user:
                return None, {"error": "User Not Found"}, 404
            
            password = data.pop("password", None)

            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user,key, value)
            if password:
                user.set_password(password)
            db.session.commit()
            return self.user_schema.dump(user),None, 200
        

        except ValidationError as err:
            db.session.rollback()
            return None, err.messages, 400   


        except Exception as err:
            db.session.rollback()
            return None, {"error": str(err)}, 500
    


    def delete_user(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return None, {"error": "User Not Found"}, 404
            
            db.session.delete(user)
            db.session.commit()
            return None, {"message": "User Delete Successfully"}, 200
        except Exception as err:
            db.session.rollback()
            return None, {"error": str(err)}, 500
    

    def login(self, email_or_username, password):
        try:
            user = User.query.filter(
                (User.username==email_or_username)|
                (User.email==email_or_username)
            ).first()
            if not user:
                return None, {"error":"Invalid Credentials"},401
            
            if not user.verify_password(password):
                return None, {"error": "Invalid email/username or password"}, 401
            
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": self.user_schema.dump(user)
            }, None, 200
        
        except Exception as err:
            db.session.rollback()
            return None,{"error": str(err)},500
    
    def logout(self,token_jti):
        try:
            self.blacklisted_tokens.add(token_jti)
            return {"message": "Logout Successful"}, None, 200
        except Exception as err:
            return None, {"error": str(err)}, 500


            
        

    





user_schema  = UserSchema()

    
            
    
        
            


        
