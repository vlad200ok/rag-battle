import pytest
from abc import ABC, abstractmethod

from rag_battle.domain.embeddings_model import (
    BaseEmbeddingsModel,
    EmbeddingsModelConfig,
)
from rag_battle.infra.embeddings.tei import TEIEmbeddingsModel, TEIEmbeddingsModelConfig
from rag_battle.infra.embeddings.service import TEIService
from rag_battle.domain.exceptions import InvalidInputException


class BaseTestEmbeddingsModel(ABC):
    @abstractmethod
    async def _create(self) -> BaseEmbeddingsModel:
        raise NotImplementedError

    @abstractmethod
    async def _create_config(self) -> EmbeddingsModelConfig:
        raise NotImplementedError

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query",
        [
            [],
            ["test query"],
            [""],
            ["hello", "how are you?"],
        ],
    )
    async def test_embed_queries(self, query: list[str]):
        config = await self._create_config()
        model = await self._create()

        embeddings = await model.embed_queries(query)

        assert len(embeddings) == len(query)
        for embedding in embeddings:
            assert len(embedding) == config.embedding_size

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "documents",
        [
            [],
            ["test document"],
            [""],
            ["hello", "how are you?"],
        ],
    )
    async def test_embed_documents(self, documents: list[str]):
        config = await self._create_config()
        model = await self._create()
        embeddings = await model.embed_queries(documents)

        assert len(embeddings) == len(documents)
        for embedding in embeddings:
            assert len(embedding) == config.embedding_size

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query",
        [
            ["very long query" * 100000],
        ],
    )
    async def test_embed_too_long_query(self, query: list[str]):
        model = await self._create()
        with pytest.raises(InvalidInputException):
            await model.embed_queries(query)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "documents",
        [
            ["very long document" * 100000],
        ],
    )
    async def test_embed_too_long_documents(self, documents: list[str]):
        model = await self._create()
        with pytest.raises(InvalidInputException):
            await model.embed_documents(documents)


class TestTEIEmbeddingsModel(BaseTestEmbeddingsModel):
    async def _create(self):
        return TEIEmbeddingsModel(
            config=await self._create_config(),
            service=TEIService(),
        )

    async def _create_config(self) -> TEIEmbeddingsModelConfig:
        return TEIEmbeddingsModelConfig()
