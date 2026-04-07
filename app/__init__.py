from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config   # ✅ IMPORTANT (direct import)
from flask_jwt_extended import JWTManager
db = SQLAlchemy()
jwt=JWTManager()

def create_app():
    app = Flask(__name__)

    # ✅ LOAD CONFIG
    app.config.from_object(Config)

    app.config["JWT_SECRET_KEY"]="super-secret-key"

    # 🔍 DEBUG
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # ✅ INIT DB
    db.init_app(app)
    jwt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.post_routes import post_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)

    return app