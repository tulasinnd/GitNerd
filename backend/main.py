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
from ai_engine.repository_interview import interview_session, evaluate_interview

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

#------------------------------------------------------
# SESSION HELPER
#------------------------------------------------------
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

class RepositoryRequest(BaseModel):
    github_url: str
#------------------------------------------------------------
# ENDPOINT FOR GITHUB URL VALIDATION
#------------------------------------------------------------
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
    "learn_chat_history": [],
    "interview_chat_history":[],
    "current_question": None,
    "score": 0
    })

    # return summary to frontend
    return {
        "success": True,
        "session_id": session_id,
        "repository_summary": analyze_repository_result["repository_summary"],
    }

#-----------------------------------------------------------
# ENDPOINTS FOR LEARNING
#-----------------------------------------------------------
class LearningRequest(BaseModel):
    session_id: str

# to make sure that repository book exists
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

# for learning chat UI
class LearningChatRequest(BaseModel):
    session_id: str
    question: str

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
        history=session["learn_chat_history"],
        question=request.question,
    )

    session["learn_chat_history"].append(
        {
            "role": "user",
            "content": request.question,
        }
    )

    session["learn_chat_history"].append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return {
        "success": True,
        "answer": answer,
    }

#----------------------------------------------------------------
# ENDPOINTS FOR INTERVIEW (current)
#-----------------------------------------------------------------

class InterviewRequest(BaseModel):
    session_id: str


@app.post("/interview")
def interview(request: InterviewRequest):

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

class InterviewChatRequest(BaseModel):
    session_id: str
    answer: str

@app.post("/interview/chat")
def interview_chat(request: InterviewChatRequest):

    session = get_session(request.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # -----------------------------
    # Start Interview
    # -----------------------------
    if session["current_question"] is None:

        introduction = """
Welcome to your GitNerd Repository Interview!

I am ready to interview you about this repository.

The interview consists of 10 repository-related questions covering different areas of the project.

I will provide the interview performance score at the end.

During the interview, please focus on answering the current question. 

This space is specially designed for interview simulation, please use Repository Learning option if you have any doubts in the repository

Let's begin.

Please introduce yourself and briefly tell me about your experience with software development and this repository.
"""

        session["current_question"] = introduction

        return {
            "success": True,
            "question": introduction,
            "interview_completed": False,
        }

    # -----------------------------
    # Ignore accidental empty requests
    # -----------------------------
    if request.answer.strip() == "":
        return {
            "success": True,
            "question": session["current_question"],
            "interview_completed": False,
        }

    # -----------------------------
    # Save previous question + answer
    # -----------------------------
    session["interview_chat_history"].append({
        "question": session["current_question"],
        "answer": request.answer,
    })

    # -----------------------------
    # Interview completed?
    # -----------------------------
    if len(session["interview_chat_history"]) >= 5:

        interview_feedback = evaluate_interview(
            repository_book=session["repository_book"],
            interview_chat_history=session["interview_chat_history"],
        )

        return {
            "success": True,
            "interview_completed": True,
            "feedback": interview_feedback,
        }

    # -----------------------------
    # Generate next repository question
    # -----------------------------
    question = interview_session(
        repository_book=session["repository_book"],
        history=session["interview_chat_history"],
    )

    session["current_question"] = question

    return {
        "success": True,
        "question": question,
        "interview_completed": False,
    }