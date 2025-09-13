"""
Logging configuration for Credit Approval System.

This module sets up comprehensive logging with datetime stamps and proper log files.
"""

import logging
from datetime import datetime
from pathlib import Path


def setup_logging():
    """
    Setup comprehensive logging for the Credit Approval System.
    
    Creates log files with datetime stamps and configures different log levels.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate timestamp for log file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # File handler for all logs
            logging.FileHandler(
                logs_dir / f"credit_system_{timestamp}.log",
                mode='a',
                encoding='utf-8'
            ),
            # Console handler for INFO and above
            logging.StreamHandler()
        ]
    )

    # Configure Django logger
    django_logger = logging.getLogger('django')
    django_logger.setLevel(logging.INFO)

    # Configure credit system logger
    credit_logger = logging.getLogger('credit_system')
    credit_logger.setLevel(logging.DEBUG)

    # Configure database logger
    db_logger = logging.getLogger('django.db.backends')
    db_logger.setLevel(logging.WARNING)  # Only show warnings and errors

    # Log application startup
    startup_logger = logging.getLogger('credit_system.startup')
    startup_logger.info("=" * 60)
    startup_logger.info("🏦 CREDIT APPROVAL SYSTEM STARTUP")
    startup_logger.info("=" * 60)
    startup_logger.info(f"Application started at: {datetime.now()}")
    startup_logger.info(f"Log file: {logs_dir / f'credit_system_{timestamp}.log'}")
    startup_logger.info("=" * 60)

    return startup_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f'credit_system.{name}')


# Initialize logging when module is imported
setup_logging()
