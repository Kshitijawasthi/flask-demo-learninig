from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from settings import Config   # ✅ IMPORTANT (direct import)
from flask_jwt_extended import JWTManager
from app.utils.errors import AppError
import os

import settings
db = SQLAlchemy()
jwt=JWTManager()

def create_app():
    app = Flask(__name__)

    env=os.getenv("FLASK_ENV")

    if(env=="development"):
        app.config.from_object(settings.DevelopmentConfig)
    else:
        app.config.from_object(settings.ProductionConfig)

    app.config["JWT_SECRET_KEY"]="super-secret-key"

    # 🔍 DEBUG
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # ✅ INIT DB
    db.init_app(app)
    jwt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.post_routes import post_bp
    from app.routes.auth import auth_bp
    from app.routes.upload import upload_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)


    # Global handlers
    @app.errorhandler(AppError)
    def handle_app_error(error):    #noqa
        return jsonify({
            "success":False,
            "message":error.message
        }), error.status_code
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return jsonify({
            "success":False,
            "message":"Internal Server Error"
        }),500

    return app