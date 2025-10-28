import logging
import sys

from .config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.info("Logging configured with rate limit %s/min", settings.rate_limit_per_min)