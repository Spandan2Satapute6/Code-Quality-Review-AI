from app.extensions.database import db


class Finding(db.Model):
    __tablename__ = "findings"

    id = db.Column(db.Integer, primary_key=True)

    review_id = db.Column(
        db.Integer,
        db.ForeignKey("reviews.id"),
        nullable=False,
    )

    severity = db.Column(db.String(20))

    category = db.Column(db.String(50))

    issue = db.Column(db.Text)

    explanation = db.Column(db.Text)

    suggestion = db.Column(db.Text)

    file_name = db.Column(db.String(255))

    line_number = db.Column(db.Integer)