from flask import Flask
from flask_cors import CORS

from app.config.config import Config

from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.bcrypt import bcrypt
from app.extensions.migrate import migrate

from app.routes.auth import auth_bp
from app.routes.project import project_bp
from app.routes.review import review_bp
from app.routes.report import report_bp
from app.routes.code import code_bp
from app.routes.profile import profile_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Authorization"],
    )

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(code_bp)
    app.register_blueprint(profile_bp)

    @app.route("/")
    def home():
        return {
            "message": "🚀 CodeQuality Review AI Backend is Running",
            "status": "success",
        }

    # Import models for Flask-Migrate
    from app.models.user import User
    from app.models.project import Project
    from app.models.review import Review
    from app.models.finding import Finding

    return app