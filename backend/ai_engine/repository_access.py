import os
import requests
from dotenv import load_dotenv
from utils.github_utils import get_repository_contents
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def access_repository(owner: str, repository: str):

    response = get_repository_contents(owner, repository)

    if response.status_code == 200:
        return {
            "success": True,
            "message": "We are inside repo"
        }

    elif response.status_code == 404:
        return {
            "success": False,
            "message": "Repository not found or is private."
        }

    elif response.status_code == 403:
        return {
            "success": False,
            "message": "GitHub API rate limit exceeded."
        }

    return {
        "success": False,
        "message": f"GitHub API returned {response.status_code}."
    }