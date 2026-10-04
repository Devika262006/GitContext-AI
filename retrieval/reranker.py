from fastembed.rerank.cross_encoder import TextCrossEncoder


MODEL_NAME = "Xenova/ms-marco-MiniLM-L-6-v2"


class CodeReranker:
    """
    Re-ranks retrieved code chunks using a cross-encoder.
    """

    def __init__(self, model_name: str = MODEL_NAME):

        print(
            f"Loading reranker model: {model_name}"
        )

        self.model = TextCrossEncoder(
            model_name=model_name
        )

        print("Reranker model loaded successfully!")

    def rerank(
        self,
        query: str,
        documents: list[dict],
        limit: int = 3
    ) -> list[dict]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if not documents:
            return []

        document_texts = [
            document["content"]
            for document in documents
        ]

        scores = list(
            self.model.rerank(
                query,
                document_texts
            )
        )

        reranked = []

        for document, score in zip(
            documents,
            scores
        ):

            result = document.copy()

            result["rerank_score"] = float(
                score
            )

            reranked.append(result)

        reranked.sort(
            key=lambda item:
                item["rerank_score"],
            reverse=True
        )

        return reranked[:limit]


if __name__ == "__main__":

    reranker = CodeReranker()

    query = "How does UserManager create a user?"

    documents = [
        {
            "name": "delete_user",
            "content": """
def delete_user(self, user_id):
    return f"Deleted {user_id}"
"""
        },
        {
            "name": "create_user",
            "content": """
def create_user(self, name):
    return {"name": name}
"""
        },
        {
            "name": "calculate_total",
            "content": """
def calculate_total(price, quantity):
    return price * quantity
"""
        },
    ]

    results = reranker.rerank(
        query,
        documents,
        limit=3
    )

    print("\nReranked Results")
    print("=" * 60)

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nRESULT {index}"
        )

        print(
            f"Name  : {result['name']}"
        )

        print(
            f"Score : "
            f"{result['rerank_score']:.4f}"
        )

        print("\nCode:")

        print(result["content"])

    print("\n" + "=" * 60)