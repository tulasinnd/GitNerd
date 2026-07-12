# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import os
# from dotenv import load_dotenv

# load_dotenv()

# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# app = FastAPI(
#     title="GitNerd API",
#     description="Backend foundation for the GitNerd repository learning platform.",
#     version="0.1.0",
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class RepositoryRequest(BaseModel):
#     github_url: str


# @app.post("/repository")
# def validate_repository(request: RepositoryRequest):
#     url = request.github_url

#     if not url.startswith("https://github.com/"):
#         return {
#             "valid": False,
#             "message": "Invalid GitHub repository URL."
#         }

#     return {
#         "valid": True,
#         "message": "Repository URL is valid.",
#         "repository_url": url
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI(
    title="GitNerd API",
    description="Backend foundation for the GitNerd repository learning platform.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepositoryRequest(BaseModel):
    github_url: str


@app.post("/repository")
def validate_repository(request: RepositoryRequest):

    url = request.github_url.strip()

    # ----------------------------
    # Validate URL format
    # ----------------------------
    parsed = urlparse(url)

    if parsed.scheme != "https" or parsed.netloc != "github.com":
        return {
            "valid": False,
            "message": "Invalid GitHub URL."
        }

    # ----------------------------
    # Extract owner/repository
    # ----------------------------
    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) != 2:
        return {
            "valid": False,
            "message": "Please enter a valid GitHub repository URL."
        }

    owner, repository = path_parts

    # ----------------------------
    # Call GitHub API
    # ----------------------------
    api_url = f"https://api.github.com/repos/{owner}/{repository}"

    headers = {}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.get(api_url, headers=headers)

    # ----------------------------
    # Handle GitHub response
    # ----------------------------
    if response.status_code == 200:
        return {
            "valid": True,
            "message": "Repository URL is valid.",
            "repository_url": url,
            "owner": owner,
            "repository": repository,
        }

    elif response.status_code == 404:
        return {
            "valid": False,
            "message": "Repository not found."
        }

    else:
        return {
            "valid": False,
            "message": f"GitHub API returned status code {response.status_code}."
        }