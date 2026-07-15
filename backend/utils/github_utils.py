from urllib.parse import urlparse
import os, pprint
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def extract_owner_repository(url: str):

    url = url.strip()

    parsed = urlparse(url)

    if parsed.scheme != "https" or parsed.netloc != "github.com":
        return {
            "success": False,
            "message": "Invalid GitHub URL."
        }

    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) != 2:
        return {
            "success": False,
            "message": "Please enter a valid GitHub repository URL."
        }

    return {
        "success": True,
        "owner": path_parts[0],
        "repository": path_parts[1]
    }

def get_repository_file(owner: str, repository: str, file_path: str):

    url = (
        f"https://api.github.com/repos/{owner}/{repository}/contents/{file_path}"
    )

    headers = {
        "Accept": "application/vnd.github.raw"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.get(url, headers=headers)

    return response

def get_repository_metadata(
    owner: str,
    repository: str,
):
    url = (
        f"https://api.github.com/repos/{owner}/{repository}"
    )

    headers = {}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return requests.get(url, headers=headers)

def get_repository_contents(
    owner: str,
    repository: str,
):
    url = (
        f"https://api.github.com/repos/{owner}/{repository}/contents"
    )

    headers = {}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    
    #pprint.pprint(requests.get(url, headers=headers))

    return requests.get(url, headers=headers)