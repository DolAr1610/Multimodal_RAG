from langchain_community.vectorstores import Chroma


def init_chroma_image():
    vectordb = Chroma(
        collection_name="rag_collection_images",
        persist_directory="chroma_db_images"
    )
    return vectordb


def add_document_image(vectordb, doc_id, embedding, metadata):
    vectordb._collection.add(
        embeddings=[embedding],
        documents=["[image]"],
        metadatas=[metadata],
        ids=[doc_id]
    )
