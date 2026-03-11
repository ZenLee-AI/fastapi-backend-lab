import logging
import time
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import RequestContextMiddleware
from app.database import engine, Base
from app.routers import books

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: tạo tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose engine (trả hết connections)
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)

# --- Routers ---
app.include_router(books.router)


# --- Utility endpoints (giữ từ Day 5-6) ---

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}


@app.get("/boom")
def boom():
    raise HTTPException(status_code=500, detail="intentional error")

@app.get("/io-blocking")
def io_blocking():
    time.sleep(2)
    return {"mode": "blocking", "slept_s": 2}


@app.get("/io-async")
async def io_async():
    await asyncio.sleep(2)
    return {"mode": "async", "slept_s": 2}


@app.get("/io-bad-async")
async def io_bad_async():
    time.sleep(2)
    return {"mode": "bad_async", "slept_s": 2}


@app.get("/cpu-bound")
def cpu_bound():
    s = 0
    for i in range(30_000_000):
        s += i
    return {"sum": s}