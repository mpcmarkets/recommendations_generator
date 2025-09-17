#!/usr/bin/env python3
"""
PDF service for report generation
"""

import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Tuple

from config import TEMPLATES_DIR, TEMP_DIR, IMAGES_DIR, PDFS_DIR, LOGS_DIR
from models.report_data import ReportData
from models.form_data import FormData


def check_latex_availability() -> bool:
    """Check if LaTeX is available on the system"""
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


class PDFService:
    """Service for PDF report generation"""
    
    def __init__(self):
        self.templates_dir = TEMPLATES_DIR
        self.temp_dir = TEMP_DIR
        self.images_dir = IMAGES_DIR
        self.pdfs_dir = PDFS_DIR
        self.logs_dir = LOGS_DIR
        
        # Ensure directories exist
        for directory in [self.temp_dir, self.images_dir, self.pdfs_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Setup temp environment (copy logo, etc.)
        self._setup_temp_environment()
    
    def _setup_temp_environment(self):
        """Setup temp environment by copying necessary files"""
        import shutil
        from config import LOGO_PATH
        
        # Copy MPC logo to temp directory if it exists
        if LOGO_PATH.exists():
            temp_logo_path = self.temp_dir / "mpc_logo.png"
            if not temp_logo_path.exists():
                shutil.copy2(LOGO_PATH, temp_logo_path)
    
    def generate_report(self, form_data: FormData) -> Tuple[Path, ReportData]:
        """
        Generate a PDF report from form data
        
        Args:
            form_data: Form data containing investment details
            
        Returns:
            Tuple of (pdf_file_path, report_data)
        """
        try:
            # Check LaTeX availability
            if not check_latex_availability():
                raise Exception(
                    "LaTeX is not available on this system. "
                    "Please ensure pdflatex is installed. "
                    "For Streamlit Cloud deployment, make sure packages.txt includes texlive packages."
                )
            # Create report data (without risk metrics)
            report_data = ReportData.from_form_data(form_data)
            
            # Generate filename
            filename = self._generate_filename(form_data)
            
            # Render LaTeX template
            template_version = form_data.template_version.value if hasattr(form_data.template_version, 'value') else str(form_data.template_version)
            tex_file = self._render_latex_template(report_data, filename, template_version)
            
            # Compile to PDF
            pdf_file = self._compile_latex_to_pdf(tex_file, filename)
            
            return pdf_file, report_data
            
        except Exception as e:
            raise Exception(f"Error generating report: {str(e)}")
    
    def _generate_filename(self, form_data: FormData) -> str:
        """Generate filename for the report"""
        ticker = form_data.ticker.upper()
        company_name = form_data.company_name
        
        if company_name and ticker:
            title_for_filename = f"{company_name} ({ticker})"
        elif company_name:
            title_for_filename = company_name
        elif ticker:
            title_for_filename = f"Investment_Recommendation ({ticker})"
        else:
            title_for_filename = 'Investment_Recommendation'
        
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Clean title for filename
        clean_title = re.sub(r'[^\w\s-]', '', title_for_filename)
        clean_title = re.sub(r'[-\s]+', '_', clean_title)
        clean_title = clean_title[:30]
        
        return f"recommendation_{ticker}_{clean_title}_{date_str}"
    
    def _render_latex_template(self, report_data: ReportData, filename: str, template_version: str) -> Path:
        """Render the LaTeX template with report data"""
        try:
            # Determine template path
            template_filename = f"recommendations_report_{template_version}.tex"
            template_path = self.templates_dir / template_filename
            
            if not template_path.exists():
                raise Exception(f"Template file not found: {template_path}")
            
            # Read template
            with open(template_path, 'r') as f:
                template_content = f.read()
            
            # Replace placeholders
            rendered_content = self._replace_template_placeholders(template_content, report_data)
            
            # Write rendered content
            temp_tex_file = self.temp_dir / f"{filename}.tex"
            with open(temp_tex_file, 'w') as f:
                f.write(rendered_content)
            
            return temp_tex_file
            
        except Exception as e:
            raise Exception(f"Error rendering LaTeX template: {str(e)}")
    
    def _replace_template_placeholders(self, template_content: str, report_data: ReportData) -> str:
        """Replace placeholders in template with actual data"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        # Import utils.py directly to avoid package conflict
        import importlib.util
        utils_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils.py")
        spec = importlib.util.spec_from_file_location("utils_py", utils_path)
        utils_py = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils_py)
        escape_latex = utils_py.escape_latex
        
        # Basic replacements - handle HTML content
        title = self._format_content_for_latex(report_data.title)
        subtitle = self._format_content_for_latex(report_data.subtitle)
        
        template_content = template_content.replace('MAINTITLEPLACEHOLDER', title)
        template_content = template_content.replace('SUBTITLEPLACEHOLDER', subtitle)
        # Format date in dd-mm-yyyy format
        formatted_date = report_data.report_date if report_data.report_date else datetime.now().strftime('%d-%m-%Y')
        template_content = template_content.replace('DATEPLACEHOLDER', escape_latex(formatted_date))
        
        # Action box
        action = report_data.action
        action_box = f"\\actionbox{{{action}}}"
        template_content = template_content.replace('ACTIONBOXPLACEHOLDER', action_box)
        
        # Other fields - handle HTML content (skip duplicates that will be handled below)
        template_content = template_content.replace('ENTRYPRICEPLACEHOLDER', escape_latex(report_data.entry_price))
        template_content = template_content.replace('TARGETPRICEPLACEHOLDER', escape_latex(report_data.target_price))
        template_content = template_content.replace('STOPLOSSPLACEHOLDER', escape_latex(report_data.stop_loss))
        template_content = template_content.replace('RISKLEVELPLACEHOLDER', escape_latex(report_data.risk_level))
        
        # Content sections
        investment_thesis_latex = self._format_content_for_latex(report_data.investment_thesis)
        rationale_latex = self._format_content_for_latex(report_data.rationale)
        
        # Replace content placeholders and ensure proper LaTeX structure
        template_content = template_content.replace('INVESTMENTTHESISPLACEHOLDER', investment_thesis_latex)
        template_content = template_content.replace('RATIONALEPLACEHOLDER', rationale_latex)
        
        # Ensure proper closing of formatting groups in template v3
        # Add explicit validation that the necessary closing braces exist
        lines = template_content.split('\n')
        corrected_lines = []
        in_investment_thesis = False
        in_rationale = False
        
        for i, line in enumerate(lines):
            if '\\section*{\\Large\\bfseries\\color{mpcblue} Investment Thesis}' in line:
                in_investment_thesis = True
            elif '\\section*{\\Large\\bfseries\\color{mpcblue} Investment Rationale}' in line:
                in_rationale = True
                # Make sure previous section was closed
                if in_investment_thesis:
                    # Check if previous lines have the closing brace
                    prev_lines = corrected_lines[-5:] if len(corrected_lines) >= 5 else corrected_lines
                    has_closing = any('}' in pline and pline.strip() == '}' for pline in prev_lines)
                    if not has_closing:
                        corrected_lines.append('}')
                        print("Added missing closing brace for Investment Thesis section")
                    in_investment_thesis = False
            elif '% Chart image section' in line and in_rationale:
                # Make sure rationale section is closed
                prev_lines = corrected_lines[-5:] if len(corrected_lines) >= 5 else corrected_lines
                has_closing = any('}' in pline and pline.strip() == '}' for pline in prev_lines)
                if not has_closing:
                    corrected_lines.append('}')
                    print("Added missing closing brace for Investment Rationale section")
                in_rationale = False
            
            corrected_lines.append(line)
        
        template_content = '\n'.join(corrected_lines)
        
        # Handle images for template v3 - copy files to temp directory
        if report_data.company_logo_filename:
            # Handle both UploadedFile objects and string filenames
            if hasattr(report_data.company_logo_filename, 'name'):
                # It's an UploadedFile object
                company_logo_filename = report_data.company_logo_filename.name
                # Save the uploaded file to images directory first
                company_logo_source = self.images_dir / company_logo_filename
                with open(company_logo_source, 'wb') as f:
                    f.write(report_data.company_logo_filename.getvalue())
            else:
                # It's a string filename
                company_logo_filename = report_data.company_logo_filename
                company_logo_source = self.images_dir / company_logo_filename
            
            company_logo_dest = self.temp_dir / company_logo_filename
            if company_logo_source.exists():
                try:
                    shutil.copy2(company_logo_source, company_logo_dest)
                    print(f"Copied company logo: {company_logo_source} -> {company_logo_dest}")
                    # Use the actual company logo filename
                    template_content = template_content.replace('COMPANYLOGOPLACEHOLDER', company_logo_filename)
                except Exception as e:
                    print(f"Warning: Could not copy company logo: {e}")
                    # Fall back to MPC logo
                    template_content = template_content.replace('COMPANYLOGOPLACEHOLDER', 'mpc_logo.png')
            else:
                print(f"Warning: Company logo not found: {company_logo_source}")
                # Fall back to MPC logo
                template_content = template_content.replace('COMPANYLOGOPLACEHOLDER', 'mpc_logo.png')
        else:
            # No company logo filename provided, use MPC logo
            template_content = template_content.replace('COMPANYLOGOPLACEHOLDER', 'mpc_logo.png')
        
        # Handle chart image if present
        if report_data.chart_image_filename:
            # Handle both UploadedFile objects and string filenames
            if hasattr(report_data.chart_image_filename, 'name'):
                # It's an UploadedFile object
                chart_image_filename = report_data.chart_image_filename.name
                # Save the uploaded file to images directory first
                chart_image_source = self.images_dir / chart_image_filename
                with open(chart_image_source, 'wb') as f:
                    f.write(report_data.chart_image_filename.getvalue())
            else:
                # It's a string filename
                chart_image_filename = report_data.chart_image_filename
                chart_image_source = self.images_dir / chart_image_filename
            
            chart_image_dest = self.temp_dir / chart_image_filename
            if chart_image_source.exists():
                try:
                    shutil.copy2(chart_image_source, chart_image_dest)
                    print(f"Copied chart image: {chart_image_source} -> {chart_image_dest}")
                    # Add chart image to template
                    chart_image_latex = f"""
\\vspace{{1em}}
\\begin{{center}}
\\includegraphics[width=\\textwidth, keepaspectratio]{{{chart_image_filename}}}
\\end{{center}}
\\vspace{{1em}}
"""
                    template_content = template_content.replace('CHARTIMAGEPLACEHOLDER', chart_image_latex)
                except Exception as e:
                    print(f"Warning: Could not copy chart image: {e}")
                    template_content = template_content.replace('CHARTIMAGEPLACEHOLDER', '')
            else:
                print(f"Warning: Chart image not found: {chart_image_source}")
                template_content = template_content.replace('CHARTIMAGEPLACEHOLDER', '')
        else:
            template_content = template_content.replace('CHARTIMAGEPLACEHOLDER', '')
        
        # Analysis types
        analysis_list = self._format_analysis_types(report_data.analysis_types)
        template_content = template_content.replace('ANALYSISTYPESPLACEHOLDER', analysis_list)
        
        # Template v3 specific placeholders
        template_content = template_content.replace('CATEGORYPLACEHOLDER', escape_latex(report_data.category))
        template_content = template_content.replace('ACTIONPLACEHOLDER', escape_latex(report_data.action))
        template_content = template_content.replace('COMPANYNAMEPLACEHOLDER', escape_latex(report_data.title))
        template_content = template_content.replace('TICKERPLACEHOLDER', escape_latex(report_data.ticker))
        
        # Ensure proper document ending
        if not template_content.strip().endswith('\\end{document}'):
            template_content = template_content.rstrip() + '\n\\end{document}\n'
        
        return template_content
    
    def _format_content_for_latex(self, content: str) -> str:
        """Format content for LaTeX display - preserve HTML formatting from QuillJS"""
        if not content:
            return ""
        
        # Normalize content to handle encoding issues
        content = self._normalize_content_encoding(content)
        
        # Check if content is HTML (from QuillJS) and convert to LaTeX
        if '<' in content and '>' in content:
            return self._html_to_latex(content)
        
        # Simple approach - treat as plain text and format for LaTeX
        return self._format_text_for_pdf_display(content)
    
    def _normalize_content_encoding(self, content: str) -> str:
        """Normalize content encoding to handle UTF-8 issues"""
        if not isinstance(content, str):
            content = str(content)
        
        # Handle common encoding issues
        try:
            # Try to encode and decode to ensure it's valid UTF-8
            # Don't actually modify the content, just test if it's valid
            content.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            # If there are encoding issues, try to fix them
            try:
                # Try to decode as latin-1 and re-encode as UTF-8
                content = content.encode('latin-1').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError):
                # If all else fails, replace problematic characters
                content = content.encode('utf-8', errors='replace').decode('utf-8')
        
        # Clean up any remaining problematic characters
        content = content.replace('\x97', '—')  # Replace em dash
        content = content.replace('\x96', '–')  # Replace en dash
        content = content.replace('\x91', "'")  # Replace left single quote
        content = content.replace('\x92', "'")  # Replace right single quote
        content = content.replace('\x93', '"')  # Replace left double quote
        content = content.replace('\x94', '"')  # Replace right double quote
        
        # Handle Unicode subscript characters that cause LaTeX errors
        unicode_replacements = {
            '\u2080': '₀',  # subscript 0
            '\u2081': '₁',  # subscript 1
            '\u2082': '₂',  # subscript 2
            '\u2083': '₃',  # subscript 3
            '\u2084': '₄',  # subscript 4
            '\u2085': '₅',  # subscript 5
            '\u2086': '₆',  # subscript 6
            '\u2087': '₇',  # subscript 7
            '\u2088': '₈',  # subscript 8
            '\u2089': '₉',  # subscript 9
            '\u208A': '₊',  # subscript +
            '\u208B': '₋',  # subscript -
            '\u208C': '₌',  # subscript =
            '\u208D': '₍',  # subscript (
            '\u208E': '₎',  # subscript )
        }
        
        # Replace Unicode subscript characters with regular characters
        for unicode_char, replacement in unicode_replacements.items():
            content = content.replace(unicode_char, replacement)
        
        # Handle other problematic Unicode characters
        content = content.replace('\u2013', '-')  # en dash
        content = content.replace('\u2014', '--')  # em dash
        content = content.replace('\u2018', "'")  # left single quote
        content = content.replace('\u2019', "'")  # right single quote
        content = content.replace('\u201C', '"')  # left double quote
        content = content.replace('\u201D', '"')  # right double quote
        content = content.replace('\u2026', '...')  # ellipsis
        
        return content
    
    def _escape_latex_content_safely(self, content: str) -> str:
        """Safely escape LaTeX content without breaking LaTeX commands"""
        import re
        
        # For LaTeX content, we should NOT escape LaTeX commands at all
        # Only escape special characters that are NOT part of LaTeX commands
        
        # First, let's identify and protect LaTeX commands more robustly
        latex_commands = []
        
        # Pattern to match LaTeX commands (including nested braces)
        def find_latex_commands(text):
            commands = []
            i = 0
            while i < len(text):
                if text[i] == '\\' and i + 1 < len(text) and text[i + 1].isalpha():
                    # Found start of LaTeX command
                    start = i
                    i += 1
                    # Find command name
                    while i < len(text) and text[i].isalpha():
                        i += 1
                    
                    # Check for optional arguments in braces
                    if i < len(text) and text[i] == '{':
                        brace_count = 0
                        while i < len(text):
                            if text[i] == '{':
                                brace_count += 1
                            elif text[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    i += 1
                                    break
                            i += 1
                    
                    command = text[start:i]
                    commands.append((start, i, command))
                else:
                    i += 1
            return commands
        
        commands = find_latex_commands(content)
        
        # Replace commands with placeholders (working backwards to maintain positions)
        for i, (start, end, command) in enumerate(reversed(commands)):
            placeholder = f"__LATEX_CMD_{len(commands) - 1 - i}__"
            content = content[:start] + placeholder + content[end:]
        
        # Now escape only the special characters that would break LaTeX
        special_chars = {
            '$': '\\$',
            '&': '\\&',
            '%': '\\%',
            '#': '\\#',
            '^': '\\textasciicircum{}',
            '_': '\\_',
            '~': '\\textasciitilde{}',
        }
        
        for char, replacement in special_chars.items():
            content = content.replace(char, replacement)
        
        # Restore LaTeX commands
        for i, (start, end, command) in enumerate(commands):
            placeholder = f"__LATEX_CMD_{i}__"
            content = content.replace(placeholder, command)
        
        return content
    
    def _validate_latex_syntax(self, latex_content: str) -> str:
        """Comprehensive validation to avoid LaTeX compilation errors"""
        if not latex_content:
            return latex_content
        
        # Remove null bytes and carriage returns
        latex_content = latex_content.replace('\x00', '')
        latex_content = latex_content.replace('\r', '')
        
        # Remove trailing backslashes
        if latex_content.strip().endswith('\\'):
            latex_content = latex_content.strip()[:-1]
        
        # Fix specific malformed patterns that cause LaTeX compilation errors
        # Pattern 1: \subsubsection{CATALYST} followed by standalone }
        latex_content = re.sub(r'\\subsubsection\{([^}]*)\}\s*\n\s*\}', r'\\subsubsection{\1}', latex_content)
        
        # Pattern 2: Any incomplete section command followed by standalone }
        latex_content = re.sub(r'\\(sub)*section\{([^}]*)\}\s*\n\s*\}', r'\\\1section{\2}', latex_content)
        
        # Pattern 3: Remove standalone } that don't belong to any command
        lines = latex_content.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            # Skip standalone closing braces that look orphaned
            if line.strip() == '}':
                # Check if previous line ends with a complete command
                if i > 0:
                    prev_line = lines[i-1].strip()
                    # If previous line doesn't end with } or {, this is likely orphaned
                    if not (prev_line.endswith('}') or prev_line.endswith('{')):
                        print(f"Warning: Removing orphaned closing brace at line {i+1}")
                        continue
            
            # Fix incomplete section commands
            if ('\\section{' in line or '\\subsection{' in line or '\\subsubsection{' in line):
                # Count braces in this line
                open_count = line.count('{')
                close_count = line.count('}')
                if open_count > close_count:
                    # This line has unmatched opening braces
                    # Check if it's a simple case we can fix
                    if open_count - close_count == 1:
                        # Add closing brace
                        line = line.rstrip() + '}'
                        print(f"Warning: Fixed incomplete command by adding closing brace")
            
            cleaned_lines.append(line)
        
        latex_content = '\n'.join(cleaned_lines)
        
        # Final check for brace balance
        open_braces = latex_content.count('{')
        close_braces = latex_content.count('}')
        if open_braces != close_braces:
            print(f"Warning: Unbalanced braces - {open_braces} opening, {close_braces} closing")
        
        return latex_content
    
    def _handle_image_placeholder(self, filename: str, image_type: str) -> str:
        """Handle image placeholder in template"""
        if not filename:
            return ""
        
        # Copy image to temp directory
        source_path = self.images_dir / filename
        dest_path = self.temp_dir / filename
        
        if source_path.exists() and source_path.stat().st_size > 0:
            try:
                shutil.copy2(source_path, dest_path)
                
                if image_type == 'company_logo':
                    return f"""
\\begin{{center}}
\\vspace{{0.2em}}
\\includegraphics[width=0.75\\textwidth, keepaspectratio]{{{filename}}}
\\vspace{{0.2em}}
\\end{{center}}
"""
                else:  # chart_image
                    return f"""
\\begin{{center}}
\\vspace{{1em}}
\\includegraphics[width=1.0\\textwidth, keepaspectratio]{{{filename}}}
\\vspace{{1em}}
\\end{{center}}
"""
            except Exception as e:
                print(f"Warning: Could not copy {image_type}: {e}")
                return ""
        
        return ""
    
    def _format_analysis_types(self, analysis_types: list) -> str:
        """Format analysis types for LaTeX display"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        # Import utils.py directly to avoid package conflict
        import importlib.util
        utils_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils.py")
        spec = importlib.util.spec_from_file_location("utils_py", utils_path)
        utils_py = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils_py)
        escape_latex = utils_py.escape_latex
        
        all_analysis_types = ['Fundamentals', 'Technical Analysis', 'Macro/Geopolitical', 'Catalyst']
        
        # Create checkbox items for template v3
        checkbox_items = []
        for analysis_type in all_analysis_types:
            if analysis_type in analysis_types:
                checkbox_items.append(f'    \\item[\\fcolorbox{{green}}{{green!20}}{{\\textbf{{\\textcolor{{white}}{{\\ding{{51}}}}}}}}] \\textbf{{{escape_latex(analysis_type)}}}')
            else:
                checkbox_items.append(f'    \\item[\\fcolorbox{{gray}}{{white}}{{\\phantom{{\\ding{{51}}}}}}] \\textbf{{{escape_latex(analysis_type)}}}')
        
        # Return as itemize list for template v3
        return '\\begin{itemize}[leftmargin=0pt, itemsep=0.5em]\n' + '\n'.join(checkbox_items) + '\n\\end{itemize}'
    
    def _compile_latex_to_pdf(self, tex_file: Path, filename: str) -> Path:
        """Compile LaTeX file to PDF"""
        try:
            # Change to temp directory
            original_dir = os.getcwd()
            os.chdir(self.temp_dir)
            
            # Run pdflatex
            result = subprocess.run([
                'pdflatex', 
                '-interaction=nonstopmode', 
                '-output-directory', str(self.temp_dir),
                str(tex_file)
            ], capture_output=True, text=True)
            
            # Change back to original directory
            os.chdir(original_dir)
            
            # Check if PDF was actually generated (more reliable than return code)
            temp_pdf_file = self.temp_dir / f"{filename}.pdf"
            
            if not temp_pdf_file.exists():
                # PDF was not generated - this is a real failure
                log_file = self.temp_dir / f"{filename}.log"
                error_details = ""
                if log_file.exists():
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            log_content = f.read()
                            lines = log_content.split('\n')
                            error_lines = [line for line in lines if '!' in line or 'Error' in line or 'Fatal' in line]
                            if error_lines:
                                error_details = "\nLast errors: " + "\n".join(error_lines[-5:])
                    except UnicodeDecodeError:
                        # Fallback to latin-1 if UTF-8 fails
                        with open(log_file, 'r', encoding='latin-1') as f:
                            log_content = f.read()
                            lines = log_content.split('\n')
                            error_lines = [line for line in lines if '!' in line or 'Error' in line or 'Fatal' in line]
                            if error_lines:
                                error_details = "\nLast errors: " + "\n".join(error_lines[-5:])
                
                raise Exception(f"LaTeX compilation failed: {result.stderr}{error_details}")
            
            # PDF exists but check if there were serious errors (not just warnings)
            elif result.returncode != 0:
                log_file = self.temp_dir / f"{filename}.log"
                if log_file.exists():
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            log_content = f.read()
                            # Only treat as failure if there are actual fatal errors
                            fatal_errors = [line for line in log_content.split('\n') 
                                          if 'Fatal' in line or 'Emergency stop' in line]
                            if fatal_errors:
                                error_details = "\nFatal errors: " + "\n".join(fatal_errors[-3:])
                                raise Exception(f"LaTeX compilation failed: {error_details}")
                    except UnicodeDecodeError:
                        pass  # Ignore encoding issues if PDF was generated successfully
                
                # Log warnings but continue since PDF was generated
                print(f"LaTeX compilation completed with warnings (exit code {result.returncode}) but PDF was generated successfully")
            
            # Move PDF to PDFs directory
            final_pdf_file = self.pdfs_dir / f"{filename}.pdf"
            
            if temp_pdf_file.exists():
                shutil.move(str(temp_pdf_file), str(final_pdf_file))
            
            # Move log file to logs directory
            temp_log_file = self.temp_dir / f"{filename}.log"
            final_log_file = self.logs_dir / f"{filename}.log"
            
            if temp_log_file.exists():
                shutil.move(str(temp_log_file), str(final_log_file))
            
            # Clean up temporary files
            self._cleanup_temp_files(filename)
            
            return final_pdf_file
            
        except Exception as e:
            raise Exception(f"Error compiling LaTeX to PDF: {str(e)}")
    
    def _cleanup_temp_files(self, filename: str):
        """Clean up temporary files after compilation"""
        try:
            temp_files = [
                self.temp_dir / f"{filename}.tex",
                self.temp_dir / f"{filename}.aux",
                self.temp_dir / f"{filename}.out",
                self.temp_dir / f"{filename}.toc",
                self.temp_dir / f"{filename}.fdb_latexmk",
                self.temp_dir / f"{filename}.fls",
                self.temp_dir / f"{filename}.synctex.gz"
            ]
            
            for temp_file in temp_files:
                if temp_file.exists():
                    temp_file.unlink()
                    
        except Exception as e:
            print(f"Warning: Could not clean up temporary files: {e}")
    
    def _format_text_for_pdf_display(self, text: str) -> str:
        """Format text for PDF display - simplified approach based on original"""
        if not isinstance(text, str):
            return str(text)
        
        # Check if text contains LaTeX commands missing backslashes
        text = self._fix_missing_latex_backslashes(text)
        
        # Clean LLM output for LaTeX compatibility
        text = self._clean_llm_output_for_latex(text)
        
        # Convert to paragraphs with proper LaTeX formatting
        paragraphs = text.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # Simple LaTeX escaping for special characters
                para = self._escape_latex_characters_safe(para)
                formatted_paragraphs.append(para)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _fix_missing_latex_backslashes(self, text: str) -> str:
        """Fix LaTeX commands that are missing backslashes"""
        import re
        
        # Common LaTeX commands that might be missing backslashes
        latex_commands = [
            'textbf', 'textit', 'textsc', 'textsf', 'texttt', 'textmd', 'textup',
            'emph', 'underline', 'sout', 'uline', 'uwave',
            'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph',
            'begin', 'end', 'item', 'itemize', 'enumerate', 'description',
            'center', 'left', 'right', 'justify', 'flushleft', 'flushright',
            'large', 'Large', 'LARGE', 'huge', 'Huge', 'small', 'footnotesize',
            'tiny', 'normalsize', 'bfseries', 'itshape', 'scshape', 'sffamily',
            'ttfamily', 'mdseries', 'upshape', 'slshape', 'scshape'
        ]
        
        # Fix commands that are missing backslashes
        for command in latex_commands:
            # Pattern: command{...} -> \command{...}
            pattern = r'\b' + command + r'\{'
            replacement = r'\\' + command + r'{'
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _clean_llm_output_for_latex(self, text: str) -> str:
        """Clean and format LLM output for LaTeX compatibility - simplified with basic formatting"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove complex markdown formatting but keep simple dashes
        text = text.replace('**', '').replace('*', '').replace('`', '')
        text = text.replace('__', '')
        
        # Clean up multiple spaces and line breaks
        import re
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple line breaks to double
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        
        # Ensure proper sentence spacing
        text = re.sub(r'\.([A-Z])', r'. \1', text)
        
        # Clean up common formatting issues
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        
        # Handle basic bullet points - convert simple dashes to LaTeX itemize
        text = self._format_simple_bullets(text)
        
        return text.strip()
    
    def _escape_latex_characters(self, text: str) -> str:
        """Simple LaTeX character escaping with HTML entity handling"""
        # First, handle HTML entities that might be in the text
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        text = text.replace('&nbsp;', ' ')
        
        # Then escape LaTeX special characters
        text = text.replace('&', '\\&')
        text = text.replace('%', '\\%')
        text = text.replace('$', '\\$')
        text = text.replace('#', '\\#')
        text = text.replace('_', '\\_')
        text = text.replace('^', '\\textasciicircum{}')
        text = text.replace('~', '\\textasciitilde{}')
        
        return text
    
    def _html_to_plain_text(self, html_content: str) -> str:
        """Convert HTML content to plain text for LaTeX processing"""
        if not html_content:
            return ""
        
        import re
        
        # Remove HTML tags but preserve content structure
        text = html_content
        
        # Convert HTML paragraphs to double newlines
        text = re.sub(r'</p>\s*<p>', '\n\n', text)
        text = re.sub(r'<p[^>]*>', '', text)
        text = re.sub(r'</p>', '', text)
        
        # Convert HTML lists to simple dashes with proper grouping
        text = re.sub(r'<ul[^>]*>', '\n', text)
        text = re.sub(r'</ul>', '\n', text)
        text = re.sub(r'<li[^>]*>', '- ', text)
        text = re.sub(r'</li>', '', text)
        
        # Remove other HTML tags but keep content
        text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'\1', text)
        text = re.sub(r'<b[^>]*>(.*?)</b>', r'\1', text)
        text = re.sub(r'<em[^>]*>(.*?)</em>', r'\1', text)
        text = re.sub(r'<i[^>]*>(.*?)</i>', r'\1', text)
        text = re.sub(r'<br\s*/?>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)  # Remove any remaining HTML tags
        
        # Handle HTML entities
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&ndash;', '–')
        text = text.replace('&mdash;', '—')
        text = text.replace('&hellip;', '...')
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        text = text.strip()
        
        return text
    
    def _html_to_latex(self, html_content: str) -> str:
        """Convert HTML content to LaTeX while preserving rich formatting"""
        if not html_content:
            return ""
        
        import re
        
        # Handle HTML entities first
        text = html_content
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&ndash;', '--')
        text = text.replace('&mdash;', '---')
        text = text.replace('&hellip;', '...')
        
        # Convert paragraphs to LaTeX paragraphs
        text = re.sub(r'</p>\s*<p[^>]*>', '\n\n', text)
        text = re.sub(r'<p[^>]*>', '', text)
        text = re.sub(r'</p>', '', text)
        
        # Convert unordered lists to LaTeX itemize
        text = re.sub(r'<ul[^>]*>', r'\n\\begin{itemize}\n', text)
        text = re.sub(r'</ul>', r'\n\\end{itemize}\n', text)
        text = re.sub(r'<li[^>]*>', r'\\item ', text)
        text = re.sub(r'</li>', '', text)
        
        # Convert ordered lists to LaTeX enumerate
        text = re.sub(r'<ol[^>]*>', r'\n\\begin{enumerate}\n', text)
        text = re.sub(r'</ol>', r'\n\\end{enumerate}\n', text)
        
        # Convert bold text to LaTeX textbf
        text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'\\textbf{\1}', text)
        text = re.sub(r'<b[^>]*>(.*?)</b>', r'\\textbf{\1}', text)
        
        # Convert italic text to LaTeX textit
        text = re.sub(r'<em[^>]*>(.*?)</em>', r'\\textit{\1}', text)
        text = re.sub(r'<i[^>]*>(.*?)</i>', r'\\textit{\1}', text)
        
        # Convert line breaks
        text = re.sub(r'<br\s*/?>', r'\\\\', text)
        
        # Convert headers (if any)
        text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\\section*{\1}', text)
        text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\\subsection*{\1}', text)
        text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\\subsubsection*{\1}', text)
        
        # Convert hyperlinks to LaTeX href
        text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'\\href{\1}{\2}', text)
        
        # Remove any remaining HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        text = text.strip()
        
        # Escape LaTeX special characters in the final text (but preserve LaTeX commands)
        # We need to be careful not to escape backslashes in LaTeX commands
        text = self._escape_latex_characters_safe(text)
        
        return text

    def _escape_latex_characters_safe(self, text: str) -> str:
        """Escape LaTeX special characters while preserving LaTeX commands"""
        import re
        
        # First, handle HTML entities that might be in the text
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        text = text.replace('&nbsp;', ' ')
        
        # Escape LaTeX special characters, but be careful with backslashes
        # Don't escape backslashes that are part of LaTeX commands
        text = text.replace('&', '\\&')
        text = text.replace('%', '\\%')
        text = text.replace('$', '\\$')
        text = text.replace('#', '\\#')
        text = text.replace('_', '\\_')
        text = text.replace('^', '\\textasciicircum{}')
        text = text.replace('~', '\\textasciitilde{}')
        
        return text

    def _format_simple_bullets(self, text: str) -> str:
        """Convert simple dash bullets to LaTeX format"""
        import re
        
        # Look for lines that start with "- " (bullet points)
        lines = text.split('\n')
        formatted_lines = []
        in_bullet_list = False
        
        for line in lines:
            line = line.strip()
            
            # Check if this line starts with a dash bullet
            if line.startswith('- '):
                if not in_bullet_list:
                    # Start a new bullet list
                    formatted_lines.append('\\begin{itemize}')
                    in_bullet_list = True
                # Convert dash to LaTeX item
                bullet_content = line[2:].strip()  # Remove "- "
                formatted_lines.append(f'\\item {bullet_content}')
            
            elif line == '':
                # Empty line - continue
                if in_bullet_list:
                    # End bullet list before empty line
                    formatted_lines.append('\\end{itemize}')
                    in_bullet_list = False
                formatted_lines.append('')
            
            else:
                # Regular text line
                if in_bullet_list:
                    # End bullet list before regular text
                    formatted_lines.append('\\end{itemize}')
                    in_bullet_list = False
                formatted_lines.append(line)
        
        # Close any open bullet list at the end
        if in_bullet_list:
            formatted_lines.append('\\end{itemize}')
        
        return '\n'.join(formatted_lines)
