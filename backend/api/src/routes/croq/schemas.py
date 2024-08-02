from pydantic import BaseModel
from typing import List


class CroqSearchQueryBase(BaseModel):
    searchQuery: str


class CroqSearchQueryResponse(BaseModel):
    searchQueryResult: List[str]
