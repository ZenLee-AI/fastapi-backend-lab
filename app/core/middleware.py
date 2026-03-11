import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        start = time.perf_counter()
        response: Response | None = None

        request.state.request_id = request_id

        try:
            response = await call_next(request)
            return response
        except Exception:
            logger.exception(
                "unhandled_error method=%s path=%s",
                request.method,
                request.url.path,
                extra={"request_id": request_id},
            )
            raise
        finally:
            total_time_ms = (time.perf_counter() - start) * 1000.0
            status_code = response.status_code if response is not None else 500
            logger.info(
                "request_completed method=%s path=%s status_code=%s total_time_ms=%.2f",
                request.method,
                request.url.path,
                status_code,
                total_time_ms,
                extra={"request_id": request_id},
            )

            if response is not None:
                response.headers["x-request-id"] = request_id
                response.headers["x-total-time-ms"] = f"{total_time_ms:.2f}"