from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Engine là một app-level DB gateway, quản lý connection pool; engine = app-level DB gateway + pool manager
engine = create_async_engine(
    settings.database_url,
    echo=(settings.env == "dev"),
)
# AsyncSessionLocal là một sessionmaker, tạo AsyncSession theo request (unit-of-work/transaction scope)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# DeclarativeBase là một base class cho tất cả model
class Base(DeclarativeBase):
    pass

# get_db là một dependency, inject AsyncSession vào endpoint/service và đảm bảo close/cleanup sau request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
