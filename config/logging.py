import structlog
import logging
import os

# Fetch log level and log file path from environment variables, set defaults
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # Default to INFO
LOG_FILE = os.getenv("LOG_FILE", "app.log")  # Default to app.log


def configure_logging():
    # Configure standard logging to output to specified log file
    logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL, logging.INFO), format="%(message)s")

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),  # Add timestamps
            structlog.processors.JSONRenderer()  # Log in JSON
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
