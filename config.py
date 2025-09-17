#!/usr/bin/env python3
"""
Configuration settings for the Investment Recommendation Generator v3
Centralized configuration for maintainability and consistency
"""

import os
from pathlib import Path
from typing import Dict, List

# Base directory
BASE_DIR = Path(__file__).parent

# Directory paths
DATA_DIR = BASE_DIR / "data"
PDFS_DIR = DATA_DIR / "pdfs"
LOGS_DIR = DATA_DIR / "logs"
TEMP_DIR = DATA_DIR / "temp"
IMAGES_DIR = DATA_DIR / "images"
TEMPLATES_DIR = BASE_DIR / "templates"

# File paths
LOGO_PATH = TEMPLATES_DIR / "mpc_logo.png"

# LLM Configuration
LLM_CONFIG: Dict[str, any] = {
    'min_intelligence': 8,
    'min_speed': 6,
    'min_context_window': 40000,
    'max_cost': 0,
    'preferred_provider': 'openrouter',
}

# Application settings
APP_TITLE = "Investment Recommendation Generator"
APP_ICON = "✒️"
DEFAULT_TEMPLATE = "v3"

# Form validation settings
MIN_PRICE = 0.01
MAX_PRICE = 1000000.0

# Image settings
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_FORMATS: List[str] = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp']
LATEX_SUPPORTED_FORMATS: List[str] = ['png', 'jpg', 'jpeg', 'pdf', 'eps']

# UI Constants
DEFAULT_FORM_CATEGORY = "ASX Alpha"
DEFAULT_FORM_ACTION = "Buy"
DEFAULT_ENTRY_PRICE = 0.01
DEFAULT_TARGET_PRICE = 0.01
DEFAULT_STOP_LOSS = 0.01

# Template settings
TEMPLATE_VERSIONS = ["v1", "v2", "v3"]
TEMPLATE_PREVIEW_IMAGES = {
    "v1": "v1_preview.png",
    "v2": "v2_preview.png", 
    "v3": "v3_preview.png"
}

# CSS Constants
CSS_FONT_FAMILIES = {
    'inter': 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    'poppins': 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap'
}

# Color scheme
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#2980b9',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'white': '#ffffff',
    'gray': '#6c757d'
}

# Analysis types
ANALYSIS_TYPES = [
    "Fundamentals",
    "Technical Analysis", 
    "Macro/Geopolitical",
    "Catalyst"
]

# Content source types
CONTENT_SOURCES = ["human", "ai"]

# Error messages
ERROR_MESSAGES = {
    'company_name_required': "Company name is required",
    'ticker_required': "Ticker is required",
    'analysis_type_required': "At least one analysis type must be selected",
    'executive_summary_required': "Executive summary is required for human-written content",
    'investment_rationale_required': "Investment rationale is required for human-written content",
    'ai_rationale_required': "Investment rationale context is required for AI generation",
    'ticker_format_invalid': "Ticker should contain only letters, numbers, dots, and hyphens",
    'company_name_too_short': "Company name should be at least 2 characters long",
    'latex_not_available': "LaTeX is not available on this system. Please install LaTeX to generate PDF reports.",
    'pdf_generation_failed': "Failed to generate PDF report. Please check the logs for details.",
    'image_upload_failed': "Failed to upload image. Please try again.",
    'ai_generation_failed': "Failed to generate AI content. Please try again."
}
