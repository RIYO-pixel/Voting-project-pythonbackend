from flask import Blueprint, request, jsonify
import base64
import numpy as np
import cv2
from deepface import DeepFace
from numpy.linalg import norm
from database.db_config import get_collection

verify_face_bp = Blueprint("verifyface", __name__, url_prefix="/face")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- UTILS ----------------
def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (norm(v1) * norm(v2)))

def load_user_embeddings(epic_no):
    collection = get_collection()

    # ✅ FIX: explicit None check
    if collection is None:
        raise Exception("Database connection failed")

    doc = collection.find_one({"epic_no": epic_no})
    if not doc:
        return []

    face_data = doc.get("face_data")

    # Case 1: face_data is list
    if isinstance(face_data, list):
        return [np.array(e, dtype=np.float32) for e in face_data]

    # Case 2: face_data is dict
    if isinstance(face_data, dict):
        return [
            np.array(e, dtype=np.float32)
            for e in face_data.get("embeddings", [])
        ]

    return []



# ---------------- VERIFY ----------------
@verify_face_bp.route("/verify", methods=["POST"])
def verify_face():
    try:
        data = request.get_json()
        epic_no = data.get("user_id")
        image_b64 = data.get("image")

        if not epic_no or not image_b64:
            return jsonify({"error": "Missing user_id or image"}), 400

        print("VERIFY → EPIC:", epic_no)
        print("Image size:", len(image_b64))

        # Decode image
        img_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image data"}), 400

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) == 0:
            return jsonify({"error": "No face detected"}), 400

        # ✅ PICK LARGEST FACE
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        x, y, w, h = faces[0]

        # ✅ REJECT SMALL FACES
        if w < 100 or h < 100:
            return jsonify({"error": "Face too small"}), 400

        roi_rgb = cv2.cvtColor(img[y:y+h, x:x+w], cv2.COLOR_BGR2RGB)

        known_embeddings = load_user_embeddings(epic_no)
        if not known_embeddings:
            return jsonify({"error": "No face embeddings found"}), 404

        input_embedding = np.array(
            DeepFace.represent(
                roi_rgb,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"],
            dtype=np.float32
        )

        # ✅ OPTIMAL THRESHOLD
        threshold = 0.62

        max_similarity = max(
            cosine_similarity(input_embedding, db_emb)
            for db_emb in known_embeddings
        )

        return jsonify({
            "verified": max_similarity >= threshold,
            "similarity": round(max_similarity, 4)
        })

    except Exception as e:
        print("❌ VERIFY ERROR:", e)
        return jsonify({"error": str(e)}), 500
