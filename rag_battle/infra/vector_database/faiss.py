import faiss
import heapq
import numpy as np
from loguru import logger
from copy import deepcopy
from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic
from dataclasses import dataclass
from rag_battle.domain.vector_database import (
    DataItemType,
    VectorDatabase,
    DataItemWithEmbeddingType,
)

IndexType = TypeVar("IndexType", bound="faiss.Index")


class TagIndex(BaseModel):
    faiss_index: IndexType
    item_ids: set[str]
    vector_ids: list[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)


@dataclass(order=True)
class ScoreItem:
    score: float
    item_id: str
    tag: str


class FaissVectorDatabase(VectorDatabase, Generic[IndexType, DataItemType]):
    def __init__(
        self,
        embedding_size: int,
        index_type: type[IndexType] = faiss.IndexFlatIP,
    ):
        self._index_type: type[IndexType] = index_type
        self._embedding_size: int = embedding_size
        self._tag_to_index: dict[str, TagIndex] = {}
        self._item_id_to_item: dict[str, DataItemType] = {}

    @classmethod
    async def create(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        return self

    async def save_items(
        self,
        items_with_embeddings: list[DataItemWithEmbeddingType],
    ) -> None:
        for i in range(len(items_with_embeddings)):
            item_with_embedding = items_with_embeddings[i]
            vector = item_with_embedding.embedding.reshape(1, -1).astype("float32")
            item = item_with_embedding.item
            item = deepcopy(item)

            item_id = item.item_id
            tags = item.tags
            vector_id = item_id

            await self._save_item(item=item)

            for tag in tags:
                tag_index: TagIndex = self._get_or_create_tag_index(tag)
                tag_index.item_ids.add(item_id)
                vector_ids: list[str] = tag_index.vector_ids
                faiss_index: IndexType = tag_index.faiss_index

                try:
                    vector_int_id = vector_ids.index(vector_id)
                    faiss_index.remove_ids(np.array([vector_int_id]))
                except ValueError:
                    vector_int_id = len(vector_ids)
                    vector_ids.append(vector_id)
                faiss_index.add_with_ids(vector, vector_int_id)

    def _get_or_create_tag_index(self, tag: str) -> TagIndex:
        try:
            tag_index: TagIndex = self._tag_to_index[tag]
        except KeyError:
            tag_index = TagIndex(
                faiss_index=self._create_faiss_index(),
                item_ids=set(),
                vector_ids=[],
            )
            self._tag_to_index[tag] = tag_index
        return tag_index

    def _create_faiss_index(self) -> IndexType:
        return faiss.IndexIDMap(self._index_type(self._embedding_size))

    async def query(
        self,
        query_embeddings: list[np.ndarray],
        tags: list[str],
        num_items: int,
        remove_duplicates: bool,
    ) -> list[DataItemType]:
        tags = list(set(tags))

        score_item_ids: list[ScoreItem] = []

        query_embeddings = np.array(query_embeddings).astype("float32")
        for tag in tags:
            if tag not in self._tag_to_index:
                continue

            tag_index: TagIndex = self._tag_to_index[tag]

            faiss_index: IndexType = tag_index.faiss_index
            if faiss_index.ntotal == 0:
                continue

            scores, indexes = faiss_index.search(
                query_embeddings,
                min(num_items, faiss_index.ntotal),
            )
            vector_ids: list[str] = tag_index.vector_ids
            for i in range(len(scores)):
                for score, local_index in zip(scores[i], indexes[i]):
                    vector_id = vector_ids[local_index]
                    # TODO: add support for multivector items
                    #  vector_id may be item_id + "_0", + "_1", etc
                    item_id = vector_id
                    heapq.heappush(
                        score_item_ids,
                        ScoreItem(
                            score=score,
                            item_id=item_id,
                            tag=tag,
                        ),
                    )

        items: list[DataItemType] = []
        unique_item_ids = set()
        for score_item in sorted(score_item_ids, key=lambda x: x, reverse=True):
            item_id = score_item.item_id
            try:
                if remove_duplicates:
                    if item_id in unique_item_ids:
                        continue
                    unique_item_ids.add(item_id)

                item: DataItemType = self._item_id_to_item[item_id]
                item = deepcopy(item)
                item.score = score_item.score
                items.append(item)
            except KeyError:
                logger.error(
                    f"Key: `{item_id}`, "
                    f"tag: `{score_item.tag}`, "
                    f"score: `{score_item.score}`"
                )
                raise KeyError
        return items[:num_items]

    async def _save_item(
        self,
        item: DataItemType,
    ) -> None:
        self._item_id_to_item[item.item_id] = item
