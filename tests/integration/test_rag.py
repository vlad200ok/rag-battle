import pytest
from httpx import AsyncClient

from rag_battle.server import app
from fixtures.query import QUERY, TAGS, NUM_ITEMS, REMOVE_DUPLICATES
from fixtures.documents import DOCUMENTS
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
            assert response.status_code == 200
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
            assert response.status_code == 204
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
            assert response.status_code == 204
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
            assert response.status_code == 200
            extracted = response.json()

            extracted_items = extracted["items"]
            for item in extracted_items:
                print(item)
            assert len(extracted_items) == len(documents)
