import os

from rag_battle.domain.embeddings_model import EmbeddingsModelConfig


class TEIEmbeddingsModelConfig(EmbeddingsModelConfig):
    model_name: str = os.getenv("EMBEDDINGS_MODEL")
    embedding_size: int = int(os.getenv("EMBEDDINGS_SIZE"))
