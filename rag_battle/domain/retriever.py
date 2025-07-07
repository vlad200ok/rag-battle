from abc import ABC, abstractmethod
from rag_battle.domain.schemas import RAGQuery
from rag_battle.domain.embeddings_model import BaseEmbeddingsModel
from rag_battle.domain.vector_database import VectorDatabase, DataItemType


class BaseRetriever(ABC):
    """
    Abstract base class for retrieval components in the RAG system.

    Retrievers are responsible for converting natural language queries into vector
    representations and retrieving relevant documents from a vector database.
    Different implementations can provide various retrieval strategies and
    optimizations.
    """

    def __init__(
        self,
        embeddings_model: BaseEmbeddingsModel,
        vector_database: VectorDatabase,
    ):
        """
        Initialize the retriever with embedding model and vector database.

        :param embeddings_model: The model used to convert text to vector embeddings.
        :param vector_database: The database that stores and retrieves vectors.
        """
        self._embeddings_model = embeddings_model
        self._vector_database = vector_database

    @abstractmethod
    async def retrieve(self, query: RAGQuery) -> list[DataItemType]:
        """
        Retrieve relevant documents based on the provided query.

        :param query: The query object containing search text and parameters.

        :return: list[DataItemType]: A list of retrieved items ordered by relevance.
        """
        raise NotImplementedError
