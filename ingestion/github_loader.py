import os
import shutil
from pathlib import Path
from urllib.parse import urlparse

from git import Repo


BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR / "data" / "repos"


def get_repository_name(repo_url: str) -> str:
    """
    Extract repository name from a GitHub URL.
    """

    parsed_url = urlparse(repo_url)
    repository_name = Path(parsed_url.path).stem

    if not repository_name:
        raise ValueError("Invalid GitHub repository URL.")

    return repository_name


def clone_repository(repo_url: str) -> str:
    """
    Clone a GitHub repository into the local data/repos directory.
    """

    repository_name = get_repository_name(repo_url)

    target_path = REPO_DIR / repository_name

    REPO_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing repository if already cloned
    if target_path.exists():
        shutil.rmtree(target_path)

    print(f"Cloning repository: {repo_url}")
    print(f"Target directory: {target_path}")

    Repo.clone_from(repo_url, target_path)

    print("Repository cloned successfully!")

    return str(target_path)


if __name__ == "__main__":

    # Test repository
    test_repo_url = "https://github.com/octocat/Hello-World.git"

    cloned_path = clone_repository(test_repo_url)

    print(f"\nRepository available at:")
    print(cloned_path)