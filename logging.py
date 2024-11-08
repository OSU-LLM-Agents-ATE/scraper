import structlog
import logging
import sys

from config import LOG_LEVEL


def configure_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(message)s"
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


configure_logging()