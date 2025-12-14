from flask import Flask
from flask_cors import CORS
from models import models_blueprint
from database import mongo_health_bp
from routes import routes_blueprint
from routes.registerface import face_bp
from routes.verifyface import verify_face_bp
from utils import utils_blueprint

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Registering Blueprints
app.register_blueprint(models_blueprint)
app.register_blueprint(mongo_health_bp)
app.register_blueprint(routes_blueprint)
app.register_blueprint(utils_blueprint)
app.register_blueprint(face_bp)
app.register_blueprint(verify_face_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)