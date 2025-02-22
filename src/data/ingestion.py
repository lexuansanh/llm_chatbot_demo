import json
import os


def load_json_file(filepath: str) -> list:
    """Loads data from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r") as file:
        return json.load(file)


def save_to_vector_store(data: list, vector_store):
    """Saves documents into a vector store."""
    for doc in data:
        vector_store.add_texts([doc])
