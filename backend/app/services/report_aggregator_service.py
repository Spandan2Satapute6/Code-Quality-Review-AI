from statistics import mean


class ReportAggregatorService:

    @staticmethod
    def aggregate(review_results):

        if not review_results:
            return {
                "overall_score": 0,
                "average_score": 0,
                "total_files": 0,
                "passed_files": 0,
                "failed_files": 0,
                "total_ai_issues": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "security_issues": 0,
                "performance_issues": 0,
                "maintainability_issues": 0,
                "best_practice_issues": 0
            }

        scores = []

        critical = 0
        high = 0
        medium = 0
        low = 0

        security = 0
        performance = 0
        maintainability = 0
        best_practices = 0

        total_ai_issues = 0

        passed = 0
        failed = 0

        for file in review_results:

            score = file.get("score", 0)
            scores.append(score)

            if score >= 80:
                passed += 1
            else:
                failed += 1

            severity = str(file.get("severity", "")).lower()

            if severity == "critical":
                critical += 1

            elif severity == "high":
                high += 1

            elif severity == "medium":
                medium += 1

            elif severity == "low":
                low += 1

            security += len(file.get("security", []))
            performance += len(file.get("performance", []))
            maintainability += len(file.get("maintainability", []))
            best_practices += len(file.get("best_practices", []))

            total_ai_issues += len(file.get("issues", []))

        return {

            "overall_score": round(mean(scores), 2),

            "average_score": round(mean(scores), 2),

            "total_files": len(review_results),

            "passed_files": passed,

            "failed_files": failed,

            "total_ai_issues": total_ai_issues,

            "critical": critical,

            "high": high,

            "medium": medium,

            "low": low,

            "security_issues": security,

            "performance_issues": performance,

            "maintainability_issues": maintainability,

            "best_practice_issues": best_practices
        }

    @staticmethod
    def build_report(project_name, review, project_summary):

        dashboard = ReportAggregatorService.aggregate(review)

        return {

            "project": {

                "name": project_name,

                "total_files": dashboard["total_files"]

            },

            "dashboard": dashboard,

            "project_summary": project_summary,

            "review": review

        }