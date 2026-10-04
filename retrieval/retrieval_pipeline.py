from retrieval.hybrid_search import HybridSearch
from retrieval.reranker import CodeReranker
from llm.rag_generator import RAGAnswerGenerator


class RetrievalPipeline:
    """
    Complete GitContext retrieval + LLM answer pipeline.

    Flow:
        Query
          ↓
        Hybrid Search
          ↓
        Candidate Results
          ↓
        Reranker
          ↓
        Final Results
          ↓
        Gemini LLM
          ↓
        Final Answer + Sources
    """

    def __init__(self, candidate_limit: int = 5, final_limit: int = 3):
        print("\nInitializing GitContext Retrieval Pipeline")
        print("=" * 70)

        self.candidate_limit = candidate_limit
        self.final_limit = final_limit

        self.hybrid_search = HybridSearch()
        self.reranker = CodeReranker()
        self.answer_generator = RAGAnswerGenerator()

        print("\nRetrieval + LLM pipeline ready!")

    def search(self, query: str) -> list[dict]:
        """
        Run hybrid retrieval followed by cross-encoder reranking.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        print("\n[1/2] Running hybrid retrieval...")

        candidates = self.hybrid_search.search(
            query,
            limit=self.candidate_limit
        )

        print(f"Candidates retrieved: {len(candidates)}")

        print("\n[2/2] Running cross-encoder reranking...")

        final_results = self.reranker.rerank(
            query,
            candidates,
            limit=self.final_limit
        )

        print(f"Final results: {len(final_results)}")

        return final_results

    def answer(self, query: str) -> str:
        """
        Generate only the final AI answer.
        """

        retrieved_documents = self.search(query)

        answer = self.answer_generator.generate(
            query,
            retrieved_documents
        )

        return answer

    def answer_with_sources(self, query: str) -> dict:
        """
        Generate the AI answer along with the
        retrieved source information.
        """

        retrieved_documents = self.search(query)

        answer = self.answer_generator.generate(
            query,
            retrieved_documents
        )

        sources = []

        for doc in retrieved_documents:
            sources.append({
                "file_path": doc.get("file_path"),
                "start_line": doc.get("start_line"),
                "end_line": doc.get("end_line"),
                "name": doc.get("name"),
                "element_type": doc.get("element_type"),
                "rerank_score": doc.get("rerank_score", 0),
                "content": doc.get("content", "")
            })

        return {
            "answer": answer,
            "sources": sources
        }


if __name__ == "__main__":

    pipeline = RetrievalPipeline(
        candidate_limit=5,
        final_limit=3
    )

    query = "How does UserManager create a user?"

    print("\n")
    print("=" * 70)
    print("GitContext Retrieval + LLM Pipeline")
    print("=" * 70)

    print("\nQuery:")
    print(query)

    # ---------------------------------------------------------
    # Retrieve documents
    # ---------------------------------------------------------

    results = pipeline.search(query)

    print("\n")
    print("=" * 70)
    print("FINAL RETRIEVED CONTEXT")
    print("=" * 70)

    for index, result in enumerate(results, start=1):

        print(f"\nRESULT {index}")
        print("-" * 70)

        print(
            f"Rerank Score : "
            f"{result.get('rerank_score', 0):.4f}"
        )

        print(
            f"Hybrid Score : "
            f"{result.get('hybrid_score', 0):.4f}"
        )

        print(
            f"Name         : "
            f"{result.get('name')}"
        )

        print(
            f"Type         : "
            f"{result.get('element_type')}"
        )

        print(
            f"Parent       : "
            f"{result.get('parent')}"
        )

        print(
            f"File         : "
            f"{result.get('file_path')}"
        )

        print(
            f"Lines        : "
            f"{result.get('start_line')}-"
            f"{result.get('end_line')}"
        )

        print("\nCode:")
        print(result.get("content"))

    print("\n")
    print("=" * 70)
    print(
        f"Total final results: "
        f"{len(results)}"
    )
    print("=" * 70)

    # ---------------------------------------------------------
    # Generate Gemini answer
    # ---------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("GENERATING GEMINI ANSWER")
    print("=" * 70)

    answer_data = pipeline.answer_with_sources(query)

    print("\nQuestion:")
    print(query)

    print("\nAnswer:")
    print(answer_data["answer"])

    # ---------------------------------------------------------
    # Display sources
    # ---------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("SOURCE INFORMATION")
    print("=" * 70)

    for index, source in enumerate(
        answer_data["sources"],
        start=1
    ):

        print(f"\nSOURCE {index}")
        print("-" * 70)

        print(
            f"File       : "
            f"{source['file_path']}"
        )

        print(
            f"Lines      : "
            f"{source['start_line']}-"
            f"{source['end_line']}"
        )

        print(
            f"Name       : "
            f"{source['name']}"
        )

        print(
            f"Type       : "
            f"{source['element_type']}"
        )

        print(
            f"Rerank     : "
            f"{source['rerank_score']:.4f}"
        )

    print("\n")
    print("=" * 70)
    print("GitContext-AI Answer Complete")
    print("=" * 70)