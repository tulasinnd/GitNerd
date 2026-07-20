# Repository Book

# ├── repository_information
# │      ├── Overview
# │      ├── Technologies
# │      ├── Folder Structure
# │      ├── Configuration
# │      ├── Architecture
# │      └── Component Overview
# │
# ├── source_file_chapters
# │      ├── main.py
# │      ├── app.py
# │      ├── service.py
# │      └── ...
# │
# └── repository_relationships
#        ├── Relationships
#        ├── Execution Flow
#        └── Final Summary


from utils.llm_utils import get_llm
import json

llm = get_llm()


def create_repository_information(
    repository_analysis,
):

    prompt = f"""
You are an expert software engineer and technical writer.

Using the repository analysis below, generate the Repository Information.

Repository Analysis:
{repository_analysis}

Generate the following sections:

1. Repository Overview
   - What is the repository?
   - What problem does it solve?
   - What are its main features?

2. Technologies
   - Programming languages
   - Frameworks
   - Libraries
   - Tools

3. Folder Structure
   - Explain the purpose of the important folders.

4. Configuration
   - Explain the important configuration files.
   - Explain dependencies and environment configuration.

5. Architecture
   - Describe the high-level architecture.
   - Explain how the major parts of the project are organized.

6. Component Overview
   - Explain the major components/modules of the repository.
   - Describe the responsibility of each component.

Return ONLY valid JSON in the following format.

{{
    "overview": "...",
    "technologies": "...",
    "folder_structure": "...",
    "configuration": "...",
    "architecture": "...",
    "component_overview": "..."
}}

Rules:
- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT wrap the JSON inside ```json.
- Do NOT include any explanation.
"""

    response = llm.invoke(prompt)

    # print(response.content)

    try:
        repository_information = json.loads(response.content)
    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON for repository information.\n\nResponse:\n{response.content}"
        )

    return repository_information

def create_source_file_chapter(
    repository_analysis,
    file_path,
    file_content,
):

    prompt = f"""
You are an expert software engineer and technical writer.

Repository Analysis:
{repository_analysis}

Source File:
{file_path}

Source Code:
{file_content}

Generate a detailed chapter for this source file.

Include:

1. Purpose
2. Responsibilities
3. Important Classes with code snippet used in repository
4. Important Functions with code snippet used in repository
5. Dependencies
6. Summary

Return ONLY valid JSON in the following format.

{{
    "file_path": "{file_path}",
    "purpose": "...",
    "responsibilities": "...",
    "important_classes": "...",
    "important_functions": "...",
    "dependencies": "...",
    "summary": "..."
}}

Rules:
- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT wrap the JSON inside ```json.
- Do NOT include any explanation.
"""

    response = llm.invoke(prompt)

    try:
        chapter = json.loads(response.content)
    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON.\n\nResponse:\n{response.content}"
        )

    return chapter


def create_source_file_chapters(
    repository_analysis,
    code_files,
):

    source_file_chapters = []

    # Process only the first 5 files for now
    for file_path, file_content in list(code_files.items())[:5]:

        chapter = create_source_file_chapter(
            repository_analysis,
            file_path,
            file_content,
        )

        source_file_chapters.append(chapter)

    return source_file_chapters

def create_repository_relationships(
    repository_information,
    source_file_chapters,
):

    prompt = f"""
You are an expert software architect.

Repository Information:
{repository_information}

Source File Chapters:
{source_file_chapters}

Using the information above, generate the repository relationships.

Generate the following sections:

1. Relationships
   - Explain how the major source files interact.
   - Describe dependencies between components.
   - Explain the overall structure.

2. Execution Flow
   - Describe the execution flow from the application's entry point.
   - Explain how control moves through the repository.

3. Final Summary
   - Summarize the repository.
   - Explain how all components work together.

Return ONLY valid JSON in the following format.

{{
    "relationships": "...",
    "execution_flow": "...",
    "final_summary": "..."
}}

Rules:
- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT wrap the JSON inside ```json.
- Do NOT include any explanation.
"""

    response = llm.invoke(prompt)

    try:
        repository_relationships = json.loads(
            response.content
        )
    except json.JSONDecodeError:
        raise ValueError(
            f"LLM returned invalid JSON.\n\nResponse:\n{response.content}"
        )

    return repository_relationships


def create_book(
    repository_analysis,
    code_files,
):

    repository_book = {}

    # -----------------------------------------
    # Repository Information
    # -----------------------------------------

    repository_information = create_repository_information(
        repository_analysis
    )

    repository_book["repository_information"] = (
        repository_information
    )

    # -----------------------------------------
    # Source File Chapters
    # -----------------------------------------

    source_file_chapters = create_source_file_chapters(
        repository_analysis,
        code_files,
    )

    repository_book["source_file_chapters"] = (
        source_file_chapters
    )

    # -----------------------------------------
    # Repository Relationships 
    # -----------------------------------------

    repository_relationships = create_repository_relationships(
        repository_information,
        source_file_chapters,
    )

    repository_book["repository_relationships"] = (
        repository_relationships
    )

    return repository_book