#!/usr/bin/env python3
"""
Robust content converter using Python libraries for markdown → HTML → LaTeX pipeline
"""

import re
import html
from typing import Optional
import markdown
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import html2text


class ContentConverter:
    """Convert content between different formats using robust libraries"""
    
    @staticmethod
    def markdown_to_html(markdown_content: str) -> str:
        """Convert markdown content to clean HTML for QuillJS using the markdown library"""
        if not markdown_content:
            return ""
        
        # Use the markdown library for robust conversion
        html_content = markdown.markdown(
            markdown_content,
            extensions=[
                'markdown.extensions.extra',     # Tables, footnotes, etc.
                'markdown.extensions.nl2br',     # Convert newlines to <br>
                'markdown.extensions.sane_lists' # Better list handling
            ]
        )
        
        # Clean up the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Ensure proper paragraph structure for QuillJS
        # QuillJS expects block elements to be properly formatted
        cleaned_html = str(soup)
        
        # Remove any empty paragraphs
        cleaned_html = re.sub(r'<p>\s*</p>', '', cleaned_html)
        
        return cleaned_html.strip()
    
    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """Convert HTML content back to markdown using html2text"""
        if not html_content:
            return ""
        
        # Configure html2text for clean markdown output
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # Don't wrap lines
        h.unicode_snob = True  # Use unicode characters
        h.escape_snob = False  # Don't escape markdown characters
        
        markdown_content = h.handle(html_content)
        
        # Clean up the output
        markdown_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_content)
        
        return markdown_content.strip()
    
    @staticmethod
    def html_to_latex(html_content: str) -> str:
        """Convert HTML content to LaTeX using BeautifulSoup for robust parsing"""
        if not html_content:
            return ""
        
        # Parse HTML with BeautifulSoup for robust handling
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Convert to LaTeX formatting without aggressive escaping first
        latex_content = ContentConverter._convert_soup_to_latex(soup)
        
        # Apply minimal LaTeX escaping (only on text content, not commands)
        latex_content = ContentConverter._escape_latex_minimal(latex_content)
        
        return latex_content.strip()
    
    @staticmethod
    def _convert_soup_to_latex(soup) -> str:
        """Convert BeautifulSoup element to LaTeX recursively"""
        if isinstance(soup, str):
            return soup
        
        latex_parts = []
        
        for element in soup.children:
            if isinstance(element, str):
                # Text node - add directly
                latex_parts.append(element)
            else:
                # HTML element - convert based on tag
                tag_name = element.name.lower() if element.name else ""
                
                if tag_name == 'p':
                    # Paragraph
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"{inner_latex}\n\n")
                
                elif tag_name in ['strong', 'b']:
                    # Bold text
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"\\textbf{{{inner_latex}}}")
                
                elif tag_name in ['em', 'i']:
                    # Italic text
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"\\textit{{{inner_latex}}}")
                
                elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    # Headers - use starred versions to prevent numbering
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    # Clean up the header text - remove markdown artifacts
                    clean_header = inner_latex.strip().replace('**', '').replace('*', '')
                    if tag_name == 'h1':
                        latex_parts.append(f"\\section*{{{clean_header}}}\n\n")
                    elif tag_name == 'h2':
                        latex_parts.append(f"\\subsection*{{{clean_header}}}\n\n")
                    elif tag_name == 'h3':
                        latex_parts.append(f"\\subsubsection*{{{clean_header}}}\n\n")
                    else:
                        latex_parts.append(f"\\paragraph*{{{clean_header}}}\n\n")
                
                elif tag_name == 'blockquote':
                    # Blockquote
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"\\begin{{quote}}\n{inner_latex}\n\\end{{quote}}\n\n")
                
                elif tag_name == 'ul':
                    # Unordered list
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"\\begin{{itemize}}\n{inner_latex}\\end{{itemize}}\n\n")
                
                elif tag_name == 'ol':
                    # Ordered list
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"\\begin{{enumerate}}\n{inner_latex}\\end{{enumerate}}\n\n")
                
                elif tag_name == 'li':
                    # List item
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(f"\\item {inner_latex}\n")
                
                elif tag_name == 'br':
                    # Line break
                    latex_parts.append("\n\n")
                
                elif tag_name in ['div', 'span']:
                    # Generic containers - just process contents
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(inner_latex)
                
                else:
                    # Unknown tag - just process contents
                    inner_latex = ContentConverter._convert_soup_to_latex(element)
                    latex_parts.append(inner_latex)
        
        return ''.join(latex_parts)
    
    @staticmethod
    def _escape_latex_minimal(text: str) -> str:
        """Minimal LaTeX escaping - ONLY escape text content, NEVER LaTeX commands"""
        if not text:
            return text
        
        # First, fix common AI-generated content issues
        text = ContentConverter._fix_ai_formatting_issues(text)
        
        # Handle problematic Unicode characters
        unicode_replacements = {
            '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
            '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9',
            '\u2013': '-', '\u2014': '--', '\u2018': "'", '\u2019': "'",
            '\u201C': '"', '\u201D': '"', '\u2026': '...', '\u00A0': ' ',
            '\u2032': "'", '\u2033': '"', '\u2019': "'", '\u201D': '"'  # Smart quotes
        }
        
        for unicode_char, replacement in unicode_replacements.items():
            text = text.replace(unicode_char, replacement)
        
        # IMPORTANT: Don't process any markdown conversion here
        # The HTML to LaTeX conversion should have already created proper LaTeX commands
        
        # Only escape characters that could break LaTeX compilation
        # Be VERY conservative - only escape the most dangerous characters
        
        # Temporarily protect LaTeX commands by replacing them with placeholders
        latex_commands = []
        
        def protect_command(match):
            latex_commands.append(match.group(0))
            return f"__LATEXCMD_{len(latex_commands)-1}__"
        
        # Protect ALL LaTeX constructs
        protected_text = re.sub(r'\\[a-zA-Z]+(?:\*)?(?:\[[^\]]*\])?(?:\{[^}]*\})*', protect_command, text)
        protected_text = re.sub(r'\\begin\{[^}]*\}.*?\\end\{[^}]*\}', protect_command, protected_text, flags=re.DOTALL)
        
        # Now ONLY escape problematic characters in the remaining text
        # Only escape characters that absolutely need it
        replacements = {
            '&': '\\&',
            '%': '\\%', 
            '$': '\\$',
            '#': '\\#'
        }
        
        for char, replacement in replacements.items():
            protected_text = protected_text.replace(char, replacement)
        
        # Restore LaTeX commands exactly as they were
        for i, command in enumerate(latex_commands):
            protected_text = protected_text.replace(f"__LATEXCMD_{i}__", command)
        
        # Clean up excessive whitespace only
        result = re.sub(r'\n\s*\n\s*\n+', '\n\n', protected_text)
        
        return result
    
    @staticmethod
    def _escape_latex_comprehensive(text: str) -> str:
        """Comprehensive LaTeX escaping with Unicode handling"""
        if not text:
            return text
        
        # First, handle problematic Unicode characters
        unicode_replacements = {
            # Subscript characters
            '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
            '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9',
            '\u208A': '+', '\u208B': '-', '\u208C': '=', '\u208D': '(', '\u208E': ')',
            # Superscript characters
            '\u2070': '0', '\u00B9': '1', '\u00B2': '2', '\u00B3': '3', '\u2074': '4',
            '\u2075': '5', '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
            # Smart quotes and dashes
            '\u2013': '-',    # en dash
            '\u2014': '--',   # em dash
            '\u2018': "'",    # left single quote
            '\u2019': "'",    # right single quote
            '\u201C': '"',    # left double quote
            '\u201D': '"',    # right double quote
            '\u2026': '...',  # ellipsis
            # Other problematic characters
            '\u00A0': ' ',    # non-breaking space
            '\u2022': '-',    # bullet point
        }
        
        for unicode_char, replacement in unicode_replacements.items():
            text = text.replace(unicode_char, replacement)
        
        # Protect existing LaTeX commands
        latex_commands = []
        
        # Pattern to match LaTeX commands - more comprehensive
        command_pattern = r'\\(?:textbf|textit|emph|begin|end|section|subsection|subsubsection|paragraph|item|quote|itemize|enumerate)\s*\{[^}]*\}|\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*'
        
        def protect_command(match):
            latex_commands.append(match.group(0))
            return f"__LATEX_PROTECTED_{len(latex_commands)-1}__"
        
        protected_text = re.sub(command_pattern, protect_command, text)
        
        # Now escape special LaTeX characters
        escape_map = {
            '\\': '\\textbackslash{}',  # Must be first
            '{': '\\{',
            '}': '\\}',
            '$': '\\$',
            '&': '\\&',
            '%': '\\%',
            '#': '\\#',
            '^': '\\textasciicircum{}',
            '_': '\\_',
            '~': '\\textasciitilde{}',
        }
        
        for char, replacement in escape_map.items():
            protected_text = protected_text.replace(char, replacement)
        
        # Restore protected LaTeX commands
        for i, command in enumerate(latex_commands):
            protected_text = protected_text.replace(f"__LATEX_PROTECTED_{i}__", command)
        
        # Clean up excessive whitespace
        protected_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', protected_text)
        protected_text = re.sub(r' +', ' ', protected_text)
        
        return protected_text
    
    @staticmethod
    def markdown_to_latex(markdown_content: str) -> str:
        """Convert markdown directly to LaTeX (bypassing HTML)"""
        if not markdown_content:
            return ""
        
        # Convert to HTML first, then to LaTeX for consistency
        html_content = ContentConverter.markdown_to_html(markdown_content)
        return ContentConverter.html_to_latex(html_content)
    
    @staticmethod
    def clean_ai_content(content: str) -> str:
        """Clean AI-generated content for better processing"""
        if not content:
            return ""
        
        # Remove common AI artifacts
        content = re.sub(r'^(Here\'s|Here is|Based on)', '', content, flags=re.IGNORECASE | re.MULTILINE)
        content = re.sub(r'\*\*Note:\*\*.*$', '', content, flags=re.MULTILINE)
        
        # Fix incomplete sections that might cause LaTeX issues
        # Remove incomplete headers at the end
        lines = content.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check for incomplete markdown headers at the end
            if line.startswith('#') and i == len(lines) - 1:
                # This is a header at the very end - might be incomplete
                # Only keep it if it has substantial content after the #
                header_content = line.lstrip('#').strip()
                if len(header_content) < 3:  # Very short headers are likely incomplete
                    print(f"Warning: Removing incomplete header: {line}")
                    continue
            
            # Check for markdown patterns that suggest incomplete content
            if line.startswith('**') and not line.endswith('**') and i >= len(lines) - 2:
                # Incomplete bold formatting near the end
                print(f"Warning: Removing incomplete formatting: {line}")
                continue
            
            if line:
                cleaned_lines.append(line)
            elif cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
        
        # Remove trailing empty lines
        while cleaned_lines and cleaned_lines[-1] == '':
            cleaned_lines.pop()
        
        # Normalize whitespace
        content = '\n'.join(cleaned_lines)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = re.sub(r'[ \t]+', ' ', content)
        
        return content.strip()
    
    @staticmethod
    def _fix_ai_formatting_issues(text: str) -> str:
        """Fix common AI-generated content formatting issues"""
        if not text:
            return text
        
        # Fix missing spaces after punctuation
        text = re.sub(r'([.!?,:;])([A-Z])', r'\1 \2', text)
        
        # Fix missing spaces around common words (but be careful not to break normal words)
        # Only fix specific problematic patterns
        
        # Fix specific common AI artifacts
        text = text.replace('basedon', 'based on')
        text = text.replace('based onacomprehensive', 'based on a comprehensive')
        text = text.replace('onacomprehensive', 'on a comprehensive')
        text = text.replace('acomprehensive', 'a comprehensive')
        text = text.replace('comprehensiveanalysis', 'comprehensive analysis')
        text = text.replace('analysisof', 'analysis of')
        text = text.replace('companyÂ´s', "company's")
        text = text.replace('company′s', "company's")
        text = text.replace('companys', "company's")
        text = text.replace('robustf inancial', 'robust financial')
        text = text.replace('f inancial', 'financial')
        text = text.replace('financialhealth', 'financial health')
        text = text.replace('financialperformance', 'financial performance')
        text = text.replace('bullishthesis', 'bullish thesis')
        text = text.replace('thesisis', 'thesis is')
        text = text.replace('dominantpositioning', 'dominant positioning')
        text = text.replace('predicatedon', 'predicated on')
        text = text.replace('thecompany', 'the company')
        text = text.replace('sdominant', "'s dominant")
        text = text.replace('andnet', 'and net')
        text = text.replace('netincome', 'net income')
        text = text.replace('billionand', 'billion and')
        text = text.replace('andnet', 'and net')
        text = text.replace('Ourbullish', 'Our bullish')
        text = text.replace('ourbulli', 'our bullish')
        text = text.replace('thesisis', 'thesis is')
        text = text.replace('ispredicatedon', 'is predicated on')
        text = text.replace('onthe', 'on the')
        text = text.replace('Geopoliticallandscape', 'Geopolitical landscape')
        text = text.replace('landscape.Our', 'landscape. Our')
        text = text.replace('landscape.Ou', 'landscape. Our')
        text = text.replace('ispredicated', 'is predicated')
        text = text.replace('itsFundamentals', 'its Fundamentals')
        text = text.replace('million.robust', 'million. Robust')
        text = text.replace('pr0', 'price')
        text = text.replace('0.1', '')  # Remove section numbering artifacts
        text = text.replace('0.2', '')
        text = text.replace('0.3', '')
        text = text.replace('0.4', '')
        text = text.replace('0.5', '')
        
        # Fix currency formatting
        text = re.sub(r'(\d+)\.0([^0-9])', r'$\1\2', text)  # 200.0 -> $200
        text = re.sub(r'(\d+)billion', r'\1 billion', text)
        text = re.sub(r'(\d+)million', r'\1 million', text)
        
        # Fix percentage formatting
        text = re.sub(r'(\d+)%', r'\1\\%', text)
        
        # Fix apostrophes and contractions
        text = re.sub(r'([a-z])′([a-z])', r"\1'\2", text)
        text = re.sub(r'([a-z])Â´([a-z])', r"\1'\2", text)
        
        # Remove the overly aggressive pattern that breaks normal words
        
        # Clean up excessive whitespace but preserve intentional spacing
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
        
        # Fix hyphenated words that got broken
        text = text.replace('high−growthmarkets', 'high-growth markets')
        text = text.replace('high−growth', 'high-growth')
        text = text.replace('long−term', 'long-term')
        text = text.replace('multi−dimensional', 'multi-dimensional')
        
        return text.strip()