from langchain_core.messages import HumanMessage
from utils.llm_utils import get_llm

llm = get_llm()


def generate_repository_summary(repository_analysis):

    llm = get_llm()

    prompt = f"""
You are an expert software architect.

Analyze the following repository information and generate
a short summary about 100 words in a user friendly readable format in plain text only, do NOT use Markdown.
No matter how big the repositoty, just generate 100 word summary.
Repository Information:
{repository_analysis}

Explain:

1. What the project does.
2. What technologies appear to be used in the given repository.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    return response.content