import structlog
import logging
import sys

from config import LOG_LEVEL


def configure_logging():
    # Configure standard logging to stdout
    logging.basicConfig(
        stream=sys.stdout,  # Set to stdout
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(message)s"
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),  # Add timestamps
            structlog.processors.JSONRenderer()  # Log in JSON
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


# Initialize logging once when this module is imported
configure_logging()
