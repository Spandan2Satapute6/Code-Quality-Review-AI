from datetime import datetime


class ReportAggregatorService:

    @staticmethod
    def build_report(project_name, review, project_summary):

        total_files = len(review)

        total_lines = sum(
            file.get("lines", 0)
            for file in review
        )

        average_score = 0

        if total_files > 0:
            average_score = round(
                sum(file.get("score", 0) for file in review)
                / total_files,
                2
            )

        return {

            "metadata": {

                "project_name": project_name,

                "generated_at": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

                "report_version": "1.0",

                "total_files": total_files,

                "total_lines": total_lines,

                "average_score": average_score
            },

            "summary": project_summary,

            "analysis": {

                "files": review

            }
        }