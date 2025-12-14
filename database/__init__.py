from flask import Blueprint, jsonify
from .db_config import get_collection

mongo_health_bp = Blueprint("mongo_health", __name__, url_prefix="/health")

@mongo_health_bp.route("/mongo", methods=["GET"])
def mongo_health_check():
    try:
        collection = get_collection()

        # 🔥 FIX IS HERE
        if collection is None:
            return jsonify({
                "status": "error",
                "message": "MongoDB connection failed"
            }), 500

        # Lightweight read test
        collection.find_one()

        return jsonify({
            "status": "success",
            "message": "MongoDB connection successful",
            "database": collection.database.name,
            "collection": collection.name
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
