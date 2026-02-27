from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    data: List[T]

def get_pagination_params(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return skip, page_size
