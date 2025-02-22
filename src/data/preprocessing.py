def clean_text(text: str) -> str:
    """Cleans and normalizes input text for processing."""
    import re

    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text.strip().lower()


def normalize_data(data: list) -> list:
    """Normalizes a list of text documents."""
    return [clean_text(doc) for doc in data]
