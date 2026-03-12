import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    logger = logging.getLogger()
    
    # We want to catch everything from INFO and above
    logger.setLevel(logging.INFO)

    # Remove existing handlers (like uvicorn defaults) if any, but we will keep them separate or just override
    # It's better to clear handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create standard output handler
    log_handler = logging.StreamHandler(sys.stdout)
    
    # Create file handler for Fluentd ingestion
    file_handler = logging.FileHandler("app.log")
    
    # Custom format including standard fields
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    
    log_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(log_handler)
    logger.addHandler(file_handler)

    # Optionally, also configure uvicorn loggers to use JSON
    for logger_name in ("uvicorn.access", "uvicorn.error", "fastapi"):
        uv_logger = logging.getLogger(logger_name)
        uv_logger.handlers = [log_handler, file_handler]
        # Keep their level as is
        uv_logger.propagate = False
