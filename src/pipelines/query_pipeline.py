from langchain_google_genai import ChatGoogleGenerativeAI

from src.llm.chain_builder import build_qa_chain
from src.retriever.vector_store import initialize_vector_store


def run_query_pipeline(
    question: str, vector_store_path: str, embedding_model: str, llm_model_name: str
):
    """Runs the full RAG pipeline."""
    # Initialize components
    vector_store = initialize_vector_store(embedding_model, vector_store_path)
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    )
    llm_model = ChatGoogleGenerativeAI(model=llm_model_name)

    # Build chain and execute
    qa_chain = build_qa_chain(llm_model, retriever)
    return qa_chain({"query": question})
