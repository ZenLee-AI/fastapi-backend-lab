import logging
from app.core.config import settings

LOG_FORMAT = "%(asctime)s %(levelname)s request_id=%(request_id)s %(message)s"


class RequestAwareFormatter(logging.Formatter):
    """Fallback missing request_id so 3rd-party logs don't break formatting."""

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return super().format(record)


def setup_logging() -> None:
    level_name = (settings.log_level or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
    )

    root_logger = logging.getLogger()
    formatter = RequestAwareFormatter(LOG_FORMAT)
    request_id_filter = RequestIdFilter()

    for handler in root_logger.handlers:
        handler.setFormatter(formatter)
        handler.addFilter(request_id_filter)

    root_logger.addFilter(request_id_filter)

    # Ensure 3rd-party loggers don't spam too much
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)


class RequestIdFilter(logging.Filter):
    """Inject request_id into log records (so formatter never breaks)."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True