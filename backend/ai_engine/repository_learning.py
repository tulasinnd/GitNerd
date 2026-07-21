from utils.llm_utils import get_llm
llm = get_llm()


def ask_repository_question(
    repository_book,
    history,
    question,
):
    prompt = f"""
you are a great software developer and your job is to explain any question asked in the github repository
below is the repository details
{repository_book}

the previous chats are
{history}

here is the Question related to repository

{question}

Answer the question in context with chat history provided if applicable
Answer the question using only the Repository Book. 
Answer any technical definitions or concepts you know related to repository only
If the question is not related to repository learning then sofly tell user its out of scope question
give very short and direct answers.
"""

    response = llm.invoke(prompt)

    return response.content