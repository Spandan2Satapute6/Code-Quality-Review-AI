from app.services.ai_review_service import AIReviewService
from app.services.pylint_service import PylintService
from app.services.bandit_service import BanditService
from app.services.radon_service import RadonService


class ReviewService:

    @staticmethod
    def review_project(files):

        results = []

        for file in files:

            print("Reviewing:", file["filename"])

            ai_review = AIReviewService.review_file(file)

            pylint_review = PylintService.analyze_code(file["content"])

            bandit_review = BanditService.analyze_code(file["content"])

            radon_review = RadonService.analyze_code(file["content"])

            print("Finished:", file["filename"])

            results.append({
                "filename": file["filename"],
                "path": file["path"],
                "lines": len(file["content"].splitlines()),

                "score": ai_review.get("score", 0),
                "issues": ai_review.get("issues", []),
                "suggestions": ai_review.get("suggestions", []),

                "pylint": pylint_review,
                "bandit": bandit_review,
                "radon": radon_review
            })

        return results