# Investment Recommendation Generator v3

A professional Streamlit application for generating investment recommendation reports with AI-powered content generation and LaTeX PDF output.

## ✨ Features

- **🤖 AI Content Generation**: OpenRouter integration with 57+ free models
- **✍️ Human Content Support**: Rich text editors with QuillJS
- **📄 Professional PDF Generation**: LaTeX-based reports with 3 template versions
- **🖼️ Smart Image Upload**: Automatic format conversion and LaTeX compatibility
- **🐳 Docker Deployment**: Containerized with health checks
- **📊 Risk Analysis**: Automatic risk metrics calculation
- **🎨 Template Selection**: Choose between professional report templates
- **✅ Comprehensive Validation**: Form validation with clear error messages

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/mpcmarkets/recommendations_generator.git
cd recommendations_generator

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8501

# Stop the application
docker-compose down
```

### Option 2: Local Development
```bash
# Set up local environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start the application
streamlit run app.py

# Access the application
open http://localhost:8501
```

## 📋 Available Commands

### Docker Compose Commands
```bash
docker-compose up -d          # Start the application in background
docker-compose down           # Stop the application
docker-compose logs           # View application logs
docker-compose ps             # Check container status
docker-compose restart        # Restart the application
docker-compose build          # Rebuild the Docker image
```

### Local Development Commands
```bash
streamlit run app.py          # Start the application locally
pip install -r requirements.txt  # Install dependencies
```

## 🎯 How to Use

### Step 1: Fill Out the Form
1. **Basic Information**: Company name, ticker, category, action
2. **Analysis Types**: Select from Fundamentals, Technical Analysis, Macro/Geopolitical, Catalyst
3. **Trade Plan**: Enter entry price, target price, and stop loss
4. **Images**: Upload company logo and chart images (optional)
5. **Template**: Select your preferred report template (v1, v2, or v3)

### Step 2: Generate Content
- **For AI Content**: Choose your preferred AI model, provide investment rationale and context, then click "Generate AI Content"
- **For Human Content**: Write your executive summary and investment rationale directly

### Step 3: Review and Generate
1. Review the generated content
2. Edit if needed using the rich text editors
3. Click "Generate Final Report" to create the PDF
4. Download your professional investment recommendation report

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with modular design
- **PDF Generation**: LaTeX compilation with pdflatex
- **AI Integration**: OpenRouter API with 57+ free models via ai_tools library
- **Image Processing**: PIL/Pillow with automatic format conversion
- **Modular Design**: ai_tools installed from separate private repository

### AI Models Available
- **DeepSeek Chat v3.1** (32K context) - Default
- **Sonoma Dusk Alpha** (2M context)
- **GPT-OSS 120B** (32K context)
- **Microsoft MAI DS R1** (163K context)
- **Meta Llama 4 Maverick** (128K context)
- **And 52+ more free models...**

### Templates
- **Template v1**: Classic layout with side-by-side elements
- **Template v2**: Modern centered layout
- **Template v3**: Clean layout with dynamic checkboxes (New)

### Image Support
- **Supported Formats**: PNG, JPG, JPEG, PDF, EPS
- **Auto-Converted**: WEBP, GIF, BMP, TIFF → PNG
- **Features**: Format conversion, transparency handling, LaTeX compatibility
- **Size Limit**: 10MB maximum per image

## 📁 Project Structure

```
recommendation_generator/
├── start.sh                    # Main entry point script
├── scripts/
│   └── deploy.sh              # Unified deployment script
├── app.py                     # Main Streamlit application
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies (includes ai_tools from private repo)
├── Dockerfile                 # Docker configuration
├── .env.example               # Environment variables template
├── components/                # UI components
│   ├── form_components.py     # Form input components
│   ├── model_selector.py      # AI model selection
│   ├── navigation.py          # Navigation components
│   ├── quill_editor.py        # Rich text editor
│   └── review_components.py   # Review and generation
├── services/                  # Business logic services
│   ├── openrouter_ai_service.py    # AI content generation
│   ├── openrouter_models.py        # Model management
│   ├── image_service.py            # Image processing
│   ├── pdf_service.py              # PDF generation
│   └── content_converter.py        # Content conversion
├── models/                    # Data models
│   ├── form_data.py           # Form data model
│   └── report_data.py         # Report data structure
├── templates/                 # LaTeX templates and assets
│   ├── recommendations_report_v1.tex
│   ├── recommendations_report_v2.tex
│   ├── recommendations_report_v3.tex
│   ├── v1_preview.png
│   ├── v2_preview.png
│   └── v3_preview.png
└── data/                      # Generated files (auto-created)
    ├── pdfs/                  # Generated PDF reports
    ├── images/                # Uploaded images
    ├── logs/                  # Application logs
    └── temp/                  # Temporary files
```

## 🔧 Configuration

Edit `config.py` to customize:
- Directory paths
- AI model settings
- Application settings
- Form validation settings
- Image processing settings

## 🐛 Troubleshooting

### LaTeX Issues
- Ensure LaTeX is properly installed
- Check that `pdflatex` is available in PATH
- Review logs in `data/logs/` for compilation errors

### AI Generation Issues
- Ensure OpenRouter API key is set in environment
- Check model availability and selection
- Review error messages in the application

### Docker Issues
- Ensure Docker is running
- Check container logs: `./start.sh logs`
- Verify port 8501 is available

### General Issues
- Check that all dependencies are installed
- Ensure you have write permissions in the application directory
- Review the console output for detailed error messages

## 🧪 Testing

The application has been thoroughly tested:
- ✅ Module imports and dependencies
- ✅ Form validation and data models
- ✅ AI content generation with multiple models
- ✅ Image upload and processing
- ✅ PDF generation with all templates
- ✅ Docker deployment and health checks

## 📄 License

This project is part of the MPC Markets research toolkit.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Check the logs in `data/logs/`
4. Ensure all dependencies are properly installed

---

**Investment Recommendation Generator v3** - Professional, AI-powered, and ready for production use! 🚀