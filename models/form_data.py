#!/usr/bin/env python3
"""
Form data models and validation for the Investment Recommendation Generator
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum
import streamlit as st
from config import (
    DEFAULT_FORM_CATEGORY, DEFAULT_FORM_ACTION, 
    DEFAULT_ENTRY_PRICE, DEFAULT_TARGET_PRICE, DEFAULT_STOP_LOSS,
    ERROR_MESSAGES
)


class AnalysisType(Enum):
    """Analysis types for investment recommendations"""
    FUNDAMENTALS = "Fundamentals"
    TECHNICAL = "Technical Analysis"
    MACRO = "Macro/Geopolitical"
    CATALYST = "Catalyst"


class ContentSource(Enum):
    """Content generation source"""
    HUMAN = "human"
    AI = "ai"


class TemplateVersion(Enum):
    """Template versions"""
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


@dataclass
class FormData:
    """
    Investment recommendation form data model.
    
    This class represents all the data collected from the investment recommendation form,
    including basic information, analysis types, trade plan, content, and metadata.
    """
    # Basic Information
    category: str = DEFAULT_FORM_CATEGORY
    action: str = DEFAULT_FORM_ACTION
    ticker: str = ""
    company_name: str = ""
    subtitle: str = ""
    
    # Analysis
    analysis_types: List[AnalysisType] = field(default_factory=list)
    
    # Trade Plan - Different fields based on action type
    # For Buy/Add: entry_price, target_price, stop_loss
    # For Sell/Take Profit: exit_price only
    entry_price: float = DEFAULT_ENTRY_PRICE
    target_price: float = DEFAULT_TARGET_PRICE
    stop_loss: float = DEFAULT_STOP_LOSS
    exit_price: float = DEFAULT_ENTRY_PRICE  # For Sell/Take Profit actions
    
    # Content
    content_source: ContentSource = ContentSource.HUMAN
    human_executive_summary: str = ""
    human_investment_rationale: str = ""
    ai_rationale: str = ""
    ai_context: str = ""
    ai_executive_summary: str = ""
    ai_investment_rationale: str = ""
    # Store original Markdown content for PDF generation
    ai_executive_summary_markdown: str = ""
    ai_investment_rationale_markdown: str = ""
    
    # Images
    company_logo: Optional[Any] = None  # Streamlit UploadedFile
    chart_image: Optional[Any] = None   # Streamlit UploadedFile
    company_logo_filename: Optional[str] = None
    chart_image_filename: Optional[str] = None
    
    # Template
    template_version: TemplateVersion = TemplateVersion.V2
    
    # Metadata
    timestamp: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for processing"""
        return {
            'category': self.category,
            'action': self.action,
            'ticker': self.ticker,
            'company_name': self.company_name,
            'subtitle': self.subtitle,
            'analysis_types': [at if isinstance(at, str) else at.value for at in self.analysis_types],
            'entry_price': self.entry_price,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'exit_price': self.exit_price,
            'content_source': self.content_source.value if hasattr(self.content_source, 'value') else str(self.content_source),
            'human_executive_summary': self.human_executive_summary,
            'human_investment_rationale': self.human_investment_rationale,
            'ai_rationale': self.ai_rationale,
            'ai_context': self.ai_context,
            'ai_executive_summary': self.ai_executive_summary,
            'ai_investment_rationale': self.ai_investment_rationale,
            'ai_executive_summary_markdown': self.ai_executive_summary_markdown,
            'ai_investment_rationale_markdown': self.ai_investment_rationale_markdown,
            'company_logo_filename': self.company_logo_filename,
            'chart_image_filename': self.chart_image_filename,
            'template_version': self.template_version.value if hasattr(self.template_version, 'value') else str(self.template_version),
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FormData':
        """Create from dictionary"""
        return cls(
            category=data.get('category', 'ASX Alpha'),
            action=data.get('action', 'Buy'),
            ticker=data.get('ticker', ''),
            company_name=data.get('company_name', ''),
            subtitle=data.get('subtitle', ''),
            analysis_types=[AnalysisType(at) for at in data.get('analysis_types', [])],
            entry_price=data.get('entry_price', 0.0),
            target_price=data.get('target_price', 0.0),
            stop_loss=data.get('stop_loss', 0.0),
            exit_price=data.get('exit_price', 0.0),
            content_source=ContentSource(data.get('content_source', 'human')),
            human_executive_summary=data.get('human_executive_summary', ''),
            human_investment_rationale=data.get('human_investment_rationale', ''),
            ai_rationale=data.get('ai_rationale', ''),
            ai_context=data.get('ai_context', ''),
            ai_executive_summary=data.get('ai_executive_summary', ''),
            ai_investment_rationale=data.get('ai_investment_rationale', ''),
            ai_executive_summary_markdown=data.get('ai_executive_summary_markdown', ''),
            ai_investment_rationale_markdown=data.get('ai_investment_rationale_markdown', ''),
            company_logo_filename=data.get('company_logo_filename'),
            chart_image_filename=data.get('chart_image_filename'),
            template_version=TemplateVersion(data.get('template_version', 'v2')),
            timestamp=data.get('timestamp', '')
        )
    
    def validate(self) -> List[str]:
        """
        Validate form data and return list of error messages.
        
        Returns:
            List[str]: List of validation error messages. Empty list if validation passes.
        """
        errors = []
        
        # Required fields validation
        errors.extend(self._validate_required_fields())
        
        # Content validation based on source
        errors.extend(self._validate_content())
        
        # Price validation
        errors.extend(self._validate_prices())
        
        # Business rule validation
        errors.extend(self._validate_business_rules())
        
        return errors
    
    def _validate_required_fields(self) -> List[str]:
        """Validate required fields."""
        errors = []
        
        if not self.company_name.strip():
            errors.append(ERROR_MESSAGES['company_name_required'])
        
        if not self.ticker.strip():
            errors.append(ERROR_MESSAGES['ticker_required'])
        
        if not self.analysis_types:
            errors.append(ERROR_MESSAGES['analysis_type_required'])
        
        return errors
    
    def _validate_content(self) -> List[str]:
        """Validate content based on source."""
        errors = []
        
        if self.content_source == ContentSource.HUMAN:
            if not self.human_executive_summary.strip():
                errors.append(ERROR_MESSAGES['executive_summary_required'])
            if not self.human_investment_rationale.strip():
                errors.append(ERROR_MESSAGES['investment_rationale_required'])
        elif self.content_source == ContentSource.AI:
            if not self.ai_rationale.strip():
                errors.append(ERROR_MESSAGES['ai_rationale_required'])
        
        return errors
    
    def _validate_prices(self) -> List[str]:
        """Validate price fields."""
        errors = []
        
        # Price validation is optional - no validation needed
        # This method is kept for future extensibility
        
        return errors
    
    def _validate_business_rules(self) -> List[str]:
        """Validate business rules."""
        errors = []
        
        # Validate ticker format (basic check)
        if self.ticker and not self.ticker.replace('.', '').replace('-', '').isalnum():
            errors.append(ERROR_MESSAGES['ticker_format_invalid'])
        
        # Validate company name length
        if self.company_name and len(self.company_name.strip()) < 2:
            errors.append(ERROR_MESSAGES['company_name_too_short'])
        
        return errors
    
    def get_executive_summary(self) -> str:
        """
        Get the appropriate executive summary based on content source.
        
        Returns:
            str: Executive summary content from the active content source.
        """
        if self.content_source == ContentSource.AI:
            return self.ai_executive_summary
        return self.human_executive_summary
    
    def get_investment_rationale(self) -> str:
        """
        Get the appropriate investment rationale based on content source.
        
        Returns:
            str: Investment rationale content from the active content source.
        """
        if self.content_source == ContentSource.AI:
            return self.ai_investment_rationale
        return self.human_investment_rationale
    
    def get_executive_summary_for_pdf(self) -> str:
        """
        Get the appropriate executive summary for PDF generation.
        
        For AI content, prefers original Markdown content if available.
        
        Returns:
            str: Executive summary content optimized for PDF generation.
        """
        if self.content_source == ContentSource.AI:
            return self.ai_executive_summary_markdown if self.ai_executive_summary_markdown else self.ai_executive_summary
        return self.human_executive_summary
    
    def get_investment_rationale_for_pdf(self) -> str:
        """
        Get the appropriate investment rationale for PDF generation.
        
        For AI content, prefers original Markdown content if available.
        
        Returns:
            str: Investment rationale content optimized for PDF generation.
        """
        if self.content_source == ContentSource.AI:
            return self.ai_investment_rationale_markdown if self.ai_investment_rationale_markdown else self.ai_investment_rationale
        return self.human_investment_rationale
    
    def is_buy_or_add_action(self) -> bool:
        """
        Check if the action is Buy, Add, or Switch (requires entry, target, stop loss).
        
        Returns:
            bool: True if action is Buy, Add, or Switch, False otherwise.
        """
        return self.action.lower() in ['buy', 'add', 'switch']
    
    def is_sell_or_take_profit_action(self) -> bool:
        """
        Check if the action is Sell or Take Profit (requires only exit price).
        
        Returns:
            bool: True if action is Sell or Take Profit, False otherwise.
        """
        return self.action.lower() in ['sell', 'take profit']
    
    def get_primary_price(self) -> float:
        """
        Get the primary price field based on action type.
        
        Returns:
            float: Entry price for Buy/Add actions, exit price for Sell/Take Profit actions.
        """
        if self.is_buy_or_add_action():
            return self.entry_price
        else:
            return self.exit_price
    
    def get_price_fields_for_display(self) -> Dict[str, float]:
        """
        Get the appropriate price fields for display based on action type.
        
        Returns:
            Dict[str, float]: Dictionary with appropriate price fields for the action.
        """
        if self.is_buy_or_add_action():
            return {
                'entry_price': self.entry_price,
                'target_price': self.target_price,
                'stop_loss': self.stop_loss
            }
        else:
            return {
                'exit_price': self.exit_price
            }
