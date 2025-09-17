#!/usr/bin/env python3
"""
Form components for the investment recommendation form
"""

import streamlit as st
import os
import base64
from typing import Dict, Any, List
from models.form_data import FormData, AnalysisType, ContentSource, TemplateVersion
from config import (
    DEFAULT_FORM_CATEGORY, DEFAULT_FORM_ACTION, 
    DEFAULT_ENTRY_PRICE, DEFAULT_TARGET_PRICE, DEFAULT_STOP_LOSS,
    TEMPLATE_PREVIEW_IMAGES, COLORS
)


def get_template_preview_html(template_version: str) -> str:
    """
    Generate HTML for template preview.
    
    Args:
        template_version: The template version ('v1', 'v2', 'v3')
        
    Returns:
        str: HTML string for template preview
    """
    try:
        templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        
        # Template configuration
        template_config = {
            'v1': {
                'image': 'v1_preview.png',
                'border_color': COLORS['secondary'],
                'name': 'Template v1',
                'description': 'Classic layout with side-by-side elements'
            },
            'v2': {
                'image': 'v2_preview.png',
                'border_color': '#9b59b6',
                'name': 'Template v2',
                'description': 'Modern centered layout'
            },
            'v3': {
                'image': 'v3_preview.png',
                'border_color': COLORS['danger'],
                'name': 'Template v3',
                'description': 'Clean layout with dynamic checkboxes (New)'
            }
        }
        
        config = template_config.get(template_version, template_config['v2'])
        image_path = os.path.join(templates_dir, config['image'])
        border_color = config['border_color']
        template_name = config['name']
        description = config['description']
        
        # Read and encode the image
        with open(image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        return f"""
            <div style='display: flex; flex-direction: column; align-items: center; background: #f8f9fa; padding: 12px; border-radius: 8px; border: 2px solid {border_color}; box-shadow: 0 4px 8px rgba(0,0,0,0.1); overflow: hidden; width: 100%; max-width: 100%; box-sizing: border-box;'>
                <div style='text-align: center; margin-bottom: 10px; width: 100%; max-width: 100%; overflow: hidden;'>
                    <h3 style='margin: 0 0 3px 0; color: #2c3e50; font-size: 16px; font-weight: bold; word-wrap: break-word;'>{template_name}</h3>
                    <p style='margin: 0; color: #6c757d; font-size: 12px; font-style: italic; word-wrap: break-word;'>{description}</p>
                </div>
                <div style='width: 100%; max-width: 100%; text-align: center; overflow: hidden; position: relative;'>
                    <img src="data:image/png;base64,{img_base64}" 
                         style='max-width: 100%; width: auto; max-height: 250px; height: auto; border-radius: 6px; box-shadow: 0 3px 8px rgba(0,0,0,0.15); object-fit: contain; display: block; margin: 0 auto;' 
                         alt='{template_name} Preview' />
                </div>
                <div style='margin-top: 8px; text-align: center; width: 100%; max-width: 100%; overflow: hidden;'>
                    <div style='background: {border_color}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; max-width: 100%; word-wrap: break-word;'>
                        ✓ Currently Selected
                    </div>
                </div>
            </div>
        """
        
    except FileNotFoundError:
        return f"""
            <div style='display: flex; justify-content: center; align-items: center; background: #f8f9fa; padding: 40px; border-radius: 8px; border: 2px solid #e74c3c;'>
                <div style='text-align: center; color: #e74c3c;'>
                    <h3 style='margin: 0 0 10px 0;'>Preview Image Not Found</h3>
                    <p style='margin: 0;'>Could not load {template_version}_preview.png</p>
                </div>
            </div>
        """


class BasicInfoForm:
    """Component for basic investment information"""
    
    @staticmethod
    def render() -> Dict[str, Any]:
        """Render basic information form"""
        st.markdown("""
        <div class="section-header">
            <h3>📊 Investment Details</h3>
            <p>Enter the core details for your investment recommendation</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Get default values from session state if available
        form_data = getattr(st.session_state, 'form_data', None)
        
        with col1:
            category_options = ['ASX Alpha', 'Global Alpha', 'High Conviction', 'ETF Elite', 'Structured Products']
            category_default = 0
            if form_data and form_data.category:
                try:
                    category_default = category_options.index(form_data.category)
                except ValueError:
                    category_default = 0
            
            category = st.selectbox(
                "Category:",
                options=category_options,
                index=category_default,
                key="form_category"
            )
        
        with col2:
            action_options = ['Buy', 'Add', 'Take Profit', 'Sell']
            action_default = 0
            if form_data and form_data.action:
                try:
                    action_default = action_options.index(form_data.action)
                except ValueError:
                    action_default = 0
                    
            action = st.selectbox(
                "Action:",
                options=action_options,
                index=action_default,
                key="form_action"
            )
        
        ticker_default = form_data.ticker if form_data and form_data.ticker else ""
        ticker = st.text_input(
            "Ticker:",
            value=ticker_default,
            placeholder="Enter ticker symbol (e.g., AAPL)",
            key="form_ticker"
        ).upper()
        
        company_name_default = form_data.company_name if form_data and form_data.company_name else ""
        company_name = st.text_input(
            "Company Name:",
            value=company_name_default,
            placeholder="Enter company name (e.g., Apple Inc.)",
            key="form_company_name"
        )
        
        subtitle_default = form_data.subtitle if form_data and form_data.subtitle else ""
        subtitle = st.text_input(
            "Subtitle:",
            value=subtitle_default,
            placeholder="Enter subtitle (optional)",
            key="form_subtitle"
        )
        
        return {
            'category': category,
            'action': action,
            'ticker': ticker,
            'company_name': company_name,
            'subtitle': subtitle
        }


class AnalysisForm:
    """Component for analysis framework selection"""
    
    @staticmethod
    def render() -> List[AnalysisType]:
        """Render analysis types form"""
        st.markdown("""
        <div class="section-header">
            <h3>🔍 Analysis Framework</h3>
            <p>Select the types of analysis to include</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get default values from session state if available
        form_data = getattr(st.session_state, 'form_data', None)
        fundamentals_default = False
        technical_default = False
        macro_default = False
        catalyst_default = False
        
        if form_data and form_data.analysis_types:
            fundamentals_default = 'Fundamentals' in form_data.analysis_types
            technical_default = 'Technical Analysis' in form_data.analysis_types
            macro_default = 'Macro/Geopolitical' in form_data.analysis_types
            catalyst_default = 'Catalyst' in form_data.analysis_types
        
        col1, col2 = st.columns(2)
        
        with col1:
            fundamentals = st.checkbox("Fundamentals", value=fundamentals_default, key="form_fundamentals")
            technical = st.checkbox("Technical Analysis", value=technical_default, key="form_technical")
        
        with col2:
            macro = st.checkbox("Macro/Geopolitical", value=macro_default, key="form_macro")
            catalyst = st.checkbox("Catalyst", value=catalyst_default, key="form_catalyst")
        
        analysis_types = []
        if fundamentals:
            analysis_types.append('Fundamentals')
        if technical:
            analysis_types.append('Technical Analysis')
        if macro:
            analysis_types.append('Macro/Geopolitical')
        if catalyst:
            analysis_types.append('Catalyst')
        
        return analysis_types


class TradePlanForm:
    """Component for trade plan input"""
    
    @staticmethod
    def render() -> Dict[str, float]:
        """Render trade plan form"""
        st.markdown("""
        <div class="section-header">
            <h3>💰 Trade Plan</h3>
            <p>Define your entry, target, and stop loss prices</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get default values from session state if available
        form_data = getattr(st.session_state, 'form_data', None)
        entry_default = form_data.entry_price if form_data and form_data.entry_price > 0 else 0.01
        target_default = form_data.target_price if form_data and form_data.target_price > 0 else 0.01
        stop_default = form_data.stop_loss if form_data and form_data.stop_loss > 0 else 0.01
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            entry_price = st.number_input(
                "Entry Price:",
                value=entry_default,
                step=0.01,
                key="form_entry_price"
            )
        
        with col2:
            target_price = st.number_input(
                "Target Price:",
                value=target_default,
                step=0.01,
                key="form_target_price"
            )
        
        with col3:
            stop_loss = st.number_input(
                "Stop Loss:",
                value=stop_default,
                step=0.01,
                key="form_stop_loss"
            )
        
        return {
            'entry_price': entry_price,
            'target_price': target_price,
            'stop_loss': stop_loss
        }


class ImageUploadForm:
    """Component for image uploads"""
    
    @staticmethod
    def render() -> Dict[str, Any]:
        """Render image upload form"""
        st.markdown("""
        <div class="section-header">
            <h3>🖼️ Images</h3>
            <p>Upload featured images and charts</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get previously uploaded images from session state
        form_data = getattr(st.session_state, 'form_data', None)
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_logo = st.file_uploader(
                "Featured Image:",
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'],
                key="form_company_logo"
            )
            
            # Handle new upload or show cached image
            if company_logo:
                # New file uploaded - update session state and show preview
                st.session_state.uploaded_company_logo = company_logo
                st.image(company_logo, caption="Featured Image Preview", width='stretch')
            elif 'uploaded_company_logo' in st.session_state:
                # Show previously uploaded image from session state
                if isinstance(st.session_state.uploaded_company_logo, str):
                    # It's a filename, show the saved image
                    from pathlib import Path
                    from config import IMAGES_DIR
                    image_path = IMAGES_DIR / st.session_state.uploaded_company_logo
                    if image_path.exists():
                        st.image(str(image_path), caption="Previously Uploaded Featured Image", width='stretch')
                        st.info(f"📷 Using previously uploaded: {st.session_state.uploaded_company_logo}")
                else:
                    # It's a file object, show it
                    st.image(st.session_state.uploaded_company_logo, caption="Previously Uploaded Featured Image", width='stretch')
                    st.info("📷 Using previously uploaded image")
            elif form_data and form_data.company_logo_filename:
                # Restore from form data if no session state
                from pathlib import Path
                from config import IMAGES_DIR
                image_path = IMAGES_DIR / form_data.company_logo_filename
                if image_path.exists():
                    st.session_state.uploaded_company_logo = form_data.company_logo_filename
                    st.image(str(image_path), caption="Previously Uploaded Featured Image", width='stretch')
                    st.info(f"📷 Using previously uploaded: {form_data.company_logo_filename}")
        
        with col2:
            chart_image = st.file_uploader(
                "Chart Image:",
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'],
                key="form_chart_image"
            )
            
            # Handle new upload or show cached image
            if chart_image:
                # New file uploaded - update session state and show preview
                st.session_state.uploaded_chart_image = chart_image
                st.image(chart_image, caption="Chart Image Preview", width='stretch')
            elif 'uploaded_chart_image' in st.session_state:
                # Show previously uploaded image from session state
                if isinstance(st.session_state.uploaded_chart_image, str):
                    # It's a filename, show the saved image
                    from pathlib import Path
                    from config import IMAGES_DIR
                    image_path = IMAGES_DIR / st.session_state.uploaded_chart_image
                    if image_path.exists():
                        st.image(str(image_path), caption="Previously Uploaded Chart Image", width='stretch')
                        st.info(f"📊 Using previously uploaded: {st.session_state.uploaded_chart_image}")
                else:
                    # It's a file object, show it
                    st.image(st.session_state.uploaded_chart_image, caption="Previously Uploaded Chart Image", width='stretch')
                    st.info("📊 Using previously uploaded image")
            elif form_data and form_data.chart_image_filename:
                # Restore from form data if no session state
                from pathlib import Path
                image_path = Path("images") / form_data.chart_image_filename
                if image_path.exists():
                    st.session_state.uploaded_chart_image = form_data.chart_image_filename
                    st.image(str(image_path), caption="Previously Uploaded Chart Image", width='stretch')
                    st.info(f"📊 Using previously uploaded: {form_data.chart_image_filename}")
        
        # Return current uploads or preserve existing filenames from session state
        return {
            'company_logo': company_logo,
            'chart_image': chart_image,
            'company_logo_filename': st.session_state.get('uploaded_company_logo') if not company_logo else None,
            'chart_image_filename': st.session_state.get('uploaded_chart_image') if not chart_image else None
        }


# ContentForm removed - content generation moved to Review & Generate section


class TemplateForm:
    """Component for template selection"""
    
    @staticmethod
    def render() -> TemplateVersion:
        """Render template selection form"""
        st.markdown("""
        <div class="section-header">
            <h3>🎨 Template Selection</h3>
            <p>Choose your preferred report template layout and see a live preview</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Get default template from session state if available
            form_data = getattr(st.session_state, 'form_data', None)
            template_options = [TemplateVersion.V1, TemplateVersion.V2, TemplateVersion.V3]
            template_default = 2  # Default to v3
            if form_data and hasattr(form_data, 'template_version'):
                try:
                    template_default = template_options.index(form_data.template_version)
                except ValueError:
                    template_default = 2
            
            template_version = st.radio(
                "Select Template:",
                options=template_options,
                format_func=lambda x: f"Template {x.value.upper()}",
                index=template_default,
                key="form_template_version"
            )
        
        with col2:
            st.markdown("### Template Preview")
            st.markdown(get_template_preview_html(template_version.value), unsafe_allow_html=True)
        
        return template_version
