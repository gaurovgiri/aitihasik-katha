import logging
import os


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(level: str | int | None = None) -> None:
    """Initialize process-wide logging configuration once."""
    if logging.getLogger().handlers:
        return

    configured_level = level or os.getenv("LOG_LEVEL", "INFO")
    if isinstance(configured_level, str):
        configured_level = getattr(logging, configured_level.upper(), logging.INFO)

    logging.basicConfig(level=configured_level, format=LOG_FORMAT)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)