import re
from app.models.model import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_load,validates, ValidationError



class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User 
        include_relationships = True
        load_instance = True
        include_fk = True
        fields = ("id", "username", "email", "created_at", "password")
        dump_only = ("id", "created_at")
        load_only = ("password")
    
    password = fields.String(required=True, load_only=True)


    @validates("email")
    def validate_email(self, value, **kargs):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Invalid Email")
    
    @validates('username')
    def validate_username(self, value, **kargs):
        if len(value) < 3:
            raise ValidationError("Username must be more than 3 characters")
    

    @post_load
    def hash_password(self, data, **kwargs):
        if "password" in data:
            user =User()
            user.set_password(data['password'])
            data['password_hash'] = user.password_hash
            del data['password']
        return data 




