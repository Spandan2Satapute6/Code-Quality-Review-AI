from app.services.ai_review_service import AIReviewService
from app.services.pylint_service import PylintService
from app.services.bandit_service import BanditService
from app.services.radon_service import RadonService


class ReviewService:

    @staticmethod
    def review_project(files, language="python"):

        results = []

        for file in files:

            print("Reviewing:", file["filename"])

            ai_review = AIReviewService.review_file(file)

            # Default values for non-Python languages
            pylint_review = {
                "status": "Not Applicable",
                "message": "Pylint supports only Python."
            }

            bandit_review = {
                "status": "Not Applicable",
                "message": "Bandit supports only Python."
            }

            radon_review = {
                "status": "Not Applicable",
                "message": "Radon supports only Python."
            }

            # Run static analysis only for Python
            if language.lower() == "python":
                pylint_review = PylintService.analyze_code(file["content"])
                bandit_review = BanditService.analyze_code(file["content"])
                radon_review = RadonService.analyze_code(file["content"])

            print("Finished:", file["filename"])

            results.append({
                "filename": file["filename"],
                "path": file.get("path", ""),
                "lines": len(file["content"].splitlines()),

                "score": ai_review.get("score", 0),
                "issues": ai_review.get("issues", []),
                "suggestions": ai_review.get("suggestions", []),

                "pylint": pylint_review,
                "bandit": bandit_review,
                "radon": radon_review,
            })

        return results