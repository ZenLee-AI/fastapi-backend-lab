# app/schemas.py — SỬA (thêm category + BookDetail)
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str
    category: str = "general"


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    category: str
    created_at: datetime