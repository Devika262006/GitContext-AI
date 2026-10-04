from pathlib import Path
import re

from rank_bm25 import BM25Okapi

from ingestion.code_chunker import extract_code_chunks
from ingestion.document_schema import create_document


BASE_DIR = Path(__file__).resolve().parent.parent

TEST_FILE = BASE_DIR / "data" / "sample_test.py"


class BM25Search:
    """
    Keyword-based search using BM25.
    """

    def __init__(self, documents: list[dict]):

        self.documents = documents

        # Tokenize document content
        tokenized_documents = [
            self.tokenize(
                document["content"]
            )
            for document in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

        print(
            f"BM25 index created with "
            f"{len(documents)} documents."
        )

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """
        Tokenize code while preserving useful
        identifiers such as create_user.
        """

        return re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*",
            text.lower()
        )

    def search(
        self,
        query: str,
        limit: int = 3
    ) -> list[dict]:

        if not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        query_tokens = self.tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices[:limit]:

            document = self.documents[index].copy()

            document["score"] = float(
                scores[index]
            )

            results.append(document)

        return results


def load_test_documents() -> list[dict]:
    """
    Load structure-aware code chunks
    as searchable documents.
    """

    chunks = extract_code_chunks(
        str(TEST_FILE)
    )

    documents = []

    for chunk in chunks:

        document = create_document(
            chunk,
            repository="GitContext-Test"
        )

        documents.append({
            "content": document.content,
            "repository": document.repository,
            "file_path": document.file_path,
            "element_type": document.element_type,
            "name": document.name,
            "parent": document.parent,
            "start_line": document.start_line,
            "end_line": document.end_line,
            "language": document.language,
            "source": document.source,
        })

    return documents


if __name__ == "__main__":

    print("\nGitContext BM25 Keyword Search")
    print("=" * 70)

    documents = load_test_documents()

    search_engine = BM25Search(
        documents
    )

    query = "create_user"

    print(f"\nSearch Query:")
    print(query)

    print("\nSearch Results")
    print("=" * 70)

    results = search_engine.search(
        query,
        limit=3
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(f"\nRESULT {index}")
        print("-" * 70)

        print(
            f"Score      : "
            f"{result['score']:.4f}"
        )

        print(
            f"Type       : "
            f"{result['element_type']}"
        )

        print(
            f"Name       : "
            f"{result['name']}"
        )

        print(
            f"Parent     : "
            f"{result['parent']}"
        )

        print(
            f"Lines      : "
            f"{result['start_line']}-"
            f"{result['end_line']}"
        )

        print("\nCode:")
        print(result["content"])

    print("\n" + "=" * 70)

    print(
        f"Total results: {len(results)}"
    )