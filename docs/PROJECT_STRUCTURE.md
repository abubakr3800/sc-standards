# AI Standards Training System - Project Structure

## 📁 **Complete Project Structure**

```
ai-standards-training/
├── 📄 Core System Files
│   ├── main.py                    # Main entry point and CLI
│   ├── config.py                  # System configuration
│   ├── pdf_processor.py           # PDF text extraction and processing
│   ├── ai_trainer.py              # AI model training pipeline
│   ├── comparison_model.py        # Standards comparison and analysis
│   └── web_interface.py           # Streamlit web UI and FastAPI
│
├── 📦 Installation & Setup
│   ├── requirements.txt           # Python dependencies
│   ├── install.py                 # Smart installation script
│   ├── setup_environment.py       # Environment setup
│   ├── test_installation.py       # Installation verification
│   └── env_template               # Environment variables template
│
├── 🐳 Docker & Deployment
│   ├── Dockerfile                 # Docker container configuration
│   ├── docker-compose.yml         # Multi-service Docker setup
│   └── Makefile                   # Build and deployment commands
│
├── 📋 Project Configuration
│   ├── pyproject.toml             # Modern Python project config
│   ├── setup.cfg                  # Setuptools configuration
│   ├── .gitignore                 # Git ignore rules
│   ├── .env                       # Environment variables (auto-generated)
│   └── LICENSE                    # MIT License
│
├── 📚 Documentation
│   ├── README.md                  # Main documentation
│   ├── WORKFLOW_EXPLANATION.md    # Detailed workflow explanation
│   ├── CONFIRMATION.md            # System confirmation
│   ├── SYSTEM_OVERVIEW.md         # Complete system overview
│   └── PROJECT_STRUCTURE.md       # This file
│
├── 🧪 Testing & Examples
│   ├── example_usage.py           # Usage examples
│   ├── table_extraction_demo.py   # PDF extraction demo
│   └── simple_extraction_test.py  # Simple extraction test
│
├── 📁 Data Directories
│   ├── base/                      # Source PDF files
│   │   ├── ODLI20150723_001-UPD-en_AA-Lighting-for-BREEAM-in-offices.pdf
│   │   ├── prEN 12464-1.pdf
│   │   └── .gitkeep
│   ├── data/                      # Processed data and databases
│   │   ├── standards.db           # SQLite database
│   │   ├── vector_db/             # ChromaDB vector database
│   │   └── .gitkeep
│   ├── models/                    # Trained AI models
│   │   ├── classification/        # Classification models
│   │   ├── embeddings/            # Embedding models
│   │   └── .gitkeep
│   ├── uploads/                   # Uploaded files for processing
│   │   └── .gitkeep
│   ├── outputs/                   # Training results and reports
│   │   └── .gitkeep
│   └── logs/                      # System logs
│       └── .gitkeep
│
└── 🔧 Development Files
    ├── tests/                     # Unit and integration tests
    ├── docs/                      # Additional documentation
    └── examples/                  # Example scripts and notebooks
```

## 🎯 **Key Files Explained**

### **Core System Files**
- **`main.py`** - Command-line interface and main entry point
- **`config.py`** - Centralized configuration management
- **`pdf_processor.py`** - Handles PDF text extraction and preprocessing
- **`ai_trainer.py`** - Manages AI model training and fine-tuning
- **`comparison_model.py`** - Performs standards comparison and analysis
- **`web_interface.py`** - Provides web UI and REST API

### **Installation & Setup**
- **`requirements.txt`** - Python package dependencies
- **`install.py`** - Smart installer with version compatibility
- **`setup_environment.py`** - Creates .env file and directories
- **`test_installation.py`** - Verifies installation success

### **Docker & Deployment**
- **`Dockerfile`** - Container configuration for deployment
- **`docker-compose.yml`** - Multi-service orchestration
- **`Makefile`** - Build, test, and deployment commands

### **Project Configuration**
- **`pyproject.toml`** - Modern Python project metadata
- **`setup.cfg`** - Setuptools configuration
- **`.gitignore`** - Git ignore patterns for clean repository
- **`.env`** - Environment variables (auto-generated with secrets)

### **Documentation**
- **`README.md`** - Main project documentation
- **`WORKFLOW_EXPLANATION.md`** - Detailed workflow explanation
- **`CONFIRMATION.md`** - System capabilities confirmation
- **`SYSTEM_OVERVIEW.md`** - Complete system overview

## 🚀 **Quick Start Commands**

### **Setup**
```bash
py setup_environment.py    # Create .env and directories
py install.py              # Install dependencies
```

### **Processing**
```bash
py main.py process         # Process PDFs in base/ folder
py main.py train           # Train AI models
py main.py demo            # Run complete demo
```

### **Usage**
```bash
py main.py web             # Start web interface
py main.py api             # Start API server
py main.py compare --standard-a file1.pdf --standard-b file2.pdf
```

### **Docker**
```bash
make docker-build          # Build Docker image
make docker-run            # Run with Docker Compose
```

### **Development**
```bash
make dev-setup             # Setup development environment
make test                  # Run tests
make clean                 # Clean temporary files
```

## 📊 **Data Flow**

```
base/ (PDFs) → pdf_processor.py → data/ (processed)
     ↓
ai_trainer.py → models/ (trained AI)
     ↓
comparison_model.py → outputs/ (reports)
     ↓
web_interface.py → User Interface
```

## 🔧 **Environment Variables**

The `.env` file contains:
- Database paths
- API configuration
- Model parameters
- Processing settings
- Security keys
- Performance tuning

## 📦 **Dependencies**

### **Core AI/ML**
- PyTorch, Transformers, Sentence-Transformers
- Scikit-learn, NumPy, Pandas

### **PDF Processing**
- PyPDF2, pdfplumber, PyMuPDF, pdfminer

### **NLP & Translation**
- spaCy, NLTK, langdetect, googletrans

### **Web Interface**
- Streamlit, FastAPI, Uvicorn

### **Data Storage**
- SQLAlchemy, ChromaDB, FAISS

### **Visualization**
- Matplotlib, Seaborn, Plotly

## 🎯 **System Capabilities**

✅ **PDF Processing** - Extract text, tables, and structured data
✅ **Multilingual Support** - Auto-detect and translate languages
✅ **AI Training** - Create custom models for standards understanding
✅ **Vector Search** - Semantic similarity and search
✅ **Standards Comparison** - Detailed analysis and recommendations
✅ **Web Interface** - User-friendly dashboard
✅ **REST API** - Programmatic access
✅ **Docker Support** - Easy deployment
✅ **Comprehensive Testing** - Installation and functionality tests

Your AI Standards Training System is now fully configured and ready to use! 🎉

