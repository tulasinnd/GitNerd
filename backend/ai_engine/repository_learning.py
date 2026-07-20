from utils.llm_utils import get_llm
llm = get_llm()


def ask_repository_question(
    repository_book,
    question,
):
    prompt = f"""
you are a great software developer and your job is to explain any question asked in the github repository
below is the repository details
{repository_book}

here is the Question related to repository

{question}

Answer the question using only the Repository Book. 
If the question is not related to repository learning then sofly tell user its out of scope question
"""

    response = llm.invoke(prompt)

    return response.content