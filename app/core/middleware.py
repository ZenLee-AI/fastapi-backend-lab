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

        # Attach request_id to request.state for downstream usage
        request.state.request_id = request_id

        try:
            response: Response = await call_next(request)
            return response
        except Exception:
            # Log stacktrace + request context
            logger.exception(
                "unhandled_error method=%s path=%s",
                request.method,
                request.url.path,
                extra={"request_id": request_id},
            )
            raise
        finally:
            total_time_ms = (time.perf_counter() - start) * 1000.0
            # Always log end-of-request line
            # status_code may not exist if exception happened before response
            status_code = getattr(locals().get("response", None), "status_code", 500)
            logger.info(
                "request_completed method=%s path=%s status_code=%s total_time_ms=%.2f",
                request.method,
                request.url.path,
                status_code,
                total_time_ms,
                extra={"request_id": request_id},
            )

            # If we have a response, add headers (best-effort)
            resp = locals().get("response", None)
            if resp is not None:
                resp.headers["x-request-id"] = request_id
                resp.headers["x-total-time-ms"] = f"{total_time_ms:.2f}"