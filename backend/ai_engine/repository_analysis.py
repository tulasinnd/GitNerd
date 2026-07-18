from utils.github_utils import (
    get_repository_file,
    get_repository_metadata,
    get_repository_contents,
    get_repository_tree
)

from .repository_summary import generate_repository_summary

"""
Milestone 2.3 — Repository Analysis

Tasks:
1. Collect repository structure.
2. Collect important repository files.
"""

def analyze_repository(
    owner: str,
    repository: str,
):

    repository_analysis = {}

    # ----------------------------------------
    # Task 1: Collect complete repository structure
    # ----------------------------------------

    response = get_repository_tree(
        owner,
        repository,
    )

    repository_tree = []

    if response.status_code == 200:

        for item in response.json()["tree"]:

            repository_tree.append({
                "path": item["path"],
                "type": item["type"],
            })

    repository_analysis["repository_structure"] = repository_tree

    # ----------------------------------------
    # Task 2: Collect important repository files
    # ----------------------------------------

    important_files = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
        "Dockerfile",
        "docker-compose.yml",
        "vite.config.js",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Cargo.toml",
        "go.mod",
        "composer.json",
        "Gemfile",
    ]

    collected_files = {}

    for file_name in important_files:

        response = get_repository_file(
            owner,
            repository,
            file_name,
        )

        if response.status_code == 200:
            collected_files[file_name] = response.text

    repository_analysis["configuration_files"] = collected_files

    summary= generate_repository_summary(repository_analysis)

    return {
    "success": True,
    "repository_analysis": repository_analysis,
    "repository_summary": summary,
    }