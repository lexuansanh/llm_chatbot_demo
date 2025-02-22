from langchain.embeddings import OpenAIEmbeddings


class EmbeddingManager:
    def __init__(self, model_name: str):
        self.model = OpenAIEmbeddings(model=model_name)

    def generate_embedding(self, text: str):
        """Generates an embedding for a given text."""
        return self.model.embed_query(text)
