from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from urllib.parse import urlparse
import pprint

from ai_engine.repository_access import access_repository
from ai_engine.repository_analysis import analyze_repository
from utils.github_utils import extract_owner_repository

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

    # check ulr through parsing and then extract owner and repository name (dont waste API call for trivial things)
    result = extract_owner_repository(request.github_url)
    if not result["success"]: # if the url is not a githubrepo then return the error in url
        return result
    owner = result["owner"]
    repository = result["repository"]

    # once url is correct then check url through github API, it will check if exists, is it accessable ... 
    access_repository_result = access_repository(owner, repository)

    # if the above function returns the repo structure then it will go for further analysis like extact readme, configs, technologies...
    if not access_repository_result["success"]:
        return access_repository_result
    
    analyze_repository_result = analyze_repository(owner, repository)

    return analyze_repository_result

