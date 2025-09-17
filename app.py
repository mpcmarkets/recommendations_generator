#!/usr/bin/env python3
"""
Investment Recommendation Generator v2 - Modular Architecture
Clean, maintainable, and fully functional Streamlit application
"""

import streamlit as st
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# AI tools library is now installed as a package

# Import our modules
from config import APP_TITLE, APP_ICON, DEFAULT_TEMPLATE, ERROR_MESSAGES
from models import FormData, ContentSource
from services import ImageService, PDFService
from services.openrouter_ai_service import OpenRouterAIService
from components import (
    AppHeader, NavigationSidebar,
    BasicInfoForm, AnalysisForm, TradePlanForm, 
    ImageUploadForm, TemplateForm,
    ContentReview, ReportGeneration
)
from constants import MAIN_CSS
from utils import get_logger

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set default theme to light mode
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        color-scheme: light;
    }
    
    /* Override dark theme elements */
    .stApp > header {
        background-color: transparent;
    }
    .stApp > div[data-testid="stToolbar"] {
        background-color: transparent;
    }
    .stApp > div[data-testid="stDecoration"] {
        background-color: transparent;
    }
    .stApp > div[data-testid="stStatusWidget"] {
        background-color: transparent;
    }
    .stApp > div[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    
    /* Ensure light theme for main content */
    .main .block-container {
        background-color: white;
        color: black;
    }
    
    /* Light theme for sidebar */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    
    /* Override any dark theme text colors */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: black;
    }
    
    .stApp p, .stApp div, .stApp span {
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Apply custom CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)


class InvestmentRecommendationApp:
    """
    Main application class for the Investment Recommendation Generator.
    
    This class manages the entire application flow, including form rendering,
    content generation, and report creation. It handles navigation between
    different sections and maintains application state.
    """
    
    def __init__(self):
        """
        Initialize the application with required services and session state.
        
        Sets up AI service (singleton), image service, and initializes the session state.
        PDF service is lazy-loaded to avoid startup errors.
        """
        self.logger = get_logger()
        
        try:
            # Use singleton pattern for OpenRouter AI service to avoid re-initialization
            self.ai_service = OpenRouterAIService.get_instance()
            self.image_service = ImageService()
            # PDF service will be lazy-loaded when needed
            self._pdf_service = None
            
            # Initialize session state
            self._initialize_session_state()
            
            self.logger.info("Application initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}", exc_info=True)
            st.error("Application initialization failed. Please refresh the page and try again.")
            raise
    
    @property
    def pdf_service(self):
        """Lazy-load PDF service to avoid startup errors"""
        if self._pdf_service is None:
            try:
                self._pdf_service = PDFService()
                self.logger.info("PDF service initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize PDF service: {e}", exc_info=True)
                st.error("PDF service initialization failed. Please check LaTeX installation.")
                raise
        return self._pdf_service
    
    def _initialize_session_state(self) -> None:
        """
        Initialize session state with default values.
        
        Sets up default values for form data, current step, AI content flags,
        content source, and template version if they don't exist in session state.
        """
        defaults: Dict[str, Any] = {
            'form_data': None,
            'current_step': 'form',
            'ai_content_generated': False,
            'ai_executive_summary': '',
            'ai_investment_rationale': '',
            'content_source': 'human',
            'template_version': DEFAULT_TEMPLATE
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def run(self) -> None:
        """
        Run the main application.
        
        This is the main entry point that renders the header, sidebar,
        and main content based on the current step in the application flow.
        """
        # Render header
        AppHeader.render()
        
        # Render sidebar
        NavigationSidebar.render()
        
        # Render main content based on current step
        if st.session_state.current_step == 'form':
            self._render_form_section()
        elif st.session_state.current_step == 'review':
            self._render_review_section()
    
    def _render_form_section(self) -> None:
        """
        Render the form input section.
        
        This method renders all form components including basic information,
        analysis types, trade plan, images, and template selection. It also
        handles form validation and navigation to the review section.
        """
        # Basic Information
        basic_info = BasicInfoForm.render()
        
        # Analysis Types
        analysis_types = AnalysisForm.render()
        
        # Trade Plan
        trade_plan = TradePlanForm.render()
        
        # Images
        images = ImageUploadForm.render()
        
        # Content Generation removed - moved to Review & Generate section
        
        # Template Selection
        template_version = TemplateForm.render()
        
        # Create form data object
        # Get existing form data to preserve image filenames
        existing_form_data = getattr(st.session_state, 'form_data', None)
        
        # Save uploaded images if any
        company_logo_filename = None
        chart_image_filename = None
        
        if images['company_logo']:
            company_logo_filename = self.image_service.save_uploaded_image(
                images['company_logo'], 'company_logo'
            )
        elif images.get('company_logo_filename'):
            company_logo_filename = images['company_logo_filename']
        elif existing_form_data and existing_form_data.company_logo_filename:
            company_logo_filename = existing_form_data.company_logo_filename
        
        if images['chart_image']:
            chart_image_filename = self.image_service.save_uploaded_image(
                images['chart_image'], 'chart_image'
            )
        elif images.get('chart_image_filename'):
            chart_image_filename = images['chart_image_filename']
        elif existing_form_data and existing_form_data.chart_image_filename:
            chart_image_filename = existing_form_data.chart_image_filename
        
        form_data = FormData(
            category=basic_info['category'],
            action=basic_info['action'],
            ticker=basic_info['ticker'],
            company_name=basic_info['company_name'],
            subtitle=basic_info['subtitle'],
            analysis_types=analysis_types,
            entry_price=trade_plan['entry_price'],
            target_price=trade_plan['target_price'],
            stop_loss=trade_plan['stop_loss'],
            # content_source will be set in Review & Generate section
            company_logo=images['company_logo'],
            chart_image=images['chart_image'],
            company_logo_filename=company_logo_filename,
            chart_image_filename=chart_image_filename,
            template_version=template_version,
            timestamp=datetime.now().isoformat()
        )
        
        # Content generation moved to Review & Generate section
        
        # Store form data
        st.session_state.form_data = form_data
        
        # Navigation to Review & Generate
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
            <h3 style='color: #27ae60; margin: 0 0 8px 0;'>✅ Form Complete</h3>
            <p style='color: #2e7d32; margin: 0;'>All form data has been collected. Ready to generate content and create your report.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Generate Content", width='stretch'):
            st.session_state.current_step = 'review'
            st.rerun()
    
    # _process_form_submission method removed - content generation moved to Review & Generate section
    
    def _render_review_section(self) -> None:
        """
        Render the review and generate section.
        
        This method handles the content generation and review phase, including
        AI content generation, QuillJS editors for content editing, and
        final report generation. It manages content persistence across navigation
        and ensures proper content source selection.
        """
        if not st.session_state.form_data:
            st.info("Please fill out the form first in the Form Input section.")
            if st.button("Go to Form Input"):
                st.session_state.current_step = 'form'
                st.rerun()
            return
        
        form_data = st.session_state.form_data
        
        # Restore content from session state if available (for persistence across navigation)
        if 'human_executive_summary' in st.session_state:
            form_data.human_executive_summary = st.session_state.human_executive_summary
        if 'human_investment_rationale' in st.session_state:
            form_data.human_investment_rationale = st.session_state.human_investment_rationale
        if 'ai_executive_summary' in st.session_state:
            form_data.ai_executive_summary = st.session_state.ai_executive_summary
        if 'ai_investment_rationale' in st.session_state:
            form_data.ai_investment_rationale = st.session_state.ai_investment_rationale
        
        # Content generation and editing
        content_updates = ContentReview.render(form_data)
        
        # Update form data with content based on active tab
        if content_updates:
            if st.session_state.active_content_tab == 0:  # Human tab
                form_data.human_executive_summary = content_updates.get('executive_summary', '')
                form_data.human_investment_rationale = content_updates.get('investment_rationale', '')
                form_data.content_source = ContentSource.HUMAN
            else:  # AI tab
                form_data.ai_executive_summary = content_updates.get('executive_summary', '')
                form_data.ai_investment_rationale = content_updates.get('investment_rationale', '')
                form_data.content_source = ContentSource.AI
        
        # Ensure content source is set based on active tab
        if st.session_state.active_content_tab == 0:
            form_data.content_source = ContentSource.HUMAN
        else:
            form_data.content_source = ContentSource.AI
        
        # Save updated form data back to session state
        st.session_state.form_data = form_data
        
        # Generate Report
        if ReportGeneration.render_generation_button():
            self._generate_final_report(form_data)
    
    def _generate_final_report(self, form_data: FormData):
        """
        Generate the final PDF report.
        
        Args:
            form_data: The form data containing all information for the report
            
        This method ensures the content source is correctly set based on the
        active tab, generates the PDF report using the PDF service, and
        displays the results to the user.
        """
        with st.spinner("Generating final report..."):
            try:
                self.logger.info("Starting report generation")
                
                # CRITICAL: Ensure content source is correctly set based on active tab
                if st.session_state.get('active_content_tab', 0) == 0:
                    form_data.content_source = ContentSource.HUMAN
                    self.logger.info("Content source set to HUMAN")
                else:
                    form_data.content_source = ContentSource.AI
                    self.logger.info("Content source set to AI")
                
                # Generate PDF
                pdf_file, report_data = self.pdf_service.generate_report(form_data)
                
                # Display results
                ReportGeneration.render(form_data, str(pdf_file), report_data.to_dict())
                
                self.logger.info(f"Report generated successfully: {pdf_file}")
                
            except Exception as e:
                self.logger.error(f"Error generating report: {e}", exc_info=True)
                st.error(ERROR_MESSAGES['pdf_generation_failed'])
                st.error("Please check the logs for more details.")


def main() -> None:
    """
    Main application function.
    
    Initializes and runs the Investment Recommendation Generator application
    with proper error handling and logging.
    """
    try:
        app = InvestmentRecommendationApp()
        app.run()
    except Exception as e:
        logger = get_logger()
        logger.critical(f"Application crashed: {e}", exc_info=True)
        st.error("Application encountered an unexpected error. Please refresh the page and try again.")
        st.error("If the problem persists, please check the logs for more details.")


if __name__ == "__main__":
    main()
