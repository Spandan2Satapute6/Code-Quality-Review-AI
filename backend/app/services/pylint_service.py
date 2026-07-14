import json
import subprocess
import tempfile
import os


class PylintService:

    @staticmethod
    def analyze_code(code: str):

        temp_file = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".py",
                mode="w",
                encoding="utf-8"
            ) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                [
                    "pylint",
                    temp_file,
                    "--output-format=json",
                    "--score=y"
                ],
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                issues = json.loads(result.stdout)
            else:
                issues = []

            return {
                "success": True,
                "issues": issues
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)