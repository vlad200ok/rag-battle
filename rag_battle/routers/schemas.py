from pydantic import BaseModel


class DocumentDTO(BaseModel):
    item_id: str
    content: str
    tags: list[str]


class DocumentWithScoreDTO(DocumentDTO):
    score: float


class RAGQueryDTO(BaseModel):
    query: str
    tags: list[str]
    num_items: int
    remove_duplicates: bool = True


class RAGQueryResponseDTO(BaseModel):
    items: list[DocumentWithScoreDTO]


class RAGAddDocumentsDTO(BaseModel):
    documents: list[DocumentDTO]
