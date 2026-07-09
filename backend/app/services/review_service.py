from app.services.ai_review_service import AIReviewService


class ReviewService:

    @staticmethod
    def review_project(files):

        results = []

        for file in files:

            print("Reviewing:", file["filename"])

            ai_review = AIReviewService.review_file(file)

            print("Finished:", file["filename"])

            results.append({
                "filename": file["filename"],
                "path": file["path"],
                "lines": len(file["content"].splitlines()),
                "score": ai_review.get("score", 0),
                "issues": ai_review.get("issues", []),
                "suggestions": ai_review.get("suggestions", [])
            })

        return results