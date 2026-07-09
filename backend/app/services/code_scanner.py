import os


class CodeScanner:

    ALLOWED_EXTENSIONS = (
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".html",
        ".css",
        ".sql",
        ".json",
        ".xml",
    )

    @staticmethod
    def scan_project(project_path):

        files = []

        for root, dirs, filenames in os.walk(project_path):

            dirs[:] = [
                d for d in dirs
                if d not in (
                    "__pycache__",
                    ".git",
                    "node_modules",
                    ".venv",
                    "venv"
                )
            ]

            for filename in filenames:

                if filename.endswith(CodeScanner.ALLOWED_EXTENSIONS):

                    path = os.path.join(root, filename)

                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()

                        files.append({
                            "filename": filename,
                            "path": path,
                            "content": content
                        })

                    except Exception:
                        pass

        return files