# AI Standards Training System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/GitHub-sc--standards-green.svg)](https://github.com/abubakr3800/sc-standards)

A comprehensive AI system for processing, understanding, and comparing lighting standards from PDF documents in multiple languages.

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

### 7. 🆕 Dialux Report Analysis

```bash
# Analyze a single Dialux report
python main.py dialux --input /path/to/dialux_report.pdf

# Analyze multiple Dialux reports in a folder
python main.py dialux --input-dir /path/to/dialux_reports/

# Analyze with specific output directory
python main.py dialux --input /path/to/report.pdf --output-dir /path/to/results/

# Analyze with detailed verbose output
python main.py dialux --input /path/to/report.pdf --verbose

# Analyze with custom standards comparison
python main.py dialux --input /path/to/report.pdf --standards EN_12464_1,BREEAM

# Analyze and save detailed report
python main.py dialux --input /path/to/report.pdf --save-report --report-format json
```

### 8. 🆕 Dialux Web Interface

```bash
# Start dedicated Dialux analysis web interface
streamlit run dialux_classifier_web.py

# Or use the main web interface with Dialux support
python main.py web
```

## Web Interface

The Streamlit web interface provides:

- **Upload & Process**: Upload PDF files and process them with language detection
- **Train Models**: Configure and train AI models for standards understanding
- **Compare Standards**: Compare two standards with detailed analysis
- **Analytics**: View training performance and system statistics
- **Settings**: Configure system parameters and manage data
- **🆕 Dialux Report Analysis**: Dedicated interface for analyzing Dialux lighting reports

### Main Web Interface
Access the main web interface at `http://localhost:8501` when running `python main.py web`

### 🆕 Dialux Analysis Web Interface
Access the dedicated Dialux analysis interface at `http://localhost:8501` when running `streamlit run dialux_classifier_web.py`

**Dialux Web Interface Features:**
- **Upload Dialux Reports**: Drag and drop or browse to upload Dialux PDF reports
- **Real-time Analysis**: Instant analysis with intelligent parameter extraction
- **Room-by-Room Details**: Detailed analysis for each room/space in the report
- **Standards Compliance**: Automatic compliance checking against multiple standards
- **Visual Reports**: Interactive charts and graphs showing compliance rates
- **Export Results**: Download detailed analysis reports in JSON or PDF format
- **Parameter Extraction**: Comprehensive extraction of all lighting parameters:
  - Illuminance (average, minimum, maximum)
  - Uniformity ratios
  - UGR (Unified Glare Rating)
  - Power density
  - Color temperature and CRI
  - Luminous efficacy
  - Mounting heights
  - Area calculations

## API Endpoints

The FastAPI server provides REST endpoints:

- `POST /upload` - Upload and process PDF files
- `POST /train` - Train AI models
- `POST /compare` - Compare two standards
- `GET /standards` - List available standards
- `GET /docs` - API documentation
- **🆕 `POST /dialux/analyze`** - Analyze Dialux reports
- **🆕 `GET /dialux/standards`** - List available lighting standards for compliance checking
- **🆕 `POST /dialux/batch`** - Batch analyze multiple Dialux reports

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

5. **🆕 Dialux Report Processor** (`intelligent_dialux_processor.py`)
   - Intelligent parameter extraction from Dialux reports
   - Multi-method text extraction (pdfplumber, PyMuPDF)
   - Smart room section detection and data consolidation
   - Comprehensive lighting parameter analysis

6. **🆕 Dialux Report Classifier** (`dialux_classifier.py`)
   - Standards compliance checking (EN 12464-1, BREEAM)
   - Room-by-room analysis and scoring
   - Detailed report generation with recommendations
   - Fallback processing for non-standard PDF formats

7. **🆕 Dialux Web Interface** (`dialux_classifier_web.py`)
   - Dedicated Streamlit interface for Dialux analysis
   - Real-time report processing and visualization
   - Interactive compliance checking and reporting
   - Export functionality for analysis results

### Data Flow

```
PDF Files → PDF Processor → Training Data → AI Trainer → Trained Models
                ↓
         Vector Database ← Embeddings ← Comparison Model
                ↓
         Web Interface ← API Endpoints ← Comparison Results

🆕 Dialux Reports → Intelligent Processor → Room Analysis → Standards Compliance
                ↓
         Detailed Reports ← Classifier ← Compliance Checking
                ↓
         Dialux Web Interface ← Real-time Analysis ← Export Results
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

## 🆕 Dialux Report Analysis

### Supported Lighting Parameters

The Dialux analysis system extracts and analyzes these comprehensive lighting parameters:

#### Core Lighting Parameters
- **Illuminance Values**:
  - Average illuminance (E_avg)
  - Minimum illuminance (E_min)
  - Maximum illuminance (E_max)
  - Maintained illuminance (E_m)
  - Initial illuminance (E_i)

- **Uniformity Metrics**:
  - Uniformity ratio (U0)
  - Min/Max uniformity
  - Overall uniformity assessment

- **Glare Assessment**:
  - UGR (Unified Glare Rating)
  - Glare index
  - Glare rating

- **Power and Efficiency**:
  - Power density (W/m²)
  - Total power consumption
  - Luminous efficacy (lm/W)
  - Energy efficiency rating

#### Additional Parameters
- **Color Properties**:
  - Color temperature (K)
  - Color Rendering Index (CRI)
  - Color quality assessment

- **Physical Properties**:
  - Room/space area (m²)
  - Mounting height (m)
  - Light distribution type
  - Luminaire specifications

- **Environmental Factors**:
  - Daylight factor (%)
  - Daylight autonomy (%)
  - Environmental conditions

### Supported Standards for Compliance Checking

1. **EN 12464-1:2021** - Light and lighting - Lighting of work places
   - Office spaces
   - Meeting rooms
   - Corridors and circulation areas
   - Storage areas
   - Industrial spaces

2. **BREEAM** - Building Research Establishment Environmental Assessment Method
   - Office lighting requirements
   - Energy efficiency standards
   - Environmental performance

3. **Custom Standards** - Configurable standards for specific requirements

### Analysis Output

Each Dialux report analysis provides:

- **Project Overview**: Project name, type, total area, room count
- **Overall Statistics**: Average illuminance, uniformity, UGR, power density
- **Compliance Rates**: Overall and category-specific compliance percentages
- **Room-by-Room Analysis**: Detailed analysis for each space including:
  - All extracted lighting parameters
  - Compliance status for each standard
  - Data quality and confidence scores
  - Specific recommendations for improvement
- **Standards Comparison**: Compliance rates against multiple standards
- **Best Matching Standard**: Identification of the most applicable standard
- **Detailed Recommendations**: Specific actions to improve compliance

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

### 🆕 Analyzing Dialux Reports

#### Command Line Analysis

1. **Single Report Analysis**:
   ```bash
   python main.py dialux --input /path/to/dialux_report.pdf
   ```
   The system will:
   - Extract all lighting parameters from the report
   - Analyze each room/space individually
   - Check compliance against multiple standards
   - Generate detailed recommendations
   - Provide overall project assessment

2. **Batch Analysis**:
   ```bash
   python main.py dialux --input-dir /path/to/dialux_reports/
   ```
   The system will:
   - Process all Dialux reports in the directory
   - Generate individual reports for each file
   - Create comparative analysis across all reports
   - Provide summary statistics

3. **Detailed Analysis with Export**:
   ```bash
   python main.py dialux --input /path/to/report.pdf --save-report --report-format json --verbose
   ```
   The system will:
   - Perform comprehensive analysis
   - Save detailed results to JSON file
   - Provide verbose output with extraction details
   - Include confidence scores and data quality metrics

#### Web Interface Analysis

1. **Start the Dialux Web Interface**:
   ```bash
   streamlit run dialux_classifier_web.py
   ```

2. **Upload and Analyze**:
   - Drag and drop your Dialux PDF report
   - View real-time analysis results
   - Explore room-by-room details
   - Check compliance against different standards
   - Export results in various formats

3. **Interactive Features**:
   - Visual compliance charts
   - Parameter comparison graphs
   - Standards compliance matrix
   - Detailed recommendations panel
   - Export functionality for reports

#### Example Analysis Output

```
🔍 Intelligent processing of Dialux PDF: office_lighting_report.pdf
📄 Extracted 15,432 characters of text
🏢 Project: Modern Office Building - Floor 2
📊 Found 47 data points
🏠 Created 8 intelligent rooms

✅ Successfully created intelligent report with 8 rooms
📊 Project Type: Office
✅ Overall Compliance: 87.5%
📈 Data Quality: 92.3%
💡 Average Illuminance: 487.5 lux
⚡ Average Power Density: 9.2 W/m²
🎯 Best Matching Standard: EN_12464_1_Office

🏠 Room Details:
   Main Office Area:
     💡 Illuminance: 520 lux
     📐 Area: 45.2 m²
     ⚡ Power: 8.5 W/m²
     🎨 CRI: 85
     🌡️  Color Temp: 4000K
     📊 Data Quality: 95%
     🎯 Confidence: 98%
     ✅ Compliant: I:True U:True G:True P:True

   Meeting Room:
     💡 Illuminance: 485 lux
     📐 Area: 12.8 m²
     ⚡ Power: 9.1 W/m²
     🎨 CRI: 82
     🌡️  Color Temp: 4000K
     📊 Data Quality: 88%
     🎯 Confidence: 92%
     ✅ Compliant: I:True U:True G:True P:True
```

## Output Files

The system creates several output directories:

- `data/` - Processed documents and vector database
- `models/` - Trained AI models
- `uploads/` - Uploaded and processed PDFs
- `outputs/` - Training results and comparison reports
- `logs/` - System logs
- **🆕 `dialux_reports/`** - Dialux analysis results and detailed reports
- **🆕 `compliance_reports/`** - Standards compliance analysis results

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

5. **🆕 Dialux Report Processing Issues**
   - Ensure Dialux PDFs contain readable text (not just images)
   - Try different PDF extraction methods (pdfplumber, PyMuPDF)
   - Check if the report follows standard Dialux format
   - Use fallback processing for non-standard formats
   - Verify lighting parameters are present in the report

6. **🆕 Standards Compliance Issues**
   - Check if the room type is correctly identified
   - Verify that lighting parameters are within reasonable ranges
   - Ensure the applicable standard is correctly selected
   - Review data quality and confidence scores

### Logs

Check `logs/app.log` for detailed error messages and system information.

### 🆕 Dialux-Specific Troubleshooting

1. **No Room Data Found**
   - The system will automatically try fallback processing
   - Check if the PDF contains lighting-related text
   - Verify the report format matches Dialux standards

2. **Low Data Quality Scores**
   - Review extracted parameters for reasonableness
   - Check if room names are correctly identified
   - Verify parameter extraction patterns

3. **Compliance Issues**
   - Review the applicable standard selection
   - Check parameter values against standard requirements
   - Verify room type classification accuracy

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

## 🆕 Complete Command Reference

### Main System Commands

```bash
# Process PDF standards
python main.py process [OPTIONS]

# Train AI models
python main.py train [OPTIONS]

# Compare standards
python main.py compare [OPTIONS]

# Start web interface
python main.py web [OPTIONS]

# Start API server
python main.py api [OPTIONS]

# Run complete demo
python main.py demo [OPTIONS]

# 🆕 Analyze Dialux reports
python main.py dialux [OPTIONS]
```

### 🆕 Dialux Analysis Commands

#### Basic Dialux Analysis
```bash
# Analyze single Dialux report
python main.py dialux --input /path/to/dialux_report.pdf

# Analyze multiple reports in directory
python main.py dialux --input-dir /path/to/dialux_reports/

# Analyze with verbose output
python main.py dialux --input /path/to/report.pdf --verbose
```

#### Advanced Dialux Options
```bash
# Specify output directory
python main.py dialux --input /path/to/report.pdf --output-dir /path/to/results/

# Compare against specific standards
python main.py dialux --input /path/to/report.pdf --standards EN_12464_1,BREEAM

# Save detailed report
python main.py dialux --input /path/to/report.pdf --save-report

# Choose report format
python main.py dialux --input /path/to/report.pdf --save-report --report-format json
python main.py dialux --input /path/to/report.pdf --save-report --report-format pdf

# Batch processing with custom settings
python main.py dialux --input-dir /path/to/reports/ --output-dir /path/to/results/ --verbose --save-report
```

#### Dialux Web Interface
```bash
# Start dedicated Dialux web interface
streamlit run dialux_classifier_web.py

# Start with custom port
streamlit run dialux_classifier_web.py --server.port 8502

# Start main web interface (includes Dialux support)
python main.py web
```

### Command Line Options

#### General Options
- `--input` / `-i`: Input PDF file path
- `--input-dir` / `-d`: Input directory containing PDFs
- `--output-dir` / `-o`: Output directory for results
- `--verbose` / `-v`: Enable verbose output
- `--help` / `-h`: Show help message

#### Dialux-Specific Options
- `--standards`: Comma-separated list of standards to check (EN_12464_1, BREEAM, etc.)
- `--save-report`: Save detailed analysis report
- `--report-format`: Report format (json, pdf, html)
- `--confidence-threshold`: Minimum confidence threshold for data inclusion
- `--compliance-threshold`: Minimum compliance threshold for reporting

#### Processing Options
- `--target-language`: Target language for processing (en, de, fr, etc.)
- `--extraction-method`: PDF extraction method (pdfplumber, pymupdf, pdfminer)
- `--chunk-size`: Text chunk size for processing
- `--batch-size`: Batch size for processing multiple files

### Environment Variables

Create a `.env` file in the project root to set:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Web Interface Configuration
WEB_HOST=localhost
WEB_PORT=8501

# Database Configuration
VECTOR_DB_PATH=./data/vector_db
MODEL_PATH=./models

# Dialux Analysis Configuration
DIALUX_OUTPUT_DIR=./dialux_reports
COMPLIANCE_OUTPUT_DIR=./compliance_reports
DEFAULT_STANDARDS=EN_12464_1,BREEAM

# Processing Configuration
DEFAULT_TARGET_LANGUAGE=en
DEFAULT_EXTRACTION_METHOD=pdfplumber
DEFAULT_CHUNK_SIZE=1000
DEFAULT_BATCH_SIZE=10

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### File Structure

```
AI_projects/standards/
├── main.py                          # Main entry point
├── dialux_classifier.py             # Dialux report classifier
├── dialux_classifier_web.py         # Dialux web interface
├── intelligent_dialux_processor.py  # Intelligent Dialux processor
├── comprehensive_dialux_processor.py # Comprehensive Dialux processor
├── advanced_dialux_processor.py     # Advanced Dialux processor
├── improved_dialux_processor.py     # Improved Dialux processor
├── run_web_interface.py             # Web interface runner
├── src/
│   └── ai_standards/
│       ├── core/                    # Core processing modules
│       ├── models/                  # AI models and training
│       ├── web/                     # Web interface components
│       └── api/                     # API endpoints
├── data/
│   ├── processed/                   # Processed documents
│   ├── vector_db/                   # Vector database
│   └── standards/                   # Standards PDFs
├── models/                          # Trained AI models
├── dialux_reports/                  # Dialux analysis results
├── compliance_reports/              # Compliance analysis results
├── outputs/                         # General outputs
├── logs/                            # System logs
└── requirements.txt                 # Python dependencies
```

## Acknowledgments

- Built with modern Python AI/ML libraries
- Uses state-of-the-art NLP models for text processing
- Implements professional software engineering practices
- Designed for scalability and maintainability
- **🆕 Enhanced with intelligent Dialux report analysis capabilities**
