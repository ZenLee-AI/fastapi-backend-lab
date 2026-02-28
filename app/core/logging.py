import logging
from app.core.config import settings


def setup_logging() -> None:
    level_name = (settings.log_level or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s request_id=%(request_id)s %(message)s",
    )

    # Ensure 3rd-party loggers don't spam too much
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)


class RequestIdFilter(logging.Filter):
    """Inject request_id into log records (so formatter never breaks)."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True