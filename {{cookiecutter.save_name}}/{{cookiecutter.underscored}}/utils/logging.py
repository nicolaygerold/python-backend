"""Logging configuration."""

import os

import structlog
from structlog._config import BoundLoggerLazyProxy

__all__ = ["logger", "BoundLoggerLazyProxy"]


def setup_logger() -> None:
    """Setup logging for the application."""
    # Validate and convert log level
    valid_levels = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0,
    }
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    if log_level not in valid_levels:
        log_level = "INFO"  # Fallback to INFO if invalid level

    # Configure structlog processors
    processors = [
        # Context & metadata first
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        # Call site info early for visibility
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.MODULE,
            ]
        ),
        # Timestamps and stack info
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.StackInfoRenderer(),
        # Exception handling
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.ExceptionPrettyPrinter(),
        # Cleanup and encoding
        structlog.processors.UnicodeDecoder(),
        # Final rendering (Cloudwatch by AWS automatically formats JSON)
        structlog.dev.ConsoleRenderer(
            colors=False, exception_formatter=structlog.dev.plain_traceback
        ),
    ]

    # Configure structlog with numeric level
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(valid_levels[log_level]),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


setup_logger()

# Get structured logger
logger = structlog.get_logger()

