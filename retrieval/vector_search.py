from pathlib import Path

from qdrant_client import QdrantClient

from ingestion.embedding_generator import EmbeddingGenerator


BASE_DIR = Path(__file__).resolve().parent.parent

QDRANT_PATH = BASE_DIR / "data" / "qdrant_storage"

COLLECTION_NAME = "gitcontext_code"


class VectorSearch:
    """
    Semantic search over GitContext code embeddings.
    """

    def __init__(self):

        print("Loading GitContext vector search...")

        self.client = QdrantClient(
            path=str(QDRANT_PATH)
        )

        self.embedding_generator = (
            EmbeddingGenerator()
        )

        print("Vector search ready!")

    def search(
        self,
        query: str,
        limit: int = 3
    ) -> list:

        if not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        # Convert user query into an embedding
        query_embedding = (
            self.embedding_generator
            .generate_embedding(query)
        )

        # Search Qdrant
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
            with_payload=True,
        ).points

        return results


if __name__ == "__main__":

    search_engine = VectorSearch()

    query = "How does UserManager create a user?"

    print("\nSearch Query:")
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

        payload = result.payload

        print(f"\nRESULT {index}")
        print("-" * 70)

        print(
            f"Score      : {result.score:.4f}"
        )

        print(
            f"Type       : "
            f"{payload.get('element_type')}"
        )

        print(
            f"Name       : "
            f"{payload.get('name')}"
        )

        print(
            f"Parent     : "
            f"{payload.get('parent')}"
        )

        print(
            f"File       : "
            f"{payload.get('file_path')}"
        )

        print(
            f"Lines      : "
            f"{payload.get('start_line')}-"
            f"{payload.get('end_line')}"
        )

        print("\nCode:")
        print(
            payload.get("content")
        )

    print("\n" + "=" * 70)
    print(
        f"Total results: {len(results)}"
    )