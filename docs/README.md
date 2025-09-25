# AI Standards Training System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/GitHub-sc--standards-green.svg)](https://github.com/abubakr3800/sc-standards)

A comprehensive AI system for processing, understanding, and comparing lighting standards from PDF documents in multiple languages.

**🆕 NEW: Dialux Report Analysis System** - Comprehensive analysis of Dialux lighting reports with intelligent parameter extraction and standards compliance checking.

**Developed by [Short Circuit Company](mailto:Scc@shortcircuitcompany.com)**

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Web Interface](#web-interface)
- [API Endpoints](#api-endpoints)
- [System Architecture](#system-architecture)
- [Configuration](#configuration)
- [Supported Languages](#supported-languages)
- [Standards Categories](#standards-categories)
- [Example Usage](#example-usage)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Multi-language PDF Processing**: Extract text from PDFs in any language with automatic language detection and translation
- **AI Model Training**: Train custom models to understand and categorize lighting standards
- **Standards Comparison**: Compare standards across different regions and languages
- **Vector Database**: Store and search through standards using semantic similarity
- **Web Interface**: User-friendly Streamlit interface for easy interaction
- **REST API**: FastAPI-based API for programmatic access
- **🆕 Dialux Report Analysis**: Comprehensive analysis of Dialux lighting reports with intelligent parameter extraction
- **🆕 Standards Compliance Checking**: Automated compliance assessment against EN 12464-1, BREEAM, and other lighting standards
- **🆕 Detailed Room Analysis**: Individual room-by-room analysis with complete lighting parameter extraction
- **🆕 Intelligent Data Processing**: Smart extraction that consolidates data and focuses on actual room spaces

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abubakr3800/sc-standards.git
   cd sc-standards
   ```

2. **Place your PDF standards files in the `base/` folder**:
   ```bash
   # The system will automatically look for PDFs in the base/ folder
   # You can also specify a different directory with --input-dir
   ```

3. **Install dependencies** (choose one method):

   **Method A: Automatic installation (recommended)**:
   ```bash
   python scripts/install.py
   ```

   **Method B: Manual installation**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python -m spacy download de_core_news_sm
   python -m spacy download fr_core_news_sm
   # Add other language models as needed
   ```

   **Method C: Using Make**:
   ```bash
   make setup
   make install
   ```

   **Note**: If you encounter Python version compatibility issues, use the automatic installer which handles version conflicts.

## Quick Start

### 1. Process PDF Standards

```bash
# Process all PDFs in base/ folder (default)
python main.py process --target-language en

# Process specific directory
python main.py process --input-dir /path/to/pdfs --target-language en
```

### 2. Train AI Models

```bash
# Train models from processed data
python main.py train
```

### 3. Compare Standards

```bash
# Compare two specific standards
python main.py compare --standard-a standard1.pdf --standard-b standard2.pdf
```

### 4. Run Web Interface

```bash
# Start Streamlit web interface
python main.py web
```

### 5. Run API Server

```bash
# Start FastAPI server
python main.py api --host 0.0.0.0 --port 8000
```

### 6. Run Complete Demo

```bash
# Process PDFs, train models, and compare standards
python main.py demo
```

## Web Interface

The Streamlit web interface provides:

- **Upload & Process**: Upload PDF files and process them with language detection
- **Train Models**: Configure and train AI models for standards understanding
- **Compare Standards**: Compare two standards with detailed analysis
- **Analytics**: View training performance and system statistics
- **Settings**: Configure system parameters and manage data

Access the web interface at `http://localhost:8501` when running `python main.py web`

## API Endpoints

The FastAPI server provides REST endpoints:

- `POST /upload` - Upload and process PDF files
- `POST /train` - Train AI models
- `POST /compare` - Compare two standards
- `GET /standards` - List available standards
- `GET /docs` - API documentation

Access the API at `http://localhost:8000` when running `python main.py api`

## System Architecture

### Core Components

1. **PDF Processor** (`src/ai_standards/core/pdf_processor.py`)
   - Multi-method PDF text extraction (pdfplumber, PyMuPDF, pdfminer)
   - Language detection and translation
   - Text preprocessing and chunking
   - Structured data extraction

2. **AI Trainer** (`src/ai_standards/models/ai_trainer.py`)
   - Sentence transformer fine-tuning
   - Classification model training
   - Vector database integration
   - Training pipeline management

3. **Comparison Model** (`src/ai_standards/models/comparison_model.py`)
   - Semantic similarity analysis
   - Category-specific comparisons
   - Compliance checking
   - Recommendation generation

4. **Web Interface** (`src/ai_standards/web/web_interface.py`)
   - Streamlit dashboard
   - FastAPI REST endpoints
   - Interactive visualizations

### Data Flow

```
PDF Files → PDF Processor → Training Data → AI Trainer → Trained Models
                ↓
         Vector Database ← Embeddings ← Comparison Model
                ↓
         Web Interface ← API Endpoints ← Comparison Results
```

## Configuration

Edit `src/ai_standards/core/config.py` to customize:

- **PDF Processing**: Supported languages, extraction methods, chunk sizes
- **AI Models**: Model names, training parameters, batch sizes
- **Comparison**: Similarity thresholds, feature weights
- **Database**: Storage paths and settings

You can also use environment variables by copying `configs/env_template` to `.env` and modifying the values.

## Supported Languages

The system supports processing PDFs in:
- English (en)
- German (de)
- French (fr)
- Spanish (es)
- Italian (it)
- Portuguese (pt)
- Dutch (nl)
- Swedish (sv)
- Norwegian (no)
- Danish (da)
- Finnish (fi)

## Standards Categories

The system analyzes standards across these categories:

1. **Illuminance Requirements** - Lighting levels and brightness
2. **Color Rendering** - Color temperature and CRI values
3. **Glare Control** - UGR ratings and visual comfort
4. **Energy Efficiency** - Power consumption and efficiency
5. **Safety Standards** - Emergency lighting and safety requirements
6. **Measurement Methods** - Testing procedures and protocols
7. **Compliance Criteria** - Requirements and standards
8. **Environmental Conditions** - Temperature and climate factors
9. **Equipment Specifications** - Luminaire and fixture requirements
10. **General Requirements** - Overall lighting standards

## Example Usage

### Processing Your PDFs

1. Place your PDF standards files in the project directory
2. Run: `python main.py process`
3. The system will:
   - Extract text from each PDF
   - Detect the language
   - Translate to English (if needed)
   - Extract structured data (illuminance values, CRI, etc.)
   - Create text chunks for AI processing

### Training Custom Models

1. After processing PDFs, run: `python main.py train`
2. The system will:
   - Create training data from processed documents
   - Train a classification model for standards categorization
   - Fine-tune an embedding model for semantic understanding
   - Store embeddings in a vector database

### Comparing Standards

1. Run: `python main.py compare --standard-a file1.pdf --standard-b file2.pdf`
2. The system will:
   - Calculate overall similarity scores
   - Compare category-specific requirements
   - Identify key differences
   - Generate recommendations for harmonization

## Output Files

The system creates several output directories:

- `data/` - Processed documents and vector database
- `models/` - Trained AI models
- `uploads/` - Uploaded and processed PDFs
- `outputs/` - Training results and comparison reports
- `logs/` - System logs

## Troubleshooting

### Common Issues

1. **PDF Processing Fails**
   - Ensure PDFs are not password-protected
   - Try different extraction methods in config
   - Check if PDFs contain text (not just images)

2. **Language Detection Issues**
   - Install additional spaCy language models
   - Check if text is sufficient for language detection

3. **Training Fails**
   - Ensure sufficient processed documents
   - Check available memory and disk space
   - Verify all dependencies are installed

4. **Vector Database Issues**
   - Clear and recreate vector database
   - Check disk space and permissions

### Logs

Check `logs/app.log` for detailed error messages and system information.

## Contributing

We welcome contributions! To extend the system:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add new PDF extraction methods in `src/ai_standards/core/pdf_processor.py`
4. Implement additional comparison metrics in `src/ai_standards/models/comparison_model.py`
5. Add new visualization components in `src/ai_standards/web/web_interface.py`
6. Extend the API with new endpoints
7. Commit your changes (`git commit -m 'Add some amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This system is designed for processing and analyzing lighting standards documents. Please ensure compliance with relevant copyright and usage restrictions for the standards documents you process.

## Contact

**Short Circuit Company**
- Email: [Scc@shortcircuitcompany.com](mailto:Scc@shortcircuitcompany.com)
- GitHub: [https://github.com/abubakr3800/sc-standards](https://github.com/abubakr3800/sc-standards)

## 📚 Documentation

### Latest Updates
- **[LATEST_NEWS.md](LATEST_NEWS.md)** - Latest features and updates including Dialux Report Analysis System
- **[DESIGN_PROJECT_STEPS.md](DESIGN_PROJECT_STEPS.md)** - Complete development process and all libraries used
- **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** - Comprehensive system overview with new Dialux capabilities

### Core Documentation
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project organization and file structure
- **[WORKFLOW_EXPLANATION.md](WORKFLOW_EXPLANATION.md)** - Detailed workflow and process explanation
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Setup and installation guide

## Acknowledgments

- Built with modern Python AI/ML libraries
- Uses state-of-the-art NLP models for text processing
- Implements professional software engineering practices
- Designed for scalability and maintainability
- **🆕 Enhanced with intelligent Dialux report analysis capabilities**
