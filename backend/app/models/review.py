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

    # Overall Scores
    overall_score = db.Column(db.Float, nullable=False)
    quality_score = db.Column(db.Float)
    security_score = db.Column(db.Float)
    maintainability_score = db.Column(db.Float)
    complexity_score = db.Column(db.Float)

    # AI Summary
    summary = db.Column(db.Text)

    # Complete report returned after analysis
    report_json = db.Column(db.JSON, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship
    project = db.relationship(
        "Project",
        back_populates="reviews",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "overall_score": self.overall_score,
            "quality_score": self.quality_score,
            "security_score": self.security_score,
            "maintainability_score": self.maintainability_score,
            "complexity_score": self.complexity_score,
            "summary": self.summary,
            "report_json": self.report_json,
            "created_at": self.created_at.isoformat(),
        }