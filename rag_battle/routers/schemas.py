import uuid
from pydantic import BaseModel, field_validator


class DocumentDTO(BaseModel):
    item_id: str
    content: str
    tags: list[str]

    @field_validator("item_id")
    @classmethod
    def item_id_must_be_hex(cls, value: str):
        return uuid.UUID(value, version=4).hex

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item_id": "0e556d891af44b139c34322ea21ff382",
                    "content": "Document 1.",
                    "tags": ["films", "books", "movies"],
                },
            ]
        }
    }


class DocumentWithScoreDTO(DocumentDTO):
    score: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item_id": "0e556d891af44b139c34322ea21ff382",
                    "content": "Document 1.",
                    "tags": ["films", "books", "movies"],
                    "score": 0.9,
                },
            ]
        }
    }


class RAGQueryDTO(BaseModel):
    query: str
    tags: list[str]
    num_items: int
    remove_duplicates: bool = True

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Tell me about your favorite film.",
                    "tags": ["films", "movies"],
                    "num_items": 3,
                    "remove_duplicates": True,
                },
            ]
        }
    }


class RAGQueryResponseDTO(BaseModel):
    items: list[DocumentWithScoreDTO]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documents": [
                        {
                            "item_id": "0e556d891af44b139c34322ea21ff382",
                            "content": "Document 1.",
                            "tags": ["films", "books", "movies"],
                            "score": 0.9,
                        },
                        {
                            "item_id": "ecd5b5d8f85d4ef8899202080efeaf74",
                            "content": "Document 2.",
                            "tags": ["films"],
                            "score": 0.85,
                        },
                        {
                            "item_id": "0a00a27714764693abc68442997d7a6e",
                            "content": "Document 3.",
                            "tags": ["books"],
                            "score": 0.8,
                        },
                        {
                            "item_id": "498c9ba039c5458a830deb5bb083d6c9",
                            "content": "Document 4.",
                            "tags": ["movies"],
                            "score": 0.7,
                        },
                    ]
                }
            ]
        }
    }


class RAGAddDocumentsDTO(BaseModel):
    documents: list[DocumentDTO]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documents": [
                        {
                            "item_id": "0e556d891af44b139c34322ea21ff382",
                            "content": "Document 1.",
                            "tags": ["films", "books", "movies"],
                        },
                        {
                            "item_id": "ecd5b5d8f85d4ef8899202080efeaf74",
                            "content": "Document 2.",
                            "tags": ["films"],
                        },
                        {
                            "item_id": "0a00a27714764693abc68442997d7a6e",
                            "content": "Document 3.",
                            "tags": ["books"],
                        },
                        {
                            "item_id": "498c9ba039c5458a830deb5bb083d6c9",
                            "content": "Document 4.",
                            "tags": ["movies"],
                        },
                    ]
                }
            ]
        }
    }
