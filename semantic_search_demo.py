import sys
import time

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer

# Sample data
documents = [
    {"id": 1, "text": "king"}, {"id": 2, "text": "queen"},
    {"id": 3, "text": "prince"}, {"id": 4, "text": "princess"},
    {"id": 5, "text": "man"}, {"id": 6, "text": "woman"},
    {"id": 7, "text": "boy"}, {"id": 8, "text": "girl"},
    {"id": 9, "text": "apple"}, {"id": 10, "text": "banana"},
    {"id": 11, "text": "orange"}, {"id": 12, "text": "grape"},
    {"id": 13, "text": "happy"}, {"id": 14, "text": "joyful"},
    {"id": 15, "text": "sad"}, {"id": 16, "text": "angry"},
    {"id": 17, "text": "car"}, {"id": 18, "text": "bicycle"},
    {"id": 19, "text": "train"}, {"id": 20, "text": "airplane"},
    {"id": 21, "text": "dog"}, {"id": 22, "text": "cat"},
    {"id": 23, "text": "lion"}, {"id": 24, "text": "tiger"},
    {"id": 25, "text": "computer"}, {"id": 26, "text": "keyboard"},
    {"id": 27, "text": "mouse"}, {"id": 28, "text": "monitor"},
    {"id": 29, "text": "summer"}, {"id": 30, "text": "winter"}
]

COLLECTION_NAME = "my_word_collection"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333


def main():
    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    dim = model.get_sentence_embedding_dimension()
    print(f"Model loaded. Embedding dimension: {dim}")

    print(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        client.get_collections()
    except Exception as e:
        print(f"Error: Could not connect to Qdrant ({e})")
        sys.exit(1)

    print(f"(Re)creating collection '{COLLECTION_NAME}'...")
    try:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=dim,
                distance=models.Distance.COSINE
            )
        )
    except Exception as e:
        print(f"Error creating collection: {e}")
        sys.exit(1)

    print("Generating embeddings for sample data...")
    texts = [doc["text"] for doc in documents]
    vectors = model.encode(texts, show_progress_bar=True)

    print("Upserting points to Qdrant...")
    points = [
        PointStruct(
            id=doc["id"],
            vector=vector.tolist() if hasattr(vector, 'tolist') else list(vector),
            payload={"text": doc["text"]}
        )
        for doc, vector in zip(documents, vectors)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
    print("Upsert complete.")

    print("\nSemantic search ready! Try queries like: 'royal female', 'fruit', 'vehicle', 'sadness', 'computer peripheral', 'hot season'.")
    while True:
        try:
            query = input("\nEnter a word to search (or 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if query.lower() == "quit":
            print("Goodbye!")
            break
        if not query:
            continue
        query_vec = model.encode([query])[0]
        try:
            results = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vec.tolist() if hasattr(query_vec, 'tolist') else list(query_vec),
                limit=5
            )
        except Exception as e:
            print(f"Search error: {e}")
            continue
        print("Results:")
        for hit in results:
            text = hit.payload.get("text", "?")
            score = hit.score
            print(f"  - {text} (score: {score:.4f})")

if __name__ == "__main__":
    main() 