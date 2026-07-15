import os
import zipfile
from werkzeug.utils import secure_filename

from app.services.code_scanner import CodeScanner
from app.services.review_service import ReviewService
from app.services.project_summary_service import ProjectSummaryService
from app.services.report_aggregator_service import ReportAggregatorService


class ProjectService:

    UPLOAD_FOLDER = "uploads"
    EXTRACT_FOLDER = "extracted"

    @staticmethod
    def upload_project(file):

        print("\n========== PROJECT UPLOAD START ==========")

        if file is None:
            print("ERROR: File is None")
            return None, "No file uploaded"

        print("Received File:", file)

        filename = secure_filename(file.filename)

        if filename == "":
            print("ERROR: Empty filename")
            return None, "No file selected"

        if not filename.lower().endswith(".zip"):
            print("ERROR: Not a ZIP file")
            return None, "Only ZIP files are allowed"

        os.makedirs(ProjectService.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(ProjectService.EXTRACT_FOLDER, exist_ok=True)

        zip_path = os.path.join(ProjectService.UPLOAD_FOLDER, filename)

        print("Saving ZIP...")
        file.save(zip_path)
        print("ZIP Saved Successfully")

        extract_folder = os.path.join(
            ProjectService.EXTRACT_FOLDER,
            os.path.splitext(filename)[0]
        )

        os.makedirs(extract_folder, exist_ok=True)

        print("Extracting ZIP...")

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_folder)

            print("ZIP Extracted Successfully")

        except Exception as e:
            print("ZIP Extraction Error:", str(e))
            return None, str(e)

        print("Scanning Project...")

        try:
            files = CodeScanner.scan_project(extract_folder)

            print("Running Static Analysis...")

            review = ReviewService.review_project(files)

            print("Generating AI Project Summary...")

            project_summary = ProjectSummaryService.generate_summary(review)

            print("Building Final Report...")

            report = ReportAggregatorService.build_report(
                project_name=filename,
                review=review,
                project_summary=project_summary
            )

        except Exception as e:
            print("Scanner Error:", str(e))
            return None, str(e)

        print("========== PROJECT UPLOAD SUCCESS ==========\n")

        return report, None