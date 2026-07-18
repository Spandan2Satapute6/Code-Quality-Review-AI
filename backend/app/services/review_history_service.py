from app.models.review import Review


class ReviewHistoryService:

    @staticmethod
    def save_review(project_id, report):

        dashboard = report.get("dashboard", {})
        project_summary = report.get("project_summary", {})

        review = Review(
            project_id=project_id,
            overall_score=dashboard.get("overall_score", 0),
            quality_score=dashboard.get("average_score", 0),
            security_score=dashboard.get("security_issues", 0),
            maintainability_score=dashboard.get("maintainability_issues", 0),
            complexity_score=dashboard.get("performance_issues", 0),
            summary=project_summary.get("overall_summary", ""),
            report_json=report,
        )

        from app.extensions.database import db

        db.session.add(review)
        db.session.commit()

        return review

    @staticmethod
    def get_all_reviews():

        reviews = Review.query.order_by(
            Review.created_at.desc()
        ).all()

        return [review.to_dict() for review in reviews]

    @staticmethod
    def get_review(review_id):

        review = Review.query.get(review_id)

        if not review:
            return None

        return review.to_dict()

    @staticmethod
    def delete_review(review_id):

        from app.extensions.database import db

        review = Review.query.get(review_id)

        if not review:
            return False

        db.session.delete(review)
        db.session.commit()

        return True