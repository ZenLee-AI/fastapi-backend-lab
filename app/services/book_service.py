# app/services/book_service.py — SỬA (thêm get_by_id, list with filter)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Book
from app.schemas import BookCreate


class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: BookCreate) -> Book:
        book = Book(title=data.title, author=data.author, category=data.category)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def get_by_id(self, book_id: int) -> Book | None:
        result = await self.db.execute(
            select(Book).where(Book.id == book_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, category: str | None = None) -> list[Book]:
        query = select(Book).order_by(Book.id)
        if category is not None:
            query = query.where(Book.category == category)
        return list((await self.db.execute(query)).scalars().all())