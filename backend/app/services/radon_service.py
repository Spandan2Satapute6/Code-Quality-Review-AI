import subprocess
import tempfile
import os


class RadonService:

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

            cc = subprocess.run(
                ["radon", "cc", temp_file, "-j"],
                capture_output=True,
                text=True
            )

            mi = subprocess.run(
                ["radon", "mi", temp_file, "-j"],
                capture_output=True,
                text=True
            )

            raw = subprocess.run(
                ["radon", "raw", temp_file, "-j"],
                capture_output=True,
                text=True
            )

            return {
                "success": True,
                "complexity": cc.stdout,
                "maintainability": mi.stdout,
                "raw_metrics": raw.stdout
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)