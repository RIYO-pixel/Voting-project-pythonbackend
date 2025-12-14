from flask import Blueprint

models_blueprint = Blueprint('models', __name__)

@models_blueprint.route('/models_status')
def models_status():
    return "Models are up and running"
