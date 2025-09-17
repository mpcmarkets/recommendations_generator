#!/usr/bin/env python3
"""
Image service for handling image uploads and processing
"""

import io
from typing import Optional
import streamlit as st
from PIL import Image

from config import IMAGES_DIR, MAX_IMAGE_SIZE, SUPPORTED_IMAGE_FORMATS, LATEX_SUPPORTED_FORMATS


class ImageService:
    """Service for image processing and management"""
    
    def __init__(self):
        self.images_dir = IMAGES_DIR
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def save_uploaded_image(self, uploaded_file, filename_prefix: str) -> Optional[str]:
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
                file_content, original_ext = self._convert_image_format(file_content, original_ext)
                if file_content is None:
                    return None
            
            # Create filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.{original_ext}"
            file_path = self.images_dir / filename
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            return filename
            
        except Exception as e:
            st.error(f"Error saving image: {e}")
            return None
    
    def _convert_image_format(self, file_content: bytes, original_ext: str) -> tuple[Optional[bytes], str]:
        """
        Convert image to LaTeX-compatible format
        
        Args:
            file_content: Original image content
            original_ext: Original file extension
            
        Returns:
            Tuple of (converted_content, new_extension) or (None, original_ext) if failed
        """
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
            return output_buffer.getvalue(), 'png'
            
        except Exception as e:
            st.warning(f"Could not convert image format: {e}")
            return None, original_ext
    
    def get_image_path(self, filename: str) -> Optional[str]:
        """
        Get full path to image file
        
        Args:
            filename: Image filename
            
        Returns:
            Full path to image or None if not found
        """
        file_path = self.images_dir / filename
        if file_path.exists():
            return str(file_path)
        return None
    
    def validate_image_file(self, uploaded_file) -> tuple[bool, str]:
        """
        Validate uploaded image file
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not uploaded_file:
            return True, ""  # No file is valid (optional)
        
        # Check file size
        if uploaded_file.size > MAX_IMAGE_SIZE:
            return False, f"Image too large. Maximum size: {MAX_IMAGE_SIZE // (1024*1024)}MB"
        
        # Check file extension
        if '.' in uploaded_file.name:
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext not in SUPPORTED_IMAGE_FORMATS:
                return False, f"Unsupported image format: {ext}. Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
        
        # Try to open with PIL to validate it's a valid image
        try:
            uploaded_file.seek(0)  # Reset file pointer
            Image.open(io.BytesIO(uploaded_file.read()))
            uploaded_file.seek(0)  # Reset again for later use
            return True, ""
        except Exception as e:
            return False, f"Invalid image file: {e}"
    
    def cleanup_old_images(self, days_old: int = 7):
        """
        Clean up old uploaded images
        
        Args:
            days_old: Remove images older than this many days
        """
        try:
            from datetime import datetime, timedelta
            cutoff_time = datetime.now() - timedelta(days=days_old)
            
            for file_path in self.images_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time.timestamp():
                    file_path.unlink()
                    
        except Exception as e:
            st.warning(f"Could not clean up old images: {e}")
