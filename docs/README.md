# AI Standards Training System

A comprehensive AI system for processing, understanding, and comparing lighting standards from PDF documents in multiple languages.

## Features

- **Multi-language PDF Processing**: Extract text from PDFs in any language with automatic language detection and translation
- **AI Model Training**: Train custom models to understand and categorize lighting standards
- **Standards Comparison**: Compare standards across different regions and languages
- **Vector Database**: Store and search through standards using semantic similarity
- **Web Interface**: User-friendly Streamlit interface for easy interaction
- **REST API**: FastAPI-based API for programmatic access

## Installation

1. **Clone or download the system files**

2. **Place your PDF standards files in the `base/` folder**:
   ```bash
   # The system will automatically look for PDFs in the base/ folder
   # You can also specify a different directory with --input-dir
   ```

3. **Install dependencies** (choose one method):

   **Method A: Automatic installation (recommended)**:
   ```bash
   python install.py
   ```

   **Method B: Manual installation**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python -m spacy download de_core_news_sm
   python -m spacy download fr_core_news_sm
   # Add other language models as needed
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

1. **PDF Processor** (`pdf_processor.py`)
   - Multi-method PDF text extraction (pdfplumber, PyMuPDF, pdfminer)
   - Language detection and translation
   - Text preprocessing and chunking
   - Structured data extraction

2. **AI Trainer** (`ai_trainer.py`)
   - Sentence transformer fine-tuning
   - Classification model training
   - Vector database integration
   - Training pipeline management

3. **Comparison Model** (`comparison_model.py`)
   - Semantic similarity analysis
   - Category-specific comparisons
   - Compliance checking
   - Recommendation generation

4. **Web Interface** (`web_interface.py`)
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

Edit `config.py` to customize:

- **PDF Processing**: Supported languages, extraction methods, chunk sizes
- **AI Models**: Model names, training parameters, batch sizes
- **Comparison**: Similarity thresholds, feature weights
- **Database**: Storage paths and settings

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

To extend the system:

1. Add new PDF extraction methods in `pdf_processor.py`
2. Implement additional comparison metrics in `comparison_model.py`
3. Add new visualization components in `web_interface.py`
4. Extend the API with new endpoints

## License

This system is designed for processing and analyzing lighting standards documents. Please ensure compliance with relevant copyright and usage restrictions for the standards documents you process.
