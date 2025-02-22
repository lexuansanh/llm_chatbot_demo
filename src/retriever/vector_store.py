import os

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def initialize_vector_store(embedding_model: str, path: str):
    """Initializes or loads the vector store."""
    embeddings = OpenAIEmbeddings(model=embedding_model)
    if os.path.exists(path):
        return FAISS.load_local(path, embeddings)
    return FAISS(embeddings)
