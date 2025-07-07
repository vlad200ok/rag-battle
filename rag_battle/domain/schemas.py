from dataclasses import dataclass


@dataclass
class RAGQuery:
    query: str
    tags: list[str]
    num_items: int
    remove_duplicates: bool = True
