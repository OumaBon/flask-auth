from flask import Blueprint



api = Blueprint("api",__name__)



@api.route('/', methods=["GET"])
def index():
    return "<h1>Welcome to flask authentication</h1>"


@api.route("/home/<name>", methods=["GET"])
def get_name(name):
    name = "Hevin"
    return "<h1>Good morning from</h1>".format({name})