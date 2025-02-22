import logging
import os
import traceback

from src.config import configsetting

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Đảm bảo thư mục logs tồn tại
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def exception_logging(exctype, value, tb):
    """
    Logs uncaught exceptions with traceback details.

    Args:
        exctype (Type[BaseException]): Exception type.
        value (BaseException): Exception instance.
        tb (traceback): Traceback object.
    """
    write_val = {
        "exception_type": exctype.__name__,
        "message": str(value) + " Traceback: " + "".join(traceback.format_tb(tb, 20)),
    }
    logger.error(str(write_val))


def custom_logger(app_name="APP"):
    """
    Creates and configures a logger instance.

    Args:
        app_name (str): Name of the application for logging context.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    # StreamHandler (console)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # File Handler (Logs will be stored in a file)
    fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    # Log format
    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(name)s][%(threadName)s][%(module)s]  %(message)s"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


# Initialize logger
logger = custom_logger(app_name=configsetting.PROJECT_NAME)

# Log a test message
logger.info("Logger initialized successfully")
