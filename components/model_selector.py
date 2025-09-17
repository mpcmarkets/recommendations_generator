#!/usr/bin/env python3
"""
Model selector component for OpenRouter models
"""

import streamlit as st
from typing import Optional
from services.openrouter_models import OpenRouterModelManager, OpenRouterModel


class ModelSelector:
    """Component for selecting OpenRouter models"""
    
    @staticmethod
    def render() -> Optional[OpenRouterModel]:
        """Render model selector and return selected model"""
        st.markdown("""
        <div class="model-selector-box">
            <h4 style='color: #2980b9; margin: 0 0 8px 0;'>🤖 AI Model Selection</h4>
            <p style='color: #34495e; margin: 0;'>Choose your preferred AI model for content generation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize session state
        OpenRouterModelManager.initialize_session_state()
        
        # Get all free models
        models = OpenRouterModelManager.get_free_models()
        
        # Create model options for selectbox
        model_options = {}
        for model_id, model in models.items():
            # Create simple display name with just name and context
            display_name = f"{model.display_name} ({model.context_display} context)"
            model_options[display_name] = model_id
        
        # Get current selection
        current_model = OpenRouterModelManager.get_selected_model()
        current_display_name = f"{current_model.display_name} ({current_model.context_display} context)"
        
        # Find the current selection index
        display_names = list(model_options.keys())
        try:
            current_index = display_names.index(current_display_name)
        except ValueError:
            current_index = 0
        
        # Model selector with refresh button
        col1, col2 = st.columns([4, 1])
        
        with col1:
            selected_display_name = st.selectbox(
                "Select AI Model:",
                options=display_names,
                index=current_index,
                key="model_selector",
                help="Choose the AI model for content generation. All models shown are free."
            )
        
        with col2:
            if st.button("🔄", key="refresh_models", help="Refresh models from API"):
                OpenRouterModelManager.refresh_models()
                st.rerun()
        
        # Update session state if selection changed
        selected_model_id = model_options[selected_display_name]
        if selected_model_id != st.session_state.get('selected_openrouter_model'):
            OpenRouterModelManager.set_selected_model(selected_model_id)
        
        # Get the selected model
        selected_model = OpenRouterModelManager.get_model_by_id(selected_model_id)
        
        return selected_model
    
    @staticmethod
    def _display_model_details(model: OpenRouterModel):
        """Display detailed information about the selected model"""
        st.markdown("---")
        
        # Create columns for model details
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Context Length",
                value=model.context_display,
                help="Maximum input length the model can handle"
            )
        
        with col2:
            if model.is_free:
                st.metric(
                    label="Cost",
                    value="Free",
                    help="No cost for usage"
                )
            else:
                st.metric(
                    label="Cost",
                    value="Paid",
                    help="Requires payment for usage"
                )
        
        # Model description
        if model.description:
            st.markdown(f"**Description:** {model.description}")
        
        # Cost indicator
        if model.is_free:
            st.success("🆓 **Free Model** - No cost for usage")
        else:
            st.info("💰 **Paid Model** - Requires payment for usage")
    
    @staticmethod
    def render_compact() -> Optional[OpenRouterModel]:
        """Render a compact model selector for smaller spaces"""
        # Initialize session state
        OpenRouterModelManager.initialize_session_state()
        
        # Get all free models
        models = OpenRouterModelManager.get_free_models()
        
        # Create model options for selectbox
        model_options = {}
        for model_id, model in models.items():
            # Create compact display name
            display_name = f"{model.display_name} ({model.context_display})"
            model_options[display_name] = model_id
        
        # Get current selection
        current_model = OpenRouterModelManager.get_selected_model()
        current_display_name = f"{current_model.display_name} ({current_model.context_display})"
        
        # Find the current selection index
        display_names = list(model_options.keys())
        try:
            current_index = display_names.index(current_display_name)
        except ValueError:
            current_index = 0
        
        # Compact model selector
        selected_display_name = st.selectbox(
            "AI Model:",
            options=display_names,
            index=current_index,
            key="compact_model_selector",
            help="Choose the AI model for content generation"
        )
        
        # Update session state if selection changed
        selected_model_id = model_options[selected_display_name]
        if selected_model_id != st.session_state.get('selected_openrouter_model'):
            OpenRouterModelManager.set_selected_model(selected_model_id)
        
        # Get the selected model
        selected_model = OpenRouterModelManager.get_model_by_id(selected_model_id)
        
        return selected_model
