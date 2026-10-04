from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from ingestion.code_chunker import extract_code_chunks
from ingestion.embedding_generator import EmbeddingGenerator
from ingestion.document_schema import create_document


BASE_DIR = Path(__file__).resolve().parent.parent

QDRANT_PATH = BASE_DIR / "data" / "qdrant_storage"

COLLECTION_NAME = "gitcontext_code"

VECTOR_SIZE = 384


class VectorStore:
    """
    Local Qdrant vector database for GitContext.
    """

    def __init__(self):

        QDRANT_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            f"Opening Qdrant database at:\n{QDRANT_PATH}"
        )

        self.client = QdrantClient(
            path=str(QDRANT_PATH)
        )

        self.create_collection()

    def create_collection(self):
        """
        Create the GitContext collection if it does not exist.
        """

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if COLLECTION_NAME not in collection_names:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )

            print(
                f"Collection created: {COLLECTION_NAME}"
            )

        else:

            print(
                f"Collection already exists: "
                f"{COLLECTION_NAME}"
            )

    def insert_documents(
        self,
        documents: list[dict],
        embeddings: list[list[float]]
    ):
        """
        Insert embeddings and document metadata into Qdrant.
        """

        if len(documents) != len(embeddings):
            raise ValueError(
                "Documents and embeddings count do not match."
            )

        points = []

        for index, (document, embedding) in enumerate(
            zip(documents, embeddings),
            start=1
        ):

            point = PointStruct(
                id=index,
                vector=embedding,
                payload=document
            )

            points.append(point)

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

        print(
            f"Inserted {len(points)} vectors into Qdrant."
        )

    def collection_info(self):

        return self.client.get_collection(
            collection_name=COLLECTION_NAME
        )


if __name__ == "__main__":

    print("\nGitContext Qdrant Vector Store")
    print("=" * 60)

    # ---------------------------------
    # 1. Load code chunks
    # ---------------------------------

    test_file = BASE_DIR / "data" / "sample_test.py"

    chunks = extract_code_chunks(
        str(test_file)
    )

    print(
        f"\nCode chunks discovered: {len(chunks)}"
    )

    # ---------------------------------
    # 2. Convert chunks to documents
    # ---------------------------------

    documents = []

    for chunk in chunks:

        document = create_document(
            chunk,
            repository="GitContext-Test"
        )

        documents.append(
            {
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
            }
        )

    # ---------------------------------
    # 3. Generate embeddings
    # ---------------------------------

    print("\nGenerating embeddings...")

    embedding_generator = EmbeddingGenerator()

    texts = [
        document["content"]
        for document in documents
    ]

    embeddings = (
        embedding_generator.generate_embeddings(
            texts
        )
    )

    print(
        f"Embeddings generated: {len(embeddings)}"
    )

    # ---------------------------------
    # 4. Store in Qdrant
    # ---------------------------------

    vector_store = VectorStore()

    vector_store.insert_documents(
        documents,
        embeddings
    )

    # ---------------------------------
    # 5. Verify
    # ---------------------------------

    info = vector_store.collection_info()

    print("\nQdrant Collection Information")
    print("=" * 60)

    print(
        f"Collection : {COLLECTION_NAME}"
    )

    print(
        f"Points     : {info.points_count}"
    )

    print("=" * 60)

    print("\nVector insertion successful!")