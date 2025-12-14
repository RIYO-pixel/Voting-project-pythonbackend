from flask import Blueprint, request, jsonify
import base64
import numpy as np
import cv2
from deepface import DeepFace

face_bp = Blueprint("face", __name__, url_prefix="/api")

@face_bp.route("/register_face", methods=["POST"])
def register_face():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        face_data_list = data.get("face_data")

        if not user_id or not face_data_list or not isinstance(face_data_list, list):
            return jsonify({"status": "error", "message": "Invalid request data"}), 400

        embeddings = []

        for face_data_base64 in face_data_list:
            # Remove base64 prefix if present
            if face_data_base64.startswith("data:image"):
                face_data_base64 = face_data_base64.split(",")[1]

            # Decode base64 string to byte data
            face_bytes = base64.b64decode(face_data_base64)
            np_arr = np.frombuffer(face_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Convert to grayscale for face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            if len(faces) > 0:
                # Extract the first face only
                (x, y, w, h) = faces[0]
                face_image = frame[y:y+h, x:x+w]

                # Convert BGR to RGB as required by DeepFace
                face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

                # Get face embedding from DeepFace (Facenet model)
                embedding_obj = DeepFace.represent(face_rgb, model_name='Facenet', enforce_detection=False)[0]["embedding"]
                embeddings.append(embedding_obj)

        if not embeddings:
            return jsonify({"status": "error", "message": "No valid face embeddings generated"}), 400

        return jsonify({
            "status": "success",
            "user_id": user_id,
            "embeddings": embeddings
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
