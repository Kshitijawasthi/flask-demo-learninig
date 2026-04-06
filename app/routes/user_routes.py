# app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from app.models.user_model import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/api')

# CREATE
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email required"}), 400

    user = User(name=name, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


# READ ALL
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

# get user + posts
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_with_post(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "posts": [p.to_dict() for p in user.posts]
    }), 200
