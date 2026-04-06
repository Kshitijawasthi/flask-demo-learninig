from flask import Blueprint, request, jsonify
from app.models.post import Post
from app import db  
post_bp = Blueprint('post_bp', __name__)


@post_bp.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400 
    post=Post(
    title = data.get("title"),
    content = data.get("content"),
    user_id = data.get("user_id"),
    )
    db.session.add(post)
    db.session.commit() 
    return jsonify(post.to_dict()), 201

# get all posts
@post_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts= Post.query.all()
    return jsonify([p.to_dict() for p in posts]), 200


