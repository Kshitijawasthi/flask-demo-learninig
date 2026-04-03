from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import settings

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ LOAD CONFIG FIRST
    app.config.from_object(settings.Config)

    # 🔍 DEBUG (add this)
    print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # ✅ THEN INIT DB
    db.init_app(app)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app