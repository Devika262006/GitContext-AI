from pathlib import Path

from retrieval.vector_search import VectorSearch
from retrieval.bm25_search import (
    BM25Search,
    load_test_documents,
)


BASE_DIR = Path(__file__).resolve().parent.parent


class HybridSearch:
    """
    Combines semantic vector search and BM25
    keyword search.
    """

    def __init__(self):

        print("Initializing Hybrid Search...")

        # Semantic search
        self.vector_search = VectorSearch()

        # BM25 documents
        documents = load_test_documents()

        self.bm25_search = BM25Search(
            documents
        )

        print("Hybrid Search ready!")

    @staticmethod
    def normalize_scores(
        results: list[dict],
        score_key: str
    ) -> list[dict]:
        """
        Normalize scores between 0 and 1.
        """

        if not results:
            return []

        scores = [
            result[score_key]
            for result in results
        ]

        min_score = min(scores)
        max_score = max(scores)

        # All scores are equal
        if max_score == min_score:

            for result in results:
                result["normalized_score"] = 1.0

            return results

        for result in results:

            result["normalized_score"] = (
                (result[score_key] - min_score)
                / (max_score - min_score)
            )

        return results

    def search(
        self,
        query: str,
        limit: int = 3,
        vector_weight: float = 0.6,
        keyword_weight: float = 0.4,
    ) -> list[dict]:

        # -------------------------
        # 1. Vector Search
        # -------------------------

        vector_results = (
            self.vector_search.search(
                query,
                limit=limit
            )
        )

        vector_data = []

        for result in vector_results:

            payload = result.payload

            vector_data.append({
                "key": (
                    payload.get("file_path"),
                    payload.get("start_line"),
                    payload.get("end_line"),
                ),
                "content": payload.get("content"),
                "repository": payload.get("repository"),
                "file_path": payload.get("file_path"),
                "element_type": payload.get("element_type"),
                "name": payload.get("name"),
                "parent": payload.get("parent"),
                "start_line": payload.get("start_line"),
                "end_line": payload.get("end_line"),
                "vector_score": float(
                    result.score
                ),
            })

        # -------------------------
        # 2. BM25 Search
        # -------------------------

        bm25_results = (
            self.bm25_search.search(
                query,
                limit=limit
            )
        )

        keyword_data = []

        for result in bm25_results:

            keyword_data.append({
                "key": (
                    result["file_path"],
                    result["start_line"],
                    result["end_line"],
                ),
                "content": result["content"],
                "repository": result["repository"],
                "file_path": result["file_path"],
                "element_type": result["element_type"],
                "name": result["name"],
                "parent": result["parent"],
                "start_line": result["start_line"],
                "end_line": result["end_line"],
                "keyword_score": float(
                    result["score"]
                ),
            })

        # -------------------------
        # 3. Normalize Scores
        # -------------------------

        vector_data = self.normalize_scores(
            vector_data,
            "vector_score"
        )

        keyword_data = self.normalize_scores(
            keyword_data,
            "keyword_score"
        )

        # -------------------------
        # 4. Merge Results
        # -------------------------

        combined = {}

        for result in vector_data:

            key = result["key"]

            combined[key] = result

            combined[key][
                "vector_normalized"
            ] = result[
                "normalized_score"
            ]

            combined[key][
                "keyword_normalized"
            ] = 0.0

        for result in keyword_data:

            key = result["key"]

            if key not in combined:

                combined[key] = result

                combined[key][
                    "vector_normalized"
                ] = 0.0

                combined[key][
                    "keyword_normalized"
                ] = result[
                    "normalized_score"
                ]

            else:

                combined[key][
                    "keyword_normalized"
                ] = result[
                    "normalized_score"
                ]

        # -------------------------
        # 5. Hybrid Score
        # -------------------------

        final_results = []

        for result in combined.values():

            hybrid_score = (
                vector_weight
                * result.get(
                    "vector_normalized",
                    0.0
                )
                +
                keyword_weight
                * result.get(
                    "keyword_normalized",
                    0.0
                )
            )

            result["hybrid_score"] = (
                hybrid_score
            )

            final_results.append(result)

        # -------------------------
        # 6. Sort
        # -------------------------

        final_results.sort(
            key=lambda result:
                result["hybrid_score"],
            reverse=True
        )

        return final_results[:limit]


if __name__ == "__main__":

    print("\nGitContext Hybrid Search")
    print("=" * 70)

    search_engine = HybridSearch()

    query = "create_user"

    print("\nQuery:")
    print(query)

    print("\nHybrid Results")
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
            f"Hybrid Score : "
            f"{result['hybrid_score']:.4f}"
        )

        print(
            f"Vector Score : "
            f"{result.get('vector_score', 0):.4f}"
        )

        print(
            f"Keyword Score: "
            f"{result.get('keyword_score', 0):.4f}"
        )

        print(
            f"Type         : "
            f"{result['element_type']}"
        )

        print(
            f"Name         : "
            f"{result['name']}"
        )

        print(
            f"Parent       : "
            f"{result['parent']}"
        )

        print(
            f"Lines        : "
            f"{result['start_line']}-"
            f"{result['end_line']}"
        )

        print("\nCode:")
        print(result["content"])

    print("\n" + "=" * 70)

    print(
        f"Total hybrid results: "
        f"{len(results)}"
    )