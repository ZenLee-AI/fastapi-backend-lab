# app/routers/books.py — SỬA (thêm GET by ID + filter)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import BookCreate, BookResponse
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    body: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    service = BookService(db)
    return await service.create(body)


@router.get("/", response_model=list[BookResponse])
async def list_books(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = BookService(db)
    return await service.list_all(category=category)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = BookService(db)
    book = await service.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book