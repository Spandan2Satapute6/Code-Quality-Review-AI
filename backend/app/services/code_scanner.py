import os


class CodeScanner:
    """
    Scans a project directory and returns only supported source code files.

    Currently, AI Review, Pylint, Bandit, and Radon support Python source files.
    """

    # Files to analyze
    ALLOWED_EXTENSIONS = (
        ".py",
        ".js",
    )

    # Directories to ignore
    IGNORED_DIRECTORIES = {
        "__pycache__",
        ".git",
        ".github",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "dist",
        "build",
        "target",
        "bin",
        "obj",
        "coverage",
        ".pytest_cache",
        "uploads",
        "extracted",
        "migrations",
    }

    @staticmethod
    def scan_project(project_path):
        files = []

        for root, dirs, filenames in os.walk(project_path):

            # Skip unnecessary directories
            dirs[:] = [
                d for d in dirs
                if d not in CodeScanner.IGNORED_DIRECTORIES
            ]

            for filename in filenames:

                # Ignore unsupported file types
                if not filename.lower().endswith(CodeScanner.ALLOWED_EXTENSIONS):
                    continue

                file_path = os.path.join(root, filename)

                try:
                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:
                        content = f.read()

                    files.append({
                        "filename": filename,
                        "path": os.path.relpath(file_path, project_path),
                        "content": content,
                    })

                except Exception as e:
                    print(f"Skipped {file_path}: {e}")

        return files