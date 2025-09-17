#!/usr/bin/env python3
"""
Utility functions for the Investment Recommendation Generator v2
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import streamlit as st
from PIL import Image
import io

from config import (
    DATA_DIR, PDFS_DIR, LOGS_DIR, TEMP_DIR, IMAGES_DIR, TEMPLATES_DIR,
    LOGO_PATH, MAX_IMAGE_SIZE, SUPPORTED_IMAGE_FORMATS, LATEX_SUPPORTED_FORMATS
)


def setup_directories():
    """Create all necessary directories"""
    for directory in [DATA_DIR, PDFS_DIR, LOGS_DIR, TEMP_DIR, IMAGES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Copy MPC logo to temp directory if it exists
    if LOGO_PATH.exists():
        temp_logo_path = TEMP_DIR / "mpc_logo.png"
        if not temp_logo_path.exists():
            shutil.copy2(LOGO_PATH, temp_logo_path)


def save_uploaded_image(uploaded_file, filename_prefix: str) -> Optional[str]:
    """
    Save uploaded image with format conversion for LaTeX compatibility
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        filename_prefix: Prefix for the filename
        
    Returns:
        Filename of saved image or None if failed
    """
    if not uploaded_file:
        return None
    
    try:
        # Check file size
        if uploaded_file.size > MAX_IMAGE_SIZE:
            st.error(f"Image too large. Maximum size: {MAX_IMAGE_SIZE // (1024*1024)}MB")
            return None
        
        # Read file content
        file_content = uploaded_file.read()
        
        # Get original extension
        original_name = uploaded_file.name
        if '.' in original_name:
            original_ext = original_name.split('.')[-1].lower()
        else:
            original_ext = 'png'
        
        # Convert unsupported formats to PNG
        if original_ext not in LATEX_SUPPORTED_FORMATS:
            try:
                # Open and convert image
                image = Image.open(io.BytesIO(file_content))
                
                # Handle transparency
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save as PNG
                output_buffer = io.BytesIO()
                image.save(output_buffer, format='PNG')
                file_content = output_buffer.getvalue()
                original_ext = 'png'
                
            except Exception as e:
                st.warning(f"Could not convert image format: {e}")
                return None
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.{original_ext}"
        file_path = IMAGES_DIR / filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return filename
        
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None


def validate_form_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate form data and return list of errors
    
    Args:
        data: Form data dictionary
        
    Returns:
        List of error messages
    """
    errors = []
    
    # Required fields
    if not data.get('company_name', '').strip():
        errors.append("Company name is required")
    
    if not data.get('ticker', '').strip():
        errors.append("Ticker is required")
    
    if not data.get('analysis_types'):
        errors.append("At least one analysis type must be selected")
    
    # Content validation
    if data.get('content_source') == 'human':
        if not data.get('human_executive_summary', '').strip():
            errors.append("Executive summary is required for human-written content")
        if not data.get('human_investment_rationale', '').strip():
            errors.append("Investment rationale is required for human-written content")
    elif data.get('content_source') == 'ai':
        if not data.get('ai_context', '').strip():
            errors.append("Investment rationale context is required for AI generation")
    
    # Price validation
    entry_price = data.get('entry_price', 0)
    target_price = data.get('target_price', 0)
    stop_loss = data.get('stop_loss', 0)
    
    if entry_price <= 0:
        errors.append("Entry price must be greater than 0")
    
    if target_price <= 0:
        errors.append("Target price must be greater than 0")
    
    if stop_loss <= 0:
        errors.append("Stop loss must be greater than 0")
    
    if target_price <= entry_price:
        errors.append("Target price should be higher than entry price")
    
    if stop_loss >= entry_price:
        errors.append("Stop loss should be lower than entry price")
    
    return errors


def calculate_risk_metrics(entry_price: float, target_price: float, stop_loss: float) -> Dict[str, Any]:
    """Calculate risk metrics from prices"""
    if entry_price <= 0:
        return {
            'potential_return': 0.0,
            'risk_amount': 0.0,
            'risk_reward_ratio': 0.0,
            'risk_level': 'Unknown'
        }
    
    potential_return = ((target_price - entry_price) / entry_price * 100)
    risk_amount = ((entry_price - stop_loss) / entry_price * 100)
    risk_reward_ratio = potential_return / risk_amount if risk_amount > 0 else 0
    
    # Determine risk level
    if risk_amount == 0:
        risk_level = "Low"
    elif risk_reward_ratio > 2:
        risk_level = "Low"
    elif risk_reward_ratio > 1:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return {
        'potential_return': potential_return,
        'risk_amount': risk_amount,
        'risk_reward_ratio': risk_reward_ratio,
        'risk_level': risk_level
    }


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters"""
    if not isinstance(text, str):
        return str(text)
    
    # Handle special characters
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('$', '\\$')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('_', '\\_')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('|', '\\textbar{}')
    text = text.replace('<', '\\textless{}')
    text = text.replace('>', '\\textgreater{}')
    
    return text


def compile_latex_to_pdf(tex_file: Path, output_filename: str) -> Path:
    """Compile LaTeX file to PDF"""
    try:
        # Change to temp directory
        original_dir = os.getcwd()
        os.chdir(TEMP_DIR)
        
        # Run pdflatex
        result = subprocess.run([
            'pdflatex', 
            '-interaction=nonstopmode', 
            '-output-directory', str(TEMP_DIR),
            str(tex_file)
        ], capture_output=True, text=True)
        
        # Change back to original directory
        os.chdir(original_dir)
        
        if result.returncode != 0:
            # Get log file content for error reporting
            log_file = TEMP_DIR / f"{output_filename}.log"
            error_details = ""
            if log_file.exists():
                with open(log_file, 'r') as f:
                    log_content = f.read()
                    lines = log_content.split('\n')
                    error_lines = [line for line in lines if '!' in line or 'Error' in line or 'Fatal' in line]
                    if error_lines:
                        error_details = "\nLast errors: " + "\n".join(error_lines[-5:])
            
            raise Exception(f"LaTeX compilation failed: {result.stderr}{error_details}")
        
        # Move PDF to PDFs directory
        temp_pdf_file = TEMP_DIR / f"{output_filename}.pdf"
        final_pdf_file = PDFS_DIR / f"{output_filename}.pdf"
        if temp_pdf_file.exists():
            shutil.move(str(temp_pdf_file), str(final_pdf_file))
        
        # Move log file to logs directory
        temp_log_file = TEMP_DIR / f"{output_filename}.log"
        final_log_file = LOGS_DIR / f"{output_filename}.log"
        if temp_log_file.exists():
            shutil.move(str(temp_log_file), str(final_log_file))
        
        # Clean up temporary files
        cleanup_temp_files(output_filename)
        
        return final_pdf_file
        
    except Exception as e:
        raise Exception(f"Error compiling LaTeX to PDF: {str(e)}")


def cleanup_temp_files(output_filename: str):
    """Clean up temporary files after compilation"""
    try:
        temp_files = [
            TEMP_DIR / f"{output_filename}.tex",
            TEMP_DIR / f"{output_filename}.aux",
            TEMP_DIR / f"{output_filename}.out",
            TEMP_DIR / f"{output_filename}.toc",
            TEMP_DIR / f"{output_filename}.fdb_latexmk",
            TEMP_DIR / f"{output_filename}.fls",
            TEMP_DIR / f"{output_filename}.synctex.gz"
        ]
        
        for temp_file in temp_files:
            if temp_file.exists():
                temp_file.unlink()
                
    except Exception as e:
        print(f"Warning: Could not clean up temporary files: {e}")
