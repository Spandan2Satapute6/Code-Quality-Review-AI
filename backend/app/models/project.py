from datetime import datetime
from app.extensions.database import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    project_name = db.Column(db.String(200), nullable=False)

    upload_type = db.Column(db.String(50), nullable=False)

    language = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)