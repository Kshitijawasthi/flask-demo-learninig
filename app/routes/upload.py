from flask import Blueprint,request,jsonify
from app.services.upload_service import upload_image
from app.utils.errors import AppError

upload_bp = Blueprint("upload",__name__)

@upload_bp.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")

    if not file:
        return jsonify({"error":"No file required"}),400
    
    image_url = upload_image(file)

    return jsonify({
        "success":"True",
        "url":image_url
    }),201
    
