from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"


class EmbeddingGenerator:
    """
    Generates embeddings for GitContext code chunks
    using FastEmbed.
    """

    def __init__(self, model_name: str = MODEL_NAME):

        print(f"Loading embedding model: {model_name}")

        self.model = TextEmbedding(
            model_name=model_name
        )

        print("Embedding model loaded successfully!")

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for one text.
        """

        if not text.strip():
            raise ValueError(
                "Cannot generate embedding for empty text."
            )

        embedding = next(
            self.model.embed([text])
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.embed(texts)

        return [
            embedding.tolist()
            for embedding in embeddings
        ]


if __name__ == "__main__":

    generator = EmbeddingGenerator()

    sample_code = """
def calculate_total(price, quantity):
    return price * quantity
"""

    embedding = generator.generate_embedding(
        sample_code
    )

    print("\nEmbedding generated successfully!")

    print(
        f"Vector dimensions: {len(embedding)}"
    )

    print("\nFirst 10 values:")

    print(embedding[:10])