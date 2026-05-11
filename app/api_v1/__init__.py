from flask import Blueprint



api = Blueprint("api",__name__)



@api.route('/', methods=["GET"])
def index():
    return "<h1>Welcome to flask authentication</h1>"



from . import auth, users, errors