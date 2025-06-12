import json
from tqdm import tqdm
from db.text_db import init_chroma, add_document_text
from embeddings.text_embedder import get_text_embedding
from ingestion.config import JSON_PATH


def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks


def ingest_texts():
    vectordb = init_chroma()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)
    print(f"Found {len(articles)} articles.")

    for article in tqdm(articles, desc="Indexing texts"):
        full_text = f"{article.get('title', '')}\n{article.get('description', '')}\n{article.get('content', '')}"

        metadata = {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "image_url": article.get("image_url", ""),
            "date": article.get("date", ""),
            "content": article.get("content", ""),
            "source_url": article.get("source_url", "")
        }

        chunks = chunk_text(full_text, chunk_size=400, overlap=50)

        for i, chunk in enumerate(chunks):
            emb = get_text_embedding(chunk)
            if emb:
                doc_id = f"{metadata['source_url']}#chunk{i}" if metadata[
                    "source_url"] else f"{metadata['title']}#chunk{i}"
                add_document_text(vectordb, doc_id, emb, chunk, metadata)
            else:
                print(f"Failed to embed chunk {i} of {metadata['title']}")

    print("Done indexing texts.")
