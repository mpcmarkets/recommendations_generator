# Investment Recommendation Generator

A professional Streamlit application for generating investment recommendation reports with AI-powered content generation and LaTeX PDF output.

## 🚀 Features

- **📝 Form-Based Input**: Comprehensive investment recommendation forms
- **🤖 AI Content Generation**: Generate executive summaries and analysis using LLM
- **✏️ Rich Text Editing**: QuillJS editor for content review and editing
- **📊 PDF Report Generation**: Professional LaTeX-based PDF reports with multiple templates
- **🖼️ Image Support**: Upload company logos and chart images
- **🎨 Multiple Templates**: Three different LaTeX report templates
- **🔄 Content Pipeline**: Clean markdown → HTML → LaTeX conversion
- **🐳 Docker Support**: Complete containerization with Docker Compose
- **⚡ Local Development**: Virtual environment setup and development tools

## 🏗️ Architecture

```
recommendation_generator/
├── models/                   # Data models and validation
│   ├── form_data.py         # Form data structure
│   └── report_data.py       # Report data structure
├── services/                 # Business logic services
│   ├── ai_service.py        # AI content generation
│   ├── pdf_service.py       # PDF generation and LaTeX processing
│   └── image_service.py     # Image processing utilities
├── components/               # UI components
│   ├── form_components.py   # Form input components
│   ├── review_components.py # Content review and editing
│   ├── navigation.py        # Navigation components
│   └── quill_editor.py      # Rich text editor
├── templates/                # LaTeX report templates
│   ├── recommendations_report_v1.tex
│   ├── recommendations_report_v2.tex
│   └── recommendations_report_v3.tex
├── data/                     # Application data
│   ├── pdfs/                # Generated PDF reports
│   ├── images/              # Uploaded images
│   ├── logs/                # Application logs
│   └── temp/                # Temporary files
├── constants/                # CSS and styling constants
├── utils/                    # Utility functions
├── config.py                # Application configuration
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Docker orchestration
├── activate.sh              # Local development setup
├── docker-deploy.sh         # Docker deployment script
└── run.sh                   # Quick start script
```

## 🔄 Content Pipeline

1. **📝 Form Input**: User fills out investment recommendation form
2. **🤖 AI Generation**: LLM generates content in clean markdown format
3. **✏️ Rich Text Editing**: Markdown converted to HTML for QuillJS editing
4. **📊 PDF Generation**: HTML content converted to LaTeX for professional PDF output

### 🐳 Docker (Recommended)

```bash
# Clone and navigate to the project
cd /home/kaichen/repo/recommendation_generator

# Start with Docker (new improved script)
./docker-run.sh start

# Access the application
open http://localhost:8501

# Alternative: Legacy Docker Compose (may have compatibility issues)
./docker-deploy.sh start
```

### 💻 Local Development

```bash
# Navigate to the project
cd /home/kaichen/repo/recommendation_generator

# Setup virtual environment
./activate.sh

# Start the application
streamlit run app.py
```

### ⚡ Quick Start (No Setup)

```bash
# Navigate to the project
cd /home/kaichen/repo/recommendation_generator

# Run directly (installs dependencies automatically)
./run.sh
```

## 📋 Prerequisites

- **Python 3.11+** (for local development)
- **Docker & Docker Compose** (for containerized deployment)
- **LaTeX** (for PDF generation - optional but recommended)

### LaTeX Installation

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

**macOS:**
```bash
brew install --cask mactex
```

**Windows:**
Download and install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)

## 🛠️ Development

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `./activate.sh` | Setup virtual environment | `./activate.sh` |
| `./docker-deploy.sh` | Docker deployment | `./docker-deploy.sh start` |
| `./run.sh` | Quick start without setup | `./run.sh` |

### Docker Commands

**New Improved Script (Recommended):**
```bash
./docker-run.sh start        # Start the application
./docker-run.sh stop         # Stop the application
./docker-run.sh restart      # Restart (rebuild and start)
./docker-run.sh logs         # View logs
./docker-run.sh status       # Check status
./docker-run.sh build        # Build image only
```

**Legacy Docker Compose (may have compatibility issues):**
```bash
./docker-deploy.sh start     # Start the application
./docker-deploy.sh stop      # Stop the application
./docker-deploy.sh logs      # View logs
./docker-deploy.sh status    # Check status
./docker-deploy.sh cleanup   # Clean up resources
```

### Local Development Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Start with auto-reload
streamlit run app.py --server.runOnSave true

# Start on different port
streamlit run app.py --server.port 8502

# Test imports
python -c "import app"
```

## 📁 Data Directory

All application data is stored in the `data/` directory:

- `data/pdfs/` - Generated PDF reports
- `data/images/` - Uploaded company logos and charts
- `data/logs/` - Application logs
- `data/temp/` - Temporary processing files

## 🔧 Configuration

The application configuration is centralized in `config.py`:

- Directory paths
- Application settings
- Error messages
- UI constants
- Template configurations

## 📚 Documentation

- **[Docker Deployment Guide](DOCKER_README.md)** - Complete Docker setup and deployment
- **[Local Development Guide](LOCAL_DEVELOPMENT.md)** - Local development setup and tips

## 🎯 Usage

1. **📝 Fill Out Form**: Complete the investment recommendation form with company details, prices, and analysis
2. **🤖 Generate Content**: Choose between AI-generated or human-written content
3. **✏️ Edit Content**: Review and edit content using the rich text editor
4. **📊 Generate Report**: Create professional PDF reports with multiple template options

## 🔧 Technical Details

### Content Format

The application uses a clean markdown format that works seamlessly across all components:

- **Headers**: `## Section Header`
- **Bold**: `**bold text**`
- **Italic**: `*italic text*`
- **Lists**: `- bullet point`
- **Links**: `[link text](url)`

This format is automatically converted to HTML for QuillJS editing and then to LaTeX for PDF generation.

### Key Improvements

- **✅ Clean Content Pipeline**: Fixed markdown → HTML → LaTeX conversion issues
- **✅ Better Content Parsing**: No more parsing errors with bullet points and formatting
- **✅ Robust Error Handling**: Improved error handling in content conversion
- **✅ Proper QuillJS Integration**: Seamless rich text editing with clean HTML output
- **✅ Docker Support**: Complete containerization with health checks and volume management
- **✅ Development Tools**: Virtual environment setup and deployment scripts

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the documentation in `DOCKER_README.md` and `LOCAL_DEVELOPMENT.md`
2. Review application logs in `data/logs/`
3. Test with the provided scripts and examples
