#!/usr/bin/env python3
"""
Review components for content review and report generation
"""

import streamlit as st
from typing import Dict, Any
from models.form_data import FormData


class ContentReview:
    """Component for content generation and review"""
    
    @staticmethod
    def render(form_data: FormData) -> Dict[str, str]:
        """Render content generation and review form"""
        st.markdown("""
        <div class="section-header">
            <h3>📝 Content Generation & Review</h3>
            <p>Generate or write your content, then review before creating the final report</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Content source selection using tab-like buttons
        from models.form_data import ContentSource
        
        # Get current content source from form_data or default to HUMAN
        current_source = getattr(form_data, 'content_source', ContentSource.HUMAN)
        
        # Use session state to track which tab is active
        if 'active_content_tab' not in st.session_state:
            st.session_state.active_content_tab = 0 if current_source == ContentSource.HUMAN else 1
        
        # Create a custom tab-like interface with buttons next to each other
        col1, col2 = st.columns([1, 1])  # Equal width columns for compact layout
        
        with col1:
            human_active = st.session_state.active_content_tab == 0
            if st.button("✍️ Human Written", key="human_tab", type="primary" if human_active else "secondary", use_container_width=True):
                st.session_state.active_content_tab = 0
                st.rerun()
        
        with col2:
            ai_active = st.session_state.active_content_tab == 1
            if st.button("🤖 AI Generated", key="ai_tab", type="primary" if ai_active else "secondary", use_container_width=True):
                st.session_state.active_content_tab = 1
                st.rerun()
        
        # Render content based on active tab
        if st.session_state.active_content_tab == 0:
            form_data.content_source = ContentSource.HUMAN
            return ContentReview._render_human_content_generation(form_data)
        else:
            form_data.content_source = ContentSource.AI
            return ContentReview._render_ai_content_generation(form_data)
    
    @staticmethod
    def _render_ai_content_generation(form_data: FormData) -> Dict[str, str]:
        """Render AI content generation section"""
        st.markdown("""
        <div class="ai-box">
            <h3 style='color: #2980b9; margin: 0 0 8px 0;'>🤖 AI Content Generation</h3>
            <p style='color: #34495e; margin: 0;'>Choose your AI model and provide key points for content generation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Model selector
        from components.model_selector import ModelSelector
        selected_model = ModelSelector.render()
        
        st.markdown("")  # Add spacing
        
        # AI input fields
        st.markdown("**Provide Context for AI Generation:**")
        col1, col2 = st.columns(2)
        
        with col1:
            ai_rationale = st.text_area(
                "Investment Rationale Points:",
                value=getattr(form_data, 'ai_rationale', ''),
                placeholder="Enter key investment rationale points for AI to expand...",
                height=150,
                key="review_ai_rationale"
            )
        
        with col2:
            ai_context = st.text_area(
                "Additional Context:",
                value=getattr(form_data, 'ai_context', ''),
                placeholder="Enter additional context for AI analysis...",
                height=150,
                key="review_ai_context"
            )
        
        # Update form_data with AI inputs
        form_data.ai_rationale = ai_rationale
        form_data.ai_context = ai_context
        
        # AI Generation button
        st.markdown("")  # Add some spacing
        
        if st.button("🤖 Generate AI Content", key="generate_ai_content", use_container_width=True):
            with st.spinner(f"Generating AI content using {selected_model.display_name if selected_model else 'selected model'}..."):
                from services.openrouter_ai_service import OpenRouterAIService
                ai_service = OpenRouterAIService.get_instance()
                try:
                    executive_summary, investment_rationale = ai_service.generate_content(form_data)
                    
                    # Store in form_data
                    form_data.ai_executive_summary = executive_summary
                    form_data.ai_investment_rationale = investment_rationale
                    
                    # Store in session state for persistence (this will update the editors)
                    st.session_state.ai_executive_summary = executive_summary
                    st.session_state.ai_investment_rationale = investment_rationale
                    
                    # Also update form_data in session state to ensure persistence
                    if 'form_data' in st.session_state:
                        st.session_state.form_data.ai_executive_summary = executive_summary
                        st.session_state.form_data.ai_investment_rationale = investment_rationale
                    
                    # Update editor refresh key to force QuillJS editors to reload with new content
                    import time
                    st.session_state.ai_content_refresh_key = int(time.time() * 1000)
                    
                    # Force refresh to show new content in editors
                    st.success(f"AI content generated successfully using {selected_model.display_name if selected_model else 'selected model'}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating AI content: {e}")
        
        # Display generated content for review
        # Check both form_data and session state for AI content
        has_ai_content = (
            (hasattr(form_data, 'ai_executive_summary') and form_data.ai_executive_summary) or
            ('ai_executive_summary' in st.session_state and st.session_state.ai_executive_summary)
        )
        
        if has_ai_content:
            st.markdown("""
            <div class="success-box">
                <h3 style='color: #27ae60; margin: 0 0 8px 0;'>📝 Generated Content Review</h3>
                <p style='color: #2e7d32; margin: 0;'>Review and edit the AI-generated content below</p>
            </div>
            """, unsafe_allow_html=True)
            
            from components.quill_editor import quill_editor
            
            # Get existing content with priority to session state (most recent)
            # Session state always has the latest generated content
            ai_exec_default = st.session_state.get('ai_executive_summary', '')
            ai_rationale_default = st.session_state.get('ai_investment_rationale', '')
            
            # Fallback to form_data if session state is empty (shouldn't happen after generation)
            if not ai_exec_default and hasattr(form_data, 'ai_executive_summary'):
                ai_exec_default = form_data.ai_executive_summary
            if not ai_rationale_default and hasattr(form_data, 'ai_investment_rationale'):
                ai_rationale_default = form_data.ai_investment_rationale
            
            # Get refresh key for editor reloading
            refresh_key = st.session_state.get('ai_content_refresh_key', 0)
            
            st.markdown("**Summary:**")
            executive_summary = quill_editor(
                label="",
                value=ai_exec_default,
                key=f"review_ai_exec_summary_{refresh_key}",
                height=200
            )
            
            st.markdown("")  # Add some spacing
            st.markdown("**Investment Rationale:**")
            investment_rationale = quill_editor(
                label="",
                value=ai_rationale_default,
                key=f"review_ai_inv_rationale_{refresh_key}",
                height=300
            )
            
            # Store content in session state for persistence
            st.session_state.ai_executive_summary = executive_summary
            st.session_state.ai_investment_rationale = investment_rationale
            
            # Update form_data with AI content (same as human section)
            form_data.ai_executive_summary = executive_summary
            form_data.ai_investment_rationale = investment_rationale
            
            # CRITICAL: Also update the form_data in session state to ensure persistence
            if 'form_data' in st.session_state:
                st.session_state.form_data.ai_executive_summary = executive_summary
                st.session_state.form_data.ai_investment_rationale = investment_rationale
            
            return {
                'executive_summary': executive_summary,
                'investment_rationale': investment_rationale
            }
        else:
            return {
                'executive_summary': '',
                'investment_rationale': ''
            }
    
    @staticmethod
    def _render_human_content_generation(form_data: FormData) -> Dict[str, str]:
        """Render human content generation section"""
        st.markdown("""
        <div class="success-box">
            <h3 style='color: #27ae60; margin: 0 0 8px 0;'>✍️ Human Content Writing</h3>
            <p style='color: #2e7d32; margin: 0;'>Write your professional investment analysis content directly</p>
        </div>
        """, unsafe_allow_html=True)
        
        from components.quill_editor import quill_editor
        
        # Get existing content if available, with fallback to session state
        human_exec_default = getattr(form_data, 'human_executive_summary', '')
        human_rationale_default = getattr(form_data, 'human_investment_rationale', '')
        
        # Check if content exists in session state (for persistence across navigation)
        if 'human_executive_summary' in st.session_state and not human_exec_default:
            human_exec_default = st.session_state.human_executive_summary
        if 'human_investment_rationale' in st.session_state and not human_rationale_default:
            human_rationale_default = st.session_state.human_investment_rationale
        
        st.markdown("**Write Your Content:**")
        st.markdown("")  # Add some spacing
        st.markdown("**Summary:**")
        executive_summary = quill_editor(
            label="",
            value=human_exec_default,
            key="review_human_exec_summary",
            height=200
        )
        
        st.markdown("")  # Add some spacing
        st.markdown("**Investment Rationale:**")
        investment_rationale = quill_editor(
            label="",
            value=human_rationale_default,
            key="review_human_inv_rationale",
            height=300
        )
        
        # Store content in session state for persistence
        st.session_state.human_executive_summary = executive_summary
        st.session_state.human_investment_rationale = investment_rationale
        
        # Update form_data with human content
        form_data.human_executive_summary = executive_summary
        form_data.human_investment_rationale = investment_rationale
        
        # CRITICAL: Also update the form_data in session state to ensure persistence
        if 'form_data' in st.session_state:
            st.session_state.form_data.human_executive_summary = executive_summary
            st.session_state.form_data.human_investment_rationale = investment_rationale
        
        return {
            'executive_summary': executive_summary,
            'investment_rationale': investment_rationale
        }


class ReportGeneration:
    """Component for report generation and display"""
    
    @staticmethod
    def render(form_data: FormData, pdf_file_path: str, report_data: Dict[str, Any]):
        """Render report generation results"""
        st.success("Final report generated successfully!")
        
        
        # Download button
        with open(pdf_file_path, "rb") as pdf_file_obj:
            pdf_bytes = pdf_file_obj.read()
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name=pdf_file_path.split('/')[-1],
                mime="application/pdf"
            )
        
        st.info(f"📁 File saved to: {pdf_file_path}")
    
    @staticmethod
    def render_generation_button():
        """Render the report generation button"""
        st.markdown("---")
        st.markdown("""
        <div class="success-box">
            <h3 style='color: #27ae60; margin: 0 0 8px 0;'>Ready to Generate Report</h3>
        </div>
        """, unsafe_allow_html=True)
        
        return st.button("📄 Generate Final Report", width='stretch')
