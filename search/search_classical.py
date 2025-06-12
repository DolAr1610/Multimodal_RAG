from db.text_db import init_chroma
from embeddings.text_embedder import get_text_embedding


def classical_search(query, k=5):
    db = init_chroma()
    emb = get_text_embedding(query)
    results = db.similarity_search_by_vector(emb, k=k)
    articles = []
    seen = set()

    for r in results:
        meta = r.metadata
        aid = meta.get("source_url") or meta.get("title")
        if aid not in seen:
            seen.add(aid)
            articles.append({
                "title": meta.get("title"),
                "image_url": meta.get("image_url"),
                "date": meta.get("date"),
                "description": meta.get("description"),
                "content": meta.get("content"),
                "source_url": meta.get("source_url"),
            })

    return articles
