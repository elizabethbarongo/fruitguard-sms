import logging
import sys
from config import Config

def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Set up a logger with the specified configuration
    
    Args:
        name: The name of the logger (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Create a default logger instance
logger = setup_logger('fruitguard_sms')

