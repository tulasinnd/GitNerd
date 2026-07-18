"""
Repository Understanding

Tasks:
1. Select important repository files.
2. Read important repository files.
3. Understand repository.
4. Create repository book.
5. Build vector knowledge base.

understand_repository()

│

├── select_important_files()

├── read_important_files()

├── understand_repository_files()

├── create_repository_book()

└── build_vector_knowledge_base()

"""

from utils.github_utils import get_repository_file
import json
from utils.llm_utils import get_llm

llm = get_llm()
def select_important_files(repository_analysis):

    prompt = f"""
        You are an expert software engineer.

        Below is the repository analysis
        Repository Information:{repository_analysis}

        Your task is to identify the most important SOURCE CODE files that are required
        to understand how this repository works. select files only present in the above repository, dont invent new files on your own

        Rules:
        - Select only source code files.
        - Ignore README.md.
        - Ignore requirements.txt.
        - Ignore package.json.
        - Ignore pyproject.toml.
        - Ignore Dockerfile.
        - Ignore images.
        - Ignore documentation.
        - Ignore configuration files.
        - Ignore test files unless they are essential.
        - Return ONLY a JSON array of file paths.
        - Do not explain your answer.

        """

    response = llm.invoke(prompt)

    result = json.loads(response.content)

    # Normalize the output
    if isinstance(result, str):
        result = [result]

    return result

def read_important_files(
    owner,
    repository,
    important_files,
):
    code_files = {}

    for file_path in important_files:

        response = get_repository_file(
            owner,
            repository,
            file_path
        )

        if response.status_code == 200:
            code_files[file_path] = response.text
        else:
            code_files[file_path] = (
                f"Unable to fetch file. Status Code: {response.status_code}"
            )

    return code_files


def create_book():
    # llm will read full view now it has full repo analysis, code files data, now the llm understands everything and generates book of info
    # about repository

    return 


def understand_repository(
    owner,
    repository,
    repository_analysis,
):

    important_files = select_important_files(
        repository_analysis
    )

    code_files = read_important_files(
        owner,
        repository,
        important_files
    )

    # repository_book = create_book(
    #     repository_analysis,
    #     code_files
    # )

    return code_files