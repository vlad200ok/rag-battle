from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel, ConfigDict


class EmbeddingsModelConfig(BaseModel):
    """
    Base configuration for embedding models.

    This class defines the common configuration parameters required
    by all embedding model implementations in the system.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model_name: str  # The name or identifier of the embedding model
    embedding_size: int  # The dimension size of the generated embeddings


EmbeddingsModelConfigType = TypeVar(
    "EmbeddingsModelConfigType", bound=EmbeddingsModelConfig
)


class BaseEmbeddingsModel(Generic[EmbeddingsModelConfigType], ABC):
    """
    Abstract base class for text embedding models.

    This class defines the interface for all embedding models in the RAG system.
    Embedding models convert text into dense vector representations that capture
    semantic meaning, enabling similarity-based retrieval operations.

    Type Parameters:
        EmbeddingsModelConfigType: The specific configuration type for the model.
    """

    def __init__(self, config: EmbeddingsModelConfigType):
        """
        Initialize the embeddings model with a configuration.

        :param config: Configuration parameters for the model.
        """
        self._config = config

    @abstractmethod
    async def embed_queries(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for query texts.

        This method is optimized for embedding search queries, which may have
        different requirements than document embeddings (e.g., different model,
        different pooling strategy, or preprocessing).

        :param texts: List of query texts to embed.

        :return: list[list[float]]: List of embedding vectors, one for each input text.

        """
        raise NotImplementedError

    @abstractmethod
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for document texts.

        This method is optimized for embedding documents for storage in the vector
        database. It may use different parameters or approaches than query embedding.

        :param texts: List of document texts to embed.

        :return: list[list[float]]: List of embedding vectors, one for each input text.

        """
        raise NotImplementedError
