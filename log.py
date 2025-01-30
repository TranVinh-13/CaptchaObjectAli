from rich.logging import RichHandler
import logging

# Set up the rich handler
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format="%(message)s",  # You can customize your format here
    handlers=[RichHandler()]  # Use RichHandler for colored logs
)

logger = logging.getLogger("logCaptcha")

# # Example log messages with different log levels
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
