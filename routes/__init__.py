from flask import Blueprint

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/default')
def home():
    return "Hello, World!"