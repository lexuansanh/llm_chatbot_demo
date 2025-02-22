def validate_answer(answer: str) -> str:
    """Validates and cleans the answer from the LLM."""
    return answer.strip() if answer else "No valid answer found."


def format_response(result, question: str):
    """Formats the result for API consumption."""
    answer = validate_answer(result.get("result"))
    documents = [doc.page_content for doc in result.get("source_documents", [])]
    return {"question": question, "answer": answer, "documents": documents}
