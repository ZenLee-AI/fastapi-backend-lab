import logging
from fastapi import FastAPI, HTTPException

from app.core.config import settings
from app.core.logging import RequestIdFilter, setup_logging
from app.core.middleware import RequestContextMiddleware

setup_logging()
logging.getLogger().addFilter(RequestIdFilter())

app = FastAPI(title=settings.app_name)

app.add_middleware(RequestContextMiddleware)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}


@app.get("/boom")
def boom():
    # Endpoint để cố tình gây lỗi cho Day 5
    raise HTTPException(status_code=500, detail="intentional error")