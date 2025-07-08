import pytest
import fastapi
from httpx import AsyncClient

from rag_battle.server import app
from fixtures.query import VERY_LONG_QUERY, QUERY, TAGS, NUM_ITEMS, REMOVE_DUPLICATES
from fixtures.documents import DOCUMENTS, VERY_LONG_DOCUMENTS
from integration.utils import override_dependencies


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("query", QUERY)
@pytest.mark.parametrize("tags", TAGS)
@pytest.mark.parametrize("num_items", NUM_ITEMS)
@pytest.mark.parametrize("remove_duplicates", REMOVE_DUPLICATES)
async def test_empty_database(
    query: str,
    tags: list[str],
    num_items: int,
    remove_duplicates: bool,
) -> None:
    async for _ in override_dependencies(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/v1/query",
                json={
                    "query": query,
                    "tags": tags,
                    "num_items": num_items,
                    "remove_duplicates": remove_duplicates,
                },
            )
            assert response.status_code == fastapi.status.HTTP_200_OK
            assert response.json() == {"items": []}


@pytest.mark.asyncio(scope="session")
async def test_empty_ingestion() -> None:
    async for _ in override_dependencies(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(
                "/v1/",
                json={
                    "documents": [],
                },
            )
            assert response.status_code == fastapi.status.HTTP_204_NO_CONTENT
            assert response.content == b""


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("documents", DOCUMENTS)
async def test_ingestion(documents: list[dict]) -> None:
    async for _ in override_dependencies(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Ingest
            response = await client.put(
                "/v1/",
                json={
                    "documents": documents,
                },
            )
            assert response.status_code == fastapi.status.HTTP_204_NO_CONTENT
            assert response.content == b""

            # Test to ensure that each document was saved.
            tags = set()
            for document in documents:
                tags.update(document["tags"])
            response = await client.post(
                "/v1/query",
                json={
                    "query": "",
                    "tags": list(tags),
                    "num_items": len(documents) * 100,  # very big number
                    "remove_duplicates": True,
                },
            )
            assert response.status_code == fastapi.status.HTTP_200_OK
            extracted = response.json()

            extracted_items = extracted["items"]
            for item in extracted_items:
                print(item)
            assert len(extracted_items) == len(documents)


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("documents", VERY_LONG_DOCUMENTS)
async def test_very_long_document_ingestion(documents: list[dict]) -> None:
    async for _ in override_dependencies(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Ingest
            response = await client.put(
                "/v1/",
                json={
                    "documents": documents,
                },
            )
            assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
            assert response.json()["detail"]


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("query", VERY_LONG_QUERY)
async def test_very_long_query(
    query: str,
) -> None:
    async for _ in override_dependencies(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/v1/query",
                json={
                    "query": query,
                    "tags": [],
                    "num_items": 0,
                    "remove_duplicates": True,
                },
            )
            assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY
            assert response.json()["detail"]


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("documents", DOCUMENTS)
async def test_tags_query(documents: list[dict]) -> None:
    async for _ in override_dependencies(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Ingest
            response = await client.put(
                "/v1/",
                json={
                    "documents": documents,
                },
            )
            assert response.status_code == fastapi.status.HTTP_204_NO_CONTENT
            assert response.content == b""

            # Test tags
            tags: dict[str, list[dict]] = {}
            for document in documents:
                for tag in document["tags"]:
                    if tag not in tags:
                        tags[tag] = []
                    tags[tag].append(document)

            for tag in tags:
                response = await client.post(
                    "/v1/query",
                    json={
                        "query": "",
                        "tags": [tag],
                        "num_items": len(documents) * 100,  # very big number
                        "remove_duplicates": True,
                    },
                )
                assert response.status_code == fastapi.status.HTTP_200_OK
                extracted = response.json()
                extracted_items = extracted["items"]
                assert len(extracted_items) == len(tags[tag])
                for item in extracted_items:
                    assert tag in item["tags"]
