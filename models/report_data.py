#!/usr/bin/env python3
"""
Report data model for PDF generation
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from .form_data import FormData


@dataclass
class ReportData:
    """Data structure for report generation"""
    # Basic Information
    title: str
    subtitle: str
    category: str
    action: str
    ticker: str
    
    # Trade Plan
    entry_price: str
    target_price: str
    stop_loss: str
    exit_price: str
    
    # Analysis
    analysis_types: List[str]
    
    # Content
    investment_thesis: str
    rationale: str
    
    # Images
    company_logo_filename: Optional[str]
    chart_image_filename: Optional[str]
    
    # Metadata
    report_date: str
    risk_level: str
    potential_return: str
    risk_amount: str
    
    @classmethod
    def from_form_data(cls, form_data: FormData) -> 'ReportData':
        """Create report data from form data and risk metrics"""
        # Generate title
        if form_data.company_name and form_data.ticker:
            title = f"{form_data.company_name} ({form_data.ticker})"
        elif form_data.company_name:
            title = form_data.company_name
        elif form_data.ticker:
            title = f"Investment Recommendation ({form_data.ticker})"
        else:
            title = 'Investment Recommendation'
        
        return cls(
            title=title,
            subtitle=form_data.subtitle,
            category=form_data.category,
            action=form_data.action,
            ticker=form_data.ticker,
            entry_price=f"{form_data.entry_price:.2f}",
            target_price=f"{form_data.target_price:.2f}",
            stop_loss=f"{form_data.stop_loss:.2f}",
            exit_price=f"{form_data.exit_price:.2f}",
            analysis_types=[at if isinstance(at, str) else at.value for at in form_data.analysis_types],
            investment_thesis=form_data.get_executive_summary_for_pdf(),
            rationale=form_data.get_investment_rationale_for_pdf(),
            company_logo_filename=form_data.company_logo_filename,
            chart_image_filename=form_data.chart_image_filename,
            report_date=datetime.now().strftime('%d-%m-%Y'),
            risk_level="Medium",  # Default risk level
            potential_return="N/A",  # No risk metrics calculation
            risk_amount="N/A"  # No risk metrics calculation
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for template processing"""
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'category': self.category,
            'action': self.action,
            'ticker': self.ticker,
            'entry_price': self.entry_price,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'exit_price': self.exit_price,
            'analysis_types': self.analysis_types,
            'investment_thesis': self.investment_thesis,
            'rationale': self.rationale,
            'company_logo_filename': self.company_logo_filename,
            'chart_image_filename': self.chart_image_filename,
            'report_date': self.report_date,
            'risk_level': self.risk_level,
            'potential_return': self.potential_return,
            'risk_amount': self.risk_amount
        }
