from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config   # ✅ IMPORTANT (direct import)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ LOAD CONFIG
    app.config.from_object(Config)

    # 🔍 DEBUG
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # ✅ INIT DB
    db.init_app(app)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app