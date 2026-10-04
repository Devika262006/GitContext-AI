from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class CodeDocument:
    """
    Standard document format used by GitContext
    before embedding and vector storage.
    """

    content: str

    repository: str

    file_path: str

    element_type: str

    name: str

    parent: Optional[str]

    start_line: int

    end_line: int

    language: str = "python"

    source: str = "github"


def create_document(chunk: dict, repository: str) -> CodeDocument:
    """
    Convert a raw code chunk into a standardized CodeDocument.
    """

    return CodeDocument(
        content=chunk["code"],
        repository=repository,
        file_path=chunk["file_path"],
        element_type=chunk["type"],
        name=chunk["name"],
        parent=chunk["parent"],
        start_line=chunk["start_line"],
        end_line=chunk["end_line"],
    )


def document_to_dict(document: CodeDocument) -> dict:
    """
    Convert CodeDocument into a dictionary.
    """

    return asdict(document)


if __name__ == "__main__":

    sample_chunk = {
        "type": "method",
        "name": "create_user",
        "parent": "UserManager",
        "file_path": "data/sample_test.py",
        "start_line": 3,
        "end_line": 4,
        "code": (
            "def create_user(self, name):\n"
            '    return {"name": name}'
        ),
    }

    document = create_document(
        sample_chunk,
        repository="Hello-World"
    )

    print("\nGitContext Document")
    print("=" * 60)

    document_dict = document_to_dict(document)

    for key, value in document_dict.items():
        print(f"{key:15}: {value}")

    print("=" * 60)