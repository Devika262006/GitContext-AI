from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".php",
    ".html",
    ".css",
    ".scss",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
}

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


def discover_files(repository_path: str) -> list[Path]:
    """
    Discover supported source/documentation files
    while ignoring unnecessary directories.
    """

    repository = Path(repository_path)

    if not repository.exists():
        raise FileNotFoundError(
            f"Repository not found: {repository}"
        )

    discovered_files = []

    for path in repository.rglob("*"):

        if not path.is_file():
            continue

        # Ignore files inside unwanted directories
        if any(
            ignored_dir in path.parts
            for ignored_dir in IGNORED_DIRECTORIES
        ):
            continue

        # Keep only supported extensions
        # Keep supported extensions and important repository files
        important_files = {
            "README",
            "README.md",
            "README.txt",
            "LICENSE",
            "CONTRIBUTING.md",
        }

        if (
            path.name not in important_files
            and path.suffix.lower() not in SUPPORTED_EXTENSIONS
        ):
            continue

        discovered_files.append(path)
        return discovered_files


if __name__ == "__main__":

    repository_path = (
        "data/repos/Hello-World"
    )

    files = discover_files(repository_path)

    print("\nDiscovered files:")
    print("-" * 50)

    for file in files:
        print(file)

    print("-" * 50)
    print(f"Total files discovered: {len(files)}")