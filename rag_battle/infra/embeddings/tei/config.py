from pydantic import Field

from rag_battle.domain.embeddings_model import EmbeddingsModelConfig


class TEIEmbeddingsModelConfig(EmbeddingsModelConfig):
    model_name: str = Field(
        default=None,
        validation_alias="EMBEDDINGS_MODEL",
        description="The name or identifier of the embedding model.",
    )
    embedding_size: int = Field(
        default=None,
        validation_alias="EMBEDDINGS_SIZE",
        description="The dimension size of the generated embeddings.",
    )
