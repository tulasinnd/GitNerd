from utils.llm_utils import get_llm
llm = get_llm()


def interview_session(
    repository_book,
    history,
):

    prompt = f"""
You are an experienced Software Engineering interviewer.

Your job is to interview a candidate about the following repository.

Repository Book:
{repository_book}

Interview History:
{history}

Generate the NEXT interview question.

Rules:
- Ask only ONE question.
- Never repeat a previous question.
- Start with easier questions and gradually increase the difficulty.
- Ask only about information present in the Repository Book.
- Do not provide answers or hints.
- Return only the interview question.
"""

    response = llm.invoke(prompt)

    return response.content


def evaluate_interview(
        repository_book,
        interview_chat_history,
):

    prompt = f"""
You are an experienced Senior Software Engineer conducting a repository interview.

Your task is to evaluate the candidate's understanding of the repository using ONLY the information provided below.

Repository Book
---------------
{repository_book}

Interview Transcript
--------------------
{interview_chat_history}

Instructions
------------
- Evaluate every answer using only the Repository Book.
- Ignore grammar and language mistakes unless they change the technical meaning.
- Reward technically correct explanations, even if they are short.
- Penalize incorrect, incomplete, or fabricated explanations.
- Consider the interview as a whole before assigning a final score.
- Keep the report concise and easy to read.
- Focus on helping the candidate understand what they know and what they should revise.
- Return the report in Markdown only.

Generate the report using EXACTLY the following format.

### Repository Interview Report

#### Repository Score
Give a score out of 100.

#### What You Know Well
List 1 to 5 repository concepts the candidate demonstrated a good understanding of.

#### What Needs Improvement
List 1 to 5 repository concepts where the candidate showed weak, incomplete, or incorrect understanding.

#### Topics to Revise
Provide a short list of the most important repository topics the candidate should revisit.
Only mention topic names, not explanations.

#### Final Feedback
Write a short paragraph (2 sentences) summarizing the candidate's repository understanding, encouraging continued learning while highlighting the most important areas to improve.
"""

    response = llm.invoke(prompt)

    return response.content
