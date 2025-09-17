#!/usr/bin/env python3
"""
Data models for Investment Recommendation Generator v2
"""

from .form_data import FormData, AnalysisType, ContentSource, TemplateVersion
from .report_data import ReportData

__all__ = [
    'FormData', 'AnalysisType', 'ContentSource', 'TemplateVersion',
    'ReportData'
]
