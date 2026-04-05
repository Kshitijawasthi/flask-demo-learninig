from flask import Blueprint, request, jsonify
from app.models.post import Post
from app import db  
post_bp = Blueprint('post_bp', __name__)


@post_bp.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400 
    title = data.get("title")
    content = data.get("content")
    

