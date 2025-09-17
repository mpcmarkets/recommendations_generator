#!/usr/bin/env python3
"""
OpenRouter-specific AI service for content generation
"""

import os
import sys
from typing import Optional, Tuple
import streamlit as st

from models.form_data import FormData
from services.openrouter_models import OpenRouterModelManager, OpenRouterModel


class OpenRouterAIService:
    """Service for OpenRouter AI content generation with singleton pattern"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenRouterAIService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if not self._initialized:
            self._llm_instance = None
            self._ai_available = False
            self._initialize_ai()
            OpenRouterAIService._initialized = True
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset singleton instance (for testing or reinitialization)"""
        cls._instance = None
        cls._initialized = False
    
    def _initialize_ai(self):
        """Initialize OpenRouter AI service"""
        try:
            from ai_tools import LLMFactory
            from prompts import format_investment_thesis_prompt, format_analysis_prompt
            
            # Initialize the LLM factory
            llm_factory = LLMFactory()
            
            # Get the OpenRouter provider
            self._openrouter_provider = llm_factory.get_provider('openrouter')
            
            if not self._openrouter_provider:
                raise Exception("OpenRouter provider not available")
            
            # Test OpenRouter availability
            if not self._openrouter_provider.test_availability():
                raise Exception("OpenRouter API is not available")
            
            self._ai_available = True
            
        except ImportError as e:
            self._ai_available = False
            raise ImportError(f"AI service dependencies not available: {e}. Please install ai_tools and prompts modules.")
        except Exception as e:
            self._ai_available = False
            raise Exception(f"OpenRouter AI service initialization failed: {e}")
    
    @property
    def is_available(self) -> bool:
        """Check if OpenRouter AI service is available"""
        return self._ai_available
    
    def get_llm_for_model(self, model: OpenRouterModel):
        """Get LLM instance for a specific model"""
        if not self._ai_available or not self._openrouter_provider:
            raise RuntimeError("OpenRouter AI service is not available")
        
        return self._openrouter_provider.get_llm(model_name=model.model_name)
    
    def generate_content(self, form_data: FormData) -> Tuple[str, str]:
        """
        Generate AI content for investment recommendation using selected model
        
        Args:
            form_data: Form data containing investment details
            
        Returns:
            Tuple of (executive_summary_html, investment_rationale_html)
        """
        if not self._ai_available:
            raise RuntimeError("OpenRouter AI service is not available. Please ensure ai_tools and prompts modules are installed.")
        
        try:
            # Get the selected model
            selected_model = OpenRouterModelManager.get_selected_model()
            
            # Get LLM instance for the selected model
            llm_instance = self.get_llm_for_model(selected_model)
            
            # Generate investment summary (returns markdown)
            executive_summary_markdown = self._generate_investment_thesis(form_data, llm_instance)
            
            # Generate investment rationale (returns markdown)
            investment_rationale_markdown = self._generate_analysis(form_data, llm_instance)
            
            # Store original Markdown content for PDF generation
            form_data.ai_executive_summary_markdown = executive_summary_markdown
            form_data.ai_investment_rationale_markdown = investment_rationale_markdown
            
            # Convert Markdown to HTML for QuillJS display
            executive_summary_html = self._format_text_for_display(executive_summary_markdown)
            investment_rationale_html = self._format_text_for_display(investment_rationale_markdown)
            
            # Store HTML content for QuillJS
            form_data.ai_executive_summary = executive_summary_html
            form_data.ai_investment_rationale = investment_rationale_html
            
            return executive_summary_html, investment_rationale_html
            
        except Exception as e:
            raise Exception(f"AI content generation failed: {e}")
    
    def _generate_investment_thesis(self, form_data: FormData, llm_instance) -> str:
        """Generate investment summary using AI (returns raw markdown)"""
        try:
            from prompts import format_investment_thesis_prompt
            
            prompt = format_investment_thesis_prompt(
                ticker=form_data.ticker,
                action=form_data.action,
                entry_price=form_data.entry_price,
                target_price=form_data.target_price,
                stop_loss=form_data.stop_loss,
                analysis_types=form_data.analysis_types,
                investment_rationale=form_data.ai_rationale,
                context=form_data.ai_context,
                exit_price=form_data.exit_price
            )
            
            response = llm_instance.invoke(prompt)
            raw_content = response.content if hasattr(response, 'content') else str(response)
            
            # Return raw markdown content (don't format here)
            return self._normalize_encoding(raw_content)
            
        except Exception as e:
            st.warning(f"AI thesis generation failed: {e}")
            return self._generate_fallback_thesis(form_data)
    
    def _generate_analysis(self, form_data: FormData, llm_instance) -> str:
        """Generate investment rationale using AI (returns raw markdown)"""
        try:
            from prompts import format_analysis_prompt
            
            prompt = format_analysis_prompt(
                ticker=form_data.ticker,
                action=form_data.action,
                entry_price=form_data.entry_price,
                target_price=form_data.target_price,
                stop_loss=form_data.stop_loss,
                analysis_types=form_data.analysis_types,
                investment_rationale=form_data.ai_rationale,
                context=form_data.ai_context,
                exit_price=form_data.exit_price
            )
            
            response = llm_instance.invoke(prompt)
            raw_content = response.content if hasattr(response, 'content') else str(response)
            
            # Return raw markdown content (don't format here)
            return self._normalize_encoding(raw_content)
            
        except Exception as e:
            st.warning(f"AI analysis generation failed: {e}")
            return self._generate_fallback_analysis(form_data)
    
    def _generate_fallback_thesis(self, form_data: FormData) -> str:
        """Generate fallback investment thesis in simple format"""
        analysis_types_str = ', '.join(form_data.analysis_types)
        return f"""
**Investment Thesis for {form_data.company_name} ({form_data.ticker})**

We recommend a **{form_data.action}** position in **{form_data.ticker}** based on comprehensive *{analysis_types_str}* analysis. The investment thesis centers on the company's strong fundamentals and favorable risk-reward profile.

With an entry price of **${form_data.entry_price}**, target price of **${form_data.target_price}**, and stop loss at **${form_data.stop_loss}**, this recommendation offers a compelling risk-adjusted return opportunity. The analysis indicates strong potential for capital appreciation while maintaining disciplined risk management.

Key investment drivers include:
• The company's competitive positioning
• Robust financial metrics
• Positive industry trends

The risk management framework ensures capital preservation through the defined stop loss level.
        """.strip()
    
    def _generate_fallback_analysis(self, form_data: FormData) -> str:
        """Generate fallback investment analysis in simple format"""
        analysis_types_str = ', '.join(form_data.analysis_types)
        return f"""
## **Detailed Investment Analysis for {form_data.company_name} ({form_data.ticker})**

### **ANALYSIS FRAMEWORK**
Our recommendation is based on comprehensive *{analysis_types_str}* analysis, providing a multi-dimensional view of the investment opportunity.

### **FUNDAMENTAL ANALYSIS**
The company demonstrates strong financial fundamentals with consistent revenue growth and improving profitability metrics. Key financial ratios indicate healthy balance sheet management and efficient capital allocation.

### **TECHNICAL ANALYSIS**
Chart analysis reveals favorable technical patterns with the stock trading above key support levels. Momentum indicators suggest positive price action potential, supporting our bullish outlook.

### **RISK ASSESSMENT**
While the investment presents attractive upside potential, key risks include:
• Market volatility
• Sector-specific headwinds
• Broader economic uncertainties

Our stop loss at **${form_data.stop_loss}** provides downside protection.

### **CONCLUSION**
The combination of strong fundamentals, positive technical indicators, and favorable risk-reward profile supports our **{form_data.action}** recommendation with a target price of **${form_data.target_price}**.
        """.strip()
    
    def _format_text_for_display(self, text: str) -> str:
        """Simple text formatting for QuillJS display - based on original approach"""
        if not isinstance(text, str):
            return str(text)
        
        # Normalize encoding first
        text = self._normalize_encoding(text)
        
        # Simple cleaning based on original approach
        text = self._clean_llm_output_for_display(text)
        
        # Convert plain text to simple HTML paragraphs for QuillJS
        return self._convert_plain_text_to_html(text)
    
    def _normalize_encoding(self, text: str) -> str:
        """Normalize text encoding to handle UTF-8 issues"""
        if not isinstance(text, str):
            text = str(text)
        
        # Handle common encoding issues
        try:
            # Try to encode and decode to ensure it's valid UTF-8
            text.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            # If there are encoding issues, try to fix them
            try:
                # Try to decode as latin-1 and re-encode as UTF-8
                text = text.encode('latin-1').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                # If all else fails, replace problematic characters
                text = text.encode('utf-8', errors='replace').decode('utf-8')
        
        # Clean up any remaining problematic characters
        text = text.replace('\x97', '—')  # Replace em dash
        text = text.replace('\x96', '–')  # Replace en dash
        text = text.replace('\x91', "'")  # Replace left single quote
        text = text.replace('\x92', "'")  # Replace right single quote
        text = text.replace('\x93', '"')  # Replace left double quote
        text = text.replace('\x94', '"')  # Replace right double quote
        
        return text
    
    def _clean_llm_output_for_display(self, text: str) -> str:
        """Clean and format LLM output for display - simplified approach"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove any markdown formatting
        text = text.replace('**', '').replace('*', '').replace('`', '')
        text = text.replace('__', '')  # Remove markdown bold/italic markers
        
        # Clean up multiple spaces and line breaks
        import re
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple line breaks to double
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        
        # Ensure proper sentence spacing
        text = re.sub(r'\.([A-Z])', r'. \1', text)  # Add space after periods before capitals
        
        # Clean up common formatting issues
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)  # Remove spaces before punctuation
        
        return text.strip()
    
    def _convert_plain_text_to_html(self, text: str) -> str:
        """Convert plain text with paragraph breaks and basic formatting to simple HTML"""
        if not text:
            return ""
        
        # Split by double newlines (paragraph breaks)
        paragraphs = text.split('\n\n')
        
        # Convert each paragraph to HTML
        html_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if para:
                # Check if this paragraph contains bullet points
                if '- ' in para and para.count('\n') > 0:
                    # Handle bullet points
                    html_para = self._format_bullets_for_html(para)
                    html_paragraphs.append(html_para)
                else:
                    # Regular paragraph
                    # Handle basic subsections (text ending with colon)
                    if ':' in para and not para.endswith('.') and not para.endswith('!') and not para.endswith('?'):
                        para = self._format_subsections_for_html(para)
                    html_paragraphs.append(f"<p>{para}</p>")
        
        return '\n'.join(html_paragraphs)
    
    def _format_bullets_for_html(self, text: str) -> str:
        """Convert dash bullets to HTML list"""
        lines = text.split('\n')
        html_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                bullet_content = line[2:].strip()
                html_lines.append(f'<li>{bullet_content}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if line:
                    html_lines.append(f'<p>{line}</p>')
        
        if in_list:
            html_lines.append('</ul>')
        
        return '\n'.join(html_lines)
    
    def _format_subsections_for_html(self, text: str) -> str:
        """Format basic subsections with bold headings"""
        # Simple pattern: if a line ends with colon, make it bold
        import re
        # Match text like "Key Strengths:" at the start of a line
        text = re.sub(r'^([^:]+:)\s*', r'<strong>\1</strong> ', text, flags=re.MULTILINE)
        return text
