#!/usr/bin/env python3
"""
Navigation components for the application
"""

import streamlit as st
from config import APP_TITLE, APP_ICON


class AppHeader:
    """Application header component"""
    
    @staticmethod
    def render():
        """Render the main header"""
        st.markdown(f"""
        <div class="main-header">
            <h1>{APP_TITLE}</h1>
        </div>
        """, unsafe_allow_html=True)


class NavigationSidebar:
    """Navigation sidebar component"""
    
    @staticmethod
    def render():
        """Render the sidebar navigation"""
        with st.sidebar:
            st.markdown("""
            <div style='text-align: left; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;'>
                <h2 style='color: #ffffff; margin: 0; font-family: "Poppins", "Segoe UI", sans-serif; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.02em;'>
                    Create Report
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation buttons
            if st.button("📝 Form Input", width='stretch'):
                st.session_state.current_step = 'form'
                st.rerun()
            
            if st.button("📋 Generate Content", width='stretch'):
                st.session_state.current_step = 'review'
                st.rerun()
            
            # Reset button
            st.markdown("---")
            if st.button("🔄 Reset Form", width='stretch'):
                NavigationSidebar._reset_form()
    
    @staticmethod
    def _reset_form():
        """Reset the form data while preserving analysis checkboxes and images"""
        # Preserve important form data
        preserved_data = {}
        if 'form_data' in st.session_state:
            form_data = st.session_state.form_data
            # Preserve analysis types and image filenames
            preserved_data = {
                'analysis_types': getattr(form_data, 'analysis_types', []),
                'company_logo_filename': getattr(form_data, 'company_logo_filename', None),
                'chart_image_filename': getattr(form_data, 'chart_image_filename', None)
            }
        
        # Preserve uploaded image session state
        preserved_uploaded_images = {}
        if 'uploaded_company_logo' in st.session_state:
            preserved_uploaded_images['uploaded_company_logo'] = st.session_state.uploaded_company_logo
        if 'uploaded_chart_image' in st.session_state:
            preserved_uploaded_images['uploaded_chart_image'] = st.session_state.uploaded_chart_image
        
        # Clear all form data
        for key in list(st.session_state.keys()):
            if key.startswith(('form_', 'ai_', 'content_', 'template_', 'uploaded_')):
                del st.session_state[key]
        
        # Restore preserved data
        if preserved_data:
            from models.form_data import FormData
            st.session_state.form_data = FormData()
            st.session_state.form_data.analysis_types = preserved_data['analysis_types']
            st.session_state.form_data.company_logo_filename = preserved_data['company_logo_filename']
            st.session_state.form_data.chart_image_filename = preserved_data['chart_image_filename']
        
        # Restore uploaded image session state
        for key, value in preserved_uploaded_images.items():
            st.session_state[key] = value
        
        st.session_state.current_step = 'form'
        st.rerun()
