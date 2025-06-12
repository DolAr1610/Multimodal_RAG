from langchain_community.vectorstores import Chroma
from embeddings.text_embedder import TextEmbeddings


def init_chroma():
    return Chroma(
        collection_name="text_collection",
        embedding_function=TextEmbeddings(),
        persist_directory="chroma_db_text"
    )


def add_document_text(vectordb, doc_id, embedding, document_text, metadata):
    vectordb._collection.add(
        embeddings=[embedding],
        documents=[document_text],
        metadatas=[metadata],
        ids=[doc_id]
    )
