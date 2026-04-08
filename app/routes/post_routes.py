from flask import Blueprint, request, jsonify
from app.models.post import Post
from app import db
from app.utils.errors import AppError  
post_bp = Blueprint('post_bp', __name__,url_prefix='/posts')
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt

@post_bp.route('', methods=['POST'])
@jwt_required()
def add_post():
    data = request.get_json(silent=True)
    if not data:
        return AppError("Invalid JSON",400) 
    user_id=int(get_jwt_identity())
    post=Post(
    title = data.get("title"),
    content = data.get("content"),
    user_id = user_id
    )
    db.session.add(post)
    db.session.commit() 
    return jsonify(post.to_dict()), 201

# get all posts
@post_bp.route('', methods=['GET'])
def get_all_posts():
    posts= Post.query.all()
    return jsonify([p.to_dict() for p in posts]), 200

@post_bp.route('/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_post(id):
    user_id=get_jwt_identity()
    claims=get_jwt()
    role=claims.get("role")

    post= Post.query.get(id)

    if not post:
        return AppError("Post not found",404)
    
    if post.user_id != int(user_id) and role!="admin":
        return AppError("Not allowed",403)
    
    db.session.delete(post)
    db.session.commit()

    return {"message":"deleted sucessfully"}

