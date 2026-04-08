from flask import Blueprint,request,jsonify
from app import db
from app.models.user import User
import bcrypt
from flask_jwt_extended import create_access_token
from app.utils.errors import AppError

auth_bp= Blueprint("auth",__name__)

@auth_bp.route('/register',methods=['POST'])
def register():
    data=request.get_json()

    if not data.get("email"):
        raise AppError("email is required",400)
    
    if not data.get("password"):
        raise AppError("Password is required",400)

    username=data.get("username")
    email=data.get("email")
    password=data.get("password")

    # basic validation
    if not username or not email or not password:
        return AppError("All fields are required",400)
    
    existing_user = User.query.filter(
        (User.email==email) | (User.username==username)
    ).first()

    if existing_user:
        return AppError("User already exists",400)
    
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
    
    #create password for now
    new_user=User(
        username=username,
        email=email,
        password=hashed_password,
        role="user"
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()),201


@auth_bp.route('/login',methods=['POST'])
def login():
    data=request.get_json()

    email=data.get("email")
    password=data.get("password")

    if not email or not password:
        return AppError("Email and password required",401)
    
    user=User.query.filter_by(email=email).first()

    if not user:
        return AppError("Invalid Credentials",401)
    
    if not bcrypt.checkpw(password.encode("utf-8"),user.password.encode("utf-8")):
        return AppError("Invalid credentails",401)
    
    # create access token
    access_token=create_access_token(identity=str(user.id),additional_claims={"role":user.role})
    
    return jsonify({
        "message":"login successful",
        "token":access_token
    }),200

