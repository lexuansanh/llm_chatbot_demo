from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def build_qa_chain(llm_model, retriever):
    """Creates a RAG chain with the specified LLM model and retriever."""
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="Context: {context}\n\nQuestion: {question}\n\nAnswer:",
    )
    return RetrievalQA(llm=llm_model, retriever=retriever, prompt=prompt_template)
