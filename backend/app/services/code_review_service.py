from app.services.review_service import ReviewService
from app.services.project_summary_service import ProjectSummaryService
from app.services.report_aggregator_service import ReportAggregatorService


class CodeReviewService:

    @staticmethod
    def review_code(code, language="python"):

        files = [
            {
                "filename": f"main.{language}",
                "content": code,
                "language": language,
            }
        ]

        review = ReviewService.review_project(
            files,
            language=language,
        )

        project_summary = ProjectSummaryService.generate_summary(review)

        report = ReportAggregatorService.build_report(
            project_name="Pasted Code",
            review=review,
            project_summary=project_summary,
        )

        return report
    