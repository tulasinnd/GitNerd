from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import HTTPException

from ai_engine.repository_access import access_repository
from ai_engine.repository_analysis import analyze_repository
from utils.github_utils import extract_owner_repository
from database.session_manager import create_session, get_session
from ai_engine.repository_understanding import understand_repository
from ai_engine.repository_learning import ask_repository_question

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

# ENDPOINT FOR URL VALIDATION
@app.post("/repository")
def validate_repository(request: RepositoryRequest):

    # Validate URL without API call
    result = extract_owner_repository(request.github_url)

    if not result["success"]:
        return result

    owner = result["owner"]
    repository = result["repository"]

    # Verify repository exists with github API call
    access_repository_result = access_repository(owner, repository)

    if not access_repository_result["success"]:
        return access_repository_result

    # Analyze repository by collecting info from repo and generate a short analysis summary
    analyze_repository_result = analyze_repository(
        owner,
        repository,
    )

    # create session
    session_id = create_session({
    "owner": owner,
    "repository": repository,
    "repository_analysis": analyze_repository_result["repository_analysis"],
    "repository_summary": analyze_repository_result["repository_summary"],
    "repository_book": None,
    })

    # return summary to frontend
    return {
        "success": True,
        "session_id": session_id,
        "repository_summary": analyze_repository_result["repository_summary"],
    }

# Session Helper
def get_or_create_repository_book(session):

    if session["repository_book"] is not None:
        return session["repository_book"]

    repository_book = understand_repository(
        owner=session["owner"],
        repository=session["repository"],
        repository_analysis=session["repository_analysis"],
    )

    session["repository_book"] = repository_book

    return repository_book


# ENDPOINT FOR LEARNING
class LearningRequest(BaseModel):
    session_id: str

@app.post("/learning")
def learning(request: LearningRequest):

    session = get_session(request.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Ensure the Repository Book exists
    get_or_create_repository_book(session)

    return {
    "success": True
        }

# endpoint for learning chat
class LearningChatRequest(BaseModel):
    session_id: str
    question: str

# @app.post("/learning/chat")
# def learning_chat(request: LearningChatRequest):

#     session = get_session(request.session_id)

#     if session is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Session not found"
#         )

#     # Ensure the Repository Book exists
#     get_or_create_repository_book(session)

#     return {
#         "success": True,
#         "answer": f"You asked: {request.question}"
#     }

@app.post("/learning/chat")
def learning_chat(request: LearningChatRequest):

    session = get_session(request.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    get_or_create_repository_book(session)

    answer = ask_repository_question(
        repository_book=session["repository_book"],
        question=request.question,
    )

    return {
        "success": True,
        "answer": answer,
    }