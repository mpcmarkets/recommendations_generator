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
        
        # Configure enhanced QuillJS toolbar with more options
        toolbar_options = [
            # Header options (H1, H2, H3, Normal)
            [{"header": [1, 2, 3, 4, 5, 6, False]}],
            
            # Font family and size options
            [{"font": []}],
            [{"size": ["small", False, "large", "huge"]}],
            
            # Text formatting
            ["bold", "italic", "underline", "strike"],
            
            # Text color and background
            [{"color": []}, {"background": []}],
            
            # Script formatting (subscript/superscript)
            [{"script": "sub"}, {"script": "super"}],
            
            # Lists and indentation
            [{"list": "ordered"}, {"list": "bullet"}],
            [{"indent": "-1"}, {"indent": "+1"}],
            
            # Text direction and alignment
            [{"direction": "rtl"}],
            [{"align": []}],
            
            # Special formatting
            ["blockquote", "code-block"],
            
            # Links and media
            ["link", "image"],
            
            # Utility
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


def quill_editor_basic(
    label: str,
    value: str = "",
    key: str = None,
    height: int = 200,
    placeholder: str = "Start writing..."
) -> str:
    """
    Basic QuillJS editor with minimal formatting options
    
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
        key = f"quill_basic_{label.replace(' ', '_').lower()}"
    
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
        
        # Basic toolbar configuration
        toolbar_options = [
            [{"header": [1, 2, 3, False]}],
            ["bold", "italic", "underline"],
            [{"list": "ordered"}, {"list": "bullet"}],
            ["blockquote"],
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
            
            return content if content is not None else value
            
        except Exception as e:
            st.error(f"Error with QuillJS editor: {e}")
            st.warning("Falling back to text area due to QuillJS error")
            return st.text_area(
                label=f"{label} (Fallback)",
                value=value,
                height=height,
                key=f"{key}_fallback"
            )


def quill_editor_advanced(
    label: str,
    value: str = "",
    key: str = None,
    height: int = 300,
    placeholder: str = "Start writing..."
) -> str:
    """
    Advanced QuillJS editor with full formatting options including tables and formulas
    
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
        key = f"quill_advanced_{label.replace(' ', '_').lower()}"
    
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
        
        # Advanced toolbar configuration with all options
        toolbar_options = [
            # Header options
            [{"header": [1, 2, 3, 4, 5, 6, False]}],
            
            # Font options
            [{"font": []}],
            [{"size": ["small", False, "large", "huge"]}],
            
            # Text formatting
            ["bold", "italic", "underline", "strike"],
            
            # Colors
            [{"color": []}, {"background": []}],
            
            # Script formatting
            [{"script": "sub"}, {"script": "super"}],
            
            # Lists and indentation
            [{"list": "ordered"}, {"list": "bullet"}],
            [{"indent": "-1"}, {"indent": "+1"}],
            
            # Direction and alignment
            [{"direction": "rtl"}],
            [{"align": []}],
            
            # Special formatting
            ["blockquote", "code-block"],
            
            # Media and links
            ["link", "image", "video"],
            
            # Tables (if supported)
            ["table"],
            
            # Utility
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
            
            return content if content is not None else value
            
        except Exception as e:
            st.error(f"Error with QuillJS editor: {e}")
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
    placeholder: str = "Start writing...",
    toolbar_type: str = "standard"
) -> str:
    """
    QuillJS editor with configurable toolbar type
    
    Args:
        label: Label for the editor
        value: Initial value (HTML content)
        key: Unique key for the widget
        height: Height of the editor in pixels
        placeholder: Placeholder text
        toolbar_type: Type of toolbar ("basic", "standard", "advanced")
        
    Returns:
        HTML content from the QuillJS editor
    """
    
    if toolbar_type == "basic":
        return quill_editor_basic(label, value, key, height, placeholder)
    elif toolbar_type == "advanced":
        return quill_editor_advanced(label, value, key, height, placeholder)
    else:  # standard (default)
        return quill_rich_text_editor(label, value, key, height, placeholder)