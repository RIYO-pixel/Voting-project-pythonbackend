from flask import Blueprint

utils_blueprint = Blueprint('utils', __name__)

@utils_blueprint.route('/utils_status')
def utils_status():
    return "Utils Module"
