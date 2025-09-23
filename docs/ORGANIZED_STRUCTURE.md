# AI Standards Training System - Organized Project Structure

## 📁 **New Organized Structure**

```
ai-standards-training/
├── 📦 Source Code (src/)
│   └── ai_standards/
│       ├── __init__.py            # Main package initialization
│       ├── core/                  # Core functionality
│       │   ├── __init__.py
│       │   ├── config.py          # System configuration
│       │   └── pdf_processor.py   # PDF text extraction
│       ├── models/                # AI models and training
│       │   ├── __init__.py
│       │   ├── ai_trainer.py      # AI model training
│       │   └── comparison_model.py # Standards comparison
│       ├── web/                   # Web interfaces
│       │   ├── __init__.py
│       │   └── web_interface.py   # Streamlit & FastAPI
│       └── utils/                 # Utility functions
│           └── __init__.py
│
├── 🧪 Tests (tests/)
│   ├── __init__.py
│   └── test_installation.py      # Installation verification
│
├── 📚 Documentation (docs/)
│   ├── README.md                  # Main documentation
│   ├── WORKFLOW_EXPLANATION.md    # Detailed workflow
│   ├── CONFIRMATION.md            # System confirmation
│   ├── SYSTEM_OVERVIEW.md         # Complete overview
│   ├── PROJECT_STRUCTURE.md       # Project structure
│   ├── ORGANIZED_STRUCTURE.md     # This file
│   └── SETUP_COMPLETE.md          # Setup completion
│
├── 🔧 Scripts (scripts/)
│   ├── install.py                 # Smart installation
│   └── setup_environment.py       # Environment setup
│
├── ⚙️ Configuration (configs/)
│   └── env_template               # Environment template
│
├── 📖 Examples (examples/)
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
├── 🐳 Deployment Files
│   ├── Dockerfile                 # Docker container
│   ├── docker-compose.yml         # Multi-service setup
│   └── Makefile                   # Build commands
│
├── 📋 Project Configuration
│   ├── main.py                    # Main entry point
│   ├── requirements.txt           # Python dependencies
│   ├── pyproject.toml             # Modern Python config
│   ├── setup.cfg                  # Setuptools config
│   ├── .gitignore                 # Git ignore rules
│   ├── .env                       # Environment variables
│   └── LICENSE                    # MIT License
│
└── 🔧 Legacy Files (to be cleaned up)
    └── extract_dialux_improved.py # Old extraction script
```

## 🎯 **Benefits of New Organization**

### **1. Professional Structure**
- ✅ **src/** - Source code in proper package structure
- ✅ **tests/** - Dedicated testing directory
- ✅ **docs/** - All documentation in one place
- ✅ **scripts/** - Setup and utility scripts
- ✅ **configs/** - Configuration templates
- ✅ **examples/** - Example code and demos

### **2. Modular Design**
- ✅ **ai_standards.core** - Core functionality (config, PDF processing)
- ✅ **ai_standards.models** - AI models and training
- ✅ **ai_standards.web** - Web interfaces
- ✅ **ai_standards.utils** - Utility functions

### **3. Clean Separation**
- ✅ **Source code** separated from configuration
- ✅ **Documentation** organized and accessible
- ✅ **Scripts** for setup and maintenance
- ✅ **Examples** for learning and testing

### **4. Easy Maintenance**
- ✅ **Clear imports** with proper package structure
- ✅ **Modular components** that can be updated independently
- ✅ **Organized data** in dedicated directories
- ✅ **Professional deployment** with Docker support

## 🚀 **Updated Usage Commands**

### **Installation**
```bash
# From project root
py scripts/install.py
py scripts/setup_environment.py
```

### **Main Usage**
```bash
# From project root
py main.py process         # Process PDFs
py main.py train           # Train models
py main.py web             # Start web interface
py main.py api             # Start API server
```

### **Examples**
```bash
# From project root
py examples/example_usage.py
py examples/table_extraction_demo.py
py examples/simple_extraction_test.py
```

### **Testing**
```bash
# From project root
py tests/test_installation.py
```

### **Docker**
```bash
make docker-build          # Build Docker image
make docker-run            # Run with Docker Compose
```

## 📦 **Package Structure**

### **ai_standards Package**
```python
from ai_standards.core.config import config
from ai_standards.core.pdf_processor import PDFProcessor
from ai_standards.models.ai_trainer import AIStandardsTrainer
from ai_standards.models.comparison_model import StandardsComparisonModel
from ai_standards.web.web_interface import create_streamlit_app
```

### **Main Entry Point**
```python
# main.py automatically adds src/ to path
from ai_standards.core.config import config
from ai_standards.core.pdf_processor import PDFProcessor
# ... other imports
```

## 🎉 **Organization Complete!**

Your AI Standards Training System now has:
- ✅ **Professional package structure**
- ✅ **Modular, maintainable code**
- ✅ **Organized documentation**
- ✅ **Clear separation of concerns**
- ✅ **Easy deployment and testing**

The system is now organized like a professional Python project while maintaining all its powerful capabilities! 🚀
