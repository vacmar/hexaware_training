from fastapi import Query
from app.core.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from sqlalchemy.orm import Query as SQLAlchemyQuery
from typing import Any, Dict


def paginate_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, 
                      description="Number of items per page")
) -> Dict[str, Any]:
    size = min(size, MAX_PAGE_SIZE)
    return {"page": page, "size": size}


# Apply Pagination to SQLAlchemy Query
def paginate_query(query: SQLAlchemyQuery, page: int, size: int) -> Dict[str, Any]:
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": items
    }
