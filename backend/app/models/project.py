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

    project_name = db.Column(
        db.String(200),
        nullable=False,
    )

    upload_type = db.Column(
        db.String(50),
        nullable=False,
    )

    language = db.Column(
        db.String(50),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with Review
    reviews = db.relationship(
        "Review",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            
            "id": self.id,
            "user_id": self.user_id,
            "project_name": self.project_name,
            "upload_type": self.upload_type,
            "language": self.language,
            "created_at": self.created_at.isoformat(),
        }