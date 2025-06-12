import json
from tqdm import tqdm
from db.image_db import init_chroma_image, add_document_image
from embeddings.image_embedder import get_image_embedding
from ingestion.config import JSON_PATH


def ingest_images():
    vectordb = init_chroma_image()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)
    print(f"Found {len(articles)} articles.")

    for article in tqdm(articles, desc="Indexing images"):
        metadata = {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "image_url": article.get("image_url", ""),
            "date": article.get("date", ""),
            "content": article.get("content", ""),
            "source_url": article.get("source_url", "")
        }

        image_url = metadata["image_url"]
        if not image_url:
            print(f"No image in: {metadata['title']}")
            continue

        emb = get_image_embedding(image_url)
        if emb:
            doc_id = f"{metadata['source_url']}#image" if metadata["source_url"] else f"image#{metadata['title']}"
            add_document_image(vectordb, doc_id, emb, {**metadata, "modality": "image"})
        else:
            print(f"Failed to embed image for: {metadata['title']}")

    print("Done indexing images.")
