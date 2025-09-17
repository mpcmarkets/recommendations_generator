#!/usr/bin/env python3
"""
CSS constants and styling for the Investment Recommendation Generator
Centralized CSS for maintainability and consistency
"""

from config import CSS_FONT_FAMILIES, COLORS

# Main CSS styles
MAIN_CSS = f"""
<style>
    /* Import Google Fonts */
    @import url('{CSS_FONT_FAMILIES['inter']}');
    @import url('{CSS_FONT_FAMILIES['poppins']}');
    
    /* Global Styles */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Main Header */
    .main-header {{
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(30, 58, 138, 0.3);
    }}
    
    .main-header h1 {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    .main-header p {{
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }}
    
    /* Section Headers */
    .section-header {{
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 2rem 0 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }}
    
    .section-header h3 {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
        font-size: 1.3rem;
    }}
    
    .section-header p {{
        color: #6c757d;
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }}
    
    /* Form Elements */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }}
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    /* Success/Info Boxes */
    .success-box {{
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.2);
    }}
    
    .ai-box {{
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #2196f3;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.2);
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%) !important;
    }}
    
    section[data-testid="stSidebar"] .stButton > button {{
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        margin: 0.5rem 0 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.2s ease !important;
    }}
    
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Template Preview Styles */
    .template-preview {{
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid {COLORS['secondary']};
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        overflow: hidden;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
    }}
    
    .template-preview h3 {{
        margin: 0 0 3px 0;
        color: {COLORS['primary']};
        font-size: 16px;
        font-weight: bold;
        word-wrap: break-word;
    }}
    
    .template-preview p {{
        margin: 0;
        color: {COLORS['gray']};
        font-size: 12px;
        font-style: italic;
        word-wrap: break-word;
    }}
    
    .template-preview img {{
        max-width: 100%;
        width: auto;
        max-height: 250px;
        height: auto;
        border-radius: 6px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        object-fit: contain;
        display: block;
        margin: 0 auto;
    }}
    
    /* QuillJS Editor Styles */
    .ql-editor {{
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }}
    
    .ql-toolbar {{
        border-top: 1px solid #ccc;
        border-left: 1px solid #ccc;
        border-right: 1px solid #ccc;
        border-radius: 8px 8px 0 0;
    }}
    
    .ql-container {{
        border-bottom: 1px solid #ccc;
        border-left: 1px solid #ccc;
        border-right: 1px solid #ccc;
        border-radius: 0 0 8px 8px;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }}
        
        .template-preview {{
            padding: 8px;
        }}
        
        .template-preview img {{
            max-height: 200px;
        }}
    }}
</style>
"""

# Sidebar CSS
SIDEBAR_CSS = f"""
<style>
    .css-1d391kg {{
        background-color: {COLORS['dark']};
    }}
    
    .css-1d391kg .css-1v0mbdj {{
        color: {COLORS['white']};
    }}
    
    .sidebar .sidebar-content {{
        background-color: {COLORS['dark']};
    }}
    
    .sidebar .sidebar-content .stButton > button {{
        background-color: transparent;
        color: {COLORS['white']};
        border: 2px solid {COLORS['white']}20;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0;
        width: 100%;
        text-align: left;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .sidebar .sidebar-content .stButton > button:hover {{
        background-color: {COLORS['white']}10;
        border-color: {COLORS['white']}40;
        transform: translateX(4px);
    }}
    
    .sidebar .sidebar-content .stButton > button[kind="primary"] {{
        background-color: {COLORS['secondary']};
        border-color: {COLORS['secondary']};
    }}
</style>
"""
