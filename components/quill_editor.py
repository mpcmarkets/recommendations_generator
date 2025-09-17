#!/usr/bin/env python3
"""
QuillJS rich text editor component for Streamlit
Consolidated from multiple files into one clean implementation
"""

import streamlit as st
from streamlit_quill import st_quill
from typing import Optional


def quill_rich_text_editor(
    label: str,
    value: str = "",
    key: str = None,
    height: int = 200,
    placeholder: str = "Start writing..."
) -> str:
    """
    Create a QuillJS rich text editor
    
    Args:
        label: Label for the editor
        value: Initial value (HTML content)
        key: Unique key for the widget
        height: Height of the editor in pixels
        placeholder: Placeholder text
        
    Returns:
        HTML content from the QuillJS editor
    """
    
    # Generate unique key if not provided
    if key is None:
        key = f"quill_editor_{label.replace(' ', '_').lower()}"
    
    # Create a container for the editor
    with st.container():
        st.markdown(f"**{label}**")
        
        # Add CSS for QuillJS editor height
        st.markdown(f"""
        <style>
        .ql-editor {{
            min-height: {height}px !important;
            max-height: {height * 2}px !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Configure QuillJS toolbar
        toolbar_options = [
            [{"header": [1, 2, 3, False]}],
            ["bold", "italic", "underline", "strike"],
            [{"list": "ordered"}, {"list": "bullet"}],
            [{"indent": "-1"}, {"indent": "+1"}],
            ["blockquote", "code-block"],
            ["link"],
            ["clean"]
        ]
        
        # Create the QuillJS editor
        try:
            content = st_quill(
                value=value,
                html=True,
                toolbar=toolbar_options,
                placeholder=placeholder,
                key=key
            )
            
            # Return the HTML content
            return content if content is not None else value
            
        except Exception as e:
            st.error(f"Error with QuillJS editor: {e}")
            # Fallback to text area
            st.warning("Falling back to text area due to QuillJS error")
            return st.text_area(
                label=f"{label} (Fallback)",
                value=value,
                height=height,
                key=f"{key}_fallback"
            )


def quill_editor(
    label: str,
    value: str = "",
    key: str = None,
    height: int = 200,
    placeholder: str = "Start writing..."
) -> str:
    """
    Alias for quill_rich_text_editor for backward compatibility
    """
    return quill_rich_text_editor(label, value, key, height, placeholder)