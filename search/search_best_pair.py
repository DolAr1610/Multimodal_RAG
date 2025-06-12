from db.text_db import init_chroma
from db.image_db import init_chroma_image
from embeddings.text_embedder import get_text_embedding
from embeddings.image_embedder import get_text_embedding_clip


def best_pair_search(query, k=3):
    text_db = init_chroma()
    image_db = init_chroma_image()

    text_emb = get_text_embedding(query)
    image_emb = get_text_embedding_clip(query)

    t_res = text_db.similarity_search_by_vector(text_emb, k=k)
    i_res = image_db.similarity_search_by_vector(image_emb, k=k)

    results = []
    for i in range(k):
        text_meta = t_res[i].metadata if i < len(t_res) else {}
        image_meta = i_res[i].metadata if i < len(i_res) else {}

        results.append({
            "title": text_meta.get("title"),
            "description": text_meta.get("description"),
            "date": text_meta.get("date"),
            "source_url": text_meta.get("source_url"),
            "content": text_meta.get("content"),
            "image_url": image_meta.get("image_url") if image_meta else None
        })

    return results
