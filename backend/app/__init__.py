from flask import Flask
from flask_cors import CORS

from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.bcrypt import bcrypt
from app.config.config import Config
from app.extensions.migrate import migrate
from app.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    app.register_blueprint(auth_bp)

    # Health Check Route
    @app.route("/")
    def home():
        return {
            "message": "🚀 Codequality review  AI Backend is Running",
            "status": "success"
        }
        # Import models so Flask-Migrate detects them
    from app.models.user import User
    from app.models.project import Project
    from app.models.review import Review
    from app.models.finding import Finding

    return app
