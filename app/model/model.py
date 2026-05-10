from app import db 


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), index=True, unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(256),unique=True)

