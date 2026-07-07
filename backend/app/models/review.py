from datetime import datetime
from app.extensions.database import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
    )

    overall_score = db.Column(db.Float)

    quality_score = db.Column(db.Float)

    security_score = db.Column(db.Float)

    maintainability_score = db.Column(db.Float)

    complexity_score = db.Column(db.Float)

    summary = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)