#!/usr/bin/env python3
"""
OpenRouter model configuration and management
"""

from typing import Dict, List, Optional, Any
import streamlit as st
from dataclasses import dataclass


@dataclass
class OpenRouterModel:
    """Represents an OpenRouter model configuration"""
    id: str
    name: str
    description: Optional[str] = None
    context_length: Optional[int] = None
    pricing: Optional[Dict[str, Any]] = None
    model_name: str = None  # The actual model name for API calls
    
    def __post_init__(self):
        if self.model_name is None:
            self.model_name = self.id
    
    @property
    def is_free(self) -> bool:
        """Check if the model is free based on pricing"""
        if not self.pricing:
            return False
        return self.pricing.get('prompt', '0') == '0' and self.pricing.get('completion', '0') == '0'
    
    @property
    def display_name(self) -> str:
        """Get display name for the model"""
        return self.name or self.id
    
    @property
    def context_display(self) -> str:
        """Get context length display"""
        if not self.context_length:
            return "Unknown"
        if self.context_length >= 1000000:
            return f"{self.context_length // 1000000}M"
        elif self.context_length >= 1000:
            return f"{self.context_length // 1000}K"
        else:
            return str(self.context_length)


class OpenRouterModelManager:
    """Manager for OpenRouter model selection and configuration"""
    
    _models_cache: Dict[str, OpenRouterModel] = {}
    _free_models_cache: Dict[str, OpenRouterModel] = {}
    
    @staticmethod
    def _fetch_models_from_api() -> Dict[str, OpenRouterModel]:
        """Fetch all models from OpenRouter API using ai_tools library"""
        try:
            from ai_tools import LLMFactory
            
            # Get OpenRouter provider from ai_tools
            llm_factory = LLMFactory()
            openrouter_provider = llm_factory.get_provider('openrouter')
            
            if not openrouter_provider:
                print("OpenRouter provider not available")
                return OpenRouterModelManager._get_fallback_models()
            
            # Use the existing get_model_details method from ai_tools
            models_data = openrouter_provider.get_model_details()
            
            if not models_data:
                print("No models data received from OpenRouter")
                return OpenRouterModelManager._get_fallback_models()
            
            models = {}
            for model_data in models_data:
                model_id = model_data.get('id', '')
                if not model_id:
                    continue
                
                model = OpenRouterModel(
                    id=model_id,
                    name=model_data.get('name', model_id),
                    description=model_data.get('description'),
                    context_length=model_data.get('context_length'),
                    pricing=model_data.get('pricing', {}),
                    model_name=model_id
                )
                models[model_id] = model
            
            print(f"Successfully fetched {len(models)} models from OpenRouter API")
            return models
                
        except Exception as e:
            print(f"Error fetching models from OpenRouter API: {e}")
            return OpenRouterModelManager._get_fallback_models()
    
    @staticmethod
    def _get_fallback_models() -> Dict[str, OpenRouterModel]:
        """Get fallback models when API is unavailable"""
        return {
            "deepseek/deepseek-chat-v3.1:free": OpenRouterModel(
                id="deepseek/deepseek-chat-v3.1:free",
                name="DeepSeek Chat v3.1",
                description="Advanced reasoning model",
                context_length=64000,
                pricing={"prompt": "0", "completion": "0"}
            )
        }
    
    @staticmethod
    def get_all_models() -> Dict[str, OpenRouterModel]:
        """Get all models from OpenRouter API (cached)"""
        if not OpenRouterModelManager._models_cache:
            OpenRouterModelManager._models_cache = OpenRouterModelManager._fetch_models_from_api()
        return OpenRouterModelManager._models_cache.copy()
    
    @staticmethod
    def get_free_models() -> Dict[str, OpenRouterModel]:
        """Get all free OpenRouter models (cached)"""
        if not OpenRouterModelManager._free_models_cache:
            all_models = OpenRouterModelManager.get_all_models()
            free_models = {}
            for model_id, model in all_models.items():
                if model.is_free:
                    free_models[model_id] = model
            OpenRouterModelManager._free_models_cache = free_models
        return OpenRouterModelManager._free_models_cache.copy()
    
    @staticmethod
    def get_model_by_id(model_id: str) -> Optional[OpenRouterModel]:
        """Get a specific model by ID"""
        all_models = OpenRouterModelManager.get_all_models()
        return all_models.get(model_id)
    
    @staticmethod
    def get_default_model() -> OpenRouterModel:
        """Get the default recommended model (DeepSeek Chat v3.1)"""
        default_id = "deepseek/deepseek-chat-v3.1:free"
        model = OpenRouterModelManager.get_model_by_id(default_id)
        if model:
            return model
        
        # Fallback if default model not found
        free_models = OpenRouterModelManager.get_free_models()
        if free_models:
            return list(free_models.values())[0]
        
        # Last resort fallback
        return OpenRouterModel(
            id=default_id,
            name="DeepSeek Chat v3.1",
            description="Advanced reasoning model",
            context_length=64000,
            pricing={"prompt": "0", "completion": "0"}
        )
    
    @staticmethod
    def initialize_session_state():
        """Initialize session state for model selection"""
        if 'selected_openrouter_model' not in st.session_state:
            default_model = OpenRouterModelManager.get_default_model()
            st.session_state.selected_openrouter_model = default_model.id
    
    @staticmethod
    def get_selected_model() -> OpenRouterModel:
        """Get the currently selected model from session state"""
        OpenRouterModelManager.initialize_session_state()
        model_id = st.session_state.get('selected_openrouter_model', 'deepseek/deepseek-chat-v3.1:free')
        model = OpenRouterModelManager.get_model_by_id(model_id)
        return model or OpenRouterModelManager.get_default_model()
    
    @staticmethod
    def set_selected_model(model_id: str):
        """Set the selected model in session state"""
        all_models = OpenRouterModelManager.get_all_models()
        if model_id in all_models:
            st.session_state.selected_openrouter_model = model_id
    
    @staticmethod
    def refresh_models():
        """Refresh models from API (clear cache)"""
        OpenRouterModelManager._models_cache.clear()
        OpenRouterModelManager._free_models_cache.clear()
