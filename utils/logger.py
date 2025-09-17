#!/usr/bin/env python3
"""
Logging utility for the Investment Recommendation Generator
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import LOGS_DIR


class AppLogger:
    """
    Application logger with file and console output.
    
    Provides structured logging for the application with different log levels
    and automatic log file rotation.
    """
    
    _instance: Optional['AppLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'AppLogger':
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self) -> None:
        """Setup the logger with file and console handlers."""
        # Ensure logs directory exists
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger('investment_recommendation_app')
        self._logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self._logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        log_file = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        
        # Console handler (only for errors and warnings)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        """Log error message."""
        self._logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self._logger.debug(message)
    
    def critical(self, message: str, exc_info: bool = False) -> None:
        """Log critical message."""
        self._logger.critical(message, exc_info=exc_info)


def get_logger() -> AppLogger:
    """
    Get the application logger instance.
    
    Returns:
        AppLogger: The singleton logger instance
    """
    return AppLogger()
